from functions import *
from generate_cv import *
import streamlit as st
from streamlit_cropper import st_cropper
import os
import fitz

from dropbox_client import TransferData

BASE_PATH = "/home/Team/testing cvbia"

## PAGE TITLE
st.title("CVBIA")


def button_load_data_to_dropbox(yaml_text, file):
    transferData = TransferData()

    cv_data = yaml.safe_load(yaml_text)
    first_name = cv_data["first_name"].replace(" ", "_")
    last_name = cv_data["last_name"].replace(" ", "_")
    base_file_name = f"{first_name}_{last_name}"
    print(f"{BASE_PATH}/{base_file_name}")

    transferData.upload_file(file, file_to=f"{BASE_PATH}/{base_file_name}.pdf")
    transferData.upload_file_yaml(
        yaml_text, file_to=f"{BASE_PATH}/{base_file_name}.yaml"
    )


## IMAGE UPLOAD WIDGET
with st.container():
    uploaded_image = st.file_uploader("Upload and crop your picture: (png, jpg, jpeg)")
    if uploaded_image:
        img = Image.open(uploaded_image)
        cropped_img = st_cropper(img, aspect_ratio=(1, 1), box_color="green")
        img_byte_arr = io.BytesIO()
        cropped_img.save(img_byte_arr, format="PNG")
        image_bytes_data = img_byte_arr.getvalue()
    else:
        image_bytes_data = None

## YAML INPUT WIDGET
with open("cv_data.yaml", "r") as file:
    yaml_input = file.read()
yaml_text = st.text_area("YAML input:", value=str(yaml_input), height=500)

## GENERATE CV BUTTON
st.button(
    "Generate CV",
    key="RunBtn",
    on_click=generate_cv(image=image_bytes_data, yaml_input=yaml_text),
    args=None,
    kwargs=None,
)

## DOWNLOAD BUTTONS
with open("cv_output/cv.pdf", "rb") as file:
    # st.download_button("Download PDF", file, file_name=f"{cv_data['first_name']}_{cv_data['first_name']}_cv.pdf")
    st.sidebar.download_button("Download PDF", file, file_name="cv.pdf")
with open("cv_output/cv.pptx", "rb") as file:
    # st.download_button("Download PDF", file, file_name=f"{cv_data['first_name']}_{cv_data['first_name']}_cv.pdf")
    st.sidebar.download_button("Download PPTX", file, file_name="cv.pptx")

st.sidebar.button(
    "Load CV to Xebia Dropbox YAML",
    key="CV",
    on_click=button_load_data_to_dropbox,
    args=(yaml_text, "cv_output/cv.pdf"),
)

## PDF PREVIEW: need to convert resulting cv.pdf to images, in order to display cv preview on streamlit page
dpi = 100
zoom = dpi / 72
magnify = fitz.Matrix(zoom, zoom)
doc = fitz.open("cv_output/cv.pdf")  # open document
for page in doc:
    pix = page.get_pixmap(matrix=magnify)  # render page to an image
    pix.save(f"cv_images/page-{page.number}.png")
directory = "cv_images"
for filename in sorted(os.listdir(directory), reverse=False):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and filename != ".gitkeep":
        st.sidebar.image(f)

## Footnote
st.caption(
    """
⚠️Note: Please save your `YAML input` locally, refreshing this page will reset the input to the default values and the loss of any data you have entered.

Developed By: Erkan Celen
"""
)
