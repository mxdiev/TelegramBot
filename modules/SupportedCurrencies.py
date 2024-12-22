from modules.config import *
import requests

class SupportedCurrencies:
    @staticmethod
    def get_supported():
        url = f"{CURRENCY_API_URL}/USD"
        headers = {"apikey": API_KEY}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return list(data.get("rates", {}).keys())
        return None