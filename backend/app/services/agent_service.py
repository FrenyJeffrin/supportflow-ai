from langchain_core.messages import (
    AIMessage,
    HumanMessage,
)

from app.agents.graph import (
    agent_graph,
)


class AgentService:

    async def run(
        self,
        history: list[
            dict[str, str]
        ],
    ) -> str:

        messages = []


        for item in history:

            if item["role"] == "user":

                messages.append(
                    HumanMessage(
                        content=item[
                            "content"
                        ]
                    )
                )

            elif (
                item["role"]
                == "assistant"
            ):

                messages.append(
                    AIMessage(
                        content=item[
                            "content"
                        ]
                    )
                )


        result = await (
            agent_graph.ainvoke({
                "messages": messages
            })
        )


        final_message = (
            result["messages"][-1]
        )


        return str(
            final_message.content
        )


agent_service = AgentService()