import discord
from discord import app_commands
from discord.ext import commands

class ChatBot(commands.GroupCog, group_name="chatbot", group_description="Chatbot commands"):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="set", description="Set the provider and language model to use")
    @app_commands.describe(
        provider="The LLM provider, e.g. openai, anthropic, cohere, deepinfra, google, groq, mistral",
        model="The specfic model, e.g. gpt-3.5-turbo",
    )
    async def set(self, interaction: discord.Interaction, provider: str, model: str = None):
        """Sets the provider and language model to use""" # given that the host has the key
        # user_api_key = 
        try:
            self.client.chatbot.set_llm(provider, model)
        except ValueError as e:
            await interaction.response.send_message(f"{e}", ephemeral=False)
            raise e
        await interaction.response.send_message(f"LLM set to {provider} {model}")


class ChatHistory(commands.GroupCog, group_name="history", group_description="Chat history commands"):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="view", description="View saved chat history")
    async def view(self, interaction: discord.Interaction):
        """Shows the chat history"""
        chat_history = self.client.chatbot.get_session_history(interaction.channel.name)
        chat_history_display = "\n".join([str(m.content) for m in chat_history.messages])
        if len(chat_history_display) > 2000:
            chat_history_display = chat_history_display[:990] + "\n...\n" + chat_history_display[-990:]
        elif len(chat_history_display) == 0:
            chat_history_display = "No message history saved."
        await interaction.response.send_message(chat_history_display, ephemeral=False)

    @app_commands.command(name="clear", description="Clear chat history")
    async def clear(self, interaction: discord.Interaction):
        """Clears the chat history"""
        self.client.chatbot.clear_session_history(interaction.channel.name)
        await interaction.response.send_message(f"Chat history cleared.")

    @app_commands.command(name="limit", description="Maximum amount of chat entries to save")
    async def limit(self, interaction: discord.Interaction, max: int):
        """Limits the length of chat history"""
        self.client.chatbot.chat_history_limit = max
        await interaction.response.send_message(f"Chat history limit set to {max}.")


class SystemPrompt(commands.GroupCog, group_name="prompt", group_description="System prompt commands"):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="view", description="View saved system prompt")
    async def view(self, interaction: discord.Interaction):
        system_prompt = self.client.chatbot.system_prompt
        await interaction.response.send_message(f"Current system prompt: \n{system_prompt}", ephemeral=False)

    @app_commands.command(name="edit", description="Edit system prompt")
    async def edit(self, interaction: discord.Interaction, prompt: str):
        """Sets the system prompt to use in chat"""
        self.client.chatbot.system_prompt = prompt
        await interaction.response.send_message(f"New system prompt set.")


async def setup(client):
    await client.add_cog(ChatBot(client))
    await client.add_cog(ChatHistory(client))
    await client.add_cog(SystemPrompt(client))