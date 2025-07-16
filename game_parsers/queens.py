import re

def parse_queens(text: str, username: str) -> list[str, dict]:
    """
    Extracts and formats Queens game information from a given text.
    Args:
        text (str): The input text containing Queens game information.

    Queens #426 | 0:27 and flawless
    First 👑s: 🟩 🟦 ⬜ 
    🏅 I’m in the Top 25% of all players today!
    lnkd.in/queens
    """
    regex = r"Queens\s+#(?P<game_number>\d+)\s*\|\s*(?P<minutes>\d+):(?P<seconds>\d+)"
    match = re.search(regex, text)
    if not match:
        return "No Queens game information found."
    
    game_number = match.group("game_number")
    minutes = match.group("minutes")
    seconds = match.group("seconds")
    if not game_number or not minutes or not seconds:
        return f"""Incomplete Queens game information found.
        Game number: {game_number}, Minutes: {minutes}, Seconds: {seconds}"""
    total_seconds = int(minutes) * 60 + int(seconds)
    resp_string = f"Queens Game #{game_number} completed in {total_seconds} seconds by @{username}."
    resp_json = {
        "game_type": "queens",
        "game_number": game_number,
        "score": total_seconds,
        "username": username
    }
    return resp_string, resp_json