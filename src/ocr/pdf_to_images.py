import subprocess
from pathlib import Path
from typing import List

from src.common.config import PDF_DPI, MAX_PDF_PAGES


def pdf_to_images(pdf_path: Path, out_dir: Path) -> List[Path]:
    """
    Convert a PDF into page-wise PNG images using pdftoppm.

    This function treats PDFs as untrusted input and enforces:
    - input validation
    - explicit error handling
    - hard limits on output
    - no silent failures
    """

    # -------- input validation --------

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if not pdf_path.is_file():
        raise RuntimeError(f"PDF path is not a file: {pdf_path}")

    try:
        pdf_path.open("rb").close()
    except Exception as e:
        raise RuntimeError(f"PDF is not readable: {e}")

    # -------- output directory validation --------

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise RuntimeError(f"Cannot create output directory {out_dir}: {e}")

    if not out_dir.is_dir():
        raise RuntimeError(f"Output path is not a directory: {out_dir}")

    # pdftoppm uses an output prefix, not a directory
    prefix = out_dir / "page"

    cmd = [
        "pdftoppm",
        "-r", str(PDF_DPI),
        "-png",
        pdf_path.as_posix(),
        prefix.as_posix(),
    ]

    # -------- subprocess execution --------

    try:
        result = subprocess.run(
            cmd,
            check=True,
            timeout=120,  # safer default for large PDFs
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

    except FileNotFoundError:
        raise RuntimeError(
            "pdftoppm not found. Install poppler-utils to enable PDF rasterization."
        )

    except subprocess.TimeoutExpired:
        raise RuntimeError(
            "pdftoppm timed out while processing the PDF. "
            "The file may be very large or malformed."
        )

    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors="ignore").strip()
        raise RuntimeError(
            f"pdftoppm failed while processing PDF: {err or 'unknown error'}"
        )

    # -------- post-run validation --------

    pages = sorted(out_dir.glob("page-*.png"))

    if not pages:
        raise RuntimeError(
            "pdftoppm completed but produced no images. "
            "The PDF may be empty or unsupported."
        )

    if len(pages) > MAX_PDF_PAGES:
        raise RuntimeError(
            f"PDF produced {len(pages)} pages, exceeds limit of {MAX_PDF_PAGES}"
        )

    return pages
