# LeagueLens 🏏

**LeagueLens** is an advanced AI-powered sports intelligence system that delivers real-time analytics, dynamic match commentary, and conversational interaction. Built on a robust **Self-RAG (Self-Refining Retrieval-Augmented Generation)** pipeline powered by **LangGraph**, it combines structured statistical data with unstructured live context to provide deep cricketing insights.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-RAG-orange)
![Pathway](https://img.shields.io/badge/Pathway-Vector%20Store-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Docker](https://img.shields.io/badge/Deployment-Docker-blue)

---

## 📖 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
  - [LangGraph Pipeline](#langgraph-pipeline)
  - [Data Ingestion & Updates](#data-ingestion--updates)
  - [Live Commentary Module](#live-commentary-module)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [Future Roadmap](#future-roadmap)

---

## 🔍 Overview
LeagueLens bridges the gap between static sports statistics and real-time query resolution. Unlike standard chatbots, it utilizes a **Hybrid Retrieval** approach—querying structured SQL databases for stats (e.g., "How many runs did Kohli score in 2016?") and unstructured document stores for context (e.g., "Describe the match atmosphere").

It features a **Dynamic Commentary Engine** capable of generating text and voice commentary (TTS) using live match data.

---

## 🚀 Key Features

* **Self-RAG Question Answering:** A self-correcting pipeline that grades document relevance and triggers web searches if internal data is insufficient.
* **Hybrid Retrieval:** Combines **SQL** (for structured IPL/cricket stats) and **Vector Search** (Pathway Document Store) for unstructured bios and articles.
* **Real-Time Live Commentary:** Generates play-by-play commentary with **Text-to-Speech (TTS)** integration (ElevenLabs).
* **Multi-Modal Interaction:** Supports both Voice and Text inputs from users.
* **Automated Data Pipelines:** Uses Cron jobs and **FireCrawl** to scrape ESPNcricinfo and keep the knowledge base fresh.

---

## 🏗 System Architecture

### 1. LangGraph Pipeline (Self-RAG)
The core logic is powered by a graph-based workflow that ensures accuracy through iterative reasoning.

* **Retrieve:** Fetches data using BM25 and Semantic Search.
* **Grade:** Evaluates if the retrieved documents are relevant.
* **Web Search:** Triggered conditionally if the internal context is missing or low-quality.
* **Generate & Loop:** Generates a response and checks for usefulness; if the answer is poor, it transforms the query and loops back.



### 2. Updating Vector Database
To ensure the bot knows about the latest matches, we run a scheduled pipeline:
1.  **Base Question/Web Search:** Gathers new information.
2.  **CSV Updates:** Appends new data to the context files.
3.  **Vector Store Sync:** Pathway updates the embeddings automatically.



### 3. Live Commentary Schematic
The system ingests live data streams to generate immersive commentary.
* **Input:** Live Data feed.
* **Process:** LLM-based Comment Generator.
* **Output:** Text displayed on UI + TTS Audio output.



---

## 🛠 Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Orchestration** | LangGraph, LangChain |
| **Vector Store** | Pathway |
| **Database** | PostgreSQL (Structured Stats) |
| **Data Ingestion** | FireCrawl (Scraping), Kaggle Datasets |
| **LLM** | OpenAI GPT-4o / GPT-3.5-turbo |
| **Voice/Audio** | ElevenLabs API (Text-to-Speech) |
| **Deployment** | Docker, REST APIs |

---

## ⚡ Installation & Setup

### Prerequisites
* Docker & Docker Compose
* Python 3.10+
* API Keys: OpenAI, FireCrawl, ElevenLabs

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/LeagueLens.git](https://github.com/your-username/LeagueLens.git)
cd LeagueLens
