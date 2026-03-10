import requests
import os
from dotenv import load_dotenv
import json
from pathlib import Path
import difflib

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

STEAM_API_KEY = os.getenv("STEAM_API_KEY")

def get_game_price(app_id: int) -> dict:
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=hu&l=english"
    response = requests.get(url)
    data = response.json()

    if not data[str(app_id)]["success"]:
        return None

    game_data = data[str(app_id)]["data"]

    if "price_overview" not in game_data:
        # print(f"\t⚠️  Nincs ár adat ehhez a játékhoz.")
        return None

    price_data = game_data["price_overview"]

    return {
        "name": game_data["name"],
        "original_price": price_data["initial"] / 100,
        "current_price": price_data["final"] / 100,
        "discount": price_data["discount_percent"],
        "on_sale": price_data["discount_percent"] > 0
    }

def get_manual_games() -> list:
    path = Path(__file__).parent.parent / "games.json"
    with open(path, "r") as f:
        return json.load(f)
    
def normalize_name(name: str) -> str:
    ignore = ["™", "®", "©", "Edition", "GOTY", "Ultimate", "Director's Cut",
              "Definitive", "Enhanced", "Remastered", "Complete", "Gold", "Deluxe",
              "Premium", "Standard", "Bundle", "Collection", "Game of the Year"]
    result = name
    for word in ignore:
        result = result.replace(word, "")
    result = " ".join(result.split())
    return result.lower().strip()

def search_game_id(game_name: str) -> int:
    url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&cc=hu&l=english"
    response = requests.get(url)
    data = response.json()

    if data["total"] == 0:
        print(f"\t⚠️ Nem található a Steam-en: {game_name}")
        return None

    best_match = None
    best_ratio = 0

    for item in data["items"]:
        normalized_search = normalize_name(game_name)
        normalized_item = normalize_name(item["name"])

        # Ha a keresett név benne van a találatban → 100%
        if normalized_search in normalized_item:
            print(f"\t✅ Sikeres találat: {item['name']} (100% egyezés)")
            return item["id"]

        ratio = difflib.SequenceMatcher(None, normalized_search, normalized_item).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = item

    if best_ratio < 0.5:
        print(f"\t⚠️ Nem található pontos egyezés: {game_name} (legjobb: {best_match['name']}, {best_ratio:.0%})")
        return None

    print(f"\t✅ Sikeres találat: {best_match['name']} ({best_ratio:.0%} egyezés)")
    return best_match["id"]

if __name__ == "__main__":
    result = get_game_price(526870)
    print(result)

    games = get_manual_games()
    print(f"Figyelt játékok ({len(games)}):")
    for game in games:
        print(f"- {game['name']}")