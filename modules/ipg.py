# coding=utf-8

"""
Copyright © 2016, Matvey Vyalkov

This file is part of SysRq tools4lulz.
SysRq tools4lulz is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SysRq tools4lulz is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with SysRq tools4lulz.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import io
import time
import re
import requests
from base64 import b64decode
from textwrap import TextWrapper
from imgurpython import ImgurClient
from PIL import Image, ImageFont, ImageDraw

from . import general

image_base64 = re.compile(r"^data:image/.+;base64,")

footer = Image.open(general.static + "/img/footer.png")
line = Image.open(general.static + "/img/line.png")

client_id = "fd74deb2e272b12"
client_secret = "7f777d5fb7109bacc24e2d1667ed32494a6754a5"
client = ImgurClient(client_id, client_secret)


def image_size(url):
    """
    Getting size of image using HEAD request
    :param url:
    :return: size in Mbytes
    """
    headers = requests.head(url, headers=general.user_agent).headers
    return int(headers.get("Content-Length", 0)) / 1000000


def font_width(font_size, image_width):
    """
    Calculating 'Pobeda' font width
    :param font_size
    :param image_width
    :return: font size in pt
    """
    symbols = image_width // int(font_size * 3.5)
    if not symbols:
        symbols = 1
    return symbols


def fit_text(message, *, size, font_size):
    if isinstance(message, str):
        message = [message]
    font = ImageFont.truetype("static/fonts/pobeda-regular.ttf",
                              size=font_size)
    texts = []
    if len(message) <= 2:
        for text_line in message:
            label_size = font.getsize(text_line)
            if label_size[0] < size[0] \
                    and label_size[1] * len(message) < size[1]:
                texts.append(
                    {"text": text_line, "size": {"width": label_size[0],
                                                 "height": label_size[1]}})
            else:
                font_size -= 5
                return fit_text(
                    TextWrapper(width=font_width(font_size, size[0]),
                                break_long_words=False).wrap(
                        " ".join(message)),
                    size=size, font_size=font_size)
    else:
        font_size -= 5
        return fit_text(TextWrapper(width=font_width(font_size, size[0]),
                                    break_long_words=False).wrap(
            " ".join(message)),
            size=size, font_size=font_size)
    return texts, font


def ipg_template(background, message, size=120,
                 align="bottom", watermark=True):
    back = Image.open(background).convert("RGBA")
    back.thumbnail((2560, 2048), Image.ANTIALIAS)  # max size of VK image
    if watermark:
        fore = footer
        fore.thumbnail(back.size, Image.ANTIALIAS)
        offset = ((back.width - fore.width) // 2,
                  back.height - fore.height)
        back.paste(fore, offset, fore)

        for left in range(offset[0]):
            back.paste(line, (left, offset[1]), line)

        for right in range(offset[0] + fore.width, back.width):
            back.paste(line, (right, offset[1]), line)
    else:
        offset = (back.width // 2, back.height)
    if not size or not message:
        return back
    texts, font = fit_text(message.upper(), size=back.size, font_size=size)

    rect = Image.new("RGBA", back.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(rect)
    if len(texts) == 2:
        height = texts[0]["size"]["height"]
        if align == "bottom":
            draw.rectangle([(0, offset[1] - int(height * 1.2)),
                            (back.width, offset[1])],
                           fill=(0, 0, 0, 147))
        elif align == "top":
            draw.rectangle([(0, int(height * 2.1)),
                            (back.width, 0)],
                           fill=(0, 0, 0, 147))

        first_width = (back.width - texts[1]["size"]["width"]) // 2
        first_msg = texts[1]["text"]

        second_width = (back.width - texts[0]["size"]["width"]) // 2
        second_msg = texts[0]["text"]

        if align == "bottom":
            draw.text((first_width, offset[1] - height),
                      text=first_msg, fill="white", font=font)
            draw.text((second_width, offset[1] - int(height * 1.9)),
                      text=second_msg, fill="white", font=font)
        elif align == "top":
            draw.text((second_width, height // 10),
                      text=second_msg, fill="white", font=font)
            draw.text((first_width, int(height * 1.1)),
                      text=first_msg, fill="white", font=font)
    else:
        height = texts[0]["size"]["height"]
        if align == "bottom":
            draw.rectangle([(0, offset[1] - int(height * 1.1)),
                            (back.width, offset[1])],
                           fill=(0, 0, 0, 147))
        elif align == "top":
            draw.rectangle([(0, int(height * 1.1)),
                            (back.width, 0)],
                           fill=(0, 0, 0, 147))
        width = (back.width - texts[0]["size"]["width"]) // 2
        text = texts[0]["text"]
        if align == "bottom":
            draw.text((width, offset[1] - height),
                      text=text, fill="white", font=font)
        elif align == "top":
            draw.text((width, int(height * 0.1)),
                      text=text, fill="white", font=font)

    back = Image.alpha_composite(back, rect)
    return back


def ipg_build(link, message, size, align, mark):
    if link.startswith("data:image"):
        base64_data = image_base64.sub("", link)
        back = io.BytesIO(b64decode(base64_data))
    else:
        if image_size(link) > 9:
            raise general.SysRq("Превышем максимальный размер изображения.")
        else:
            content = requests.get(link, headers=general.user_agent).content
            back = io.BytesIO(content)
    timestamp = int(time.time())
    img_path = "/tmp/img-{}.png".format(timestamp)
    ipg_template(back, message, size, align, mark).save(img_path)
    result_link = client.upload_from_path(img_path)["link"]
    os.remove(img_path)
    return result_link
