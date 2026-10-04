import json
import uuid

from app.database import AsyncSessionLocal
from app.models import ToolAuditLog


async def log_tool_call(
    session_id: uuid.UUID,
    tool_name: str,
    input_data: dict,
    output_data: str,
    success: bool,
):

    async with AsyncSessionLocal() as db:

        log = ToolAuditLog(
            session_id=session_id,
            tool_name=tool_name,
            input_data=json.dumps(
                input_data
            ),
            output_data=output_data,
            success=success,
        )

        db.add(log)

        await db.commit()