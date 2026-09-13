import json
from pathlib import Path

INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

data = json.loads(INPUT.read_text(encoding="utf-8"))
days = data["days"]

# GitHub-style levels: 0 = none, 5 = highest
PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

CELL = 14
GAP = 4
STEP = CELL + GAP

LEFT = 30
TOP = 30

# Arrange days into weeks
weeks = []

for i in range(0, len(days), 7):
    weeks.append(days[i:i + 7])

WIDTH = LEFT + len(weeks) * STEP + 30
HEIGHT = TOP + 7 * STEP + 55

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<rect width="100%" height="100%"
      rx="14" fill="#0d1117"/>

<text x="{LEFT}" y="20"
      font-family="monospace"
      font-size="13"
      fill="#8b949e">
sean@github:~$ contributions
</text>
'''

for week_index, week in enumerate(weeks):
    for day_index, day in enumerate(week):

        level = max(0, min(5, int(day.get("level", 0))))

        x = LEFT + week_index * STEP
        y = TOP + day_index * STEP

        svg += f'''
<rect x="{x}" y="{y}"
      width="{CELL}"
      height="{CELL}"
      rx="3"
      fill="{PALETTE[level]}"/>
'''

# Legend
legend_y = TOP + 7 * STEP + 20

svg += f'''
<text x="{LEFT}" y="{legend_y}"
      font-family="monospace"
      font-size="11"
      fill="#8b949e">
Less
</text>
'''

for level in range(6):
    x = LEFT + 35 + level * STEP

    svg += f'''
<rect x="{x}" y="{legend_y - 11}"
      width="{CELL}"
      height="{CELL}"
      rx="3"
      fill="{PALETTE[level]}"/>
'''

svg += f'''
<text x="{LEFT + 35 + 6 * STEP + 8}"
      y="{legend_y}"
      font-family="monospace"
      font-size="11"
      fill="#8b949e">
More
</text>

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created {OUTPUT}")