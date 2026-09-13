import sys
from io import BytesIO

from PIL import Image, ImageEnhance

try:
    from rembg import remove
except ImportError as e:
    print("Missing library:", e)
    sys.exit(1)


if len(sys.argv) != 2:
    print("Usage: python scripts\\prep_photo.py source-photo.png")
    sys.exit(1)


input_file = sys.argv[1]
output_file = "source-prepped.png"


with open(input_file, "rb") as f:
    input_data = f.read()


# Remove the original background.
output_data = remove(input_data)

subject = Image.open(BytesIO(output_data)).convert("RGBA")


# Crop away transparent space around the subject.
alpha = subject.getchannel("A")
bbox = alpha.getbbox()

if bbox:
    subject = subject.crop(bbox)


# Add a small amount of breathing room around the subject.
padding = 80

canvas = Image.new(
    "RGBA",
    (
        subject.width + padding * 2,
        subject.height + padding * 2,
    ),
    "white",
)

canvas.alpha_composite(subject, (padding, padding))


# Convert to grayscale and increase contrast for ASCII.
gray = canvas.convert("L")
gray = ImageEnhance.Contrast(gray).enhance(1.8)


gray.save(output_file)

print(f"Created {output_file}")
print(f"Final size: {gray.size}")