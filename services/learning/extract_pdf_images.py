import fitz
import os

pdf_path = "data/source_pdfs/biomolecules.pdf"

output_dir = "data/extracted_images"

os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)

image_count = 0

for page_index in range(len(doc)):

    page = doc[page_index]

    image_list = page.get_images(full=True)

    print(f"Page {page_index + 1}: {len(image_list)} images")

    for img_index, img in enumerate(image_list):

        xref = img[0]

        base_image = doc.extract_image(xref)

        image_bytes = base_image["image"]

        image_ext = base_image["ext"]

        image_filename = (
            f"page_{page_index + 1}_img_{img_index + 1}.{image_ext}"
        )

        image_path = os.path.join(output_dir, image_filename)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        image_count += 1

print(f"\nTotal extracted images: {image_count}")