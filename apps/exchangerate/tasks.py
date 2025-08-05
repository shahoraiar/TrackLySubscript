from celery import shared_task
import requests
from .models import ExchangeRateLog

@shared_task
def fetch_usd_to_bdt_rate():
    print('called the fetch usd to bdt rate')
    try:
        url = "https://open.er-api.com/v6/latest/USD"  # Free exchange rate API
        response = requests.get(url)
        print('response : ', response)
        data = response.json()
        rate = data['rates'].get('BDT')

        if rate:
            ExchangeRateLog.objects.create(
                base_currency='USD',
                target_currency='BDT',
                rate=rate
            )
            print(f"Saved USD to BDT rate: {rate}")
        else:
            print("Rate not found.")
    except Exception as e:
        print("Error fetching exchange rate:", e)


