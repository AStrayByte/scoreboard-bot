import re
from datetime import date
from typing import Type

from orm.models import Play


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Game(metaclass=SingletonMeta):
    start_date: date = date(1997, 8, 29)
    game_type: str = "base"
    db_model: Type[Play]
    higher_score_first: bool = True

    @classmethod
    def get_update_defaults(cls, data: dict[str, int | bool]) -> dict[str, int | bool]:
        """
        Returns the defaults for updating the game record.
        Args:
            data (dict[str, int | bool]): The data dictionary containing game information.
        Returns:
            dict[str, int | bool]: A dictionary with the defaults for updating the game record.
        """
        raise NotImplementedError("This method should be implemented in subclasses.")

    @classmethod
    def date_to_game_number(cls, request_date: date) -> int:
        """
        Converts a date to a game number based on the game's start date.
        The game started on 2023-07-19, which is considered game number 1.
        """
        delta = request_date - cls.start_date
        return delta.days + 1

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

        """
        try:
            data = cls.process_to_dict(text)
        except ValueError as e:
            return str(e), {}

        data["username"] = username

        obj, is_new = await cls.update_or_create_game_record(
            username=username,
            game_number=data["game_number"],
            defaults=cls.get_update_defaults(data),
            no_db=no_db,
        )

        resp_string = f"{'(UPDATING RECORD) ' if not is_new and not no_db else ''}{cls.game_type.title()} Game #{data['game_number']} completed with score {data['score']} by {username}."

        return resp_string, data

    @classmethod
    async def _get_game_records(
        cls,
        game_number: int,
        high_score_first=True,
        values: list[str] = ["username", "score"],
        quantity: int = 10,
    ) -> list[dict[str, str | int]]:
        """
        Get all game records for a specific game number.
        """
        return (
            await cls.db_model.filter(game_number=game_number)
            .order_by("-score" if high_score_first else "score")[:quantity]
            .values(*values)
        )

    @classmethod
    async def todays_data(cls, override_date=None) -> dict:
        """
        Current day's leaderboard for Connections game.
        Show top 10 players by score.
        """
        my_date = override_date or date.today()
        today_game_number = cls.date_to_game_number(request_date=my_date)
        leaderboard = await cls._get_game_records(
            today_game_number, high_score_first=cls.higher_score_first, quantity=10
        )
        if not leaderboard:
            return {}
        resp = {
            "game_type": cls.game_type,
            "game_number": today_game_number,
            "leaderboard": [],
        }
        for entry in leaderboard:
            resp["leaderboard"].append(
                {
                    "username": entry["username"],
                    "score": entry["score"],
                }
            )
        return resp

    @classmethod
    async def update_or_create_game_record(
        cls, username: str, game_number: int, defaults: dict[str, str | int], no_db: bool = False
    ) -> tuple[(Play | None), bool]:
        """
        Update or create a game record in the database.
        Args:
            username (str): The username of the player.
            game_number (int): The game number.
            defaults (dict): Default values for the record.
        Returns:
            tuple[Type[Play], bool]: The created or updated record and a boolean indicating if it was newly created.
        """
        if no_db:
            return None, False
        obj, is_new = await cls.db_model.update_or_create(
            username=username, game_number=game_number, defaults=defaults
        )
        return obj, is_new


class LinkedInSimpleTime(Game, metaclass=SingletonMeta):
    """
    Simple Game class for handling simple time-based game logic.

    Games like Tango, Mini Sudoku, Queens, etc.

    Example:
        NameOfGame #114 | 0:06 and flawless 🏁
        With no backtracks 🟢
        🏅 I’m in the Top 1% of all players today!
        lnkd.in/nameofgame.

        NameOfGame #109 | 0:08 🏁
        With 2 backtracks 🛑
        🏅 I’m in the Top 1% of all players today!

    """

    # start_date = date(2025, 3, 18)
    # game_type = "simple_time"
    # db_model = None
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
        regex = rf"{cls.game_type.title()}\s+#(?P<game_number>\d+)\s*\|\s*(?P<minutes>\d+):(?P<seconds>\d+)"

        match = re.search(regex, text)
        if not match:
            raise ValueError(f"No {cls.game_type} game information found.")

        game_number = match.group("game_number")
        minutes = match.group("minutes")
        seconds = match.group("seconds")
        if not game_number or not minutes or not seconds:
            raise ValueError(
                f"Incomplete {cls.game_type.title()} game information found.\n"
                f"Game number: {game_number}, Minutes: {minutes}, Seconds: {seconds}"
            )
        game_number = int(game_number)
        total_seconds = int(minutes) * 60 + int(seconds)
        resp_json = {
            "game_type": cls.game_type.lower(),
            "game_number": game_number,
            "score": total_seconds,
            "seconds": total_seconds,
            "flawless": "and flawless" in text,
            "raw_text": text,
        }
        return resp_json
