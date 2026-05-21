import fitz
import os

pdf_path = "data/source_pdfs/biomolecules.pdf"

output_dir = "data/rendered_pages"

os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)

page = doc[0]

zoom = 3

matrix = fitz.Matrix(zoom, zoom)

pix = page.get_pixmap(matrix=matrix)

output_path = os.path.join(output_dir, "page_1.png")

pix.save(output_path)

print(f"Rendered page saved: {output_path}")