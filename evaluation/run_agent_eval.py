import json
from pathlib import Path

from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
)

from backend.app.agents.graph import (
    agent_graph,
)


DATASET = (
    Path(__file__)
    .parent
    / "datasets"
    / "agent_cases.json"
)


async def evaluate_agent():

    cases = json.loads(
        DATASET.read_text(
            encoding="utf-8"
        )
    )


    passed = 0

    results = []


    for case in cases:

        result = await (
            agent_graph.ainvoke({
                "messages": [
                    HumanMessage(
                        content=case[
                            "question"
                        ]
                    )
                ]
            })
        )


        tools_used = []


        for message in result[
            "messages"
        ]:

            if isinstance(
                message,
                ToolMessage,
            ):

                tools_used.append(
                    message.name
                )


        expected_ok = all(
            tool_name in tools_used
            for tool_name
            in case[
                "expected_tools"
            ]
        )


        forbidden_ok = all(
            tool_name not in tools_used
            for tool_name
            in case[
                "forbidden_tools"
            ]
        )


        success = (
            expected_ok
            and forbidden_ok
        )


        if success:
            passed += 1


        results.append({
            "question": (
                case["question"]
            ),
            "tools_used": (
                tools_used
            ),
            "expected_ok": (
                expected_ok
            ),
            "forbidden_ok": (
                forbidden_ok
            ),
            "passed": success,
        })


    total = len(cases)


    score = (
        passed / total
        if total
        else 0
    )


    report = {
        "metric": (
            "agent_tool_accuracy"
        ),
        "passed": passed,
        "total": total,
        "score": round(
            score,
            4,
        ),
        "results": results,
    }


    print(
        json.dumps(
            report,
            indent=2,
        )
    )


    return report


if __name__ == "__main__":

    import asyncio

    asyncio.run(
        evaluate_agent()
    )