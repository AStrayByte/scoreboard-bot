from datetime import date

from games.base import LinkedInSimpleTime
from orm.models import MiniSudokuPlay


class MiniSudokuGame(LinkedInSimpleTime):
    """
    Mini Sudoku Game class for handling mini sudoku game logic.

    Example:
        Mini Sudoku #10 | 10:45  ✏️

        🏅 I’m on a 2-day win streak!

        The classic game, made mini. Handcrafted by the originators of “Sudoku.”

        lnkd.in/minisudoku.
        Mini Sudoku
        Mini Sudoku, a puzzle by LinkedIn.
    """

    start_date = date(2025, 8, 12)
    game_type = "mini sudoku"
    db_model = MiniSudokuPlay
    higher_score_first = False
