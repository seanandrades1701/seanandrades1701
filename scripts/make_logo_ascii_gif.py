from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

INPUT = Path("source-photo.png")
OUTPUT = Path("github-logo-ascii.gif")

WIDTH = 70
FPS = 12
FRAME_COUNT = 36

RAMP = " .:-=+*#%@"

# Try a monospace font available on Windows.
FONT_PATHS = [
    r"C:\Windows\Fonts\consola.ttf",
    r"C:\Windows\Fonts\cour.ttf",
]

font = None

for path in FONT_PATHS:
    if Path(path).exists():
        font = ImageFont.truetype(path, 14)
        break

if font is None:
    font = ImageFont.load_default()


image = Image.open(INPUT).convert("L")

# Increase contrast so the GitHub mark survives ASCII conversion.
image = ImageEnhance.Contrast(image).enhance(2.2)

aspect = image.height / image.width

height = max(
    10,
    int(WIDTH * aspect * 0.48)
)

image = image.resize(
    (WIDTH, height)
)


# Convert image to ASCII.
ascii_lines = []

for y in range(height):

    line = ""

    for x in range(WIDTH):

        brightness = image.getpixel((x, y))

        index = int(
            (255 - brightness)
            / 255
            * (len(RAMP) - 1)
        )

        index = max(
            0,
            min(len(RAMP) - 1, index)
        )

        line += RAMP[index]

    ascii_lines.append(line)


# Calculate output dimensions.
bbox = font.getbbox("M")
char_height = bbox[3] - bbox[1]

char_width = font.getlength("M")

canvas_width = int(
    WIDTH * char_width + 50
)

canvas_height = int(
    height * (char_height + 2) + 50
)


frames = []


for frame_number in range(FRAME_COUNT):

    frame = Image.new(
        "RGB",
        (canvas_width, canvas_height),
        "#05080d"
    )

    draw = ImageDraw.Draw(frame)

    # Border.
    draw.rounded_rectangle(
        (
            5,
            5,
            canvas_width - 6,
            canvas_height - 6
        ),
        radius=14,
        outline="#30363d",
        width=2
    )

    # GitHub-style window dots.
    draw.ellipse(
        (22, 20, 34, 32),
        fill="#ff5f56"
    )

    draw.ellipse(
        (42, 20, 54, 32),
        fill="#ffbd2e"
    )

    draw.ellipse(
        (62, 20, 74, 32),
        fill="#27c93f"
    )

    # Animation sweep.
    reveal = int(
        WIDTH
        * (
            (frame_number % FRAME_COUNT)
            / FRAME_COUNT
        )
    )

    for row, line in enumerate(ascii_lines):

        for column, character in enumerate(line):

            if character == " ":
                continue

            # Add a moving scan/reveal effect.
            distance = (
                column
                - reveal
            )

            if distance < -8:
                brightness = "#183522"

            elif distance < 2:
                brightness = "#39d353"

            else:
                brightness = "#7ee787"

            x = int(
                20 + column * char_width
            )

            y = int(
                50
                + row * (char_height + 2)
            )

            draw.text(
                (x, y),
                character,
                font=font,
                fill=brightness
            )

    # Bottom label.
    draw.text(
        (
            20,
            canvas_height - 25
        ),
        "GITHUB // ASCII",
        font=font,
        fill="#6e7681"
    )

    frames.append(frame)


frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / FPS),
    loop=0,
    optimize=False
)

print(f"Created {OUTPUT}")
print(f"Frames: {len(frames)}")