import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from steam_api import normalize_name, get_game_price, get_manual_games

def test_normalize_name_removes_trademark():
    assert normalize_name("Dark Souls™ III") == "dark souls iii"

def test_normalize_name_removes_goty():
    assert normalize_name("Sekiro™: Shadows Die Twice - GOTY Edition") == "sekiro: shadows die twice -"

def test_normalize_name_lowercase():
    assert normalize_name("ELDEN RING") == "elden ring"

def test_get_game_price_returns_dict():
    result = get_game_price(526870)  # Satisfactory
    assert result is not None
    assert "name" in result
    assert "current_price" in result
    assert "original_price" in result
    assert "discount" in result
    assert "on_sale" in result

def test_get_game_price_invalid_id():
    result = get_game_price(999999999)
    assert result is None

def test_get_manual_games_returns_list():
    games = get_manual_games()
    assert isinstance(games, list)
    assert len(games) > 0

def test_get_manual_games_has_name():
    games = get_manual_games()
    for game in games:
        assert "name" in game