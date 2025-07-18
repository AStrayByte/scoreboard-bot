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
    score = total_seconds if flawless else total_seconds * 2  # Assuming a penalty for non-flawless games
    resp_string = f"Queens Game #{game_number} completed in {total_seconds} seconds by @{username}."
    if not flawless:
        resp_string += "\nPenalty: Score was doubled for non-flawless game."
    resp_json = {
        "game_type": "queens",
        "game_number": game_number,
        "score": score,
        "seconds": total_seconds,
        "flawless": flawless,
        "username": username
    }
    return resp_string, resp_json