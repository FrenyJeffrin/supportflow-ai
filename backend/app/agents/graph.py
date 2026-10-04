from langchain_core.messages import (
    SystemMessage,
)

from langchain_ollama import (
    ChatOllama,
)

from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from langgraph.prebuilt import (
    ToolNode,
    tools_condition,
)

from app.agents.prompts import (
    AGENT_SYSTEM_PROMPT,
)

from app.agents.state import (
    AgentState,
)

from app.core.config import settings

from app.tools import TOOLS

model = ChatOllama(
    model=settings.ollama_model,
    base_url=settings.ollama_base_url,
    temperature=0,
)

model_with_tools = (
    model.bind_tools(
        TOOLS
    )
)

async def call_model(
    state: AgentState,
):

    messages = [
        SystemMessage(
            content=AGENT_SYSTEM_PROMPT
        ),
        *state["messages"],
    ]

    response = await (
        model_with_tools.ainvoke(
            messages
        )
    )

    return {
        "messages": [
            response
        ]
    }

builder = StateGraph(
    AgentState
)


builder.add_node(
    "agent",
    call_model,
)


builder.add_node(
    "tools",
    ToolNode(TOOLS),
)


builder.add_edge(
    START,
    "agent",
)


builder.add_conditional_edges(
    "agent",
    tools_condition,
)


builder.add_edge(
    "tools",
    "agent",
)


agent_graph = (
    builder.compile()
)