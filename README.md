# Indonesian News AI Chatbot

An AI-powered news platform for discovering and understanding Indonesian news through conversational search.

Users can browse Indonesian news articles and ask questions directly from the article they are reading. The system uses retrieval-augmented generation (RAG) to ground responses in stored news content rather than relying entirely on the model's general knowledge.

**Live Demo →** [ask-news.vercel.app](https://ask-news.vercel.app/)

---

## Overview

The platform provides two chat experiences.

**Global news chat**

Users can ask about Indonesian news without being inside a specific article. The assistant can search the available news collection and return an answer with relevant sources when appropriate.

**Article chat**

When a user opens an article, the conversation is scoped to that article. Questions such as summaries, key points, people mentioned, and other article-specific details are answered using the article's content.

This distinction keeps the conversation relevant to the user's current context.

| | |
|---|---|
| <img src="/frontend/public/images/example2.png" width="800"> | <img src="/frontend/public/images/example1.png" width="800"> |

---

## Architecture

```text
                         ┌──────────────────┐
                         │     NewsAPI      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Article Pipeline │
                         │ Normalize        │
                         │ Clean            │
                         │ Chunk            │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ OpenAI Embedding │
                         └────────┬─────────┘
                                  │
                                  ▼
┌────────────────┐      ┌──────────────────┐
│ React Frontend │ ───► │ FastAPI Backend  │
└────────────────┘      └────────┬─────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
             ┌──────────────┐         ┌──────────────┐
             │ PostgreSQL   │         │    OpenAI    │
             │ + pgvector   │         │ Chat Model   │
             └──────────────┘         └──────────────┘
```

---

## RAG Pipeline

News articles are processed before they become available to the chatbot.

```text
Article
   │
   ▼
Normalize
   │
   ▼
Clean content
   │
   ▼
Split into chunks
   │
   ▼
Generate embeddings
   │
   ▼
Store in PostgreSQL + pgvector
```

When a user asks a question:

```text
User question
      │
      ▼
Generate query embedding
      │
      ▼
Vector similarity search
      │
      ▼
Retrieve relevant chunks
      │
      ▼
Build context
      │
      ▼
OpenAI chat model
      │
      ▼
Streaming response
```

For article-specific conversations, retrieval is restricted to the current article.

For global conversations, the model can request a news search when additional article information is required.

---

## Grounding and Scope

The assistant is intentionally designed as a **news-focused system**, rather than a general-purpose chatbot.

It is instructed to:

- answer questions related to Indonesian news
- ground responses in retrieved article content
- avoid inventing information that is not supported by the retrieved content
- avoid filling missing information with unrelated general knowledge
- keep article conversations focused on the current article
- reject unrelated requests such as programming, medical advice, legal advice, financial advice, and unrelated creative writing

Article content is treated as data, not as instructions. This prevents instructions embedded inside an article from being interpreted as system-level instructions.

---

## Chat Experience

The chat interface provides contextual quick questions so users can start a conversation without having to formulate a prompt.

On the public news page, suggestions are focused on the broader Indonesian news landscape:

```text
"What are the most popular news articles this year?",
"What are the latest trending news in Indonesia?",
```

Inside an article, suggestions are automatically changed to article-specific questions:

```text
"What is this article about?",
"Can you summarize this article?",
```

AI responses are streamed to the frontend using Server-Sent Events (SSE).

Relevant source articles are displayed when the assistant performs a news search.

---

## Data Model

The main database entities are:

```text
Article
   │
   └── ArticleChunk
          └── embedding

Conversation
   │
   └── Message

GuestQuota
```

`ArticleChunk` stores the individual pieces of article content together with their vector embeddings.

`Conversation` and `Message` store anonymous chat history, while `GuestQuota` is used to control usage for unauthenticated users.

---

## Technology
  - ### Frontend
    - React
    - TypeScript
    - Vite
    - React Router
    - TanStack Query
    - Tailwind CSS
    - shadcn/ui
    - Lucide

  - ### Backend
    - Python
    - FastAPI
    - Pydantic
    - SQLAlchemy
    - Alembic
    - PostgreSQL
    - pgvector
    - pytest

  - ### AI
    - OpenAI Python SDK
    - OpenAI chat models `gpt-4o-mini`
    - `text-embedding-3-small`
    - Retrieval-Augmented Generation
    - Function/tool calling
    - Server-Sent Events

  - ### Data
    - NewsAPI
    - PostgreSQL
    - pgvector

---

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── alembic/
│   ├── scripts/
│   └── test/
│
└── frontend/
    └── src/
        ├── components/
        ├── hooks/
        ├── lib/
        ├── pages/
        └── types/
```

The backend is organized around API routes, database models, schemas, and application services. The frontend separates reusable UI components, data-fetching hooks, pages, and application utilities.

---

## Local Development

### Requirements

- Python 3.14+
- Node.js
- PostgreSQL with pgvector
- OpenAI API key
- NewsAPI key

### Backend

```bash
cd backend

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create `.env`:

```env
# Backend .env
DATABASE_URL=database_url_here
NEWS_API_KEY=news_api_key_here
OPENAI_API_KEY=openai_api_key_here
CORS_ALLOWED_ORIGINS=cors_allowed_origins_here


# Frontend .env
VITE_API_BASE_URL=base_url_here_example_localhost:8080
```

Run migrations:

```bash
alembic upgrade head
```

Start the API using `uvicorn`:

```bash
uvicorn app.main:app --reload --port 8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend

npm install
npm run dev
```

Configure the frontend API URL through the local environment configuration.

---

## Database Migrations

Create a migration after changing the SQLAlchemy models:

```bash
alembic revision --autogenerate -m "initial migrations"
```

Apply migrations:

```bash
alembic upgrade head
```

---

## Deployment

The current deployment architecture separates the frontend, backend, and database.

```text
Frontend
   │
   ▼
Vercel

Backend
   │
   ▼
FastAPI-compatible hosting

Database
   │
   ▼
Neon PostgreSQL
```

API keys and other sensitive configuration are provided through environment variables and are not committed to the repository.

---

## Project Direction

The project started as an exploration of building an AI-powered application around real-world news data and evolved into a full-stack RAG system.

The main focus is the interaction between:

```text
News Data
     +
Semantic Retrieval
     +
LLM
     +
Context-aware UI
```

The result is a conversational interface where users can move between discovering Indonesian news, reading an article, and asking questions about what they are reading without leaving the news experience.
