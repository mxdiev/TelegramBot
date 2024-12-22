from modules.config import *
import requests

class CurrencyRates:
    @staticmethod
    def get_all_rates(base_currency: str):
        url = f"{CURRENCY_API_URL}/{base_currency}"
        headers = {"apikey": API_KEY}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data.get("rates", {})
        return None