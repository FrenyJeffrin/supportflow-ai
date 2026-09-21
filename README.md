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