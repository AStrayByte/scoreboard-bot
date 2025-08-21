from datetime import date

from games.base import LinkedInSimpleTime
from orm.models import CrossClimbPlay


class CrossClimbGame(LinkedInSimpleTime):
    """
    CrossClimb Game class for handling crossclimb game logic.

    Example:
        Crossclimb #478 | 0:57 and flawless
        Fill order: 1️⃣ 3️⃣ 4️⃣ 5️⃣ 2️⃣ ⬆️ ⬇️ 🪜
        🏅 I’m in the Top 10% of all players today!
        lnkd.in/crossclimb.
    """

    start_date = date(2024, 5, 1)
    game_type = "crossclimb"
    db_model = CrossClimbPlay
    higher_score_first = False
