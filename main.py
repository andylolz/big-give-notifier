from random import choice
from datetime import datetime, timezone
import sys
import json
import requests


def run():
    r = requests.get(sys.argv[1])
    r.raise_for_status()
    data = r.json()
    total = int(data["amountRaised"])
    donations = int(data["donationCount"])

    totaliser_size = 10
    target_total = int(data["target"])

    # start_dt = datetime.fromisoformat(data["startDate"])
    end_dt = datetime.fromisoformat(data["endDate"])

    now_dt = datetime.now(tz=timezone.utc)

    if now_dt > end_dt:
        return

    icon_pairs = [
        ("large_green_square", "large_red_square"),
        ("full_moon_with_face", "new_moon_with_face"),
        ("smiley", "no_mouth"),
        ("goodmaggie", "hotdog"),
        ("green_heart", "heart"),
        ("bell_pepper", "hot_pepper"),
        ("hatching_chick", "egg"),
        ("green_apple", "tomato"),
        ("full_moon", "new_moon"),
        ("white_check_mark", "x"),
        ("fire", "thisisfine"),
        ("full-fact", "fakenews"),
        ("here", "away"),
        ("partyblob", "thinking_face"),
        ("star", "black_square"),
        ("tulip", "seedling"),
        ("butterfly", "insect"),
        ("gratitude-thank-you", "ok"),
        ("city_sunrise", "cityscape"),
        ("tada", "eyes"),
        ("partyparrot", "sleepyparrot"),
        ("neutral_face", "dotted_line_face"),
    ]
    done_icon, todo_icon = choice(icon_pairs)

    # time_complete = 100 * (now_dt - start_dt).total_seconds() / (end_dt - start_dt).total_seconds()

    totaliser_score = round(totaliser_size * total / target_total)
    totaliser = (totaliser_score * f":{done_icon}: ") + ((totaliser_size - totaliser_score) * f":{todo_icon}: ")
    message = f"£{total:,} raised so far, from {donations:,} donations. That’s an average donation of £{(total / donations / 2):.2f}.\n\nProgress to target:\n{totaliser}\n(i.e. {(100 * total / target_total):.1f}%)"

    with open("data/output.json") as fh:
        prev_data = json.load(fh)
    if prev_data["donationCount"] != data["donationCount"]:
        requests.post(
            sys.argv[2],
            json={
                "message": message,
            })
    with open("data/output.json", "w") as fh:
        json.dump(data, fh)


if __name__ == "__main__":
    run()
