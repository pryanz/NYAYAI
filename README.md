# NyayAI

NyayAI is a legal document analysis system focused on **correctness, traceability, and auditability** for Indian legal documents.

The project is being built in phases. Right now, the focus is deliberately narrow: **document ingestion and OCR done properly**. Everything that comes later depends on this layer being correct.

NyayAI is not a chatbot and not a general-purpose assistant. It is a backend system that turns messy legal documents into **clean, reliable, reviewable text** that higher-level reasoning systems can safely depend on.

---

## What NyayAI Is (and Is Not)

NyayAI is designed to:

* handle Indian legal PDFs (judgments, bare acts, petitions, annexures)
* survive bad inputs (scanned pages, hybrid PDFs, broken files)
* avoid guessing or hallucination
* preserve uncertainty instead of hiding it

NyayAI is **not**:

* an LLM wrapper
* a “chat with your PDF” tool
* an end-user product (yet)

---

## Core Design Principles

### 1. Legal documents are hostile input

PDFs can be malformed, extremely large, partially scanned, or inconsistent across pages.

Because of this:

* OCR runs in isolation
* no network access is required during processing
* failures are expected and handled per page

---

### 2. Partial failure is acceptable

A 300-page judgment does not become useless because one page is unreadable.

* Each page is processed independently
* Failed pages are recorded, not hidden
* The document still completes with honest metadata

---

### 3. OCR is a fallback, not a default

Not all PDFs need OCR.

* Born-digital PDFs use their existing text layer
* Hybrid PDFs are handled page by page
* OCR runs only where text is missing or unusable

This avoids unnecessary GPU usage and prevents introducing OCR noise into clean documents.

---

### 4. Everything must be restartable

Large legal documents fail mid-way. That is normal.

* Intermediate outputs are written to disk
* Reruns resume instead of starting over
* No stage assumes in-memory continuity

---

## Phase 1: OCR & Text Normalization (Current)

Phase 1 is about **seeing clearly**.

### What Phase 1 Does

* Accepts PDFs and images
* Detects whether each page has a usable text layer
* Runs OCR only on pages that need it
* Reconstructs readable text
* Performs light cleanup
* Produces confidence and failure metadata

There are no embeddings, APIs, or reasoning layers in Phase 1. The goal is correctness, not intelligence.

---

### OCR Pipeline (Phase 1)

```
PDF / Image
  ↓
Page-wise analysis
  ├─ Text layer exists → extract directly
  └─ No text layer     → OCR pipeline
        ↓
        Image preprocessing
        ↓
        Layout detection (optional)
        ↓
        OCR
        ↓
        Text reconstruction
        ↓
        Cleanup & confidence
```

Each page moves independently through this flow.

---

### Why This Matters

Indian legal documents are often:

* partially scanned
* partially digital
* full of tables, seals, stamps, and annexures

Treating everything as OCR wastes resources and reduces quality.
Treating everything as text extraction misses scanned content.

NyayAI handles both, page by page.

---

## Phase 2: Embeddings & Retrieval (Planned)

Phase 2 introduces **InLegalBERT**.

Its role is not to answer questions, but to:

* embed cleaned legal text
* enable retrieval
* support cross-document comparison
* feed higher-level validation logic

At this stage:

* InLegalBERT acts purely as a feature extractor
* it does not generate text
* it does not make legal decisions

The OCR pipeline remains unchanged and feeds Phase 2.

---

## Phase 3: Legal Validation & Reasoning (Planned)

Later phases will introduce:

* statute consistency checks
* entity cross-verification (names, dates, case numbers)
* contradiction detection across pages
* full audit trails for every claim

These layers will be built on top of the clean text produced by Phase 1.

If Phase 1 lies, everything above it collapses.

---

## Security & Privacy

NyayAI is designed for sensitive legal material.

* OCR runs inside containers
* input data can be mounted read-only
* no external calls are required
* failures are logged explicitly
* no silent correction of legal text

Later phases may add encryption and access controls, but the system already assumes zero trust.

---

## Status

* OCR pipeline: implemented
* Hybrid PDF handling: implemented
* Page-level failure handling: implemented
* Restartability: implemented

Higher-level reasoning is intentionally deferred until ingestion is solid.

---

## Why This README Is Boring (On Purpose)

Legal systems fail when they overpromise.

This README describes:

* what exists
* what is planned
* what is explicitly not done yet

NyayAI is being built to be **correct first**, not impressive first.

Everything else comes later.
