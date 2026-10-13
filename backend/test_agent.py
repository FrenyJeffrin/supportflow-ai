import asyncio

from langchain_core.messages import (
    HumanMessage,
)

from app.agents.graph import (
    agent_graph,
)


async def main():

    result = await (
        agent_graph.ainvoke({
            "messages": [
                HumanMessage(
                    content=(
                        "What is the status "
                        "of order SF-1002?"
                    )
                )
            ]
        })
    )

    for message in result[
        "messages"
    ]:

        print(
            type(message).__name__
        )

        print(
            message.content
        )

        print(
            getattr(
                message,
                "tool_calls",
                None,
            )
        )

        print(
            "----------------"
        )


asyncio.run(main())