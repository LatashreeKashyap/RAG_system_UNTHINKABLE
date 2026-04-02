#  Enterprise AI Knowledge Base: Local RAG Assistant

An industry-level **Retrieval-Augmented Generation (RAG)** system built to provide secure, private, and local document intelligence. This application allows users to chat with their private PDF documents using **Llama 3.2** without their data ever leaving their machine.

---

##  Key Features
* **Privacy First:** Powered by **Ollama (Llama 3.2)** and **HuggingFace Embeddings** for 100% local processing.
* **Source Attribution:** Unlike standard chatbots, this system cites the specific PDF documents used to generate each answer.
* **High Performance:** Uses **FAISS** (Facebook AI Similarity Search) for lightning-fast document retrieval.
* **Modern UI:** A clean, professional dashboard built with **Streamlit**.
* **Scalable Backend:** Robust API architecture powered by **FastAPI**.

---

##  System Architecture
The project is split into two main components:
1.  **The Brain (Backend):** A FastAPI server that manages the RAG pipeline, document indexing, and AI inference.
2.  **The Face (Frontend):** A Streamlit user interface for seamless chat interaction and source visualization.

---

##  Getting Started

### 1. Prerequisites
* Python 3.10+
* [Ollama](https://ollama.com/) installed and running.
* Llama 3.2 model pulled:
    ```bash
    ollama pull llama3.2:1b
    ```

### 2. Installation
1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd unthinkableKnowledgeAsses
