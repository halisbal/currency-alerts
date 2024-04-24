from datetime import datetime

from chalicelib.clients.bigpara import bigpara
from chalicelib.clients.dovizcom import dovizcom
from chalicelib.clients.instagram import instagram
from chalicelib.helpers.image_service import image_service
from chalicelib.clients.mysql import mysql
from chalicelib.helpers.text_service import (
    generate_post_text,
    get_hashtags,
    generate_post_text_without_change_rate,
)
from chalicelib.models.models import MysqlLastPricesResponse
from chalicelib.clients.telegram import telegram
from chalicelib.clients.twitter import twitter


class DataService:
    def __init__(self):
        self.bigpara_data = bigpara.get_currency_rates()
        self.zloti_price = dovizcom.get_zloti_price()
        self.last_prices = self.get_last_prices()

    def format_currency_data(self):
        arr = []
        for currency in ["USDTRY", "EURTRY", "GLDGR", "GBPTRY", "PLNTRY"]:
            if currency != "PLNTRY":
                current_rate = self.bigpara_data.get(currency)
            else:
                current_rate = self.zloti_price
            last_rate = self.last_prices.get(currency)
            rate_change = round(
                ((float(current_rate) - float(last_rate)) / float(last_rate)) * 100, 2
            )
            arr.append(
                {
                    "currency": currency,
                    "rate": current_rate,
                    "last_rate": last_rate,
                    "rate_change": rate_change,
                    "emoji": self.get_emoji(rate_change),
                    "color": self.get_color(rate_change),
                }
            )
        return arr

    @classmethod
    def get_emoji(cls, rate_change):
        if rate_change > 0:
            return "🟢"
        elif rate_change < 0:
            return "🔴"
        else:
            return "⚪️"

    @classmethod
    def get_color(cls, rate_change):
        if rate_change >= 0:
            return 0, 128, 0
        else:
            return 196, 30, 58

    @classmethod
    def get_last_prices(cls):
        data = mysql.execute(
            "select * from post_currencies pc where pc.date = (select max(date) from post_currencies)"
        )
        return MysqlLastPricesResponse(**{"data": data})


class CurrencyPostService:
    def __init__(self):
        self.data_service = data_service
        self.currency_data = []
        self.message_text = ""
        self.message_text_with_out_change_rates = ""
        self.image_url = ""
        self.image_path = ""
        self.hashtags = ""

    def set_currency_data(self):
        data = self.data_service.format_currency_data()
        if not data:
            raise Exception("Data is empty")
        usd_data = list(filter(lambda x: x["currency"] == "USDTRY", data))[0]
        eur_data = list(filter(lambda x: x["currency"] == "EURTRY", data))[0]
        gold_data = list(filter(lambda x: x["currency"] == "GLDGR", data))[0]
        pound_data = list(filter(lambda x: x["currency"] == "GBPTRY", data))[0]
        zloti_data = list(filter(lambda x: x["currency"] == "PLNTRY", data))[0]
        self.currency_data = [usd_data, eur_data, gold_data, pound_data, zloti_data]

    def set_message_text(self):
        self.message_text = generate_post_text(self.currency_data)
        self.message_text_with_out_change_rates = (
            generate_post_text_without_change_rate(self.currency_data)
        )
        if not self.message_text or not self.message_text_with_out_change_rates:
            raise Exception("Message text is empty")

    def set_image(self):
        self.image_url, self.image_path = image_service.generate_post_image(
            currency_data=self.currency_data
        )
        if not self.image_url:
            raise Exception("Image url is empty")

    def set_hashtags(self):
        self.hashtags = get_hashtags()

    def run_telegram_pipeline(self):
        try:
            response = telegram.send_message(self.message_text, self.image_url)
            if not response.status_code == 200:
                print("Telegram error", response.text)
        except Exception as e:
            print("Telegram error", e)

    def run_instagram_pipeline(self):
        caption_text = self.message_text + "\n" + self.hashtags
        try:
            creation_id = instagram.upload_image(caption_text, self.image_url)
            response = instagram.publish_image(creation_id)
            if not response.status_code == 200:
                print("Instagram error", response.text)
        except Exception as e:
            print("Instagram error", e)

    def run_twitter_pipeline(self):
        message_text = self.message_text_with_out_change_rates + "\n" + self.hashtags
        try:
            twitter.post_tweet(message_text, self.image_path)
        except Exception as e:
            print("Twitter error", e)

    def save_data(self):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"""INSERT INTO post_currencies (currency, rate, date, rate_change, image_url) VALUES
            ('{self.currency_data[0].get('currency')}', {self.currency_data[0].get('rate')}, '{date}', {self.currency_data[0].get('rate_change')}, '{self.image_url}'),
            ('{self.currency_data[1].get('currency')}', {self.currency_data[1].get('rate')}, '{date}', {self.currency_data[1].get('rate_change')}, '{self.image_url}'),
            ('{self.currency_data[2].get('currency')}', {self.currency_data[2].get('rate')}, '{date}', {self.currency_data[2].get('rate_change')}, '{self.image_url}'),
            ('{self.currency_data[3].get('currency')}', {self.currency_data[3].get('rate')}, '{date}', {self.currency_data[3].get('rate_change')}, '{self.image_url}'),
            ('{self.currency_data[4].get('currency')}', {self.currency_data[4].get('rate')}, '{date}', {self.currency_data[4].get('rate_change')}, '{self.image_url}')"""
        mysql.execute(query)

    def run_pipeline(self):
        self.set_currency_data()
        self.set_message_text()
        self.set_hashtags()
        self.set_image()
        self.run_telegram_pipeline()
        self.run_instagram_pipeline()
        self.run_twitter_pipeline()
        self.save_data()


data_service = DataService()
currency_post_service = CurrencyPostService()
