import re
from orm.models import QueensPlay
from datetime import date


def queens_date_to_game_number(request_date: date) -> int:
    """
    Converts a date to a game number based on the game's start date.
    The game started on 2024-05-01, which is considered game number 1.
    """
    start_date = date(2024, 5, 1)
    delta = request_date - start_date
    return delta.days + 1


async def parse_queens(text: str, username: str, no_db=False) -> tuple[str, dict[str, str | int]]:
    """
    Extracts and formats Queens game information from a given text.
    Args:
        text (str): The input text containing Queens game information.

    Queens #426 | 0:27 and flawless
    First 👑s: 🟩 🟦 ⬜
    🏅 I’m in the Top 25% of all players today!
    lnkd.in/queens
    """
    regex = r"Queens\s+#(?P<game_number>\d+)\s*\|\s*(?P<minutes>\d+):(?P<seconds>\d+)\s(?P<flawless>and flawless)?"
    match = re.search(regex, text)
    if not match:
        return "No Queens game information found."

    game_number = match.group("game_number")
    minutes = match.group("minutes")
    seconds = match.group("seconds")
    flawless = True if match.group("flawless") else False
    if not game_number or not minutes or not seconds:
        return f"""Incomplete Queens game information found.
        Game number: {game_number}, Minutes: {minutes}, Seconds: {seconds}"""
    game_number = int(game_number)
    total_seconds = int(minutes) * 60 + int(seconds)
    score = (
        total_seconds if flawless else total_seconds * 2
    )  # Assuming a penalty for non-flawless games

    is_new = None
    if not no_db:
        obj, is_new = await QueensPlay.update_or_create(
            username=username,
            game_number=game_number,
            defaults={
                "score": score,
                "time_taken": total_seconds,
                "flawless": flawless,
                "raw_text": text,
            },
        )

    resp_string = f"{'(UPDATING RECORD) ' if is_new is False else ''}Queens Game #{game_number} completed with score {score} by {username}."
    if not flawless:
        resp_string += "\nPenalty: Score was doubled for non-flawless game."

    resp_json = {
        "game_type": "queens",
        "game_number": game_number,
        "score": score,
        "seconds": total_seconds,
        "flawless": flawless,
        "username": username,
    }
    return resp_string, resp_json


async def todays_queens_leaderboard_data(override_date=None) -> dict:
    """
    Current day's leaderboard for Connections game.
    Show top 10 players by score.
    """
    my_date = override_date or date.today()
    today_game_number = queens_date_to_game_number(my_date)
    leaderboard = (
        await QueensPlay.filter(game_number=today_game_number)
        .order_by("score")[:10]
        .values("username", "score")
    )
    if not leaderboard:
        return {}
    resp = {
        "game_type": "queens",
        "game_number": today_game_number,
        "leaderboard": [],
    }
    for entry in leaderboard:
        resp["leaderboard"].append(
            {
                "username": entry["username"],
                "score": entry["score"],
            }
        )
    return resp
