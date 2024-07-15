from dotenv import load_dotenv
import json
import os
import re

import discord
from discord.ext import commands

from chat.bot import Chatbot
from trivia import detect_trivia
from utils import format_message, substitute_mentions

load_dotenv()

# Only necessary for quicker slash command syncs
MY_GUILD = discord.Object(id=os.getenv("GUILD_ID"))  # replace with your guild id

class MyBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents, config: dict) -> None:
        super().__init__(intents=intents, command_prefix="!")
        # self.tree = app_commands.CommandTree(self)
        self.chatbot = Chatbot(llm_config=config["llm"])
        self.chatbot.set_llm()
        self.trivia = True

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
        self.chatbot.name = str(self.user).split("#")[0]

    async def on_message(self, message: discord.Message):
        """Handles messages sent in chat"""
        session_id = message.channel.id
        print(message)
        print(message.content)

        if session_id not in self.chatbot.session_messages: 
            chat_history = [format_message("human" if (m.author.id != self.user.id) else "ai", m)
                            async for m in message.channel.history(limit=self.chatbot.chat_history_limit, before=message)]
            chat_history = list(reversed(chat_history))
            self.chatbot.store_message(chat_history, session_id)

        if message.author == self.user:
                return
        if isinstance(message.channel, discord.DMChannel) or self.user.mentioned_in(message):
            # the bot should respond
            if self.chatbot.llm is None:
                await message.channel.send("LLM provider not set.")
            else:
                async with message.channel.typing():
                    output = self.chatbot.chat(format_message("human", message)["data"]["content"], session_id)
                    # split messages into multiple outputs if len(output) is over discord's limit, i.e. 2000 characters
                    chunks = [output[i:i+2000] for i in range(0, len(output), 2000)]
                    for chunk in chunks:
                        await message.channel.send(chunk)
        else:
            # not a DM Channel and bot is not mentioned: bot doesn't respond
            self.chatbot.store_message([format_message("human", message)], session_id)
            if self.trivia:
                response = detect_trivia(message.content)
                if response:
                    self.chatbot.store_message([format_message("ai", response)], session_id)
                    await message.channel.send(response)

with open("config.json") as f:
    config = json.load(f)

intents = discord.Intents().all()
bot = MyBot(intents=intents, config=config)

bot.run(os.getenv("DISCORD_TOKEN"))
