import yaml

from clients.dropbox_client import TransferData, convert_email_to_file_name


def load_data_to_dropbox(yaml_text, file):
    transferData = TransferData()
    cv_data = yaml.safe_load(yaml_text)
    base_file_name = convert_email_to_file_name(cv_data["email"])

    transferData.upload_file(file, file_to=f"{base_file_name}_v1.pdf")
    transferData.upload_file_yaml(yaml_text, file_to=f"{base_file_name}_v1.yaml")


def dowload_file_from_dropbox(yaml_text):
    transferData = TransferData()
    cv_data = yaml.safe_load(yaml_text)
    email = cv_data["email"]
    transferData.download_file(email=email)
