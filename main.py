from dotenv import load_dotenv
import json
import os
import re

import discord
from discord.ext import commands

from trivia import get_trivia
from chat.bot import Chatbot

load_dotenv()

# Only necessary for quicker slash command syncs
MY_GUILD = discord.Object(id=os.getenv("GUILD_ID"))  # replace with your guild id

class MyBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents, config: dict) -> None:
        super().__init__(intents=intents, command_prefix="!")
        # self.tree = app_commands.CommandTree(self)
        self.chatbot = Chatbot(llm_config=config["llm"])
        self.chatbot.set_llm()

    async def _load_extensions(self) -> None:
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                await bot.load_extension(f"cogs.{file[:-3]}")

    async def setup_hook(self):
        await self._load_extensions()
        self.tree.copy_global_to(guild=MY_GUILD) # take away this line for global change
        await self.tree.sync(guild=MY_GUILD)

    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    async def on_message(self, message: discord.Message):
        """Handles messages sent in chat"""
        # removes user mentions in messages for now before passing message to storage/LLM input
        regex = re.compile(r"<@\d+>")
        session_id = message.channel.name
        # print(message)
        # print(message.content)

        if session_id not in self.chatbot.session_messages: 
            chat_history = [{"type": "ai" if (m.author.id == self.user.id) else "human",
                            "data": {"content": f"{(f'{m.author.nick}:' or f'{m.author.name}:') if (m.author.id != self.user.id) else ''}{regex.sub('', m.content)}"}}
                            async for m in message.channel.history(limit=self.chatbot.chat_history_limit)]
            chat_history = list(reversed(chat_history))
            self.chatbot.store_message(chat_history[:-1], session_id)

        msg = message.content
        raw_msg = regex.sub("", msg) # TODO: only remove bot name, replace user mentions with nicknames

        if not self.user.mentioned_in(message):
            if message.author == self.user:
                return
            self.chatbot.store_message([{"type": "human",
                                    "data": {"content": raw_msg}}], 
                                    session_id)
            response = get_trivia(raw_msg)
            if response:
                self.chatbot.store_message([{"type": "ai",
                                        "data": {"content": response}}], 
                                        session_id)
                await message.channel.send(response)
        elif self.chatbot.llm is None:
            await message.channel.send("LLM provider not set.")
        else:
            async with message.channel.typing():
                output = self.chatbot.chat(f"{(message.author.nick or message.author.name)}: {raw_msg}", session_id)
                await message.channel.send(output)

with open("config.json") as f:
    config = json.load(f)

intents = discord.Intents().all()
bot = MyBot(intents=intents, config=config)

bot.run(os.getenv("DISCORD_TOKEN"))
