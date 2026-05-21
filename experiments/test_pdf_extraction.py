import fitz

pdf_path = "data/source_pdfs/biomolecules.pdf"

doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")

print("\n--- PAGE 1 TEXT ---\n")

page = doc[0]

text = page.get_text()

print(text[:3000])