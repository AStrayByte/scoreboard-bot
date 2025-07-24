#!python3
import pytest

from games.zip import ZipGame

@pytest.mark.asyncio
async def test_zip_no_backtracks():
    text = "Zip #114 | 3:06 and flawless 🏁\nWith no backtracks 🟢\n🏅 I’m in the Top 1% of all players today!\nlnkd.in/zip."
    resp_string, resp_json = await ZipGame.parse_text(text, "testuser")
    assert resp_json == {
        "game_type": "zip",
        "game_number": 114,
        "score": 186,
        "backtracks": 0,
        "username": "testuser",
        "flawless": True,
        "raw_text": text,
        "total_seconds": 186,
    }

    assert resp_string == "Zip Game #114 completed with score 186 by testuser."


@pytest.mark.asyncio
async def test_zip_with_backtracks():
    text = "Zip #109 | 0:08 🏁\nWith 2 backtracks 🛑\n🏅 I’m in the Top 1% of all players today!"
    resp_string, resp_json = await ZipGame.parse_text(text, "testuser")
    assert resp_json == {
        "game_type": "zip",
        "game_number": 109,
        "score": 18,
        "total_seconds": 8,
        "backtracks": 2,
        "username": "testuser",
        "flawless": False,
        "raw_text": text,
    }

    assert resp_string == "Zip Game #109 completed with score 18 by testuser."


