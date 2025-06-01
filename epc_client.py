import os
import requests
from dotenv import load_dotenv

load_dotenv()

EPC_API_KEY = os.getenv("EPC_API_KEY")
EPC_BASE_URL = "https://epc.opendatacommunities.org/api/v1"

def fetch_epc_data(postcode):
    headers = {
        "Authorization": f"Basic {EPC_API_KEY}"
    }
    url = f"{EPC_BASE_URL}/domestic/search?postcode={postcode}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        records = response.json().get("rows", [])
        return records[0] if records else None
    else:
        print(f"EPC API error: {response.status_code}")
        return None