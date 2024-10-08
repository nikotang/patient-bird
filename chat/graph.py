from typing_extensions import TypedDict

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

search = DuckDuckGoSearchRun()
tools = [search]

class ConfigSchema(TypedDict):
    llm: BaseChatModel
    system_message: str

def _call_model(state: MessagesState, config: RunnableConfig) -> dict[str, list]: 
    model = config["configurable"].get("llm")
    model_with_tools = model.bind_tools(tools)
    messages = [
        SystemMessage(content=config["configurable"].get("system_message"))
        ] + state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

def create_agent() -> CompiledStateGraph:
    graph_builder = StateGraph(MessagesState, config_schema=ConfigSchema)
    memory = MemorySaver()
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("chatbot", _call_model)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    graph_builder.add_edge("tools", "chatbot")
    # graph_builder.add_edge("chatbot", END)

    return graph_builder.compile(checkpointer=memory)

