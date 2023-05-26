from dropbox_client import TransferData
from functions import load_data_to_dropbox, update_cv_by_key
from generate_cv import generate_cv

td = TransferData()

yaml_content = td.download_file("tom.cruise@xebia.com")

new_content = update_cv_by_key(
    yaml_content,
    "education",
    {
        "degree": "Underwater basket weaving",
        "institution": "GDD Academy",
        "year": "1900 - 1926",
    },
)
new_content = str(new_content)

print(new_content)

generate_cv(new_content)

load_data_to_dropbox(new_content, "cv_output/cv.pdf")
