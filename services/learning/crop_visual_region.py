from PIL import Image
import os

image_path = "data/rendered_pages/page_2_blocks.png"

output_dir = "data/cropped_regions"

os.makedirs(output_dir, exist_ok=True)

image = Image.open(image_path)

# Amino acids region
crop_box = (
    1400, 400,
    2900, 1100
)

cropped = image.crop(crop_box)

output_path = os.path.join(
    output_dir,
    "amino_acids_region.png"
)

cropped.save(output_path)

print(f"Saved cropped region: {output_path}")