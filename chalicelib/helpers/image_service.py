import os

import requests
from PIL import Image, ImageFont, ImageDraw
from chalicelib.clients.cloudinary_service import cloudinary_service
from pytz import timezone
from datetime import datetime


class ImageService:
    def __init__(self):
        self.BASE_IMAGE_URL = os.environ.get("BASE_IMAGE_URL")
        self.FONT_URL = os.environ.get("FONT_URL")

    def generate_post_image(self, currency_data: list):
        response = requests.get(self.BASE_IMAGE_URL)
        with open("/tmp/image.png", "wb") as f:
            f.write(response.content)
        my_image = Image.open("/tmp/image.png")
        r = requests.get(self.FONT_URL)
        with open("/tmp/font.ttf", "wb") as f:
            f.write(r.content)
        title_font = ImageFont.truetype("/tmp/font.ttf", 50)
        title_font2 = ImageFont.truetype("/tmp/font.ttf", 35)

        image_editable = ImageDraw.Draw(my_image)
        tz = timezone("Turkey")
        tr_now = datetime.now(tz)
        curdate = tr_now.strftime("%d-%m-%Y")
        cur_time = tr_now.strftime("%H:%M")
        image_editable.text(
            (500, 404.8),
            str(currency_data[0].get("rate")),
            currency_data[0].get("color"),
            font=title_font,
        )
        image_editable.text(
            (500, 484.2),
            str(currency_data[1].get("rate")),
            currency_data[1].get("color"),
            font=title_font,
        )
        image_editable.text(
            (500, 563.5),
            str(currency_data[2].get("rate")),
            currency_data[2].get("color"),
            font=title_font,
        )
        image_editable.text(
            (500, 642.9),
            str(currency_data[3].get("rate")),
            currency_data[3].get("color"),
            font=title_font,
        )
        image_editable.text(
            (500, 722.2),
            str(currency_data[4].get("rate")),
            currency_data[4].get("color"),
            font=title_font,
        )
        image_editable.text((275, 265), curdate, (256, 256, 256), font=title_font2)
        image_editable.text((780, 265), cur_time, (256, 256, 256), font=title_font2)
        my_image.save("/tmp/result.png")
        file = "/tmp/result.png"
        return cloudinary_service.upload_image(file), file


image_service = ImageService()
