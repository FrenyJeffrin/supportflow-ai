from app.tools.knowledge_tools import (
    search_knowledge_base,
)

from app.tools.order_tools import (
    get_order,
)

from app.tools.refund_tools import (
    check_refund_eligibility,
    process_refund,
)

from app.tools.ticket_tools import (
    create_support_ticket,
)


TOOLS = [
    search_knowledge_base,
    get_order,
    check_refund_eligibility,
    process_refund,
    create_support_ticket,
]