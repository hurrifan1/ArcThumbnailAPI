from math import floor
from PIL import Image, ImageFont, ImageDraw
import os
import shutil
import random
import threading


# Load the template PNG image and instantiate
#   an ImageDraw object with it


def generate_image(text: str) -> Image:
    """
    Uses the Pillow/PIL library to generate a PNG image with user-provided
    text. Returns the resulting Image object.
    """
    img_fp = "layered-waves-haikei 3.png"
    im = Image.open(img_fp, mode="r", formats=["png"])
    draw = ImageDraw.Draw(im)

    # Load our Nexa light font, text, and text size

    my_font = ImageFont.truetype("Nexa Light.otf", 120)
    # my_text_raw = "How to Unpivot a Table in Qlik Sense"
    my_text_raw = text

    # Set the margins of the textbox

    lr_margins = 80
    tb_margins = 80

    # Calculate the line breaks

    text_width_limit = im.width - (lr_margins * 2)

    row_size = 0
    my_text_lines = ""
    for w in my_text_raw.split(" "):
        curr_size = draw.textlength(text=w + " ", font=my_font)
        if row_size + curr_size <= text_width_limit:
            row_size += curr_size
            my_text_lines = " ".join([my_text_lines, w])
        else:
            row_size = curr_size
            my_text_lines = "\n".join([my_text_lines, w])

    my_text_lines = my_text_lines.strip()

    draw.multiline_text(
        xy=(lr_margins, tb_margins),
        text=my_text_lines,
        fill="#ffffff",
        font=my_font,
        spacing=24,
        align="left",
    )

    # im.show()
    return im
    # </ def generate_image()>


def save_image(i: Image, file_name: str) -> str:
    """
    Uses the Pillow/PIL library to save the provided Image file to disk
    in a temporary folder generated on-the-fly.
    """
    new_dir = "temp_img/" + generate_nonce()
    parent_dir = os.getcwd()
    new_path = os.path.join(parent_dir, new_dir)
    os.mkdir(new_path)

    # Check result:
    # print("Directory '% s' created" % new_path)

    save_path = os.path.join(new_path, file_name)

    i.save(save_path)
    i.close()
    return save_path


def delete_image_folder(file_name: str, dur: int):
    """
    Recursively deletes the image folder at the given path.
    """

    def delfol(f):
        dir_path = os.path.dirname(f)
        shutil.rmtree(dir_path)

    t = threading.Timer(interval=dur, function=delfol, kwargs={"f": file_name})
    t.start()


def generate_nonce() -> str:
    """
    Generates a random 8 character string using numbers, upper-,
    and lowercase letters.
    """
    # Generate 4 random letters
    gen_l = ""
    for i in range(4):
        ud = random.randrange(97, 122)  # <- lowercase unicode dec points
        l = chr(ud)
        l = l.__str__().upper() if random.random() < 0.5 else l
        gen_l = "".join([gen_l, l])

    # Generate 4 random digits
    gen_n = floor(random.random() * 9999)

    # Shuffle them together
    gen_all = "".join([gen_l, gen_n.__str__()])
    gen_all_spl = [*gen_all]
    random.shuffle(gen_all_spl)
    res = "".join(gen_all_spl)
    return res
