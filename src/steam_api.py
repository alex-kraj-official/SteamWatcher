import requests
import os
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")

def get_game_price(app_id: int) -> dict:
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=hu&l=english"
    response = requests.get(url)
    data = response.json()

    if not data[str(app_id)]["success"]:
        return None

    price_data = data[str(app_id)]["data"]["price_overview"]

    return {
        "name": data[str(app_id)]["data"]["name"],
        "original_price": price_data["initial"] / 100,
        "current_price": price_data["final"] / 100,
        "discount": price_data["discount_percent"],
        "on_sale": price_data["discount_percent"] > 0
    }

if __name__ == "__main__":
    result = get_game_price(526870)  # Satisfactory
    print(result)