from datetime import datetime
from pytz import timezone
import random


def generate_post_text(currency_data):
    ist = timezone("Turkey")
    date = datetime.now(ist).strftime("%H:%M")
    return (
        "Saat: "
        + date
        + "\n"
        + "\n"
        + (
            "DOLAR/TL: "
            + str(currency_data[0].get("rate"))
            + "₺ -- %"
            + str(currency_data[0].get("rate_change"))
            + " "
            + currency_data[0].get("emoji")
        )
        + "\n"
        + (
            "EURO/TL:  "
            + str(currency_data[1].get("rate"))
            + "₺ -- %"
            + str(currency_data[1].get("rate_change"))
            + " "
            + currency_data[1].get("emoji")
        )
        + "\n"
        + (
            "ALTIN/TL: "
            + str(currency_data[2].get("rate"))
            + "₺ -- %"
            + str(currency_data[2].get("rate_change"))
            + " "
            + currency_data[2].get("emoji")
        )
        + "\n"
        + (
            "POUND/TL: "
            + str(currency_data[3].get("rate"))
            + "₺ -- %"
            + str(currency_data[3].get("rate_change"))
            + " "
            + currency_data[3].get("emoji")
        )
        + "\n"
        + (
            "ZLOTİ/TL: "
            + str(currency_data[4].get("rate"))
            + "₺ -- %"
            + str(currency_data[4].get("rate_change"))
            + " "
            + currency_data[4].get("emoji")
            + "\n"
            + "\n"
            + "Not: Değişim yüzdeleri 3 saat önceki paylaşıma kıyasla hesaplanmaktadır."
        )
    )


def generate_post_text_without_change_rate(currency_data):
    ist = timezone("Turkey")
    date = datetime.now(ist).strftime("%H:%M")
    return (
        "Saat: "
        + date
        + "\n"
        + "\n"
        + (
            "DOLAR/TL: "
            + str(currency_data[0].get("rate"))
            + "₺"
        )
        + "\n"
        + (
            "EURO/TL:  "
            + str(currency_data[1].get("rate"))
            + "₺"
        )
        + "\n"
        + (
            "ALTIN/TL: "
            + str(currency_data[2].get("rate"))
            + "₺"
        )
        + "\n"
        + (
            "POUND/TL: "
            + str(currency_data[3].get("rate"))
            + "₺"
        )
        + "\n"
        + (
            "ZLOTİ/TL: "
            + str(currency_data[4].get("rate"))
            + "₺"
            + "\n"
            + "\n"
        )
    )


def get_hashtags():
    lst1 = [
        "döviz",
        "kur",
        "dolar",
        "euro",
        "altın",
        "gramaltın",
        "pound",
        "zloti",
        "türklirası",
        "borsa",
        "istanbul",
        "türkiye",
        "yatırım",
        "ekonomi",
    ]
    lst2 = [
        "dövizkuru",
        "dövizfiyatları",
        "dövizkurları",
        "dovizkuru",
        "dövizpiyasası",
        "canlıdöviz",
        "canlıborsa",
        "piyasalarborsa",
    ]
    lst3 = ["dolarkuru", "dolartl", "dolartlkuru", "dolarnekadar", "dolarkaçlira"]
    lst4 = ["usdtry", "usdtry💰💵💲", "usdtl", "usdkuru", "usdkurları", "usdprice"]
    lst5 = ["eurotl", "eurokuru", "eurokurları", "eurofiyatları", "eurotl"]

    generalh = random.sample(lst1, 5)
    dovizh = random.sample(lst2, 3)
    dolarh = random.sample(lst3, 2)
    usdh = random.sample(lst4, 1)
    eurh = random.sample(lst5, 1)
    hashtag_text = ""
    temp_hashtags = generalh + dovizh + dolarh + usdh + eurh
    for hashtag in temp_hashtags:
        hashtag_text += "#" + hashtag + " "

    return hashtag_text
