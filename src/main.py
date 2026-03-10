import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

sys.path.append(str(Path(__file__).parent))

from notifier import notify

from steam_api import get_game_price, get_manual_games, search_game_id

def check_games() -> None:
    games = get_manual_games()
    print(f"\t🎮 {len(games)} játék ellenőrzése...")

    for game in games:
        print(f"\n\t🔍 {game['name']} ellenőrzése...")
        
        app_id = game.get("app_id") or search_game_id(game["name"])
        if app_id is None:
            print(f"\t⚠️  {game['name']} ID-ja nem elérhető.")
            continue

        price = get_game_price(app_id)
        if price is None:
            print(f"\t⚠️  {game['name']} ára nem elérhető.")
            continue

        threshold = game.get("price_threshold")
        on_sale = price["on_sale"]
        under_threshold = threshold is not None and price["current_price"] <= threshold

        if on_sale or under_threshold:
            print(f"\t🔥 {game['name']} akciós vagy küszöb alatt — értesítés küldése!")
            notify(
                game_name=price["name"],
                original_price=price["original_price"],
                current_price=price["current_price"],
                discount=price["discount"]
            )
        else:
            print(f"\t✅ {game['name']}: {price['current_price']}€ — nincs akció.")

if __name__ == "__main__":
    check_games()