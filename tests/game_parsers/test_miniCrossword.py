#!python3
import datetime
import pytest

from games.mini_crossword import MiniCrosswordGame

@pytest.mark.asyncio
async def test_mini_crossword():
    text = "I solved the 7/31/2025 New York Times Mini Crossword in 1:23! https://www.nytimes.com/crosswords/game/mini"
    resp_string, resp_json = await MiniCrosswordGame.parse_text(text, "testuser")
    assert resp_json == {
        "game_type": "miniCrossword",
        "game_date": datetime.date(2025, 7, 31),
        "game_number": 3998,
        "score": 83,
        "username": "testuser",
        "raw_text": text,
        "seconds": 83,
    }

    assert resp_string == "Minicrossword Game #3998 completed with score 83 by testuser."
