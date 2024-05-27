import logging

from langchain.schema.messages import messages_from_dict
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory

from chat.model import chat_model

logging.getLogger().setLevel(logging.ERROR)

class Chatbot():
    """A chatbot that interacts with an LLM via Langchain. """
    def __init__(self, llm_config: dict = {}) -> None:
        """Initializes the chatbot. """
        self.config = llm_config
        self.system_prompt = self.config.get("system_prompt", "")
        self.output_parser = StrOutputParser()
        self.session_messages = {}
        self.chat_history_limit = abs(self.config.get("chat_history_limit", 15))

    def set_llm(self, provider: str = None, model: str = None) -> None:
        """Initializes the LLM. """
        try:
            self.llm = chat_model(provider or self.config.get("provider"), model or self.config.get("model"))
        except ValueError as e:
            raise ValueError(e)

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Returns the chat history of a given session. """
        if session_id not in self.session_messages:
            self.session_messages[session_id] = ChatMessageHistory()
        return self.session_messages[session_id]

    def clear_session_history(self, session_id: str) -> None:
        """Clears the chat history of a given session. """
        # self.session_messages[session_id] = ChatMessageHistory()
        session_history = self.get_session_history(session_id)
        session_history.clear()

    def trim_messages(self, chain_input, session_id: str) -> bool:
        """Trims the chat history of a given session. """
        stored_messages = self.get_session_history(session_id).messages
        if len(stored_messages) <= self.chat_history_limit:
            return False

        self.get_session_history(session_id).clear()

        for message in stored_messages[-self.chat_history_limit:]:
            self.get_session_history(session_id).add_message(message)

        return True

    def store_message(self, chat_history: list[dict[str, str]], session_id: str) -> None:
        """Stores a message in the chat history of a given session (required by RunnableWithMessageHistory). """
        session_history = self.get_session_history(session_id)
        messages = messages_from_dict(chat_history)
        session_history.add_messages(messages)

    def chat(self, message_input: str, session_id: str) -> str:
        """Chats with the LLM for one round. """
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"{self.system_prompt} \
             Continue the conversation. Consider the earlier dialogues if they are relevant. \
             In each user input, the name before the colon is the name of the user."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])
        chain: Runnable = (
            RunnablePassthrough.assign(messages_trimmed=lambda x: self.trim_messages(x, session_id=session_id))
            | prompt 
            | self.llm 
            | self.output_parser
        )
        chain_with_chat_history = RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        response = chain_with_chat_history.invoke(
            {"input": message_input}, 
            config={"configurable": {"session_id": session_id}}
        )
        return response
