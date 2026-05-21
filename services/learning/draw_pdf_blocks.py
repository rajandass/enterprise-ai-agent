import fitz
from PIL import Image, ImageDraw
import os

pdf_path = "data/source_pdfs/biomolecules.pdf"

output_dir = "data/rendered_pages"

os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)

page = doc[3]

zoom = 3

matrix = fitz.Matrix(zoom, zoom)

pix = page.get_pixmap(matrix=matrix)

img_path = os.path.join(output_dir, "page_2_blocks.png")

pix.save(img_path)

image = Image.open(img_path)

draw = ImageDraw.Draw(image)

blocks = page.get_text("blocks")

for block in blocks:

    x0, y0, x1, y1, text, *_ = block

    rect = (
        x0 * zoom,
        y0 * zoom,
        x1 * zoom,
        y1 * zoom
    )

    draw.rectangle(rect, outline="red", width=3)

output_path = os.path.join(
    output_dir,
    "page_2_block_overlay.png"
)

image.save(output_path)

print(f"Saved overlay image: {output_path}")