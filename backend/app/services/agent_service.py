from langchain_core.messages import (
    AIMessage,
    HumanMessage,
)

from app.agents.graph import (
    agent_graph,
)

import time

from app.observability.metrics import (
    AGENT_ERRORS,
    AGENT_LATENCY,
    AGENT_RUNS,
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
        AGENT_RUNS.inc()

        start = time.perf_counter()

        try:

            result = await agent_graph.ainvoke({"messages": messages})

        except Exception:

            AGENT_ERRORS.inc()

            raise

        finally:

            AGENT_LATENCY.observe(time.perf_counter() - start)

        final_message = (result["messages"][-1])

        return str(final_message.content)


agent_service = AgentService()
