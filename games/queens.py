from games.base import LinkedInSimpleTime
from orm.models import QueensPlay
from datetime import date


class QueensGame(LinkedInSimpleTime):
    """
    Queens Game class for handling queens game logic.

    Example:
        Queens #426 | 0:27 and flawless
        First 👑s: 🟩 🟦 ⬜
        🏅 I’m in the Top 25% of all players today!
        lnkd.in/queens
    """

    start_date = date(2024, 5, 1)
    game_type = "queens"
    db_model = QueensPlay
