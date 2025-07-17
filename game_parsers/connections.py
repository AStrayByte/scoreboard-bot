import re


def parse_connections(text: str, username: str) -> tuple[str, dict[str, str | int]]:
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
    regex = r"Connections\s+Puzzle\s+#(?P<game_number>\d+)\s*"
    match = re.search(regex, text)
    if not match:
        return "No Connections game information found.", {}
    game_number = match.group("game_number")

    if not game_number:
        return f"""Incomplete Connections game information found.
        Game number: {game_number}""", {}

    lines = text.splitlines()
    # lines = lines[lines.index(f"Puzzle #{game_number}") + 1:]
    lines = [line.strip() for line in lines if line.strip()]
    # remove lines that contain anything except 4 of these 🟩🟨🟦🟪 in any order
    lines = [line for line in lines if re.match(r"^[🟩🟨🟦🟪]{4}$", line)]
    if not lines:
        return f"No valid Connections game lines found for game number {game_number}.", {}
    green_found = 0
    yellow_found = 0
    blue_found = 0
    purple_found = 0
    purple_first = False
    mistakes = 40
    for line in lines:
        if "🟩🟩🟩🟩" == line:
            green_found = 5
        elif "🟨🟨🟨🟨" == line:
            yellow_found = 10
        elif "🟦🟦🟦🟦" == line:
            blue_found = 15
        elif "🟪🟪🟪🟪" == line:
            purple_found = 20
            if not (yellow_found or blue_found or green_found):
                purple_first = 10
        else:
            mistakes -= 10
    score = green_found + yellow_found + blue_found + purple_found + mistakes + purple_first

    if mistakes > 0 and not all([green_found, yellow_found, blue_found, purple_found]):
        return f"Connections Game #{game_number} incomplete.", {}

    resp_string = f"Connections Game #{game_number} completed with score 100 @{username}."
    resp_json = {
        "game_type": "connections",
        "game_number": game_number,
        "score": score,
        "username": username,
    }
    return resp_string, resp_json
