import requests
import os

class Zoopla:
    def __init__(self, api_key=None, verbose=False):
        self.api_key = api_key or os.getenv("ZOOPLA_API_KEY")
        self.verbose = verbose
        self.base_url = "http://api.zoopla.co.uk/api/v1/"

    def average_area_sold_price(self, params):
        area = params.get("area")
        url = f"{self.base_url}average_area_sold_price.json"
        response = requests.get(url, params={**params, "api_key": self.api_key})
        if self.verbose:
            print("Request URL:", response.url)
            print("Status Code:", response.status_code)
        if response.ok:
            return response.json()
        else:
            raise Exception(f"Zoopla API Error: {response.status_code} - {response.text}")