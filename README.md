# NyayAI: Legal Intelligence & Document Audit System ⚖️

NyayAI is a specialized legal assistant system designed to provide high-precision document proofreading, statutory validation, and semantic search for the Indian legal framework. Unlike general-purpose LLMs, NyayAI utilizes a **discriminative RAG architecture** centered around **InLegalBERT** to act as a "Critical Reviewer" for legal professionals.

## 🏗️ System Architecture

The project is built on a "Brain and Eye" philosophy:
* **The Eye (InLegalBERT):** A transformer-based model optimized for feature extraction, Named Entity Recognition (NER), and role labeling within legal text.
* **The Brain (Logic Engine):** A state-management system that maintains an "Internal Ledger" to cross-check entities, verify statutes, and resolve conflicts across multi-page documents.

### 1. Data Intake & OCR Pipeline
Designed to handle the complexities of Indian legal documentation, including borderless tables and hybrid-quality PDFs:
* **Digital PDFs:** Processed via `PyMuPDF` or `pdfminer.six`.
* **Scanned Media:** Utilizes `EasyOCR` for better table handling and `OpenCV` with `pdf2image` for high-quality preprocessing.
* **Hybrid Logic:** Automatically triggers high-quality OCR if existing text confidence scores fall below a defined threshold.
* **Layout Detection:** Employs `YOLOv8-doc` for identifying tables and complex layouts before processing.

### 2. Internal Reasoning Layers
* **Semantic Decomposition:** Breaks documents into legal units (Citations, Facts, Prayers) to apply context-specific validation rules.
* **Entity-Relation Mapping:** Maintains a dynamic state table to find inconsistencies in names, dates, or case numbers across hundreds of pages.
* **Multi-Head Validation:** Parallel "Auditors" (Fact, Statutory, and Linguistic) cross-reference content against an internal ledger and a local Indian Law database.

### 3. Production Storage & Security
* **Vector Layer:** `ChromaDB` (via LangChain) for persistent semantic memory.
* **Relational Layer:** `PostgreSQL` for managing structured internal ledgers and entity relationships.
* **Worker-Broker Flow:** Uses `FastAPI`, `Redis`, and `Celery` to handle heavy PDF processing asynchronously.
* **Triple-Lock Security:** Implements `LUKS` for disk encryption, `TDE` for database encryption, and `AES-256` at the application layer to ensure absolute data privacy.

## 🛠️ Tech Stack
- **Model:** InLegalBERT (Embeddings & Tokenization)
- **Orchestration:** LangChain (Parent Document Retriever strategy)
- **Databases:** ChromaDB (Vector) and PostgreSQL (Relational)
- **Environment:** Dockerized Dev Containers (Ubuntu 22.04 base)


## 🧪 Evaluation Framework
NyayAI is evaluated against a "Golden Dataset" of manually audited Indian legal documents. The system prioritizes **Recall (Safety)** over Precision, ensuring that critical legal errors are caught even at the risk of higher false alarms.