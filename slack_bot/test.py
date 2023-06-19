from clients.dropbox_client import TransferData
from helpers.dropbox import load_data_to_dropbox
from helpers.file_helper import update_yaml_by_key
from helpers.generate_cv import generate_cv

td = TransferData()
yaml_content = td.download_file("tom.cruise@xebia.com")

new_content = update_yaml_by_key(
    yaml_content,
    "certifications",
    {
        "title": "the culo grande",
    },
)
new_content = str(new_content)

generate_cv(new_content)

load_data_to_dropbox(new_content, "cv_output/cv.pdf")
