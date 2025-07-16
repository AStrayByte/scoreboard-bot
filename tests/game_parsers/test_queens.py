#!python3
import unittest

from game_parsers.queens import parse_queens


class TestQueens(unittest.TestCase):
    def test_queens_1(self):
        text = "Queens #426 | 0:27 and flawless\nFirst 👑s: 🟩 🟦 ⬜ \n🏅 I’m in the Top 25% of all players today!\nlnkd.in/queens"
        resp_string, resp_json = parse_queens(text, "testuser")
        self.assertEqual(resp_json, {
            "game_type": "queens",
            "game_number": "426",
            "score": 27,
            "username": "testuser"
        })
        self.assertEqual(resp_string, "Queens Game #426 completed in 27 seconds by @testuser.")


if __name__ == "__main__":
    unittest.main()
