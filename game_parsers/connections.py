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

    if not game_number:
        return f"""Incomplete Connections game information found.
        Game number: {game_number}"""

    lines = text.splitlines()
    lines = lines[lines.index(f"Connections\nPuzzle #{game_number}") + 1:]
    lines = [line.strip() for line in lines if line.strip()]
    # remove lines that contain anything except 4 of these 🟩🟨🟦🟪 in any order
    lines = [line for line in lines if re.match(r"^[🟩🟨🟦🟪]{4}$", line)]
    if not lines:
        return f"No valid Connections game lines found for game number {game_number}."
    green_found = 0
    yellow_found = 0
    blue_found = 0
    purple_found = 0
    purple_first = False
    mistakes = 0
    for line in lines:
        if "🟩🟩🟩🟩" == line:
            green_found = 15
        elif "🟨🟨🟨🟨" == line:
            yellow_found = 20
        elif "🟦🟦🟦🟦" == line:
            blue_found = 25
        elif "🟪🟪🟪🟪" == line:
            purple_found = 30
            if not(yellow_found or blue_found or green_found):
                purple_first = True
        else:
            mistakes += 1
    score = green_found + yellow_found + blue_found + purple_found - (15 * mistakes) + purple_first



    resp_string = f"Connections Game #{game_number} completed @{username}."
    resp_json = {
        "game_type": "connections",
        "game_number": game_number,
        "score": score,
        "username": username
    }
    return resp_string, resp_json
