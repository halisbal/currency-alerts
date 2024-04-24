import os
import requests


class Telegram:
    def __init__(self):
        self.url = f'https://api.telegram.org/{os.environ.get("TELEGRAM_BOT_TOKEN")}/'
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    def send_message(self, text: str, image_url: str = None):
        url = f"{self.url}sendMessage"
        final_text = text + "\n" + f'<a href="{image_url}"> ‏ </a>'
        params = {
            "chat_id": self.chat_id,
            "text": final_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        }
        return requests.post(url, params=params)


telegram = Telegram()
