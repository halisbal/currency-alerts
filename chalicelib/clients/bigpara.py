import requests
from chalicelib.models.models import BigParaResponse
import json


class BigPara:
    def __init__(self):
        self.base_url = "http://api.bigpara.hurriyet.com.tr/doviz/headerlist/anasayfa"

    def get_currency_rates(self):
        return BigParaResponse(**json.loads(requests.get(self.base_url).text))


bigpara = BigPara()
