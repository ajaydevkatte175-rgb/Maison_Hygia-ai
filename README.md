# 🌿 Maison Hygia AI Support & Fellowship Desk

> *An intelligent, secure, production-grade wellness support and catalog assistant engineered for the Maison Hygia Campus AI Fellowship & Internship evaluation.*

---

## 🎥 Project Demo & Walkthrough
*Watch the live feature demonstration below, showcasing local RAG retrieval, safety guardrails, and the human escalation desk:*

[![Maison Hygia AI Walkthrough]((https://drive.google.com/drive/folders/1Vm5mn3wM2YvUYeXsEBSd-sIWIN_6Ygs-?usp=sharing))
*(If viewing offline, access the full walkthrough video file: `maison_project_demo.mp4`)*

---

## 🌟 Executive Summary & Motivation
As artificial intelligence rapidly transforms digital health and consumer brand interaction, safety and reliability remain paramount. **Maison Hygia AI** was architected to serve as an intelligent, context-aware digital concierge for product catalogs, skin barrier support, and wellness guidelines. 

Built specifically to showcase readiness for the **Maison Hygia Fellowship**, this project balances technical depth (RAG pipelines, local vector search, secure token management) with strict ethical guidelines (clinical crisis guardrails and human-in-the-loop escalation workflows).

---

## 🏗️ Technical Architecture & Tech Stack

The application runs on a modular, privacy-first local stack:
* **Frontend UI:** Streamlit (Responsive web interface with state management, sidebar controls, and custom styling).
* **Orchestration & Framework:** LangChain (Document processing, text chunking, and similarity query loops).
* **Vector Database:** FAISS (Facebook AI Similarity Search) for blazing-fast, localized vector similarity indexation.
* **Embeddings & Inference:** HuggingFace Transformers (`all-MiniLM-L6-v2`) running completely offline to eliminate external API billing quotas and latency.

```text
maison-hygia-ai/
├── .env                  # Environment configurations (Git-ignored for security)
├── .gitignore            # Security rules protecting local API keys & indices
├── requirements.txt      # Pinned project Python dependencies
├── data_store.py         # Markdown/PDF document loader, chunker & FAISS indexer
├── app.py                # Main Streamlit web application & local RAG controller
└── documents/            # Proprietary product line & guideline data stores
    └── maison_hygia_catalog_faq.md  # Structured knowledge base
