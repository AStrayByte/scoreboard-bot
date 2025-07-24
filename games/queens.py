import re
from games.base import Game
from orm.models import QueensPlay
from datetime import date


class QueensGame(Game):
    """
    Queens Game class for handling queens game logic.

    Example:
        Queens #426 | 0:27 and flawless
        First 👑s: 🟩 🟦 ⬜
        🏅 I’m in the Top 25% of all players today!
        lnkd.in/queens
    """

    start_date = date(2023, 6, 12)
    game_type = "queens"
    db_model = QueensPlay
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
            "time_taken": data["seconds"],
            "flawless": data["flawless"],
            "raw_text": data["raw_text"],
        }

    @classmethod
    def process_to_dict(cls, text: str) -> dict[str, str | int | bool]:
        """
        Processes the input text to extract game information.
        Args:
            text (str): The input text containing Queens game information.
        Returns:
            dict[str, str | int | bool]: A dictionary with the extracted game information.
        """
        regex = r"Queens\s+#(?P<game_number>\d+)\s*\|\s*(?P<minutes>\d+):(?P<seconds>\d+)\s(?P<flawless>and flawless)?"
        match = re.search(regex, text)
        if not match:
            raise ValueError("Invalid Queens game format. Please check the input text.")

        game_number = match.group("game_number")
        minutes = match.group("minutes")
        seconds = match.group("seconds")
        flawless = True if match.group("flawless") else False
        if not game_number or not minutes or not seconds:
            raise ValueError(
                "Missing required game information in the input text.\n/ \
Game number: {game_number}, Minutes: {minutes}, Seconds: {seconds}"
            )
        game_number = int(game_number)
        total_seconds = int(minutes) * 60 + int(seconds)
        score = (
            total_seconds if flawless else total_seconds * 2
        )  # Assuming a penalty for non-flawless games

        resp_json = {
            "game_type": "queens",
            "game_number": game_number,
            "score": score,
            "seconds": total_seconds,
            "flawless": flawless,
            "raw_text": text,
        }
        return resp_json
