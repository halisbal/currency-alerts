from __future__ import annotations
from typing import List
from pydantic import BaseModel
from datetime import datetime


class Data(BaseModel):
    SEMBOLID: int
    SEMBOL: str
    ACIKLAMA: str
    YUZDEDEGISIM: float
    NET: float
    TARIH: str
    YUKSEK: float
    DUSUK: float
    DUNKUKAPANIS: float
    ACILIS: float
    KAPANIS: float
    ALIS: float
    SATIS: float
    HACIMTL: float
    OrderId: int
    TARIHFORMAT: str

    @property
    def ALIS_FIYAT(self):
        if self.SEMBOL == "GLDGR":
            return float("{:.2f}".format(self.ALIS))
        return float("{:.3f}".format(self.ALIS))


class Ozet(BaseModel):
    ImageUrl: str
    Link: str
    Utm: str
    ClassInfo: str
    IsSeansTime: bool
    CreditName: str
    CreditInterestRate: float
    CreditUrl: str
    CreditInterestUrl: str


class BigParaResponse(BaseModel):
    data: List[Data]
    ozet: Ozet

    @property
    def currency_data(self):
        arr = []
        for d in self.data:
            arr.append(d.model_dump())
        return arr

    # available symbols: TAHVIL, XU100, BRENT, EURTRY, EURUSD, GLDGR, USDTRY, GBPTRY
    def search_currency_data(self, currency) -> Data:
        for d in self.data:
            if d.SEMBOL == currency:
                return d

    @property
    def usd_price(self):
        return str(
            "{:.3f}".format(float(self.search_currency_data("USDTRY").ALIS_FIYAT))
        )

    @property
    def eur_price(self):
        return str(
            "{:.3f}".format(float(self.search_currency_data("EURTRY").ALIS_FIYAT))
        )

    @property
    def gold_price(self):
        return str(
            "{:.2f}".format(float(self.search_currency_data("GLDGR").ALIS_FIYAT))
        )

    @property
    def pound_price(self):
        return str(
            "{:.3f}".format(float(self.search_currency_data("GBPTRY").ALIS_FIYAT))
        )

    def get(self, currency):
        mapping = {
            "USDTRY": self.usd_price,
            "EURTRY": self.eur_price,
            "GLDGR": self.gold_price,
            "GBPTRY": self.pound_price,
        }
        return mapping.get(currency)


class PostCurrenciesObject(BaseModel):
    currency: str
    rate: float
    date: datetime
    rate_change: float


class MysqlLastPricesResponse(BaseModel):
    data: List[PostCurrenciesObject]

    @property
    def currency_data(self):
        arr = []
        for d in self.data:
            arr.append(d.model_dump())
        return arr

    # available symbols: EURTRY, GLDGR, USDTRY, GBPTRY, PLNTRY
    def search_currency_data(self, currency) -> PostCurrenciesObject:
        for d in self.data:
            if d.currency == currency:
                return d

    @property
    def usd_price(self):
        return str("{:.3f}".format(float(self.search_currency_data("USDTRY").rate)))

    @property
    def eur_price(self):
        return str("{:.3f}".format(float(self.search_currency_data("EURTRY").rate)))

    @property
    def gold_price(self):
        return str("{:.2f}".format(float(self.search_currency_data("GLDGR").rate)))

    @property
    def pound_price(self):
        return str("{:.3f}".format(float(self.search_currency_data("GBPTRY").rate)))

    @property
    def pln_price(self):
        return str("{:.3f}".format(float(self.search_currency_data("PLNTRY").rate)))

    def get(self, currency):
        mapping = {
            "USDTRY": self.usd_price,
            "EURTRY": self.eur_price,
            "GLDGR": self.gold_price,
            "GBPTRY": self.pound_price,
            "PLNTRY": self.pln_price,
        }
        return mapping.get(currency)
