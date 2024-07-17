from typing import Union

import discord

def _substitute_mentions(message: discord.Message) -> str:
    """
    replace user and role mentions (e.g. @123456789) with their respective names (e.g. @Patient Bird). 
    Does the same thing as discord.Message.clean_content, but up for customisation. 
    """
    content = message.content
    
    # Replace user mentions
    for user in message.mentions:
        mention_str = f'<@{user.id}>'
        if isinstance(user, discord.Member):
            username_str = f'@{(user.nick or user.global_name or user.name)}'
        else:
            username_str = f'@{(user.global_name or user.name)}'
        content = content.replace(mention_str, username_str)
    
    # Replace role mentions
    for role in message.role_mentions:
        mention_str = f'<@&{role.id}>'
        role_str = f'@{role.name}'
        content = content.replace(mention_str, role_str)
    
    return content


def format_message(type: str, message: Union[str, discord.Message]) -> dict:
    """append speaker name before human messages and format to dict for Langchain. """
    # string responses from trivia or Message objects from Discord
    content = message if isinstance(message, str) else message.clean_content
    # human messages require Message objects to extract message author
    if type == "human":
        assert isinstance(message, discord.Message)
        if isinstance(message.author, discord.Member):
            name = message.author.nick or message.author.global_name or message.author.name
        else: # User instead of Member for private channels; User has no .nick
            name = message.author.global_name or message.author.name
        if message.stickers:
            stickers_list = []
            for sticker_item in message.stickers:
                    # sticker = await self.fetch_sticker(sticker_item.id) # TODO: this works if moved to on_message/as a bot method
                    # stickers_list.append({'name': sticker.name, 'description': sticker.description})
                    stickers_list.append({'name': sticker_item.name})
            stickers_str = f'\n<Stickers attached: \n{str(stickers_list)}>'
        content = f'{name}: {content}{stickers_str if message.stickers else ""}'
    return {
        "type": type,
        "data": {
            "content": content
        }
    }