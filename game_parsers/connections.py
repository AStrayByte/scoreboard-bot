import re

def parse_connections(text: str, username: str) -> list[str, dict]:
    """
    Extracts and formats Connections game information from a given text.
    Args:
        text (str): The input text containing Connections game information.

    Connections
    Puzzle #736
    🟪🟪🟪🟪
    🟦🟦🟦🟦
    🟨🟨🟨🟨
    🟩🟩🟩🟩

    Connections
    Puzzle #750
    🟨🟨🟨🟨
    🟩🟩🟩🟩
    🟪🟦🟦🟦
    🟦🟦🟪🟦
    🟦🟦🟦🟦
    🟪🟪🟪🟪

    Connections
    Puzzle #704
    🟨🟪🟨🟩
    🟩🟩🟩🟩
    🟨🟨🟨🟨
    🟪🟦🟪🟦
    🟦🟪🟪🟦
    🟦🟦🟦🟪        

    """
    regex = r"Connections\s+#(?P<game_number>\d+)\s*\|\s*(?P<minutes>\d+):(?P<seconds>\d+)"
    match = re.search(regex, text)
    if not match:
        return "No Connections game information found."
    
    game_number = match.group("game_number")
    minutes = match.group("minutes")
    seconds = match.group("seconds")
    if not game_number or not minutes or not seconds:
        return f"""Incomplete Connections game information found.
        Game number: {game_number}, Minutes: {minutes}, Seconds: {seconds}"""
    total_seconds = int(minutes) * 60 + int(seconds)
    resp_string = f"Connections Game #{game_number} completed in {total_seconds} seconds by @{username}."
    resp_json = {
        "game_type": "connections",
        "game_number": game_number,
        "score": total_seconds,
        "username": username
    }
    return resp_string, resp_json
