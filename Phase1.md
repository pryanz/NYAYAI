# OCR Pipeline (Phase 1)

This is the first phase of NyayAI. The goal here is simple:

**Take scanned PDFs / images and reliably turn them into clean text.**

No APIs. No embeddings. No LLMs. Just a solid OCR backbone that can survive bad inputs, crashes, and missing GPUs.

---

## Folder Structure

```
NYAYAI/
├── docker/
│   ├── ocr/
│   │   └── Dockerfile
│   └── api/
│       └── Dockerfile
│
├── src/
│   ├── ocr/
│   │   ├── pdf_to_images.py
│   │   ├── gpu_preprocessor.py
│   │   ├── layout_detector.py
│   │   ├── ocr_engine_paddle.py
│   │   ├── text_reconstructor.py
│   │   ├── text_postprocessor.py
|   |   ├── pdf_text_extractor.py
│   │   └── pipeline.py
│   │
│   ├── api/            # kept empty for Phase 2
│   └── common/
│       └── config.py
│
├── data/
│   ├── raw/            # input files (read-only in prod)
│   ├── processed/      # final outputs
│   └── temp/           # intermediate work (required)
│
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## What Phase 1 Does

Phase 1 only does **OCR and text cleanup**.

It is built with a few assumptions in mind:

* PDFs can be broken, huge, or malicious
* Long documents will fail halfway sometimes
* GPU might not be available everywhere

So the pipeline is written to be **defensive**, **restartable**, and **boring** (in a good way).

---

## Pipeline Overview

```
PDF / Image
  ↓
PDF → Images (Poppler, 300 DPI)
  ↓
Image preprocessing (GPU if available, CPU otherwise)
  ↓
Layout detection (optional but recommended)
  ↓
OCR (GPU if available)
  ↓
Text reconstruction
  ↓
Post-processing and cleanup
  ↓
Clean text + metrics
```

Each step writes its output to disk so the pipeline can resume if something crashes.

---

## Modules

### pdf_to_images.py

Turns a PDF into page images.

* Uses `pdftoppm` (Poppler)
* Fixed 300 DPI (good tradeoff for OCR)
* One image per page
* Protected with timeouts

If the images already exist on disk, this step is skipped.

---

### gpu_preprocessor.py

Prepares images for OCR.

* Denoising
* Deskewing
* Contrast normalization

If CUDA is available, it uses GPU. Otherwise it silently falls back to CPU.

---

### layout_detector.py

Finds text regions on the page.

* Uses PaddleOCR detection model
* Separates text from tables / figures
* Prevents OCR on non-text areas

This step is optional but improves speed and accuracy on complex documents.

---

### ocr_engine_paddle.py

Runs the actual OCR.

* PaddleOCR (PP-OCRv4)
* Hindi + English
* Batch processing
* GPU if available

OCR output is kept structured instead of immediately flattening to text.

---

### text_reconstructor.py

Turns OCR blocks into readable text.

* Orders lines top-to-bottom
* Left-to-right grouping
* Paragraph clustering

This is kept separate from OCR so it can be improved independently.

---

### text_postprocessor.py

Final cleanup step.

* Unicode normalization
* Light OCR error cleanup
* Header / footer removal
* Confidence calculation

No aggressive correction is done here to avoid damaging legal text.

---

### pipeline.py

This is the orchestrator.

* Runs all stages in order
* Handles page-level failures
* Makes the pipeline restartable
* Does not contain OCR logic itself

Each page is treated as an independent unit so one bad page does not kill the whole document.

---

## Output

```
data/processed/
├── text/
│   ├── document_ocr_raw.json
│   ├── document_ocr_layout.json
│   ├── document_clean_text.txt
│   └── document_metrics.json
```

For every document we get:

* raw OCR output
* layout-aware OCR
* cleaned plain text
* confidence and quality stats

---

## Usage

### From code

```python
from src.ocr.pipeline import OCRPipeline

pipeline = OCRPipeline(use_layout=True, use_postprocess=True)
doc = pipeline.run("input.pdf")
```

### From terminal

```bash
python src/ocr/pipeline.py
```

The pipeline:

1. Reads files from `data/raw/`
2. Creates a working directory in `data/temp/`
3. Skips steps that already ran
4. Writes final results to `data/processed/`

---

## Configuration

All paths and basic flags live in `config.py`.

```python
RAW_DIR = "../data/raw"
BASE_PROCESSED_DIR = "../data/processed"
TEXT_DIR = f"{BASE_PROCESSED_DIR}/text"
VISUAL_DIR = f"{BASE_PROCESSED_DIR}/visuals"
TABLE_DIR = f"{BASE_PROCESSED_DIR}/tables"

LANGUAGES = ['hi', 'en']
USE_GPU = True
```

---

## Safety Notes

* OCR runs inside Docker
* Input directory should be mounted read-only
* No network access is required
* PDFs are never trusted
* Intermediate files are isolated per document

---

## What This Phase Does NOT Do

Phase 1 intentionally avoids:

* APIs
* databases
* embeddings
* LLMs
* legal reasoning

Those come later.

---

## What Comes Next

**Phase 2**

* API ingestion
* async job handling
* multiple OCR workers
* upload validation

**Phase 3**

* embeddings (FAISS / Qdrant)
* statute linking
* semantic search
* legal intelligence layer

---

## Status

Phase 1 is done.

The OCR pipeline is stable, restartable, and safe enough to build on.

Everything else builds on top of this.
