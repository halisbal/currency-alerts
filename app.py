from chalice import Chalice


app = Chalice(app_name="telegram_currency")


@app.schedule("cron(0 */3 ? * MON-FRI *)")
def telegram_message(event):
    from chalicelib.canlidovizkuru.currency_post import currency_post_service

    currency_post_service.run_pipeline()
