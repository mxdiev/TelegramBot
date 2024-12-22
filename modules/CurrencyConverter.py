from modules.config import *
import requests

class CurrencyConverter:
    @staticmethod
    def convert(amount: float, base_currency: str, target_currency: str):
        url = f"{CURRENCY_API_URL}/{base_currency}"
        headers = {"apikey": API_KEY}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            rate = data.get("rates", {}).get(target_currency)
            if rate:
                return amount * rate
        return None