import fitz
import re
import json

pdf_path = "data/source_pdfs/biomolecules.pdf"

doc = fitz.open(pdf_path)

# Step 1 — Build section chunks

section_chunks = []

current_chunk = None

for page_number in range(len(doc)):

    page = doc[page_number]

    blocks = page.get_text("blocks")

    for block in blocks:

        x0, y0, x1, y1, text, *_ = block

        text = text.strip()

        if x0 < 150:
            continue

        if y0 > 740:
            continue

        section_match = re.match(
            r"^\d+\.\d+\s+[A-Z]",
            text
        )

        if section_match:

            if current_chunk:
                section_chunks.append(current_chunk)

            current_chunk = {
                "section": text,
                "content": ""
            }

        if current_chunk:
            current_chunk["content"] += "\n" + text

# Final section
if current_chunk:
    section_chunks.append(current_chunk)

# Step 2 — Normalize content

for chunk in section_chunks:

    chunk["content"] = re.sub(
        r"BIOMOLECULES",
        "",
        chunk["content"]
    )

    chunk["content"] = re.sub(
        r"CHAPTER\s+9",
        "",
        chunk["content"]
    )

# Step 3 — Concept splitting

concept_keywords = [
    "Amino acids",
    "Lipids",
    "Fatty acids",
    "Proteins",
    "Enzymes"
]

concept_chunks = []

for section in section_chunks:

    content = section["content"]

    split_pattern = "|".join(
        map(re.escape, concept_keywords)
    )

    parts = re.split(
        f"({split_pattern})",
        content
    )

    current_concept = ""

    for part in parts:

        part = part.strip()

        if not part:
            continue

        if part in concept_keywords:

            current_concept = part

            continue

        full_content = (
            f"{current_concept} {part}"
            if current_concept
            else part
        )

        concept_chunks.append({
            "section": section["section"],
            "concept": current_concept or "General",
            "content": full_content[:1200]
        })


with open(
    "concept_chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        concept_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )

print("\nSaved concept_chunks.json")

print(f"Concept chunks: {len(concept_chunks)}")

print("\n--- SAMPLE CONCEPT CHUNK ---\n")

print(json.dumps(concept_chunks[1], indent=2))