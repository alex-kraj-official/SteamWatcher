import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

sys.path.append(str(Path(__file__).parent))

from steam_api import get_game_price, get_manual_games
from notifier import notify

def check_games() -> None:
    games = get_manual_games()
    print(f"🎮 {len(games)} játék ellenőrzése...")

    for game in games:
        print(f"\n🔍 {game['name']} ellenőrzése...")
        price = get_game_price(game["app_id"])

        if price is None:
            print(f"⚠️ {game['name']} ára nem elérhető.")
            continue

        on_sale = price["on_sale"]
        under_threshold = price["current_price"] <= game["price_threshold"]

        if on_sale or under_threshold:
            print(f"🔥 {game['name']} akciós vagy küszöb alatt — értesítés küldése!")
            notify(
                game_name=price["name"],
                original_price=price["original_price"],
                current_price=price["current_price"],
                discount=price["discount"]
            )
        else:
            print(f"✅ {game['name']}: {price['current_price']}€ — nincs akció.")

if __name__ == "__main__":
    check_games()