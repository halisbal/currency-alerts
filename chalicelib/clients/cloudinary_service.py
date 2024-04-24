import os

import cloudinary.uploader
import cloudinary.api


class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
            api_key=os.environ.get("CLOUDINARY_API_KEY"),
            api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
            secure=True,
        )

    @classmethod
    def upload_image(cls, image_path):
        response = cloudinary.uploader.upload(image_path)
        image_url = response.get("url")
        return image_url


cloudinary_service = CloudinaryService()
