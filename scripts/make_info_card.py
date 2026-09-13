from pathlib import Path
from html import escape

OUTPUT = Path("info-card.svg")

WIDTH = 620
ROW_HEIGHT = 44
TOP = 145

profile = [
    ("STACK", "Python • C++ • JavaScript"),
    ("WEB", "Next.js • React • Node.js"),
    ("CLOUD", "AWS • Lambda • S3 • Cognito"),
    ("AI", "Gemini • AI/ML • OCR"),
    ("BUILDING", "Intelligent CKYC & AI apps"),
    ("PROJECTS", "KYCore • OrelDrive • SmaTra"),
]

roles = [
    "Computer Engineer",
    "Full-Stack Developer",
    "AI Builder",
    "Cloud Developer",
]

ROLE_TIME = 6
TOTAL_TIME = ROLE_TIME * len(roles)

HEIGHT = TOP + len(profile) * ROW_HEIGHT + 50


svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

  <filter id="glow">
    <feGaussianBlur stdDeviation="2.5" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>

</defs>


<!-- CARD -->

<rect
  width="100%"
  height="100%"
  rx="16"
  fill="#0d1117"/>

<rect
  x="1"
  y="1"
  width="{WIDTH - 2}"
  height="{HEIGHT - 2}"
  rx="16"
  fill="none"
  stroke="#30363d"/>


<!-- WINDOW CONTROLS -->

<circle cx="25" cy="25" r="7" fill="#ff5f56"/>
<circle cx="47" cy="25" r="7" fill="#ffbd2e"/>
<circle cx="69" cy="25" r="7" fill="#27c93f"/>


<!-- TITLE -->

<text
  x="25"
  y="65"
  font-family="monospace"
  font-size="18"
  font-weight="bold"
  fill="#ffffff">
WHO AM I
</text>


<!-- COMMAND PROMPT -->

<text
  x="25"
  y="103"
  font-family="monospace"
  font-size="18"
  font-weight="bold"
  fill="#39d353">
&gt;
</text>

'''


# Create the typing/deleting animation.
#
# Each role gets its own 6-second section:
#
# 0.0 - 2.0s  typing
# 2.0 - 4.5s  visible
# 4.5 - 6.0s  deleting
#
# Then the next role begins.

CHAR_WIDTH = 10.8

for role_index, role in enumerate(roles):

    role_start = role_index * ROLE_TIME
    role_length = len(role)

    # Maximum time used for typing and deleting.
    type_duration = 2.0
    hold_start = 2.0
    delete_start = 4.2
    delete_duration = 1.3

    for char_index, char in enumerate(role):

        safe_char = escape(char)

        # Spaces need to occupy width but don't need to render.
        if char == " ":
            continue

        x = 45 + char_index * CHAR_WIDTH

        type_start = role_start + (
            char_index / max(role_length, 1)
        ) * type_duration

        type_end = role_start + type_duration

        delete_char_start = (
            role_start
            + delete_start
            + (
                (role_length - char_index - 1)
                / max(role_length, 1)
            ) * delete_duration
        )

        delete_char_end = (
            delete_char_start
            + 0.15
        )

        svg += f'''
<text
  x="{x:.1f}"
  y="103"
  font-family="monospace"
  font-size="18"
  font-weight="bold"
  fill="#39d353"
  opacity="0">

  {safe_char}

  <animate
    attributeName="opacity"
    values="0;1;1;0"
    keyTimes="0;0.01;0.82;0.83"
    dur="0.01s"
    begin="{type_start:.3f}s"
    repeatCount="indefinite"
  />

</text>
'''


# Add a second, simpler animated layer that controls
# visibility of each complete role.
#
# This ensures the role disappears before the next one.

for role_index, role in enumerate(roles):

    role_start = role_index * ROLE_TIME
    safe_role = escape(role)

    svg += f'''
<text
  x="45"
  y="103"
  font-family="monospace"
  font-size="18"
  font-weight="bold"
  fill="#39d353"
  opacity="0">

  {safe_role}

  <animate
    attributeName="opacity"
    values="0;0;1;1;0;0"
    keyTimes="0;0.02;0.08;0.70;0.78;1"
    dur="{TOTAL_TIME}s"
    begin="{role_start}s"
    repeatCount="indefinite"
  />

</text>
'''


svg += f'''

<!-- BLINKING CURSOR -->

<text
  x="45"
  y="103"
  font-family="monospace"
  font-size="18"
  font-weight="bold"
  fill="#39d353">

  █

  <animate
    attributeName="opacity"
    values="1;0;1"
    dur="0.8s"
    repeatCount="indefinite"/>

</text>


<!-- PROFILE DATA -->

'''


for index, (key, value) in enumerate(profile):

    y = TOP + index * ROW_HEIGHT

    safe_key = escape(key)
    safe_value = escape(value)

    svg += f'''
<text
  x="25"
  y="{y}"
  font-family="monospace"
  font-size="10"
  font-weight="bold"
  fill="#6e7681">
{safe_key}
</text>

<text
  x="175"
  y="{y}"
  font-family="monospace"
  font-size="14"
  fill="#d0d7de">
{safe_value}
</text>

'''


# Status

status_y = HEIGHT - 20

svg += f'''
<circle
  cx="25"
  cy="{status_y - 3}"
  r="4"
  fill="#39d353"
  filter="url(#glow)">

  <animate
    attributeName="opacity"
    values="1;0.3;1"
    dur="1.5s"
    repeatCount="indefinite"/>

</circle>

<text
  x="38"
  y="{status_y}"
  font-family="monospace"
  font-size="9"
  fill="#6e7681">
SYSTEM ACTIVE
</text>

</svg>
'''


OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created {OUTPUT}")