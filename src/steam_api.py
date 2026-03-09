import requests
import os
from dotenv import load_dotenv
import json

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

def get_manual_games() -> list:
    with open("games.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    # Ár teszt
    result = get_game_price(526870)
    print(result)

    # Manuális lista teszt
    games = get_manual_games()
    print(f"Figyelt játékok ({len(games)}):")
    for game in games:
        print(f"- {game['name']} (ID: {game['app_id']}, küszöb: {game['price_threshold']}€)")