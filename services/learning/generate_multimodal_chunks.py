import fitz
import re
import json

pdf_path = "data/source_pdfs/biomolecules.pdf"

doc = fitz.open(pdf_path)

chunks = []

for page_number in range(len(doc)):

    page = doc[page_number]

    blocks = page.get_text("blocks")

    current_section = "Unknown"

    page_text_parts = []

    figure_refs = []

    for block in blocks:

        x0, y0, x1, y1, text, *_ = block

        text = text.strip()

        # Ignore sidebar blocks
        if x0 < 150:
            continue

        # Ignore footer blocks
        if y0 > 740:
            continue

        # Detect section heading
        if re.match(r"^\d+\.\d+\s+[A-Z]", text):
            current_section = text

        # Detect figure references
        figures = re.findall(r"Figure\s+\d+\.\d+", text)

        if figures:
            figure_refs.extend(figures)

        page_text_parts.append(text)

    combined_text = "\n".join(page_text_parts)

    chunk = {
        "chunk_id": f"page_{page_number + 1}",
        "section": current_section,
        "page_number": page_number + 1,
        "text_content": combined_text[:1500],
        "figure_references": list(set(figure_refs)),
        "source_document": "biomolecules.pdf"
    }

    chunks.append(chunk)

print(f"Generated chunks: {len(chunks)}")

print("\n--- SAMPLE CHUNK ---\n")

print(json.dumps(chunks[1], indent=2))