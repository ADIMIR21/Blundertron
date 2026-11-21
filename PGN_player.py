import requests
import json
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
mail = os.getenv("CHESSCOM_MAIL")
session = requests.Session()
session.headers.update({
    f"User-Agent": "PGNScraper ({mail})"
})

def game_PGN(num, player):
    try:
        out_dir = Path("pgn_files")
        out_dir.mkdir(parents=True, exist_ok=True)
        url = f"https://api.chess.com/pub/player/{player.lower()}/games/archives"
        response_archives  = session.get(url, timeout=(10, 30))
        response_archives.raise_for_status()
        data = response_archives.json()
        place_archives = 0
        pgn_list = list()
        while len(pgn_list) < num:
            place_archives -= 1
            if  abs(place_archives) > len(data["archives"]):
                break
            response_games =  session.get(data["archives"][place_archives],  timeout=(10, 30))
            response_games.raise_for_status()
            month_games = response_games.json().get("games", [])
            pgn_list = month_games + pgn_list

        games_out = []
        for game in pgn_list[-num:][::-1]:
            games_out.append({
                "url": game["url"],
                "pgn": game["pgn"],
                "end_time": game.get("end_time"),
                "time_class": game.get("time_class"),
                })
        data_data = {
            "username": player,
            "games": games_out,
        }
        file_path = out_dir / f"{player.lower()}.json"
        file_path.write_text(
            json.dumps(data_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return "JSON created"
    except requests.exceptions.HTTPError as err:
        return f"No HTTP response: {err}"
    except requests.exceptions.RequestException as err:
        return f"Problem with the request: {err}"