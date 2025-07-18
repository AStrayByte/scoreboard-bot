#!python3
import unittest

from game_parsers.zip import parse_zip


class TestZip(unittest.TestCase):
    def test_zip_no_backtracks(self):
        text = "Zip #114 | 3:06 and flawless 🏁\nWith no backtracks 🟢\n🏅 I’m in the Top 1% of all players today!\nlnkd.in/zip."
        resp_string, resp_json = parse_zip(text, "testuser")
        self.assertDictEqual(resp_json, {
        "game_type": "zip",
        "game_number": 114,
        "score": 186,
        "total_seconds": 186,
        "backtracks": 0,
        "username": "testuser"
    })
        self.assertEqual(resp_string, "Zip Game #114 completed in 186 seconds with 0 backtracks by @testuser.")

    def test_zip_with_backtracks(self):
        text = "Zip #109 | 0:08 🏁\nWith 2 backtracks 🛑\n🏅 I’m in the Top 1% of all players today!"
        resp_string, resp_json = parse_zip(text, "testuser")
        self.assertDictEqual(resp_json, {
            "game_type": "zip",
            "game_number": 109,
            "score": 18,
            "total_seconds": 8,
            "backtracks": 2,
            "username": "testuser"
        })
        self.assertEqual(resp_string, "Zip Game #109 completed in 8 seconds with 2 backtracks by @testuser.")


