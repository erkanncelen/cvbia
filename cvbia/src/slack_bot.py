import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from clients.dropbox_client import TransferData
from helpers.dropbox import load_data_to_dropbox
from helpers.file_helper import update_yaml_by_key
from helpers.generate_cv import generate_cv


app = App(token=os.environ["SLACK_BOT_TOKEN"])


def update_cv_in_dropbox(key, content, email):
    yaml_content = TransferData().download_file(email)
    new_yaml_content = update_yaml_by_key(current_yaml=yaml_content, key=key, data=content)
    generate_cv(str(new_yaml_content))
    load_data_to_dropbox(str(new_yaml_content), "cv_output/cv.pdf")

@app.view("view_experience")
def update_experience(ack, body, client):
    ack()

    state_values = body["view"]["state"]["values"]
    title = state_values["title_id_modal_input"]["title_id_value"]["value"]
    description = state_values["description_id_modal_input"]["description_id_value"][
        "value"
    ]
    company = state_values["company_id_modal_input"]["company_id_value"]["value"]
    tech = state_values["tech_id_modal_input"]["tech_id_value"]["value"]
    start_date = state_values["start_date_id_modal_input"]["start_date_id_value"][
        "value"
    ]
    end_date = state_values["end_date_id_modal_input"]["end_date_id_value"]["value"]

    yaml_to_update = {
        "title": title,
        "company": company,
        "start": start_date,
        "end": end_date,
        "description": description,
        "technologies": tech,
    }

    user = body["user"]["id"]
    user_email = app.client.users_info(user=user)["user"]["profile"]["email"]

    update_cv_in_dropbox(key="experience", content=yaml_to_update, email=user_email)
    client.chat_postMessage(
        channel=user, text="Your experience had been updated in your CV."
    )


@app.view("view_education")
def update_education(ack, body, client):
    ack()
    state_values = body["view"]["state"]["values"]

    degree = state_values["degree_id_modal_input"]["degree_id_value"]["value"]
    institution = state_values["institution_id_modal_input"]["institution_id_value"][
        "value"
    ]
    year = state_values["year_id_modal_input"]["year_id_value"]["value"]

    yaml_to_update = {"degree": degree, "institution": institution, "year": year}
    user_email = app.client.users_info(user=body["user"]["id"])["user"]["profile"][
        "email"
    ]
    user = body["user"]["id"]

    update_cv_in_dropbox(key="education", content=yaml_to_update, email=user_email)
    client.chat_postMessage(
        channel=user, text="Your education had been updated in your CV."
    )


@app.view("view_roles")
def update_roles(ack, body, client):
    ack()
    state_values = body["view"]["state"]["values"]
    title = state_values["title_id_modal_input"]["title_id_value"]["value"]
    description = state_values["description_id_modal_input"]["description_id_value"][
        "value"
    ]

    yaml_to_update = {"title": title, "description": description}

    user = body["user"]["id"]
    user_email = app.client.users_info(user=user)["user"]["profile"]["email"]

    update_cv_in_dropbox(key="roles", content=yaml_to_update, email=user_email)
    client.chat_postMessage(
        channel=user, text=f"Your roles had been updated in your CV."
    )


@app.view("view_certification")
def update_certification(ack, body, client):
    ack()
    title = body["view"]["state"]["values"]["title_id_modal_input"]["title_id_value"][
        "value"
    ]
    user = body["user"]["id"]
    user_email = app.client.users_info(user=user)["user"]["profile"]["email"]

    yaml_to_update = {
        "title": title,
    }
    update_cv_in_dropbox(key="certifications", content=yaml_to_update, email=user_email)
    client.chat_postMessage(
        channel=user, text="Your certification had been updated in your CV."
    )


@app.view("view_competences")
def update_competences(ack, body, client):
    ack()
    state_values = body["view"]["state"]["values"]
    title = state_values["title_id_modal_input"]["title_id_value"]["value"]
    description = state_values["description_id_modal_input"]["description_id_value"][
        "value"
    ]
    yaml_to_update = {"title": title, "description": description}

    user = body["user"]["id"]
    user_email = app.client.users_info(user=user)["user"]["profile"]["email"]
    
    update_cv_in_dropbox(key="competences", content=yaml_to_update, email=user_email)
    client.chat_postMessage(
        channel=user, text="Your competences had been updated in your CV."
    )


@app.action("experience")
def open_modal_experience(ack, client, body):
    ack()

    client.views_open(
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_experience",
            "title": {"type": "plain_text", "text": "CVBIA"},
            "blocks": [
                {
                    "type": "section",
                    "block_id": "say_hello_msg",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hello! You will add an experience in your CV.",
                        "verbatim": False,
                    },
                },
                {
                    "type": "input",
                    "block_id": "title_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Title :bam:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Analytics Engineer",
                            "emoji": False,
                        },
                    },
                },
                {
                    "type": "input",
                    "block_id": "description_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Description :squirrel:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "description_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Helping to achieve Fabulousness.",
                            "emoji": False,
                        },
                    },
                },
                {
                    "type": "input",
                    "block_id": "company_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Company name :rage1:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "company_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Pollos hermanos",
                            "emoji": False,
                        },
                    },
                },
                {
                    "type": "input",
                    "block_id": "tech_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Technologies :crycat:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "tech_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Python, Scala",
                            "emoji": False,
                        },
                    },
                },
                {
                    "type": "input",
                    "block_id": "start_date_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Start date :trump-smile:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "start_date_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "2018 March",
                            "emoji": False,
                        },
                    },
                },
                {
                    "type": "input",
                    "block_id": "end_date_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "End date :side_eye:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "end_date_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "2019 March",
                            "emoji": False,
                        },
                    },
                },
            ],
            "clear_on_close": True,  # when modal closes, fiels are clear
            "notify_on_close": False,
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "submit": {
                "type": "plain_text",
                "text": "Submit :shutuptakemoney:",
                "emoji": True,
            },
        },
    )


@app.action("education")
def open_modal_education(ack, client, body):
    ack()

    client.views_open(
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_education",
            "title": {"type": "plain_text", "text": "CVBIA"},
            "blocks": [
                {
                    "type": "section",
                    "block_id": "say_hello_msg",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hello! You will add a new CV entry in education.",
                        "verbatim": False,
                    },
                },
                {
                    "type": "input",
                    "block_id": "degree_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Degree :bam:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "degree_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "MSc in Acting (Cum Laude)",
                            "emoji": False,
                        },
                    },
                },
                {
                    "type": "input",
                    "block_id": "institution_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Institution :squirrel:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "institution_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Glen Ridge High School.",
                            "emoji": False,
                        },
                    },
                },
                {
                    "type": "input",
                    "block_id": "year_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Period (years) :rage1:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "year_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "2012-2018",
                            "emoji": False,
                        },
                    },
                },
            ],
            "clear_on_close": True,  # when modal closes, fiels are clear
            "notify_on_close": False,
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "submit": {
                "type": "plain_text",
                "text": "Submit :shutuptakemoney:",
                "emoji": True,
            },
        },
    )


@app.action("certification")
def open_modal_certification(ack, client, body):
    ack()

    client.views_open(
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": f"view_certification",
            "title": {"type": "plain_text", "text": "CVBIA"},
            "blocks": [
                {
                    "type": "section",
                    "block_id": "say_hello_msg",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Hello! You will add a new CV entry in your certifications.",
                        "verbatim": False,
                    },
                },
                {
                    "type": "input",
                    "block_id": "title_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Title :bam:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Analytics Engineer",
                            "emoji": False,
                        },
                    },
                },
            ],
            "clear_on_close": True,  # when modal closes, fiels are clear
            "notify_on_close": False,
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "submit": {
                "type": "plain_text",
                "text": "Submit :shutuptakemoney:",
                "emoji": True,
            },
        },
    )


@app.action("roles")
@app.action("competences")
def open_modal_general(ack, client, body, action):
    ack()

    key_to_update = action["value"]
    client.views_open(
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": f"view_{key_to_update}",
            "title": {"type": "plain_text", "text": "CVBIA"},
            "blocks": [
                {
                    "type": "section",
                    "block_id": "say_hello_msg",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Hello! You will add a new CV entry in your {key_to_update}.",
                        "verbatim": False,
                    },
                },
                {
                    "type": "input",
                    "block_id": "title_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Title :bam:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Analytics Engineer",
                            "emoji": False,
                        },
                    },
                },
                {
                    "type": "input",
                    "block_id": "description_id_modal_input",
                    "label": {
                        "type": "plain_text",
                        "text": "Description :bam:",
                        "emoji": True,
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "description_id_value",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Description",
                            "emoji": False,
                        },
                    },
                },
            ],
            "clear_on_close": True,  # when modal closes, fiels are clear
            "notify_on_close": False,
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "submit": {
                "type": "plain_text",
                "text": "Submit :shutuptakemoney:",
                "emoji": True,
            },
        },
    )


@app.command("/update_cv")
def open_modal(ack, say):
    ack()

    blocks = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "value": "education",
                    "text": {"type": "plain_text", "text": "education", "emoji": True},
                    "style": "primary",
                    "action_id": "education",
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
                    "value": "competences",
                    "text": {
                        "type": "plain_text",
                        "text": "competences",
                        "emoji": True,
                    },
                    "style": "primary",
                    "action_id": "competences",
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
                    "value": "experience",
                    "text": {
                        "type": "plain_text",
                        "text": "work experience",
                        "emoji": True,
                    },
                    "style": "primary",
                    "action_id": "experience",
                },
            ],
        }
    ]
    say(text="Hello! Which field of your CV would you like to update? :fiesta_parrot:")
    say(blocks=blocks)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
