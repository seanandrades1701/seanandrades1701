import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "seanandrades1701"
URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    level = cell.get("data-level")

    if not date:
        continue

    aria = cell.get("aria-label", "")

    match = re.search(r"(\d[\d,]*) contribution", aria)
    count = int(match.group(1).replace(",", "")) if match else 0

    days.append({
        "date": date,
        "level": int(level or 0),
        "count": count
    })

if not days:
    raise RuntimeError("No contribution data found.")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

data = {
    "username": USERNAME,
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "days": days
}

OUTPUT.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print(f"Saved {len(days)} contribution days to {OUTPUT}")