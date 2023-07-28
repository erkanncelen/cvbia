import os

import dropbox
import yaml

BASE_PATH = "/home/Team/testing cvbia"
DROPBOX_REFRESH_TOKEN = os.environ["DROPBOX_REFRESH_TOKEN"]
DROPBOX_APP_KEY = os.environ["DROPBOX_APP_KEY"]

def convert_email_to_file_name(email):
    email = email.split("@")[0].replace(".", "_").lower()
    return f"{BASE_PATH}/{email}"


class TransferData:
    def upload_file_yaml(self, content, file_to):
        """upload a file to Dropbox using API v2"""
        with dropbox.Dropbox(oauth2_refresh_token=DROPBOX_REFRESH_TOKEN, app_key=DROPBOX_APP_KEY) as dbx:
            dbx.files_upload(
                bytes(content, "utf-8"), file_to, mode=dropbox.files.WriteMode.overwrite
            )
    
    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2"""
        with dropbox.Dropbox(oauth2_refresh_token=DROPBOX_REFRESH_TOKEN, app_key=DROPBOX_APP_KEY) as dbx:
            with open(file_from, "rb") as f:
                dbx.files_upload(
                    f.read(), file_to, mode=dropbox.files.WriteMode.overwrite
                )

    def download_file(self, email):
        with dropbox.Dropbox(oauth2_refresh_token=DROPBOX_REFRESH_TOKEN, app_key=DROPBOX_APP_KEY) as dbx:
            file_path = convert_email_to_file_name(email=email)
            _, f = dbx.files_download(f"{file_path}.yaml")
            yaml_content = yaml.safe_load(f.content)
            return yaml_content
