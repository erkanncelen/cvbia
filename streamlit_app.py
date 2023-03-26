from functions import * 
from generate_cv import *
import streamlit as st
from streamlit_cropper import st_cropper
import os
import fitz

## PAGE TITLE
st.title("CVBIA")

## IMAGE UPLOAD WIDGET
with st.container():
    uploaded_image = st.file_uploader("Upload and crop your picture:")
    if uploaded_image:
        img = Image.open(uploaded_image)
        cropped_img = st_cropper(img, aspect_ratio=(1, 1), box_color='green')
        img_byte_arr = io.BytesIO()
        cropped_img.save(img_byte_arr, format='PNG')
        image_bytes_data = img_byte_arr.getvalue()
    else:
        image_bytes_data = None

## YAML INPUT WIDGET
with open("cv_data.yaml", "r") as file:
        yaml_input = file.read()
yaml_text = st.text_area("YAML input:", value=str(yaml_input), height=500)

## GENERATE CV BUTTON
st.button('Generate CV', key='RunBtn', on_click=generate_cv(image=image_bytes_data, yaml_input=yaml_text), args=None, kwargs=None)

## DOWNLOAD BUTTON
# cv_data = yaml.safe_load(yaml_text)
with open("cv_output/cv.pdf", "rb") as file:
    # st.download_button("Download PDF", file, file_name=f"{cv_data['first_name']}_{cv_data['first_name']}_cv.pdf")
    st.sidebar.download_button("Download PDF", file, file_name="cv_download.pdf")

## PDF PREVIEW: need to convert resulting cv.pdf to images, in order to display cv preview on streamlit page
dpi = 100
zoom = dpi / 72
magnify = fitz.Matrix(zoom, zoom)
doc = fitz.open("cv_output/cv.pdf")  # open document
for page in doc:
    pix = page.get_pixmap(matrix=magnify)  # render page to an image
    pix.save(f"cv_images/page-{page.number}.png")
directory = 'cv_images'
for filename in sorted(os.listdir(directory), reverse=False):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and filename != '.gitkeep':
        st.sidebar.image(f)

## Footnote
st.caption("Developed By: Erkan Celen")
