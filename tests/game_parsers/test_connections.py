from game_parsers.connections import parse_connections
from rich import print  # noqa: E402 F401
import pytest


@pytest.mark.asyncio
async def test_connections_perfect():
    text = "Connections\nPuzzle #736\n🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟨\n🟩🟩🟩🟩"
    resp_string, resp_json = await parse_connections(text, "testuser", no_db=True)
    assert resp_json == {
        "game_type": "connections",
        "game_number": "736",
        "score": 100,
        "username": "testuser",
    }
    assert resp_string == "Connections Game #736 completed with score 100 @testuser."


@pytest.mark.asyncio
async def test_connections_scores():
    start = "Connections\nPuzzle #736\n"
    tests = [
        (f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟨\n🟩🟩🟩🟩", 100),
        (f"{start}🟦🟦🟦🟦\n🟪🟪🟪🟪\n🟨🟨🟨🟨\n🟩🟩🟩🟩", 90),
        (f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟨\n🟩🟩🟩🟨\n🟩🟩🟩🟩", 90),
        (f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟩\n🟩🟩🟩🟨\n🟨🟨🟨🟨\n🟩🟩🟩🟩", 80),
        (f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟩\n🟨🟨🟨🟩\n🟨🟨🟨🟩\n🟩🟩🟩🟨\n", 45),
        (f"{start}🟨🟨🟨🟩\n🟨🟨🟨🟩\n🟨🟨🟨🟩\n🟩🟩🟩🟨\n", 0),
    ]
    for test_text, expected_score in tests:
        resp_string, resp_json = await parse_connections(test_text, "testuser", no_db=True)
        assert resp_json["score"] == expected_score


@pytest.mark.asyncio
async def test_incomplete_scores():
    start = "Connections\nPuzzle #736\n"
    tests = [
        f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟨\n",
        f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\ntest\n🟩🟩🟩🟨\n🟩🟩🟩🟩",
        f"{start}🟦🟦🟦🟦\n🟩🟩🟩🟨\n🟨🟨🟨🟨\n🟩🟩🟩🟩",
        f"{start}🟨🟨🟨🟩\n🟨🟨🟨🟩\n🟨🟨🟨🟩\n",
    ]
    for test_text in tests:
        resp_string, resp_json = await parse_connections(test_text, "testuser", no_db=True)
        assert resp_json == {}
