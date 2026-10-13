import asyncio

from worker.celery_app import (
    celery_app,
)


async def run_async_evaluation():

    from evaluation.run_rag_eval import (
        evaluate_rag,
    )

    return await evaluate_rag()


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={
        "max_retries": 3
    },
)
def run_rag_evaluation(
    self,
):

    return asyncio.run(
        run_async_evaluation()
    )