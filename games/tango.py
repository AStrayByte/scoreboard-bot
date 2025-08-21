from datetime import date

from games.base import LinkedInSimpleTime
from orm.models import TangoPlay


class TangoGame(LinkedInSimpleTime):
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

    start_date = date(2024, 10, 8)
    game_type = "tango"
    db_model = TangoPlay
    higher_score_first = False
