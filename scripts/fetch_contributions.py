import json
from datetime import date, timedelta
from pathlib import Path
from html import escape


INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")


# ============================================================
# LOAD VERIFIED DATA
# ============================================================

data = json.loads(
    INPUT.read_text(encoding="utf-8")
)

days = data["days"]

TOTAL = data["total_contributions"]
ACTIVE = data["active_days"]
STREAK = data["current_streak"]
BEST = data["best_day"]


by_date = {
    date.fromisoformat(item["date"]): item
    for item in days
}


# ============================================================
# CALENDAR RANGE
# ============================================================

latest_date = max(by_date)
earliest_date = min(by_date)

# Sunday → Saturday calendar alignment
start_date = earliest_date - timedelta(
    days=(earliest_date.weekday() + 1) % 7
)

end_date = latest_date + timedelta(
    days=6 - ((latest_date.weekday() + 1) % 7)
)


weeks = []

current = start_date

while current <= end_date:

    week = []

    for row in range(7):

        current_day = current + timedelta(
            days=row
        )

        item = by_date.get(
            current_day,
            {
                "date": current_day.isoformat(),
                "count": 0,
                "level": 0,
            },
        )

        week.append(item)

    weeks.append(week)

    current += timedelta(days=7)


# ============================================================
# VISUAL SETTINGS
# ============================================================

CELL = 17
GAP = 5
STEP = CELL + GAP

LEFT = 70
TOP = 185

GRID_WIDTH = len(weeks) * STEP
GRID_HEIGHT = 7 * STEP

WIDTH = LEFT + GRID_WIDTH + 40
HEIGHT = TOP + GRID_HEIGHT + 135


PALETTE = {
    0: "#111820",
    1: "#123522",
    2: "#176b35",
    3: "#23a447",
    4: "#39d353",
}


# ============================================================
# MONTH LABELS
# ============================================================

month_labels = []

previous_month = None

for column, week in enumerate(weeks):

    first_day = date.fromisoformat(
        week[0]["date"]
    )

    if first_day.month != previous_month:

        month_labels.append(
            (
                column,
                first_day.strftime("%b").upper()
            )
        )

        previous_month = first_day.month


# ============================================================
# SVG START
# ============================================================

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<defs>

<!-- ====================================================== -->
<!-- BACKGROUND -->
<!-- ====================================================== -->

<linearGradient
id="background"
x1="0"
y1="0"
x2="1"
y2="1">

    <stop
    offset="0%"
    stop-color="#04070a"/>

    <stop
    offset="50%"
    stop-color="#0a1016"/>

    <stop
    offset="100%"
    stop-color="#04070a"/>

</linearGradient>


<!-- ====================================================== -->
<!-- TITLE -->
<!-- ====================================================== -->

<linearGradient
id="title"
x1="0"
y1="0"
x2="1"
y2="0">

    <stop
    offset="0%"
    stop-color="#39d353"/>

    <stop
    offset="50%"
    stop-color="#7ee787"/>

    <stop
    offset="100%"
    stop-color="#39d353"/>

</linearGradient>


<!-- ====================================================== -->
<!-- GLOW -->
<!-- ====================================================== -->

<filter id="glow">

    <feGaussianBlur
    stdDeviation="3"
    result="blur"/>

    <feMerge>

        <feMergeNode
        in="blur"/>

        <feMergeNode
        in="SourceGraphic"/>

    </feMerge>

</filter>


<!-- ====================================================== -->
<!-- GRID -->
<!-- ====================================================== -->

<pattern
id="grid"
width="32"
height="32"
patternUnits="userSpaceOnUse">

    <path
    d="M 32 0 L 0 0 0 32"
    fill="none"
    stroke="#39d353"
    stroke-width="0.5"
    opacity="0.035"/>

</pattern>


<!-- ====================================================== -->
<!-- SCANLINES -->
<!-- ====================================================== -->

<pattern
id="scanlines"
width="5"
height="5"
patternUnits="userSpaceOnUse">

    <rect
    width="5"
    height="1"
    fill="white"
    opacity="0.018"/>

</pattern>

</defs>


<!-- ====================================================== -->
<!-- BACKGROUND -->
<!-- ====================================================== -->

<rect
width="100%"
height="100%"
rx="22"
fill="url(#background)"/>

<rect
width="100%"
height="100%"
rx="22"
fill="url(#grid)"/>

<rect
width="100%"
height="100%"
rx="22"
fill="url(#scanlines)"/>


<!-- ====================================================== -->
<!-- BORDER -->
<!-- ====================================================== -->

<rect
x="1"
y="1"
width="{WIDTH - 2}"
height="{HEIGHT - 2}"
rx="22"
fill="none"
stroke="#30363d"
stroke-width="2"/>


<!-- ====================================================== -->
<!-- WINDOW CONTROLS -->
<!-- ====================================================== -->

<circle
cx="28"
cy="28"
r="7"
fill="#ff5f56"/>

<circle
cx="51"
cy="28"
r="7"
fill="#ffbd2e"/>

<circle
cx="74"
cy="28"
r="7"
fill="#27c93f"/>


<!-- ====================================================== -->
<!-- BRAND -->
<!-- ====================================================== -->

<text
x="100"
y="33"
font-family="monospace"
font-size="13"
fill="#6e7681">

SEAN ANDRADES  //  GITHUB TELEMETRY

</text>


<!-- ====================================================== -->
<!-- TITLE -->
<!-- ====================================================== -->

<text
x="28"
y="78"
font-family="monospace"
font-size="27"
font-weight="bold"
fill="url(#title)"
filter="url(#glow)">

CONTRIBUTION MATRIX

</text>


<!-- ====================================================== -->
<!-- STATUS -->
<!-- ====================================================== -->

<circle
cx="{WIDTH - 105}"
cy="68"
r="5"
fill="#39d353">

<animate
attributeName="opacity"
values="1;0.25;1"
dur="1.5s"
repeatCount="indefinite"/>

</circle>


<text
x="{WIDTH - 91}"
y="73"
font-family="monospace"
font-size="11"
fill="#7ee787">

AUTO-SYNC

</text>


<!-- ====================================================== -->
<!-- SUBTITLE -->
<!-- ====================================================== -->

<text
x="30"
y="105"
font-family="monospace"
font-size="11"
fill="#8b949e">

GITHUB ACTIVITY  /  LAST YEAR  /  VERIFIED DATA

</text>


<!-- ====================================================== -->
<!-- STAT CARDS -->
<!-- ====================================================== -->

<rect
x="25"
y="122"
width="175"
height="48"
rx="9"
fill="#0d1117"
stroke="#30363d"/>

<rect
x="210"
y="122"
width="175"
height="48"
rx="9"
fill="#0d1117"
stroke="#30363d"/>

<rect
x="395"
y="122"
width="175"
height="48"
rx="9"
fill="#0d1117"
stroke="#30363d"/>


<!-- TOTAL -->

<text
x="38"
y="141"
font-family="monospace"
font-size="9"
fill="#6e7681">

CONTRIBUTIONS

</text>

<text
x="38"
y="160"
font-family="monospace"
font-size="16"
font-weight="bold"
fill="#39d353">

{TOTAL:,}

</text>


<!-- ACTIVE -->

<text
x="223"
y="141"
font-family="monospace"
font-size="9"
fill="#6e7681">

ACTIVE DAYS

</text>

<text
x="223"
y="160"
font-family="monospace"
font-size="16"
font-weight="bold"
fill="#39d353">

{ACTIVE}

</text>


<!-- STREAK -->

<text
x="408"
y="141"
font-family="monospace"
font-size="9"
fill="#6e7681">

CURRENT STREAK

</text>

<text
x="408"
y="160"
font-family="monospace"
font-size="16"
font-weight="bold"
fill="#39d353">

{STREAK} DAYS

</text>

'''


# ============================================================
# MONTH LABELS
# ============================================================

for column, label in month_labels:

    x = LEFT + column * STEP

    svg += f'''
<text
x="{x}"
y="{TOP - 20}"
font-family="monospace"
font-size="9"
fill="#8b949e">

{label}

</text>
'''


# ============================================================
# DAY LABELS
# ============================================================

for label, row in [
    ("MON", 1),
    ("WED", 3),
    ("FRI", 5),
]:

    y = TOP + row * STEP + 12

    svg += f'''
<text
x="25"
y="{y}"
font-family="monospace"
font-size="9"
fill="#6e7681">

{label}

</text>
'''


# ============================================================
# CONTRIBUTION CELLS
# ============================================================

animation_index = 0

for column, week in enumerate(weeks):

    for row, item in enumerate(week):

        x = LEFT + column * STEP
        y = TOP + row * STEP

        level = max(
            0,
            min(
                4,
                int(item.get("level", 0))
            )
        )

        count = int(
            item.get("count", 0)
        )

        color = PALETTE[level]

        delay = animation_index * 0.007

        svg += f'''
<rect
x="{x}"
y="{y}"
width="{CELL}"
height="{CELL}"
rx="4"
fill="{color}"
stroke="#30363d"
stroke-width="0.5"
opacity="0">

<title>
{escape(item["date"])} — {count} contribution{"s" if count != 1 else ""}
</title>

<animate
attributeName="opacity"
from="0"
to="1"
dur="0.28s"
begin="{delay:.3f}s"
fill="freeze"/>

</rect>
'''

        animation_index += 1


# ============================================================
# BOTTOM SECTION
# ============================================================

bottom = TOP + GRID_HEIGHT + 35


svg += f'''

<line
x1="25"
y1="{bottom - 15}"
x2="{WIDTH - 25}"
y2="{bottom - 15}"
stroke="#30363d"/>


<!-- PEAK -->

<text
x="25"
y="{bottom + 5}"
font-family="monospace"
font-size="9"
fill="#6e7681">

PEAK ACTIVITY

</text>


<text
x="25"
y="{bottom + 27}"
font-family="monospace"
font-size="12"
fill="#39d353">

{escape(BEST["date"])}  //  {BEST["count"]} CONTRIBUTIONS

</text>


<!-- LEGEND -->

<text
x="{WIDTH - 245}"
y="{bottom + 5}"
font-family="monospace"
font-size="9"
fill="#6e7681">

ACTIVITY LEVEL

</text>
'''


legend_x = WIDTH - 245

for level in range(5):

    x = legend_x + 5 + level * 24

    svg += f'''
<rect
x="{x}"
y="{bottom + 15}"
width="16"
height="16"
rx="4"
fill="{PALETTE[level]}"/>
'''


svg += f'''

<text
x="{legend_x + 5}"
y="{bottom + 47}"
font-family="monospace"
font-size="8"
fill="#484f58">

LESS

</text>


<text
x="{legend_x + 101}"
y="{bottom + 47}"
font-family="monospace"
font-size="8"
fill="#484f58">

MORE

</text>


<!-- ====================================================== -->
<!-- FOOTER -->
<!-- ====================================================== -->

<text
x="25"
y="{HEIGHT - 17}"
font-family="monospace"
font-size="8"
fill="#484f58">

@seanandrades1701  •  AUTOMATED CONTRIBUTION TELEMETRY

</text>

</svg>
'''


# ============================================================
# WRITE
# ============================================================

OUTPUT.write_text(
    svg,
    encoding="utf-8"
)

print()
print("CONTRIBUTION MATRIX GENERATED")
print("-" * 50)
print(f"Contributions : {TOTAL:,}")
print(f"Active days   : {ACTIVE}")
print(f"Current streak: {STREAK}")
print(
    f"Peak activity : "
    f"{BEST['date']} / {BEST['count']}"
)
print(f"Output        : {OUTPUT}")
print()