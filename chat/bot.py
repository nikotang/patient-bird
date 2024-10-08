import logging

from langchain_core.messages import BaseMessage, ToolMessage, AIMessage, RemoveMessage, messages_from_dict, trim_messages

from chat.model import chat_model
from chat.graph import create_agent

logging.getLogger().setLevel(logging.ERROR)

class Chatbot():
    """A chatbot that interacts with an LLM via Langchain. """
    def __init__(self, llm_config: dict = {}) -> None:
        """Initializes the chatbot. """
        self.llm_config = llm_config
        self.name = None # added by MyBot.on_ready()
        self.system_prompt = self.llm_config.get("system_prompt", "")
        self.chat_history_limit = abs(self.llm_config.get("chat_history_limit", 15))
        self.graph = create_agent()

    def set_llm(self, provider: str = None, model: str = None) -> None:
        """Initializes the LLM. """
        try:
            self.llm = chat_model(provider or self.llm_config.get("provider"), model or self.llm_config.get("model"))
        except ValueError as e:
            raise ValueError(e)

    def get_session_history(self, session_id: str) -> list:
        """Returns the chat history of a given session. """
        config = {"configurable": {"thread_id": session_id}}
        messages = self.graph.get_state(config).values.get("messages")
        return messages if messages else []

    def _update_state_messages(self, session_id: str, messages: list[BaseMessage]) -> None:
        """Updates the chat history of a given session. """
        self.graph.update_state(
            {"configurable": {"thread_id": session_id}},
            {"messages": messages},
        )

    def clear_session_history(self, session_id: str) -> None:
        """Clears the chat history of a given session. """
        stored_messages = self.get_session_history(session_id)
        self._update_state_messages(session_id, [RemoveMessage(id=m.id) for m in stored_messages])

    def store_message(self, chat_history: list[dict[str, str]], session_id: str) -> None:
        """Stores a message in the chat history of a given session (required by RunnableWithMessageHistory). """
        self._update_state_messages(session_id, messages_from_dict(chat_history))

    def _remove_tool_call_messages(self, session_id: str) -> None:
        stored_messages = self.get_session_history(session_id)
        tool_call_messages = [m for m in stored_messages if (type(m) == ToolMessage) or (type(m) == AIMessage and m.content == '')]
        self._update_state_messages(session_id, [RemoveMessage(id=m.id) for m in tool_call_messages])

    def edit_chat_length(self, session_id: str, count_by: str = "message") -> None:
        if count_by not in ("token", "message"):
            raise ValueError("count_by must be either 'token' or 'message'")
        self._remove_tool_call_messages(session_id)
        stored_messages = self.get_session_history(session_id)

        edited_messages = trim_messages(
            stored_messages,
            token_counter= len if count_by == "message" else self.llm,
            max_tokens=self.chat_history_limit,
            strategy="last",
            allow_partial=False,
            start_on="human",
            include_system=False,
        )
        # if count_by message, edited_messages could be different from self.chat_history_limit due to start_on human rounding down
        messages_to_remove = [RemoveMessage(id=m.id) for m in stored_messages[:-len(edited_messages)]]
        self._update_state_messages(session_id, messages_to_remove)

    def chat(self, message_input: str, session_id: str) -> str:
        """Chats with the LLM for one round. """
        self.edit_chat_length(session_id)

        prompt = f"{(f'Your name is {self.name}' if self.name else '')} \
             {self.system_prompt} \
             Continue the conversation. Consider the earlier dialogues if they are relevant. \
             In each user input, the name before the colon is the name of the user. \
             Do not output your own name and colon before speaking. "
        
        graph_config = {"configurable": {
            "thread_id": session_id,
            "llm": self.llm,
            "system_message": prompt}} 
        
        response = self.graph.invoke(
                {
                    "messages": [
                        ("user", message_input)
                    ]
                },
                graph_config,
            )["messages"][-1].content

        return response
