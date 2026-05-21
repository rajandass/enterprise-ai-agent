import fitz

pdf_path = "data/source_pdfs/biomolecules.pdf"

doc = fitz.open(pdf_path)

page = doc[1]

blocks = page.get_text("blocks")

print(f"Total blocks: {len(blocks)}")

print("\n--- BLOCKS ---\n")

for idx, block in enumerate(blocks):

    x0, y0, x1, y1, text, *_ = block

    print(f"\nBLOCK {idx}")
    print(f"Coordinates: ({x0}, {y0}) -> ({x1}, {y1})")

    if "Amino" in text or "Glycine" in text or "Alanine" in text:
        print("\nMATCHED BLOCK")
        print(f"Coordinates: ({x0}, {y0}) -> ({x1}, {y1})")
        print(text)

    print(text[:500])