#!python3
import unittest

from game_parsers.tango import parse_tango


class TestTango(unittest.TestCase):
    def test_tango(self):
        text = "Tango #275 | 0:25 and flawless\nFirst 5 placements:\n🟨🟨2️⃣1️⃣🟨🟨\n3️⃣🟨🟨5️⃣🟨4️⃣\n🟨🟨🟨🟨🟨🟨\n🟨🟨🟨🟨🟨🟨\n🟨🟨🟨🟨🟨🟨\n🟨🟨🟨🟨🟨🟨\n🏅 I’m in the Top 5% of all players today!\nlnkd.in/tango."
        resp_string, resp_json = parse_tango(text, "testuser")
        self.assertDictEqual(resp_json, {
            "game_type": "tango",
            "game_number": 275,
            "score": 25,
            "username": "testuser"
        })
        self.assertEqual(resp_string, "Tango Game #275 completed in 25 seconds by @testuser.")
