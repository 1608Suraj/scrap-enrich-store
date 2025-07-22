import requests
import json
import time
import os

api_url = "Paste here the api form which you want to scrap data"

def fetch_data():
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        with open("fileName.json", "w") as f:
            json.dump(data, f, indent=2)

        print("✅ Data fetched successfully.")
    except Exception as e:
        print(f"❌ Error occurred: {e}")

fetch_data()
