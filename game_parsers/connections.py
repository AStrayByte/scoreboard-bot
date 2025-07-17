import re
from orm.models import ConnectionsPlay
from tortoise.functions import Avg


async def parse_connections(
    text: str, username: str, no_db=False
) -> tuple[str, dict[str, str | int]]:
    """
    Extracts and formats Connections game information from a given text.
    Args:
        text (str): The input text containing Connections game information.
        username (str): The username of the player.
        no_db (bool): If True, does not save to the database.
    Returns:
        tuple[str, dict[str, str | int]]: A tuple containing a response string and a JSON-like
            dictionary with game details.
    Example:

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
        return (
            f"""Incomplete Connections game information found.
        Game number: {game_number}""",
            {},
        )

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
    won = all([green_found, yellow_found, blue_found, purple_found])
    if mistakes > 0 and not won:
        return f"Connections Game #{game_number} incomplete.", {}

    is_new = None
    if not no_db:
        obj, is_new = await ConnectionsPlay.update_or_create(
            username=username,
            game_number=game_number,
            defaults={
                "score": score,
                "purple_first": purple_first,
                "mistakes": mistakes,
                "won": won,
            },
        )

    resp_string = f"{'(UPDATING RECORD) ' if is_new is False else ''}Connections Game #{game_number} completed with score {score} @{username}."
    resp_json = {
        "game_type": "connections",
        "game_number": game_number,
        "score": score,
        "username": username,
    }
    return resp_string, resp_json


async def connections_stats():
    """
    Placeholder function for future Connections game statistics.
    Currently does nothing.
    """
    # Count of games played
    total_count = await ConnectionsPlay.all().count()
    # Count of wins
    win_count = await ConnectionsPlay.filter(won=True).count()
    lose_count = total_count - win_count
    # Average score

    result = await ConnectionsPlay.all().annotate(avg_score=Avg("score")).values("avg_score")
    average_score = result[0]["avg_score"] if result else None
    # Average mistakes
    result = await ConnectionsPlay.all().annotate(avg_mistakes=Avg("mistakes")).values("avg_mistakes")
    average_mistakes = result[0]["avg_mistakes"] if result else None

    average_score_by_username = await ConnectionsPlay.annotate(
        avg_score=Avg("score")
    ).group_by("username").values("username", "avg_score")

    average_mistakes_by_username = None
    total_games_by_username = None
    total_wins_by_username = None
    # Ave
    resp = f"""**Connections Game Stats**
Total Games Played: {total_count}
Total Wins: {win_count}
Total Losses: {lose_count}
Average Score: {average_score}
Average Mistakes: {average_mistakes}
Average Score by Username:
{average_score_by_username}
Average Mistakes by Username:
{average_mistakes_by_username}
Total Games by Username:
{total_games_by_username}
Total Wins by Username:
{total_wins_by_username}

"""
    return resp
