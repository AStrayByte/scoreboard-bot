#!python3
import unittest

from game_parsers.queens import parse_queens


class TestQueens(unittest.TestCase):
    def test_queens_flawless(self):
        text = "Queens #426 | 0:27 and flawless\nFirst 👑s: 🟩 🟦 ⬜ \n🏅 I’m in the Top 25% of all players today!\nlnkd.in/queens"
        resp_string, resp_json = parse_queens(text, "testuser")
        self.assertEqual(resp_json, {
            "game_type": "queens",
            "game_number": 426,
            "score": 27,
            "seconds": 27,
            "flawless": True,
            "username": "testuser"
        })
        self.assertEqual(resp_string, "Queens Game #426 completed in 27 seconds by @testuser.")

    def test_queens_flawless(self):
        text = "Queens #426 | 1:00\nFirst 👑s: 🟩 🟦 ⬜ \n🏅 I’m in the Top 25% of all players today!\nlnkd.in/queens"
        resp_string, resp_json = parse_queens(text, "testuser")
        self.assertEqual(resp_json, {
            "game_type": "queens",
            "game_number": 426,
            "score": 120,
            "seconds": 60,
            "flawless": False,
            "username": "testuser"
        })
        self.assertEqual(resp_string, "Queens Game #426 completed in 60 seconds by @testuser.\nPenalty: Score was doubled for non-flawless game.")
