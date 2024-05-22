from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
import logging

from chat.model import chat_model

logging.getLogger().setLevel(logging.ERROR)

class Chatbot():
    def __init__(self, llm_config: dict = {}) -> None:
        self.config = llm_config
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a Discord bot. {self.config.get('system_prompt', '')} \
                        Continue the conversation. Consider the earlier dialogues if they are relevant. "),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])
        self.output_parser = StrOutputParser()
        self.session_messages = {}

    def set_llm(self, provider: str = None, model: str = None) -> None:
        try:
            self.llm = chat_model(provider or self.config.get("provider"), model or self.config.get("model"))
        except ValueError as e:
            raise ValueError(e)
        if self.llm:
            self.chain: Runnable = self.prompt | self.llm | self.output_parser

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.session_messages:
            self.session_messages[session_id] = ChatMessageHistory()
        return self.session_messages[session_id]

    def clear_session_history(self, session_id: str) -> None:
        self.session_messages[session_id] = ChatMessageHistory()

    def store_message(self, chat_history: list[dict[str, str]], session_id: str) -> None:
        session_history = self.get_session_history(session_id)
        messages = messages_from_dict(chat_history)
        session_history.add_messages(messages)

    def chat(self, message_input: str, session_id: str) -> str:
        chain_with_chat_history = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        response = chain_with_chat_history.invoke(
            {"input": message_input}, 
            config={"configurable": {"session_id": session_id}}
        )
        return response
