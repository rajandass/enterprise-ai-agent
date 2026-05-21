import fitz
import re
import json

pdf_path = "data/source_pdfs/biomolecules.pdf"

doc = fitz.open(pdf_path)

chunks = []

current_chunk = None

for page_number in range(len(doc)):

    page = doc[page_number]

    blocks = page.get_text("blocks")

    for block in blocks:

        x0, y0, x1, y1, text, *_ = block

        text = text.strip()
        noise_patterns = [
            "BIOMOLECULES",
            "CHAPTER  9",
            "Reprint 2026-27"
        ]

        if text in noise_patterns:
            continue

        # Ignore sidebar
        if x0 < 150:
            continue

        # Ignore footer
        if y0 > 740:
            continue

        # Detect section heading
        section_match = re.match(
            r"^\d+\.\d+\s+[A-Z]",
            text
        )

        if section_match:

            # Save previous chunk
            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = {
                "chunk_id": f"section_{len(chunks)+1}",
                "section": text,
                "start_page": page_number + 1,
                "text_content": "",
                "figure_references": [],
                "source_document": "biomolecules.pdf"
            }

        if current_chunk:
            
            current_chunk["text_content"] += "\n" + text
            text = re.sub(r"BIOMOLECULES", "", text)
            text = re.sub(r"CHAPTER\s+9", "", text)
            text = re.sub(r"Reprint\s+\d{4}-\d{2}", "", text)

            figures = re.findall(
                r"Figure\s+\d+\.\d+",
                text
            )

            current_chunk["figure_references"].extend(figures)

# Save final chunk
if current_chunk:
    chunks.append(current_chunk)

# Remove duplicate figure refs
for chunk in chunks:

    chunk["text_content"] = re.sub(
        r"BIOMOLECULES",
        "",
        chunk["text_content"]
    )

    chunk["text_content"] = re.sub(
        r"CHAPTER\s+9",
        "",
        chunk["text_content"]
    )

    chunk["text_content"] = re.sub(
        r"Reprint\s+\d{4}-\d{2}",
        "",
        chunk["text_content"]
    )
    
    chunk["figure_references"] = list(
        set(chunk["figure_references"])
    )

print(f"Generated chunks: {len(chunks)}")

print("\n--- SAMPLE CHUNK ---\n")

print(json.dumps(chunks[0], indent=2)[:3000])