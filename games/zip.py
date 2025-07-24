import re
from datetime import date

from games.base import Game
from orm.models import ZipPlay


class ZipGame(Game):
    """
    Zip Game class for handling Zip game logic.

    Example:
        Zip #114 | 0:06 and flawless 🏁
        With no backtracks 🟢
        🏅 I’m in the Top 1% of all players today!
        lnkd.in/zip.

        Zip #109 | 0:08 🏁
        With 2 backtracks 🛑
        🏅 I’m in the Top 1% of all players today!
    """

    start_date = date(2025, 3, 18)
    game_type = "zip"
    db_model = ZipPlay
    higher_score_first = False

    @classmethod
    def get_update_defaults(cls, data: dict[str, int | bool]) -> dict[str, int | bool]:
        """
        Returns the defaults for updating the game record.
        Args:
            data (dict[str, int | bool]): The data dictionary containing game information.
        Returns:
            dict[str, int | bool]: A dictionary with the defaults for updating the game record.
        """
        return {
            "score": data["score"],
            "seconds": data["total_seconds"],
            "backtracks": data["backtracks"],
            "flawless": data["flawless"],
            "raw_text": data["raw_text"],
        }

    @classmethod
    def process_to_dict(cls, text: str) -> dict[str, str | int | bool]:
        """
        Processes the input text to extract game information.
        Args:
            text (str): The input text containing Zip game information.
        Returns:
            dict[str, str | int | bool]: A dictionary with the extracted game information.
        """
        backtracks_value = 5  # Value assigned to each backtrack
        regex = r"Zip\s+#(?P<game_number>\d+)\s*\|\s*(?P<minutes>\d+):(?P<seconds>\d+)(?:.*?\n)?(?:With\s+(?:(?P<backtracks>\d+)|no)\s+backtracks)?"
        match = re.search(regex, text)
        if not match:
            raise ValueError("No Zip game information found.")
        game_number = match.group("game_number")
        minutes = match.group("minutes")
        seconds = match.group("seconds")
        backtracks = match.group("backtracks")
        if not game_number or not minutes or not seconds:
            raise ValueError(
                f"Incomplete Zip game information found.\n"
                f"Game number: {game_number}, Minutes: {minutes}, Seconds: {seconds}, Backtracks: {backtracks}"
            )
        game_number = int(game_number)
        total_seconds = int(minutes) * 60 + int(seconds)
        if backtracks is None:
            backtracks = 0
        else:
            backtracks = int(backtracks)
        score = total_seconds + (backtracks * backtracks_value)
        data = {
            "game_type": "zip",
            "game_number": game_number,
            "score": score,
            "total_seconds": total_seconds,
            "backtracks": backtracks,
            "flawless": "and flawless" in text,
            "raw_text": text,
        }
        return data
