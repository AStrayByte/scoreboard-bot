#!python3

from games.queens import parse_queens

import pytest


@pytest.mark.asyncio
async def test_queens_flawless():
    text = "Queens #426 | 0:27 and flawless\nFirst 👑s: 🟩 🟦 ⬜ \n🏅 I’m in the Top 25% of all players today!\nlnkd.in/queens"
    resp_string, resp_json = await parse_queens(text, "testuser", no_db=True)
    assert resp_json == {
        "game_type": "queens",
        "game_number": 426,
        "score": 27,
        "seconds": 27,
        "flawless": True,
        "username": "testuser",
    }
    assert resp_string == "Queens Game #426 completed with score 27 by testuser."


@pytest.mark.asyncio
async def test_queens_not_flawless():
    text = "Queens #426 | 1:00\nFirst 👑s: 🟩 🟦 ⬜ \n🏅 I’m in the Top 25% of all players today!\nlnkd.in/queens"
    resp_string, resp_json = await parse_queens(text, "testuser", no_db=True)
    assert resp_json == {
        "game_type": "queens",
        "game_number": 426,
        "score": 120,
        "seconds": 60,
        "flawless": False,
        "username": "testuser",
    }
    assert (
        resp_string
        == "Queens Game #426 completed with score 120 by testuser.\nPenalty: Score was doubled for non-flawless game."
    )
