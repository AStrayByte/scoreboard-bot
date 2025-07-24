import re
from games.base import Game
from datetime import date

from orm.models import ConnectionsPlay


class ConnectionsGame(Game):
    """
    Connections Game class for handling connections game logic.
    Inherits from Game base class.
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

    start_date = date(2023, 6, 12)
    game_type = "connections"
    db_model = ConnectionsPlay
    higher_score_first = True

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
            "purple_first": data["purple_first"],
            "mistakes": data["mistakes"],
            "won": data["won"],
            "raw_text": data["raw_text"],
        }

    @classmethod
    def process_to_dict(cls, text: str) -> dict[str, int | bool]:
        """
        Process the given text and extract relevant information into a dictionary.
        This method also calculates the score based on the game rules.
        Args:
            text (str): The input text containing game information.
        Returns:
            dict[str, int | bool]: A dictionary containing the game score and other relevant data.
        """
        regex = r"Connections\s+Puzzle\s+#(?P<game_number>\d+)\s*"
        match = re.search(regex, text)
        if not match:
            raise ValueError("Game number not found in the text.")
        game_number = int(match.group("game_number"))
        lines = text.splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        # remove lines that contain anything except 4 of these 🟩🟨🟦🟪 in any order
        lines = [line for line in lines if re.match(r"^[🟩🟨🟦🟪]{4}$", line)]
        if not lines:
            raise ValueError("No valid game lines found in the text.")
        green_found = 0
        yellow_found = 0
        blue_found = 0
        purple_found = 0
        purple_first = False
        mistakes = 0
        for line in lines:
            if "🟨🟨🟨🟨" == line:
                if yellow_found:
                    raise ValueError("Yellow already found, invalid game.")
                yellow_found = 5
            elif "🟩🟩🟩🟩" == line:
                if green_found:
                    raise ValueError("Green already found, invalid game.")
                green_found = 10
                if not yellow_found:
                    green_found += 2  # bonus for green before yellow
            elif "🟦🟦🟦🟦" == line:
                if blue_found:
                    raise ValueError("Blue already found, invalid game.")
                blue_found = 15
                if not yellow_found:
                    blue_found += 3  # bonus for blue before yellow
                if not green_found:
                    blue_found += 3  # bonus for blue before green
            elif "🟪🟪🟪🟪" == line:
                if purple_found:
                    raise ValueError("Purple already found, invalid game.")
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
            raise ValueError("Too many mistakes, invalid game.")
        mistake_array = [0, 4, 10, 18, 30]
        mistake_penalty = 30 - mistake_array[mistakes]
        score = green_found + yellow_found + blue_found + purple_found + mistake_penalty
        won = all([green_found, yellow_found, blue_found, purple_found])
        if mistakes < 4 and not won:
            raise ValueError(f"Game not complete. Mistakes: {mistakes}, Won: {won}, invalid game.")

        return {
            "game_type": cls.game_type,
            "game_number": game_number,
            "score": score,
            "purple_first": purple_first,
            "mistakes": mistakes,
            "won": won,
            "username": "",
            "raw_text": text,
        }
