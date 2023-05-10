from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw
import io
import itertools
import os
from pathlib import Path
from pypdf import PdfMerger
import shutil
import textwrap
import subprocess


def cleanup_files(directories: list = ["cv_pages"]):
    """
    Removes directories, even if they contain files.
    Arguments:
        directories: List of directories to remove
    """

    for directory in directories:
        try:
            shutil.rmtree(Path(directory))
        except FileNotFoundError:
            pass


def write(
    c: object,
    x: int,
    y: int,
    text: str,
    width: int = 60,
    font: str = "regular",
    punto: int = 12,
    color: str = "dark_grey",
    spacing: int = 12,
    url: str = None,
):
    """
    Writes given text input with specified arguments.

    Arguments:
        c: canvas object
        x: x coordinate on the page
        y: y coordinate on the page
        text: text input to be written, must be a string
        font: regular, bold
        punto: font size
        color: white, trans_white, purple, dark_grey, light_grey
        spacing: line spacing, only used for mutliple line inputs
        url: URL to be written, starts with the URL domain, i.e. no "https://www."
    """
    # SET FONT
    c.setFont(font, punto)

    # SET COLOR
    if color == "white":
        c.setFillColorRGB(0.95, 0.95, 0.95, 1)
    elif color == "trans_white":
        c.setFillColorRGB(0.95, 0.95, 0.95, 0.8)
    elif color == "purple":
        c.setFillColorRGB(108 / 255, 29 / 255, 96 / 255, 1)
    elif color == "dark_grey":
        c.setFillColorRGB(0.5, 0.5, 0.5, 1)
    elif color == "light_grey":
        c.setFillColorRGB(0.3, 0.3, 0.3, 1)
    else:
        raise Exception(
            f"{color} is not available. Try: white, trans_white, purple, dark_grey, light_grey"
        )

    # DRAW STRING: for loop is used to manage multiple line inputs
    if text:
        for line in list(
            itertools.chain.from_iterable(
                [textwrap.wrap(x, width=width) for x in text.splitlines()]
            )
        ):
            c.drawString(x, y, f"{line}")
            if url is not None:
                c.linkURL(
                    "https://www." + url,
                    rect=(
                        x,
                        y,
                        x + (0.66 * stringWidth(text, font, punto + 4)),
                        y + punto,
                    ),
                    relative=0,
                    thickness=0,
                )
            y -= spacing

    return y


def draw_background(c, image=None, path="backgrounds/background1.jpg"):
    """
    Fills the background of document.
    """
    if image:
        bg_image = image
        c.drawImage(bg_image, 0, 0, width=A4[1], height=A4[0])
    elif path:
        bg_image = path
        c.drawImage(bg_image, 0, 0, width=A4[1], height=A4[0])

    return None


def draw_picture(c, image=None, path: str = "images/tom_cruise.jpg"):
    """
    Crops and draws the circular photo of the person on CV.
    """
    if image:
        im = Image.open(io.BytesIO(image))
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.LANCZOS)
        im.putalpha(mask)
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()
        pp_image = ImageReader(io.BytesIO(img_byte_arr))
        c.drawImage(pp_image, 20, 455, width=100, height=100, mask="auto")
    elif path:
        im = Image.open(path)
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.LANCZOS)
        im.putalpha(mask)
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()
        pp_image = ImageReader(io.BytesIO(img_byte_arr))
        c.drawImage(pp_image, 20, 455, width=100, height=100, mask="auto")

    return None


def page_end_checker(y: int, exp, spacing: int = 12, punto: int = 10):
    """
    This function is used to assess if the current cv page will be enough
    to display the next experience block. If not, a new page should be created.
    """

    def size_checker(y: int, text):
        if text:
            for line in text.splitlines():
                if len(text.splitlines()) > 1:
                    y -= spacing
        return y

    y = size_checker(y, text=f"{exp['title']} @ {exp['company']}")
    y -= 10
    y = size_checker(y, text=f"{exp['start']} - {exp['end']}")
    y -= 20
    y = size_checker(y, text=exp["description"])
    y -= 3
    y = size_checker(y, text=exp["technologies"])
    y -= 25
    print(y)
    if y < 0:
        return True
    else:
        return False


def merge_pdfs(input_directory: str = "cv_pages", output_directory: str = "cv_output"):
    """
    This function merges all pdfs into one, in the given directory.
    Also creates a .pptx copy.
    """
    try:
        os.remove(f"{output_directory}/cv.pdf")
        os.remove(f"{output_directory}/cv.pptx")
    except:
        pass
    pdfs = []
    for filename in os.listdir(input_directory):
        f = os.path.join(input_directory, filename)
        # checking if it is a file
        if os.path.isfile(f) and filename != ".gitkeep" and filename != "cv.pptx":
            pdfs.append(f)

    pdfs = sorted(pdfs, reverse=False)
    print(pdfs)

    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write(f"{output_directory}/cv.pdf")
    merger.close()
    subprocess.run(["pdf2pptx", f"{output_directory}/cv.pdf"])

    return None


def yaml_checker(yaml):
    """
    This function is used to assess if the current cv page will be enough
    to display the next experience block. If not, a new page should be created.
    """

    assert (
        "first_name" in yaml
    ), "'first_name' field is missing in yaml. this is a mandatory field."
    assert (
        "last_name" in yaml
    ), "'last_name' field is missing in yaml. this is a mandatory field."
    assert "role" in yaml, "'role' field is missing in yaml. this is a mandatory field."
    assert (
        "email" in yaml
    ), "'email' field is missing in yaml. this is a mandatory field."

    assert (
        "about_me" in yaml
    ), "'about_me' field is missing in yaml. this is a mandatory field."
    assert (
        "education" in yaml
    ), "'education' field is missing in yaml. this is a mandatory field."
    assert (
        "biography" in yaml
    ), "'biography' field is missing in yaml. this is a mandatory field."
    assert (
        "roles" in yaml
    ), "'roles' field is missing in yaml. this is a mandatory field."
    assert (
        "certifications" in yaml
    ), "'certifications' field is missing in yaml. this is a mandatory field."
    assert (
        "competences" in yaml
    ), "'competences' field is missing in yaml. this is a mandatory field."
    assert (
        "experience" in yaml
    ), "'experience' field is missing in yaml. this is a mandatory field."

    for element in yaml["education"]:
        assert (
            "degree" in element
        ), "'degree' field is missing in one of 'education' fields. you can leave them empty but you shouldn't delete the fields."
        assert (
            "institution" in element
        ), "'institution' field is missing in one of 'education' fields. you can leave them empty but you shouldn't delete the fields."
        assert (
            "year" in element
        ), "'year' field is missing in one of 'education' fields. you can leave them empty but you shouldn't delete the fields."
    for element in yaml["roles"]:
        assert (
            "title" in element
        ), "'title' field is missing in one of 'roles' fields. you can leave them empty but you shouldn't delete the fields."
        assert (
            "description" in element
        ), "'description' field is missing in one of 'roles' fields. you can leave them empty but you shouldn't delete the fields."
    if yaml["certifications"]:
        for element in yaml["certifications"]:
            assert (
                "title" in element
            ), "'title' field is missing in one of 'certifications' fields. you can leave them empty but you shouldn't delete the fields."
    for element in yaml["competences"]:
        assert (
            "title" in element
        ), "'title' field is missing in one of 'competences' fields. you can leave them empty but you shouldn't delete the fields."
        assert (
            "description" in element
        ), "'description' field is missing in one of 'competences' fields. you can leave them empty but you shouldn't delete the fields."
    for element in yaml["experience"]:
        assert (
            "title" in element
        ), "'title' field is missing in one of 'experience' fields. you can leave them empty but you shouldn't delete the fields."
        assert (
            "company" in element
        ), "'company' field is missing in one of 'experience' fields. you can leave them empty but you shouldn't delete the fields."
        assert (
            "start" in element
        ), "'start' field is missing in one of 'experience' fields. you can leave them empty but you shouldn't delete the fields."
        assert (
            "end" in element
        ), "'end' field is missing in one of 'experience' fields. you can leave them empty but you shouldn't delete the fields."
        assert (
            "description" in element
        ), "'description' field is missing in one of 'experience' fields. you can leave them empty but you shouldn't delete the fields."
        assert (
            "technologies" in element
        ), "'technologies' field is missing in one of 'experience' fields. you can leave them empty but you shouldn't delete the fields."

    return None
