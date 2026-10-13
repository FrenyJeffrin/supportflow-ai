import json
from pathlib import Path

from backend.app.database import AsyncSessionLocal

from backend.app.rag.retrieval import (
    retrieve_context,
)


DATASET = (
    Path(__file__)
    .parent
    / "datasets"
    / "rag_cases.json"
)


async def evaluate_rag():

    cases = json.loads(
        DATASET.read_text(
            encoding="utf-8"
        )
    )


    passed = 0

    results = []

    reciprocal_ranks = []


    async with AsyncSessionLocal() as db:

        for case in cases:

            retrieved = await (
                retrieve_context(
                    db=db,
                    query=case[
                        "question"
                    ],
                )
            )


            sources = [
                item.source
                for item in retrieved
            ]


            success = (
                case[
                    "expected_source"
                ]
                in sources
            )

            try:
                rank = (sources.index(case["expected_source"])+ 1)

                reciprocal_rank = 1 / rank

            except ValueError:
    
                reciprocal_rank = 0.0

                reciprocal_ranks.append(reciprocal_rank)


            if success:
                passed += 1


            results.append({
                "question": (
                    case["question"]
                ),
                "expected": (
                    case[
                        "expected_source"
                    ]
                ),
                "retrieved": sources,
                "passed": success,
            })


    total = len(cases)

    hit_rate = (
        passed / total
        if total
        else 0
    )

    mrr = (sum(reciprocal_ranks)/ len(reciprocal_ranks) if reciprocal_ranks else 0)

    report = {
        "metric": "hit_rate_at_k",
        "passed": passed,
        "total": total,
        "score": round(
            hit_rate,
            4,
        ),
        "mrr": round(mrr, 4),
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
        evaluate_rag()
    )