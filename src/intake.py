import fitz 
import os

# Define supported extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
PDF_EXTENSIONS = {'.pdf'}

def analyze_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    file_name = os.path.basename(file_path)

    # BRANCH A: Image Files
    if ext in IMAGE_EXTENSIONS:
        return f"IMAGE DETECTED: {file_name} -> [Action: Send straight to Tesseract OCR]"

    # BRANCH B: PDF Files
    elif ext in PDF_EXTENSIONS:
        doc = fitz.open(file_path)
        # Check first page as a sample
        page = doc[0]
        text = page.get_text().strip()
        fonts = page.get_fonts()
        doc.close()

        if len(text) > 100 and len(fonts) > 0:
            return f"DIGITAL PDF: {file_name} -> [Action: Use Fast Text Extraction]"
        else:
            return f"SCANNED PDF: {file_name} -> [Action: Convert to Image then OCR]"

    else:
        return f"UNKNOWN FILE TYPE: {file_name}"

# Updated loop to scan your data/raw folder
RAW_DIR = "data/raw"

# Safety check: make sure folder exists
if not os.path.exists(RAW_DIR):
    os.makedirs(RAW_DIR)
    print(f"Created {RAW_DIR} folder. Please put your files there.")

for filename in os.listdir(RAW_DIR):
    path = os.path.join(RAW_DIR, filename)
    print(analyze_file(path))