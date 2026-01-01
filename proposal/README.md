# Installation & Setup Guide

This guide explains how to set up and run the project locally using **Poetry** for dependency management.

---

## Prerequisites

Make sure you have the following installed on your system:

- **Python** (>= 3.10 recommended)
- **Poetry**  
  Install Poetry from: https://python-poetry.org/docs/#installation
- Internet access (required for web research and API calls)

---

## Clone the Repository

```bash
git clone https://github.com/kumar-sanchay/buisness-proposal.git
cd buisness-proposal
```

---

## Install Dependencies

```bash
cd proposal
poetry install
```

---

## Copy Environment Template

```bash
cp env.sample .env
```

## Configure Environment Variables inside .env
### Environment Variables Explained

- GROQ_API_KEY
  Used for LLM inference via Groq.

- LANGSMITH_API_KEY
  Enables tracing, debugging, and observability for LangChain/LangGraph workflows.

- LANGSMITH_PROJECT
  Logical project name under which traces will appear in LangSmith.

- TAVILY_API_KEY
  Used for web search and online data collection during proposal research.

- CHROMA_DB_COLLECTION_NAME and CHROMADB_DIRECTORY
  Chroma db details and directories

---

## Activate the Virtual Environment

```bash
cd proposal
python -m poetry env activate
```

---

## Run Streamlit app

```bash
streamlit run src/proposal/ui/proposal_builder.py
```