import re

def parse_tango(text: str, username: str) -> list[str, dict]:
    """
    Extracts and formats Tango game information from a given text.
    Args:
        text (str): The input text containing Tango game information.

    Tango #275 | 0:25 and flawless
    First 5 placements:
    🟨🟨2️⃣1️⃣🟨🟨
    3️⃣🟨🟨5️⃣🟨4️⃣
    🟨🟨🟨🟨🟨🟨
    🟨🟨🟨🟨🟨🟨
    🟨🟨🟨🟨🟨🟨
    🟨🟨🟨🟨🟨🟨
    🏅 I’m in the Top 5% of all players today!
    lnkd.in/tango.
    
    """
    regex = r"Tango\s+#(?P<game_number>\d+)\s*\|\s*(?P<minutes>\d+):(?P<seconds>\d+)"
    match = re.search(regex, text)
    if not match:
        return "No Tango game information found."
    
    game_number = match.group("game_number")
    minutes = match.group("minutes")
    seconds = match.group("seconds")
    if not game_number or not minutes or not seconds:
        return f"""Incomplete Tango game information found.
        Game number: {game_number}, Minutes: {minutes}, Seconds: {seconds}"""
    total_seconds = int(minutes) * 60 + int(seconds)
    resp_string = f"Tango Game #{game_number} completed in {total_seconds} seconds by @{username}."
    resp_json = {
        "game_type": "tango",
        "game_number": game_number,
        "score": total_seconds,
        "username": username
    }
    return resp_string, resp_json