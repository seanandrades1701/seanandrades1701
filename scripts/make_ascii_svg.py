from PIL import Image

INPUT = "source-prepped.png"
OUTPUT = "avi-ascii.svg"

RAMP = " .:-=+*#%@"
WIDTH = 100

img = Image.open(INPUT).convert("L")

# Keep characters roughly square-shaped
aspect_ratio = img.height / img.width
height = int(WIDTH * aspect_ratio * 0.5)

img = img.resize((WIDTH, height))

lines = []

for y in range(img.height):
    line = ""

    for x in range(img.width):
        brightness = img.getpixel((x, y))
        index = int((255 - brightness) / 255 * (len(RAMP) - 1))
        line += RAMP[index]

    lines.append(line)

svg_width = WIDTH * 8
svg_height = height * 14

text_lines = []

for y, line in enumerate(lines):
    escaped = (
        line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )

    text_lines.append(
        f'<text x="0" y="{(y + 1) * 14}" '
        f'font-family="monospace" font-size="14" '
        f'fill="#cccccc">{escaped}</text>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{svg_width}" height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">
<rect width="100%" height="100%" fill="white"/>
{"".join(text_lines)}
</svg>
'''

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Created {OUTPUT}")