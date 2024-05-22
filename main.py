import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import re
import json

from trivia import get_trivia
from chat.bot import Chatbot

load_dotenv()

MY_GUILD = discord.Object(id=os.getenv('GUILD_ID'))  # replace with your guild id

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents().all()
client = MyClient(intents=intents)

regex = re.compile(r'<@\d+>')
with open('config.json') as f:
    config = json.load(f)

chatbot = Chatbot(llm_config=config['llm'])
chatbot.set_llm()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.tree.command()
@app_commands.describe(
    provider='The LLM provider, e.g. openai, anthropic, cohere, deepinfra, google, groq, mistral',
    model='The specfic model, e.g. gpt-3.5-turbo',
)
async def set(interaction: discord.Interaction, provider: str, model: str = None):
    """Sets the provider and language model to use""" # given that the host has the key
    # user_api_key = 
    try:
        chatbot.set_llm(provider, model)
    except ValueError as e:
        await interaction.response.send_message(f'{e}')
        raise e
    await interaction.response.send_message(f'LLM set to {provider} {model}')

@client.tree.command()
async def inspect(interaction: discord.Interaction):
    """Inspects the chat history"""
    chat_history = chatbot.get_session_history(interaction.channel.name)
    chat_history_display = '\n'.join([str(m.content) for m in chat_history.messages])
    if len(chat_history_display) > 2000:
        chat_history_display = chat_history_display[:990] + '\n...\n' + chat_history_display[-990:]
    elif len(chat_history_display) == 0:
        chat_history_display = 'No message history saved.'
    await interaction.response.send_message(chat_history_display)

@client.tree.command()
async def clear(interaction: discord.Interaction):
    """Clears the chat history"""
    chatbot.clear_session_history(interaction.channel.name)
    await interaction.response.send_message(f'Cleared!')

@client.event
async def on_message(message):
    session_id = message.channel.name
    print(message)
    print(message.content)

    if session_id not in chatbot.session_messages: 
        chat_history = [{'type': 'ai' if (m.author.id == client.user.id) else 'human',
                         'data': {'content': f"{(f'{m.author.nick}:' or f'{m.author.name}:') if (m.author.id != client.user.id) else ''}{regex.sub('', m.content)}"}}
                         async for m in message.channel.history(limit=5)]
        chat_history = list(reversed(chat_history))
        chatbot.store_message(chat_history[:-1], session_id)

    msg = message.content
    raw_msg = regex.sub('', msg) # TODO: only remove bot name, replace user mentions with nicknames

    if not client.user.mentioned_in(message):
        if message.author == client.user:
            return
        chatbot.store_message([{"type": "human",
                                "data": {'content': raw_msg}}], 
                                session_id)
        response = get_trivia(raw_msg)
        if response:
            chatbot.store_message([{"type": "ai",
                                    "data": {'content': response}}], 
                                    session_id)
            await message.channel.send(response)
    elif chatbot.llm is None:
        await message.channel.send("LLM provider not set.")
    else:
        async with message.channel.typing():
            output = chatbot.chat(raw_msg, session_id)
            await message.channel.send(output)
    
client.run(os.getenv('DISCORD_TOKEN'))
