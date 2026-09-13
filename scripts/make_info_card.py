from pathlib import Path
from html import escape

OUTPUT = Path("info-card.svg")

profile = [
    ("ROLE", "Final Year Computer Engineering Student"),
    ("STACK", "Python • C++ • JavaScript"),
    ("WEB", "Next.js • React • Node.js"),
    ("CLOUD", "AWS • Lambda • S3 • Cognito"),
    ("AI", "Gemini • AI/ML • OCR"),
    ("BUILDING", "Intelligent CKYC & AI apps"),
    ("PROJECTS", "KYCore • OrelDrive • SmaTra"),
]

WIDTH = 620
ROW_HEIGHT = 48
TOP = 110
HEIGHT = TOP + len(profile) * ROW_HEIGHT + 30

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}" height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<rect width="100%" height="100%" rx="16" fill="#0d1117"/>

<rect x="1" y="1"
      width="{WIDTH - 2}" height="{HEIGHT - 2}"
      rx="16" fill="none" stroke="#30363d"/>

<circle cx="25" cy="25" r="7" fill="#ff5f56"/>
<circle cx="47" cy="25" r="7" fill="#ffbd2e"/>
<circle cx="69" cy="25" r="7" fill="#27c93f"/>

<text x="105" y="31"
      font-family="monospace"
      font-size="15"
      fill="#8b949e">
sean@github:~
</text>

<text x="25" y="65"
      font-family="monospace"
      font-size="18"
      font-weight="bold"
      fill="#ffffff">
whoami
</text>
'''

for i, (key, value) in enumerate(profile):
    y = TOP + i * ROW_HEIGHT

    safe_key = escape(key)
    safe_value = escape(value)

    svg += f'''
<text x="25" y="{y}"
      font-family="monospace"
      font-size="15"
      font-weight="bold"
      fill="#8b949e">
{safe_key}
</text>

<text x="175" y="{y}"
      font-family="monospace"
      font-size="15"
      fill="#d0d7de">
{safe_value}
</text>
'''

svg += "</svg>"

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created {OUTPUT}")