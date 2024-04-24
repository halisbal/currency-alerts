import json
import os

import requests


class InstagramClient:
    def __init__(self):
        self.access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
        self.instagram_account_id = os.environ.get("INSTAGRAM_ACCOUNT_ID")
        self.media_upload_url = (
            f"https://graph.facebook.com/v13.0/{self.instagram_account_id}/media"
        )
        self.media_publish_url = f"https://graph.facebook.com/v13.0/{self.instagram_account_id}/media_publish"

    def upload_image(self, caption, image_url):
        payload = {
            "caption": caption,
            "image_url": image_url,
            "access_token": self.access_token,
        }
        response = requests.post(self.media_upload_url, data=payload)
        if response.status_code != 200:
            print("Instagram upload error", response.text)
            return None
        result = json.loads(response.text)
        creation_id = result["id"]
        return creation_id

    def publish_image(self, creation_id):
        payload = {
            "creation_id": int(creation_id),
            "access_token": self.access_token,
        }
        response = requests.post(self.media_publish_url, data=payload)
        if response.status_code != 200:
            print("Instagram publish error", response.text)
            return None
        return response.text


instagram = InstagramClient()
