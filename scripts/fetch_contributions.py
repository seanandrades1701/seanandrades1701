import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "seanandrades1701"

URL = (
    f"https://github.com/users/"
    f"{USERNAME}/contributions"
)

OUTPUT = Path("data/contributions.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    )
}


MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def get_count_from_element(cell):
    attributes = [
        "data-count",
        "data-contributions",
        "aria-label",
        "title",
    ]

    for attribute in attributes:
        value = cell.get(attribute)

        if not value:
            continue

        match = re.search(
            r"(\d[\d,]*)\s+contributions?",
            str(value),
            re.IGNORECASE,
        )

        if match:
            return int(
                match.group(1).replace(",", "")
            )

        if re.search(
            r"no\s+contributions",
            str(value),
            re.IGNORECASE,
        ):
            return 0

    return None


def extract_calendar_labels(soup):
    pattern = re.compile(
        r"("
        r"\d[\d,]*\s+contributions?"
        r"|no\s+contributions"
        r")"
        r"\s+on\s+"
        r"([A-Za-z]+)"
        r"\s+"
        r"(\d{1,2})(?:st|nd|rd|th)?",
        re.IGNORECASE,
    )

    labels = []

    text = soup.get_text(
        " ",
        strip=True,
    )

    for match in pattern.finditer(text):

        count_text = match.group(1)
        month_text = match.group(2)
        day_text = match.group(3)

        month = MONTHS.get(
            month_text.lower()
        )

        if not month:
            continue

        day = int(day_text)

        if re.match(
            r"no\s+contributions",
            count_text,
            re.IGNORECASE,
        ):
            count = 0

        else:
            number = re.search(
                r"(\d[\d,]*)",
                count_text,
            )

            if not number:
                continue

            count = int(
                number.group(1).replace(",", "")
            )

        labels.append(
            {
                "month": month,
                "day": day,
                "count": count,
            }
        )

    return labels


def main():

    print()
    print("=" * 64)
    print("SEAN ANDRADES // CONTRIBUTION DATA SYNC")
    print("=" * 64)
    print()

    print(f"Fetching: {URL}")
    print()

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    cells = soup.select(
        "[data-date][data-level]"
    )

    if not cells:
        cells = soup.select(
            ".ContributionCalendar-day"
        )

    if not cells:
        raise RuntimeError(
            "Could not find contribution calendar cells."
        )

    print(
        f"Calendar cells found: {len(cells)}"
    )

    labels = extract_calendar_labels(
        soup
    )

    print(
        f"Contribution descriptions found: "
        f"{len(labels)}"
    )

    if not labels:
        raise RuntimeError(
            "GitHub returned calendar cells but "
            "no contribution descriptions could "
            "be parsed."
        )

    label_map = {}

    for label in labels:

        key = (
            label["month"],
            label["day"],
        )

        label_map.setdefault(
            key,
            [],
        ).append(
            label["count"]
        )

    days = []

    for cell in cells:

        contribution_date = cell.get(
            "data-date"
        )

        if not contribution_date:
            continue

        if not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}",
            contribution_date,
        ):
            continue

        level_raw = cell.get(
            "data-level",
            "0",
        )

        try:
            level = int(level_raw)

        except (
            TypeError,
            ValueError,
        ):
            level = 0

        count = get_count_from_element(
            cell
        )

        if count is None:

            parsed_date = datetime.strptime(
                contribution_date,
                "%Y-%m-%d",
            ).date()

            key = (
                parsed_date.month,
                parsed_date.day,
            )

            queue = label_map.get(
                key,
                [],
            )

            if queue:
                count = queue.pop(0)

        if count is None and level == 0:
            count = 0

        if count is None:
            raise RuntimeError(
                "Could not determine the contribution "
                f"count for {contribution_date} "
                f"(level={level})."
            )

        days.append(
            {
                "date": contribution_date,
                "count": int(count),
                "level": level,
            }
        )

    unique = {}

    for item in days:
        unique[item["date"]] = item

    days = list(
        unique.values()
    )

    days.sort(
        key=lambda item: item["date"]
    )

    total = sum(
        item["count"]
        for item in days
    )

    active_days = sum(
        1
        for item in days
        if item["count"] > 0
    )

    # If multiple days have the same maximum,
    # choose the most recent one.
    best_day = max(
        days,
        key=lambda item: (
            item["count"],
            item["date"],
        ),
    )

    latest = datetime.strptime(
        days[-1]["date"],
        "%Y-%m-%d",
    ).date()

    streak = 0

    cursor = latest

    while True:

        matching = next(
            (
                item
                for item in days
                if item["date"]
                == cursor.isoformat()
            ),
            None,
        )

        if not matching:
            break

        if matching["count"] <= 0:
            break

        streak += 1

        cursor = cursor.fromordinal(
            cursor.toordinal() - 1
        )

    active_levels = sum(
        1
        for item in days
        if item["level"] > 0
    )

    if active_levels > 0 and total == 0:

        raise RuntimeError(
            "SAFETY CHECK FAILED.\n"
            f"GitHub returned {active_levels} "
            "active cells but the calculated "
            "total is zero."
        )

    output = {
        "username": USERNAME,
        "generated_at": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "total_contributions": total,
        "active_days": active_days,
        "current_streak": streak,
        "best_day": best_day,
        "days": days,
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            output,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("=" * 64)
    print("SYNC COMPLETE")
    print("=" * 64)

    print(
        f"Calendar days : {len(days)}"
    )

    print(
        f"Contributions : {total:,}"
    )

    print(
        f"Active days   : {active_days}"
    )

    print(
        f"Current streak: {streak}"
    )

    print(
        f"Peak day      : {best_day['date']}"
    )

    print(
        f"Peak count    : {best_day['count']}"
    )

    print(
        f"Active cells  : {active_levels}"
    )

    print("-" * 64)

    print(
        f"Saved to      : {OUTPUT}"
    )

    print()


if __name__ == "__main__":
    main()