import csv
from datetime import datetime, timezone
import json
from random import choice
import requests
import sys


# def closest_fraction(target_decimal, max_denominator=10):
#     best_fraction = None
#     best_difference = float("inf")
#     for denominator in range(max_denominator, 0, -1):
#         numerator = round(target_decimal * denominator)
#         current_fraction = numerator / denominator
#         difference = abs(target_decimal - current_fraction)
#         if difference < best_difference:
#             best_fraction = (numerator, denominator)
#             best_difference = difference
#     return best_fraction


def run():
    r = requests.get(sys.argv[1])
    r.raise_for_status()
    data = r.json()

    end_dt = datetime.fromisoformat(data["endDate"])
    # start_dt = datetime.fromisoformat(data["startDate"])
    # time_complete = 100 * (now_dt - start_dt).total_seconds() / (end_dt - start_dt).total_seconds()

    now_dt = datetime.now(tz=timezone.utc)
    if now_dt > end_dt:
        return

    with open("icons.csv") as fh:
        icon_pairs = list(csv.reader(fh))[1:]
    done_icon, todo_icon = choice(icon_pairs)

    amount_raised = int(data["amountRaised"])
    target = int(data["target"])
    donation_count = int(data["donationCount"])
    # done_total, totaliser_total = closest_fraction(amount_raised / target)
    # todo_total = totaliser_total - done_total
    totaliser_size = 10
    done_total = round(totaliser_size * amount_raised / target)
    todo_total = totaliser_size - done_total
    totaliser = "{done}{todo}".format(
        done=(done_total * f":{done_icon}: "),
        todo=(todo_total * f":{todo_icon}: "),
    ).strip()
    average_donation = amount_raised / donation_count / 2
    total_percent = 100 * amount_raised / target

    message = (
        f"£{amount_raised:,} raised so far, "
        f"from {donation_count:,} donations. "
        f"That’s an average donation of £{average_donation:.2f}.\n\n"
        "Progress to target:\n"
        f"{totaliser}\n"
        f"(i.e. {total_percent:.1f}%)"
    )
    print(message)

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
