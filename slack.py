import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# user_email = app.client.users_info(user=event["user"])['user']['profile']['email']
app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.message("")
def in_message(say, message):
    response = "22nd Feb, 2023"
    block = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "value": "education",
                    "text": {"type": "plain_text", "text": "education", "emoji": True},
                    "style": "primary",
                    "action_id": "educaction",
                },
                {
                    "type": "button",
                    "value": "roles",
                    "text": {"type": "plain_text", "text": "roles", "emoji": True},
                    "style": "primary",
                    "action_id": "roles",
                },
                {
                    "type": "button",
                    "value": "certification",
                    "text": {
                        "type": "plain_text",
                        "text": "certifications",
                        "emoji": True,
                    },
                    "style": "primary",
                    "action_id": "certification",
                },
                {
                    "type": "button",
                    "value": "work",
                    "text": {
                        "type": "plain_text",
                        "text": "work experience",
                        "emoji": True,
                    },
                    "style": "primary",
                    "action_id": "work",
                },
            ],
        }
    ]
    say(blocks=block)


@app.action("educaction")
def handle_some_action(action, say):
    say(f"Enter the {action['value']} value:")


@app.action("roles")
def handle_some_action(action, say):
    say(f"Enter the {action['value']} value:")


@app.action("certification")
def handle_some_action(action, say):
    say(f"Enter the {action['value']} value:")


@app.action("work")
def handle_some_action(action, say):
    block = []

    say(blocks=block)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
