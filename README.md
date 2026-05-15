# Website Chatbot - RAG-based AI Assistant

A Retrieval-Augmented Generation (RAG) chatbot that scrapes RSS feeds, processes articles, and provides intelligent conversational responses with cited sources. Built with FastAPI, Gradio, ChromaDB, and Groq LLM.

## 📋 Project Overview

This chatbot application combines web scraping, vector databases, and large language models to create an intelligent assistant that can answer questions about web content with proper source attribution. It fetches articles from RSS feeds, processes them into a vector database, and uses retrieval-augmented generation to provide context-aware responses.

## 🏗️ Architecture & Workflow

### Data Flow Pipeline

```
1. RSS Feed Scraping
   ↓
   Fetch articles from TechCrunch RSS feed
   ↓
2. Article Parsing & Processing
   ↓
   Extract content and parse HTML
   ↓
3. Text Chunking & Embedding
   ↓
   Split articles into chunks and generate embeddings using Sentence Transformers
   ↓
4. Vector Database Storage
   ↓
   Store embeddings in ChromaDB with metadata
   ↓
5. Query Processing & Retrieval
   ↓
   Retrieve relevant documents based on user query
   ↓
6. LLM Response Generation
   ↓
   Generate answer using Groq LLM with retrieved context
   ↓
7. Multi-Interface Delivery
   ├→ Gradio Web UI
   └→ FastAPI REST API
```

## 📁 Project Structure

```
Website_chatbot/
├── app.py                 # Main application entry point (starts API + UI)
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── api/
│   └── main.py           # FastAPI application and endpoints
│
├── rag/
│   ├── chatbot.py        # Chatbot logic with conversation memory
│   ├── embeddings.py     # Embedding model initialization
│   ├── retriever.py      # Document retrieval logic
│   └── vector_store.py   # Vector database operations (ChromaDB)
│
├── scraper/
│   ├── rss_scraper.py    # RSS feed fetching and parsing
│   └── article_parser.py # Article content extraction
│
├── ui/
│   └── gradio_ui.py      # Gradio interface for web UI
│
├── chroma_db/            # Vector database storage (auto-created)
│   └── chroma.sqlite3
│
└── data/
    ├── raw_articles.json      # Raw scraped articles
    └── processed_urls.json    # Tracking of processed articles
```

## 🚀 Key Features

- **RSS Feed Integration**: Automatically fetches articles from TechCrunch
- **Vector Search**: Uses embeddings for semantic similarity matching
- **Conversational Memory**: Maintains conversation history for context-aware responses
- **Source Attribution**: Returns cited sources with each response
- **Dual Interface**: Web UI (Gradio) + REST API (FastAPI)
- **LLM Integration**: Uses Groq's fast inference with Llama 3.1 model
- **Persistent Storage**: Stores vectors in local ChromaDB database

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Groq API Key (free at https://console.groq.com)
- Internet connection for RSS feed fetching

## 🔧 Installation & Setup

### 1. Clone/Navigate to Project Directory

```bash
cd Website_chatbot
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🎯 How to Run

### Option 1: Full Application (API + Web UI)

```bash
python app.py
```

This starts:
- **FastAPI Server**: Available at `http://localhost:8002`
- **Gradio Web UI**: Available at `http://localhost:7860`

### Option 2: FastAPI Only

```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8002 --reload
```

### Option 3: Gradio UI Only

```bash
python -c "from ui.gradio_ui import demo; demo.launch()"
```

## 💬 Using the Chatbot

### Via Web UI (Gradio)

1. Open `http://localhost:7860` in your browser
2. Type your question in the chat box
3. The chatbot will:
   - Retrieve relevant articles from the database
   - Generate a response with context
   - Display source citations below the answer

### Via REST API (FastAPI)

#### Ask a Question
```bash
curl -X POST "http://localhost:8002/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest AI developments?"}'
```

#### Load New Articles
```bash
curl -X POST "http://localhost:8002/load-articles" \
  -H "Content-Type: application/json" \
  -d '{"limit": 20}'
```

#### Get Database Status
```bash
curl -X GET "http://localhost:8002/status"
```

## 🔄 Workflow Steps

### Initial Setup
1. **Data Collection**: `scraper/rss_scraper.py` fetches articles from RSS feed
2. **Content Extraction**: `scraper/article_parser.py` extracts readable content from articles
3. **Processing**: `rag/vector_store.py` chunks text and generates embeddings
4. **Storage**: Embeddings are stored in ChromaDB

### During Chatting
1. **User Query**: User submits a question via UI or API
2. **Embedding**: Query is converted to embedding
3. **Retrieval**: `rag/retriever.py` finds relevant documents from vector store
4. **Context Building**: Retrieved documents provide context
5. **LLM Processing**: `rag/chatbot.py` sends prompt with context to Groq LLM
6. **Response Generation**: LLM generates answer with source information
7. **Memory Management**: Conversation history is maintained for context

## 📚 Key Components

| Component | Purpose |
|-----------|---------|
| `vector_store.py` | Initialize ChromaDB, chunk texts, manage collections |
| `embeddings.py` | Load sentence-transformer model for embeddings |
| `retriever.py` | Search and retrieve relevant documents |
| `chatbot.py` | Generate responses using LLM with retrieved context |
| `rss_scraper.py` | Fetch and parse RSS feed articles |
| `article_parser.py` | Extract article content from HTML |
| `gradio_ui.py` | Build conversational web interface |
| `api/main.py` | Define REST API endpoints |


## 🔐 Security Notes

- Keep your `.env` file and API keys secure
- Never commit `.env` to version control
- Use environment variables for sensitive data in production

## 📄 License

This project is provided as-is for educational purposes.

---
