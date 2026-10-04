# SupportFlow AI

Production-oriented AI customer support agent.

## Day 1 - Current Stage

Implemented:

- Project setup
- Git
- Next.js
- FastAPI
- PostgreSQL
- First API


## Architecture

Next.js
    ↓
FastAPI
    ↓
PostgreSQL


## Day 2 — Local LLM

Implemented:

- Ollama local inference
- Gemma 3 1B
- LangChain ChatOllama
- LLM service layer
- Customer support system prompt
- FastAPI AI chat endpoint
- Next.js AI chat interface

### AI Architecture

User
  ↓
Next.js
  ↓
FastAPI
  ↓
LLM Service
  ↓
ChatOllama
  ↓
Ollama
  ↓
Gemma 3 1B

## Day 3 — Persistent Conversations

Implemented:

- PostgreSQL-backed chat sessions
- Persistent chat history
- Multi-turn LLM conversations
- UUID session identifiers
- Recent-message context window
- SQLAlchemy async repositories
- Alembic database migrations
- Persistent frontend sessions
- Conversation restoration after refresh

### Conversation Architecture

User
  ↓
Next.js
  ↓
Session ID
  ↓
FastAPI
  ↓
PostgreSQL chat history
  ↓
Recent messages
  ↓
ChatOllama
  ↓
Gemma 3
  ↓
Response
  ↓
PostgreSQL

## Day 4 — Retrieval-Augmented Generation

Implemented:

- Local nomic-embed-text embedding model
- 768-dimensional embeddings
- PostgreSQL pgvector extension
- Knowledge document ingestion
- Text chunking with overlap
- Idempotent document ingestion using SHA-256
- Semantic similarity retrieval
- Cosine-distance search
- Top-k retrieval
- Grounded LLM responses
- RAG source citations in the frontend
- Conversation history + RAG integration

### RAG Architecture

Documents
  ↓
Chunking
  ↓
nomic-embed-text Embeddings
  ↓
pgvector
  ↓
Semantic retrieval
  ↓
Top-k context
  ↓
Gemma 3
  ↓
Grounded answer

## Day 5 — Agentic AI and Tool Calling

Implemented:

- LangGraph agent orchestration
- Local Qwen3 tool-capable model
- Native LLM tool calling
- RAG as an agent tool
- Order lookup tool
- Deterministic refund eligibility
- Refund execution tool
- Support ticket creation
- Multi-step agent loops
- Explicit action confirmation
- Refund idempotency
- Separation of LLM decisions and business logic
- Synthetic commerce dataset
- Agent safety boundaries

### Agent Architecture

Customer
  ↓
FastAPI
  ↓
LangGraph Agent
  ↓
Qwen3
  ↓
Tool decision
  ├── Knowledge search
  ├── Order lookup
  ├── Refund eligibility
  ├── Refund processing
  └── Ticket creation
  ↓
Tool result
  ↓
Agent
  ↓
Customer response

### Safety Design

The LLM does not directly modify business data.

All state-changing actions pass through deterministic
application services.

Refund execution requires:

1. Valid order
2. Deterministic eligibility check
3. Explicit confirmation
4. Idempotency protection

For a real financial system, conversational confirmation
would be replaced by authenticated UI/API authorization.