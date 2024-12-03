from os import environ
import requests


def run():
    message = "Testing, testing. 1, 2, 3… :wave:"
    slack_trigger_url = environ.get("SLACK_TRIGGER_URL")
    if slack_trigger_url:
        requests.post(
            slack_trigger_url,
            json={
                "message": message,
            })


if __name__ == "__main__":
    run()
