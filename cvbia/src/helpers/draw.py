import io
import itertools
import textwrap

from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth


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
