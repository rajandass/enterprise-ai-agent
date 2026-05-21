import fitz
import re

pdf_path = "data/source_pdfs/biomolecules.pdf"

doc = fitz.open(pdf_path)

chunks = []

current_section = "Unknown"

for page_number in range(len(doc)):

    page = doc[page_number]

    blocks = page.get_text("blocks")

    page_text = []

    current_section = "Unknown"

    for block in blocks:

        x0, y0, x1, y1, text, *_ = block

        text = text.strip()

        # Ignore sidebar and footer blocks
        if x0 < 150:
            continue

        if y0 > 740:
            continue

        # Detect real section headings
        if re.match(r"^\d+\.\d+\s+[A-Z]", text):
            current_section = text

        page_text.append(text)

    combined_text = "\n".join(page_text)

    chunks.append({
        "page_number": page_number + 1,
        "section": current_section,
        "content": combined_text[:1000]
    })

print(f"Total chunks: {len(chunks)}")

print("\n--- SAMPLE CHUNK ---\n")

print(chunks[0])