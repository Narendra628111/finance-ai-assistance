# Finance AI Assistance

A multimodal AI assistant for banking and financial queries that understands text, documents, and images. It combines **LangGraph, RAG, Qdrant, Docling, OCR, Sentence Transformers, and LLMs** to deliver context-aware, knowledge-grounded responses with source attribution.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [RAG Pipeline](#rag-pipeline)
- [Knowledge Base](#knowledge-base)
- [Embedding Configuration](#embedding-configuration)
- [Environment Configuration](#environment-configuration)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Example Questions](#example-questions)
- [Image Processing](#image-processing)
- [Qdrant](#qdrant)
- [Knowledge Base Indexing](#knowledge-base-indexing)
- [Source Attribution](#source-attribution)
- [Development Milestones](#development-milestones)
- [Error Handling](#error-handling)
- [Frontend](#frontend)
- [Security Considerations](#security-considerations)
- [Disclaimer](#disclaimer)

---

## Overview

Finance AI Assistance helps users understand banking and financial information through a single conversational interface. The assistant can:

- Answer banking and finance-related questions
- Analyze uploaded financial documents
- Extract text from PDFs, DOCX files, TXT files, and images
- Perform OCR on image-based documents
- Analyze screenshots such as bank statements, credit card statements, and UPI screens
- Retrieve relevant information from a financial knowledge base
- Generate grounded answers using Retrieval-Augmented Generation (RAG)
- Provide the source document and page number used for an answer
- Use LangGraph to orchestrate the complete workflow

---

## Key Features

### Multimodal Input

The assistant accepts:

| Type | Formats |
|---|---|
| Text | Plain text queries |
| Documents | PDF, DOCX, TXT |
| Images | PNG, JPG/JPEG, BMP, TIFF, WEBP |

### Document Extraction

Documents are processed using **Docling**. For image-based documents, **RapidOCR with ONNX Runtime** performs OCR.

### Financial RAG

The application maintains a financial knowledge base containing documents from sources such as:

- RBI
- SBI
- NPCI
- Axis Bank
- ICICI Bank

Documents are converted into embeddings and stored in Qdrant for semantic retrieval.

### Semantic Search

Local text embeddings are generated using **`all-MiniLM-L6-v2`** (embedding dimension: **384**).

### Reranking

Retrieved documents are reranked using a cross-encoder to improve the relevance of the context supplied to the LLM.

### LangGraph Workflow

LangGraph coordinates the processing pipeline based on the type of user input.

---

## Architecture

```text
                         User
                           │
                           ▼
                    FastAPI /assistant/chat
                           │
                           ▼
                    Workflow Agent
                           │
                           ▼
                       LangGraph
                           │
              ┌────────────┴────────────┐
              │                         │
          Text Input                File/Image
              │                         │
              │                         ▼
              │                  Document Node
              │                         │
              │                  Docling + OCR
              │                         │
              └────────────┬────────────┘
                           ▼
                     Summarizer
                           │
                           ▼
                      Classifier
                           │
                           ▼
                         RAG
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
      Embeddings        Qdrant          Reranker
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                          LLM
                           │
                           ▼
                   Final Answer
                           │
                           ▼
                    Sources / Pages
```

---

## Workflow

The main workflow is implemented using LangGraph:

```text
START
  │
  ▼
Input Router
  │
  ├── Text ───────────────┐
  │                       │
  └── Document/Image      │
          │               │
          ▼               │
      Document            │
          │               │
          ▼               │
      Summarizer          │
          │               │
          └───────┬───────┘
                  ▼
              Classifier
                  │
                  ▼
                 RAG
                  │
                  ▼
                 END
```

---

## Project Structure

```text
finance-ai-assistance/
│
├── backend/
│   │
│   ├── agents/
│   │   ├── classifier_agent.py
│   │   ├── extractor_agent.py
│   │   ├── summarizer_agent.py
│   │   └── workflow_agent.py
│   │
│   ├── api/
│   │   ├── assistant.py
│   │   ├── rag.py
│   │   └── routes/
│   │       └── extractor.py
│   │
│   ├── core/
│   │   └── dependencies.py
│   │
│   ├── models/
│   │   └── ...
│   │
│   ├── prompts/
│   │   ├── domain_prompt.py
│   │   ├── general_prompt.py
│   │   └── rag_prompt.py
│   │
│   ├── services/
│   │   │
│   │   ├── classifier/
│   │   │
│   │   ├── document/
│   │   │   ├── base_loader.py
│   │   │   ├── docling_loader.py
│   │   │   ├── docling_service.py
│   │   │   └── loader_factory.py
│   │   │
│   │   ├── llm/
│   │   │   ├── base_llm.py
│   │   │   └── llm_factory.py
│   │   │
│   │   ├── rag/
│   │   │   ├── document_loader.py
│   │   │   ├── embedding_service.py
│   │   │   ├── indexing_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── retrieval_service.py
│   │   │   ├── text_splitter.py
│   │   │   └── vector_store.py
│   │   │
│   │   └── reranker/
│   │
│   ├── workflow/
│   │   ├── graph.py
│   │   ├── router.py
│   │   ├── state.py
│   │   └── nodes/
│   │       ├── classifier_node.py
│   │       ├── document_node.py
│   │       ├── rag_node.py
│   │       └── summarizer_node.py
│   │
│   ├── config.py
│   └── main.py
│
├── data/
│   ├── policies/
│   │   ├── RBI/
│   │   ├── SBI/
│   │   ├── NPCI/
│   │   ├── Axis/
│   │   └── ICICI/
│   │
│   ├── uploads/
│   ├── logs/
│   └── vector_store/
│
├── frontend/
│   └── streamlit_app.py
│
├── .env
├── pyproject.toml
└── README.md
```

---

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| API Framework | FastAPI |
| Workflow | LangGraph |
| LLM | Groq / Gemini |
| Document Processing | Docling |
| OCR | RapidOCR |
| OCR Runtime | ONNX Runtime |
| Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | Qdrant |
| Reranking | Cross Encoder |
| Frontend | Streamlit |
| Package Manager | uv |
| Server | Uvicorn |

---

## RAG Pipeline

**Indexing (offline):**

```text
Financial Documents → Document Loader → Text Splitting → Sentence Transformer
→ 384-Dimensional Embeddings → Qdrant
```

**Query time:**

```text
User Question → Embedding → Qdrant Vector Search → Candidate Documents
→ Cross-Encoder Reranking → Relevant Context → LLM → Grounded Answer
```

---

## Knowledge Base

Financial documents are stored under `data/policies/`:

```text
data/
└── policies/
    ├── RBI/
    │   ├── KYC_Master_Direction_RBI.pdf
    │   └── Customer_right_RBI.pdf
    │
    ├── SBI/
    │   └── Customer_right_SBI.pdf
    │
    ├── NPCI/
    │   └── BHIM_UPI_NPCI.pdf
    │
    ├── Axis/
    │   └── Credit_card_Axis.pdf
    │
    └── ICICI/
        └── Credit_card_ICIC.pdf
```

These documents are indexed into the Qdrant knowledge base.

---

## Embedding Configuration

```text
Model:     all-MiniLM-L6-v2
Dimension: 384
Distance:  Cosine
```

Qdrant collection configuration:

```text
Collection:  finance_knowledge
Vector Size: 384
Distance:    COSINE
Storage:     data/vector_store/
```

> **Note:** The embedding dimension and Qdrant vector size must always match.

---

## Environment Configuration

Create a `.env` file in the project root:

```env
APP_ENV=development
DEBUG=true

LLM_PROVIDER=groq

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3-flash-preview

EMBEDDING_MODEL=all-MiniLM-L6-v2

VECTOR_SIZE=384

QDRANT_COLLECTION_NAME=finance_knowledge
```

> **Never commit API keys or `.env` files to Git.**

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd finance-ai-assistance
```

### 2. Create Virtual Environment

Using `uv`:

```bash
uv venv
```

### 3. Activate Virtual Environment

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
uv pip install -e .
```

If required packages are not already included:

```bash
uv pip install sentence-transformers
uv pip install docling
uv pip install rapidocr
uv pip install onnxruntime
uv pip install qdrant-client
```

---

## Running the Application

Run the backend from the project root:

```bash
uvicorn backend.main:app --reload
```

The application starts at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### `POST /assistant/chat`

Main multimodal assistant endpoint.

**Accepts:**

| Field | Type | Required |
|---|---|---|
| `question` | string | Yes |
| `file` | file | No |

**Example request:**

```text
Question: Why was this charge deducted?
File:     credit_card_statement.png
```

**Example response:**

```json
{
  "success": true,
  "answer": "The charge was deducted for Amazon Web Services - EC2 Usage...",
  "sources": [
    {
      "document": "knowledge_base/Axis/Credit_card_Axis.pdf",
      "page": 28,
      "score": 0.4014
    }
  ]
}
```

---

## Example Questions

### Financial Knowledge

```text
What is KYC?
What is the Right to Suitability?
What are the customer rights provided by banks?
```

### Image Analysis

Upload a banking screenshot and ask:

```text
What does this screen mean?
Explain this transaction.
Why was this amount deducted?
What is this UPI screen used for?
```

### Document Analysis

Upload a financial document and ask:

```text
Summarize this document.
What are the important points?
Explain this document in simple terms.
```

---

## Image Processing

For image inputs, the application uses Docling with OCR support:

```text
Image → Docling → RapidOCR → Extracted Text → Classifier / RAG → LLM
```

OCR requires ONNX Runtime:

```bash
uv pip install onnxruntime
```

---

## Qdrant

The current development setup uses **Qdrant Local**.

Storage location:

```text
data/vector_store/
```

Only one Qdrant Local client should access this directory at a time. If you see:

```text
Storage folder ... is already accessed by another instance
```

stop the other application/process using the Qdrant storage.

> For concurrent access or production deployment, use a Qdrant server instead of Qdrant Local.

---

## Knowledge Base Indexing

The RAG indexing process:

1. Load financial documents
2. Extract document text
3. Split text into chunks
4. Generate embeddings
5. Create Qdrant points
6. Store embeddings and metadata

Each stored point contains information such as:

```json
{
  "content": "Document chunk...",
  "source": "RBI/KYC_Master_Direction_RBI.pdf",
  "page": 70
}
```

---

## Source Attribution

When an answer is generated from the knowledge base, the API returns the supporting sources so users can identify which financial document and page contributed to the answer.

**Example:**

```json
{
  "sources": [
    {
      "document": "knowledge_base/RBI/KYC_Master_Direction_RBI.pdf",
      "page": 70,
      "score": 0.5278
    },
    {
      "document": "knowledge_base/RBI/KYC_Master_Direction_RBI.pdf",
      "page": 39,
      "score": 0.5686
    }
  ]
}
```

---

## Development Milestones

| # | Milestone |
|---|---|
| 1 | Project Foundation |
| 2 | Document Extraction |
| 3 | Summarizer Agent |
| 4 | Classifier Agent |
| 5 | Vision / Image Analysis |
| 6 | RAG Agent |
| 7 | LangGraph Workflow |
| 8 | Streamlit Frontend |
| 9 | Authentication & Deployment |

---

## Error Handling

### Qdrant Storage Locked

```text
AlreadyLocked
Storage folder ... is already accessed by another instance
```

**Fix:** Stop other processes accessing `data/vector_store/`.

### Embedding Dimension Mismatch

Ensure:

```text
all-MiniLM-L6-v2 → 384 dimensions
```

matches:

```env
VECTOR_SIZE=384
```

### OCR Runtime Missing

```bash
uv pip install onnxruntime
```

### Python Module Import Errors

Run commands from the project root (`finance-ai-assistance/`), for example:

```bash
python -c "from backend.services.rag.embedding_service import EmbeddingService; print('OK')"
```

> Do not run project-level `backend.*` imports while your current directory is inside `backend/`.

---

## Frontend

The project includes a Streamlit frontend at `frontend/streamlit_app.py`. Run it with:

```bash
streamlit run frontend/streamlit_app.py
```

Use it to:

- Ask financial questions
- Upload documents
- Upload images
- View generated answers
- View retrieved sources

---

## Security Considerations

- Store API keys in environment variables.
- Do not commit `.env` source control.
- Do not expose sensitive banking documents publicly.
- Validate uploaded the file types and file sizes.
- Avoid storing personally identifiable financial information unnecessarily.
- Use authenticated access before deploying the application publicly.

---

## Disclaimer

This project is intended for **educational, demonstration, and development purposes**.

The responses generated by this application should not be considered professional financial, investment, legal, or banking advice. Always verify important financial information against the relevant bank, financial institution, or official regulatory source.