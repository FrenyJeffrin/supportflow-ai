# SupportFlow AI

Production-oriented AI customer support agent.

## Day 1: Current Stage

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