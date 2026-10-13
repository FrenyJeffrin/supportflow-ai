from prometheus_client import (
    Counter,
    Histogram,
)


HTTP_REQUESTS = Counter(
    "supportflow_http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)


HTTP_LATENCY = Histogram(
    "supportflow_http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
)


AGENT_RUNS = Counter(
    "supportflow_agent_runs_total",
    "Total agent executions",
)


AGENT_ERRORS = Counter(
    "supportflow_agent_errors_total",
    "Total failed agent executions",
)


AGENT_LATENCY = Histogram(
    "supportflow_agent_duration_seconds",
    "Agent execution latency",
)


RAG_SEARCHES = Counter(
    "supportflow_rag_searches_total",
    "Total RAG retrievals",
)


RAG_LATENCY = Histogram(
    "supportflow_rag_duration_seconds",
    "RAG retrieval latency",
)


CACHE_HITS = Counter(
    "supportflow_cache_hits_total",
    "Total cache hits",
    ["cache"],
)


CACHE_MISSES = Counter(
    "supportflow_cache_misses_total",
    "Total cache misses",
    ["cache"],
)