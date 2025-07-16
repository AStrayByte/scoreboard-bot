import re
BACKTRACKS_VALUE = 5
def parse_zip(text: str, username: str) -> list[str, dict]:
    """
    Extracts and formats Zip game information from a given text.
    Args:
        text (str): The input text containing Zip game information.
    
    Example:
        Zip #114 | 0:06 and flawless 🏁
        With no backtracks 🟢
        🏅 I’m in the Top 1% of all players today!
        lnkd.in/zip.

        Zip #109 | 0:08 🏁
        With 2 backtracks 🛑
        🏅 I’m in the Top 1% of all players today!
    """
    regex = r"Zip\s+#(?P<game_number>\d+)\s*\|\s*(?P<minutes>\d+):(?P<seconds>\d+)(?:.*?\n)?(?:With\s+(?:(?P<backtracks>\d+)|no)\s+backtracks)?"
    match = re.search(regex, text)
    if not match:
        return "No Zip game information found."
    game_number = match.group("game_number")
    minutes = match.group("minutes")
    seconds = match.group("seconds")
    backtracks = match.group("backtracks")
    if not game_number or not minutes or not seconds:
        return f"""Incomplete Zip game information found.
        Game number: {game_number}, Minutes: {minutes}, Seconds: {seconds}, Backtracks: {backtracks}"""
    total_seconds = int(minutes) * 60 + int(seconds)
    if backtracks is None:
        backtracks = "0"
    else:
        backtracks = int(backtracks)
    resp_string = f"Zip Game #{game_number} completed in {total_seconds} seconds with {backtracks} backtracks by @{username}."
    score = total_seconds + (backtracks * BACKTRACKS_VALUE)
    resp_json = {
        "game_type": "zip",
        "game_number": game_number,
        "score": score,
        "total_seconds": total_seconds,
        "backtracks": backtracks,
        "username": username
    }
    return resp_string, resp_json
    