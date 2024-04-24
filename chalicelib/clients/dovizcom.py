import requests
from bs4 import BeautifulSoup


class DovizCom:
    def __init__(self):
        self.base_url = "https://kur.doviz.com/serbest-piyasa/polonya-zlotisi"

    def get_zloti_price(self):
        response = requests.get(self.base_url)
        bs4 = BeautifulSoup(response.text, "html.parser")
        bs4 = bs4.find_all("div", {"class": "text-xl font-semibold text-white"})
        zloti_price = str("{:.3f}".format(float(bs4[0].text.replace(",", "."))))
        return zloti_price


dovizcom = DovizCom()
