import sys
from PIL import Image, ImageOps, ImageEnhance

try:
    import cv2
    import numpy as np
    from rembg import remove
except ImportError as e:
    print("Missing library:", e)
    sys.exit(1)


if len(sys.argv) != 2:
    print("Usage: python scripts\\prep_photo.py source-photo.png")
    sys.exit(1)

input_file = sys.argv[1]
output_file = "source-prepped.png"

# Remove the background
with open(input_file, "rb") as f:
    input_data = f.read()

output_data = remove(input_data)

# Open the background-removed image
from io import BytesIO

subject = Image.open(BytesIO(output_data)).convert("RGBA")

# Put the subject on a pure white background
background = Image.new("RGBA", subject.size, "white")
background.alpha_composite(subject)

# Convert to grayscale
gray = background.convert("L")

# Increase contrast
gray = ImageEnhance.Contrast(gray).enhance(1.8)

# Save the prepared image
gray.save(output_file)

print(f"Created {output_file}")