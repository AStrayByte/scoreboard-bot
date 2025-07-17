#!python3
import unittest

from game_parsers.connections import parse_connections
from rich import print

class TestConnections(unittest.TestCase):
    def test_connections_perfect(self):
        text = "Connections\nPuzzle #736\n🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟨\n🟩🟩🟩🟩"
        x = parse_connections(text, "testuser")
        print(x)
        resp_string, resp_json = parse_connections(text, "testuser")
        self.assertEqual(resp_json, {
            "game_type": "connections",
            "game_number": "736",
            "score": 100,
            "username": "testuser"
        })
        self.assertEqual(resp_string, f"Connections Game #736 completed with score 100 @testuser.")


