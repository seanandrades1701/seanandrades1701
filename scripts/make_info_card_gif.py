from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT = Path("info-card.gif")

WIDTH = 620
HEIGHT = 350

FPS = 12

roles = [
    "Computer Engineer",
    "Full-Stack Developer",
    "AI Builder",
    "Cloud Developer",
]

profile = [
    ("STACK", "Python • C++ • JavaScript"),
    ("WEB", "Next.js • React • Node.js"),
    ("CLOUD", "AWS • Lambda • S3 • Cognito"),
    ("AI", "Gemini • AI/ML • OCR"),
]

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"

if Path(FONT_PATH).exists():

    title_font = ImageFont.truetype(
        FONT_PATH,
        19
    )

    text_font = ImageFont.truetype(
        FONT_PATH,
        14
    )

    small_font = ImageFont.truetype(
        FONT_PATH,
        11
    )

else:

    title_font = ImageFont.load_default()
    text_font = ImageFont.load_default()
    small_font = ImageFont.load_default()


frames = []


def draw_base():

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        "#0d1117"
    )

    draw = ImageDraw.Draw(image)

    # Outer border
    draw.rounded_rectangle(
        (
            1,
            1,
            WIDTH - 2,
            HEIGHT - 2
        ),
        radius=16,
        outline="#30363d",
        width=2
    )

    # Window controls
    draw.ellipse(
        (18, 18, 31, 31),
        fill="#ff5f56"
    )

    draw.ellipse(
        (40, 18, 53, 31),
        fill="#ffbd2e"
    )

    draw.ellipse(
        (62, 18, 75, 31),
        fill="#27c93f"
    )

    # Heading
    draw.text(
        (25, 55),
        "WHO AM I",
        font=title_font,
        fill="#ffffff"
    )

    return image


def draw_profile(draw):

    for index, (key, value) in enumerate(profile):

        y = 145 + index * 38

        draw.text(
            (25, y),
            key,
            font=small_font,
            fill="#6e7681"
        )

        draw.text(
            (175, y),
            value,
            font=text_font,
            fill="#d0d7de"
        )


# -------------------------------------------------
# CREATE ANIMATION
# -------------------------------------------------

for role in roles:

    # TYPE
    for count in range(1, len(role) + 1):

        image = draw_base()
        draw = ImageDraw.Draw(image)

        typed = role[:count]

        draw.text(
            (25, 91),
            ">",
            font=title_font,
            fill="#39d353"
        )

        draw.text(
            (47, 91),
            typed,
            font=title_font,
            fill="#39d353"
        )

        cursor_x = 47 + int(
            draw.textlength(
                typed,
                font=title_font
            )
        )

        draw.text(
            (cursor_x, 91),
            "█",
            font=title_font,
            fill="#39d353"
        )

        draw_profile(draw)

        frames.append(image)


    # HOLD
    for _ in range(FPS * 2):

        image = draw_base()
        draw = ImageDraw.Draw(image)

        draw.text(
            (25, 91),
            ">",
            font=title_font,
            fill="#39d353"
        )

        draw.text(
            (47, 91),
            role,
            font=title_font,
            fill="#39d353"
        )

        draw_profile(draw)

        frames.append(image)


    # DELETE
    for count in range(len(role), 0, -1):

        image = draw_base()
        draw = ImageDraw.Draw(image)

        typed = role[:count]

        draw.text(
            (25, 91),
            ">",
            font=title_font,
            fill="#39d353"
        )

        draw.text(
            (47, 91),
            typed,
            font=title_font,
            fill="#39d353"
        )

        cursor_x = 47 + int(
            draw.textlength(
                typed,
                font=title_font
            )
        )

        draw.text(
            (cursor_x, 91),
            "█",
            font=title_font,
            fill="#39d353"
        )

        draw_profile(draw)

        frames.append(image)


# -------------------------------------------------
# SAVE GIF
# -------------------------------------------------

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