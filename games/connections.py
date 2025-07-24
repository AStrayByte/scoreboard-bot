import re
from games.base import Game
from datetime import date

from orm.models import ConnectionsPlay


class ConnectionsGame(Game):
    """
    Connections Game class for handling connections game logic.
    Inherits from Game base class.
    """

    start_date = date(2023, 6, 12)
    game_type = "connections"
    db_model = ConnectionsPlay
    higher_score_first = True

    @classmethod
    async def parse_text(
        cls, text: str, username: str, no_db=False
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
        game_number = int(match.group("game_number"))

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
        mistakes = 0
        for line in lines:
            if "🟨🟨🟨🟨" == line:
                if yellow_found:
                    print("Yellow already found, skipping this line.")
                    continue
                yellow_found = 5
            elif "🟩🟩🟩🟩" == line:
                if green_found:
                    print("Green already found, skipping this line.")
                    continue
                green_found = 10
                if not yellow_found:
                    green_found += 2  # bonus for green before yellow
            elif "🟦🟦🟦🟦" == line:
                if blue_found:
                    print("Blue already found, skipping this line.")
                    continue
                blue_found = 15
                if not yellow_found:
                    blue_found += 3  # bonus for blue before yellow
                if not green_found:
                    blue_found += 3  # bonus for blue before green
            elif "🟪🟪🟪🟪" == line:
                if purple_found:
                    print("Purple already found, skipping this line.")
                    continue
                purple_found = 20
                if not yellow_found:
                    purple_found += 4  # bonus for purple before yellow
                if not green_found:
                    purple_found += 4  # bonus for purple before green
                if not blue_found:
                    purple_found += 4  # bonus for purple before blue
                if not any([yellow_found, green_found, blue_found]):
                    purple_first = True
            else:
                mistakes += 1
        if mistakes > 4:
            print("Too many mistakes, setting to 4")
            mistakes = 4
        mistake_array = [0, 4, 10, 18, 30]
        mistake_penalty = 30 - mistake_array[mistakes]
        score = green_found + yellow_found + blue_found + purple_found + mistake_penalty
        won = all([green_found, yellow_found, blue_found, purple_found])
        if mistakes < 4 and not won:
            return f"Connections Game #{game_number} incomplete.", {}

        obj, is_new = await cls.update_or_create_game_record(
            username=username,
            game_number=game_number,
            defaults={
                "score": score,
                "purple_first": purple_first,
                "mistakes": mistakes,
                "won": won,
                "raw_text": text,
            },
            no_db=no_db,
        )

        resp_string = f"{'(UPDATING RECORD) ' if not is_new and not no_db else ''}Connections Game #{game_number} completed with score {score} @{username}."
        resp_json = {
            "game_type": "connections",
            "game_number": game_number,
            "score": score,
            "username": username,
        }
        return resp_string, resp_json
