import re
from games.base import Game
from orm.models import TangoPlay
from datetime import date


class TangoGame(Game):
    """
    Tango Game class for handling tango game logic.

    Example:
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

    start_date = date(2023, 11, 19)
    game_type = "tango"
    db_model = TangoPlay
    higher_score_first = False

    @classmethod
    def get_update_defaults(cls, data: dict[str, int | bool]) -> dict[str, int | bool]:
        return {
            "score": data["score"],
            "seconds": data["seconds"],
            "flawless": data["flawless"],
            "raw_text": data["raw_text"],
        }

    @classmethod
    def process_to_dict(cls, text: str) -> dict[str, str | int | bool]:
        """
        Processes the input text to extract game information.
        Args:
            text (str): The input text containing Tango game information.
        Returns:
            dict[str, str | int | bool]: A dictionary with the extracted game information.
        """
        regex = r"Tango\s+#(?P<game_number>\d+)\s*\|\s*(?P<minutes>\d+):(?P<seconds>\d+)"
        match = re.search(regex, text)
        if not match:
            raise ValueError("No Tango game information found.")

        game_number = match.group("game_number")
        minutes = match.group("minutes")
        seconds = match.group("seconds")
        if not game_number or not minutes or not seconds:
            raise ValueError(
                f"Incomplete Tango game information found.\n"
                f"Game number: {game_number}, Minutes: {minutes}, Seconds: {seconds}"
            )
        game_number = int(game_number)
        total_seconds = int(minutes) * 60 + int(seconds)
        resp_json = {
            "game_type": "tango",
            "game_number": game_number,
            "score": total_seconds,
            "seconds": total_seconds,
            "flawless": "and flawless" in text,
            "raw_text": text,
        }
        return resp_json


# IMPLEMENT TANGO IN MAIN.PY
# DO ZIP NEXT
# 3 MIGrate DB
