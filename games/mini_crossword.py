import re
from games.base import Game
from orm.models import MiniCrosswordPlay
from datetime import date


class MiniCrosswordGame(Game):
    """
    MiniCrossword Game class for handling miniCrossword game logic.

    Example:
        I solved the 7/31/2025 New York Times Mini Crossword in 1:23! https://www.nytimes.com/crosswords/game/mini
    """

    start_date = date(2014, 8, 21)
    game_type = "miniCrossword"
    db_model = MiniCrosswordPlay
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
            "seconds": data["seconds"],
            "raw_text": data["raw_text"],
            "game_date": data["game_date"],
        }

    @classmethod
    def process_to_dict(cls, text: str) -> dict[str, str | int | bool]:
        """
        Processes the input text to extract game information.
        Args:
            text (str): The input text containing MiniCrossword game information.
        Returns:
            dict[str, str | int | bool]: A dictionary with the extracted game information.
        """
        regex = r"I solved the (?P<date>\d+/\d+/\d+) New York Times Mini Crossword in (?P<minutes>\d+):(?P<seconds>\d+)"
        match = re.search(regex, text)
        if not match:
            raise ValueError("Invalid MiniCrossword game format. Please check the input text.")

        game_date = match.group("date")
        minutes = match.group("minutes")
        seconds = match.group("seconds")
        if not all([game_date, minutes,seconds]):
            raise ValueError(
                "Missing required game information in the input text.\n/ \
game_date: {game_date}, Minutes: {minutes}, Seconds: {seconds}"
            )
        # convert date from "MM/DD/YYYY" date object
        if "/" in game_date:
            month, day, year = map(int, game_date.split("/"))
            game_date = date(year, month, day)
        else:
            raise ValueError("Invalid date format. Expected MM/DD/YYYY.")
        total_seconds = int(minutes) * 60 + int(seconds)
        score = total_seconds

        resp_json = {
            "game_type": "miniCrossword",
            "game_number": cls.date_to_game_number(game_date),
            "game_date": game_date,
            "score": score,
            "seconds": total_seconds,
            "raw_text": text,
        }
        return resp_json
