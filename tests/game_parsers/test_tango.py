#!python3
import pytest

from games.tango import TangoGame

@pytest.mark.asyncio
async def test_tango():
    text = "Tango #275 | 0:25 and flawless\nFirst 5 placements:\n🟨🟨2️⃣1️⃣🟨🟨\n3️⃣🟨🟨5️⃣🟨4️⃣\n🟨🟨🟨🟨🟨🟨\n🟨🟨🟨🟨🟨🟨\n🟨🟨🟨🟨🟨🟨\n🟨🟨🟨🟨🟨🟨\n🏅 I’m in the Top 5% of all players today!\nlnkd.in/tango."
    resp_string, resp_json = await TangoGame.parse_text(text, "testuser")
    assert resp_json == {
        "game_type": "tango",
        "game_number": 275,
        "score": 25,
        "username": "testuser",
        "flawless": True,
        "raw_text": text,
        "seconds": 25,
    }

    assert resp_string == "Tango Game #275 completed with score 25 by testuser."
