from orm.models import ConnectionsPlay
from rich import print  # noqa: E402 F401
import pytest
from datetime import date
from games.connections import ConnectionsGame


@pytest.mark.asyncio
async def test_connections_perfect():
    await ConnectionsPlay.all().delete()
    text = "Connections\nPuzzle #736\n🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟩🟩🟩🟩\n🟨🟨🟨🟨"
    resp_string, resp_json = await ConnectionsGame.parse_text(text, "testuser", no_db=True)
    assert resp_json == {
        "game_type": "connections",
        "game_number": 736,
        "score": 100,
        "username": "testuser",
    }
    assert resp_string == "Connections Game #736 completed with score 100 @testuser."


@pytest.mark.asyncio
async def test_connections_scores():
    await ConnectionsPlay.all().delete()
    start = "Connections\nPuzzle #736\n"
    tests = [
        (f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟩🟩🟩🟩\n🟨🟨🟨🟨", 100),
        (f"{start}🟦🟦🟦🟦\n🟪🟪🟪🟪\n🟨🟨🟨🟨\n🟩🟩🟩🟩", 94),
        (f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟨\n🟩🟩🟩🟨\n🟩🟩🟩🟩", 94),
        (f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟩\n🟩🟩🟩🟨\n🟨🟨🟨🟨\n🟩🟩🟩🟩", 88),
        (f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟩\n🟨🟨🟨🟩\n🟨🟨🟨🟩\n🟩🟩🟩🟨\n", 53),
        (f"{start}🟨🟨🟨🟩\n🟨🟨🟨🟩\n🟨🟨🟨🟩\n🟩🟩🟩🟨\n", 0),
    ]
    for test_text, expected_score in tests:
        resp_string, resp_json = await ConnectionsGame.parse_text(test_text, "testuser", no_db=True)
        print(test_text)
        assert resp_json["score"] == expected_score


@pytest.mark.asyncio
async def test_incomplete_scores():
    ConnectionsPlay.all().delete()
    start = "Connections\nPuzzle #736\n"
    tests = [
        f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟨\n",
        f"{start}🟪🟪🟪🟪\n🟦🟦🟦🟦\ntest\n🟩🟩🟩🟨\n🟩🟩🟩🟩",
        f"{start}🟦🟦🟦🟦\n🟩🟩🟩🟨\n🟨🟨🟨🟨\n🟩🟩🟩🟩",
        f"{start}🟨🟨🟨🟩\n🟨🟨🟨🟩\n🟨🟨🟨🟩\n",
        f"{start}🟪🟪🟪🟪\n🟪🟪🟪🟪\n🟦🟦🟦🟦\n🟨🟨🟨🟨\n",
    ]
    for test_text in tests:
        resp_string, resp_json = await ConnectionsGame.parse_text(test_text, "testuser", no_db=True)
        assert resp_json == {}


# @pytest.mark.asyncio
# async def test_stats():
#     await ConnectionsPlay.all().delete()
#     con_game_objs = [
#         ConnectionsPlay(
#             game_number=1, username="user3", score=10, purple_first=True, mistakes=0, won=True
#         ),
#         ConnectionsPlay(
#             game_number=2, username="user3", score=0, purple_first=True, mistakes=0, won=True
#         ),
#         ConnectionsPlay(
#             game_number=3, username="user3", score=20, purple_first=True, mistakes=0, won=True
#         ),
#         ConnectionsPlay(
#             game_number=1, username="user1", score=100, purple_first=True, mistakes=0, won=True
#         ),
#         ConnectionsPlay(
#             game_number=2, username="user1", score=100, purple_first=True, mistakes=0, won=True
#         ),
#         ConnectionsPlay(
#             game_number=3, username="user1", score=100, purple_first=True, mistakes=0, won=True
#         ),
#         ConnectionsPlay(
#             game_number=1, username="user2", score=100, purple_first=True, mistakes=0, won=True
#         ),
#         ConnectionsPlay(
#             game_number=2, username="user2", score=0, purple_first=True, mistakes=0, won=True
#         ),
#         ConnectionsPlay(
#             game_number=3, username="user2", score=100, purple_first=True, mistakes=0, won=True
#         ),
#     ]
#     for obj in con_game_objs:
#         await obj.save()
#     stats = await connections_stats()
#     print(stats)

#     assert False


def test_connections_date_to_game_number():
    """
    Test the conversion of date to game number.
    """
    assert ConnectionsGame.date_to_game_number(date(2025, 7, 17)) == 767
    assert ConnectionsGame.date_to_game_number(date(2025, 5, 6)) == 695


@pytest.mark.asyncio
async def test_connections_daily_leaderboard():
    await ConnectionsPlay.all().delete()
    test_date = date(2025, 7, 20)
    todays_game_number = ConnectionsGame.date_to_game_number(test_date)
    con_game_objs = [
        ConnectionsPlay(
            game_number=todays_game_number,
            username="user3",
            score=100,
            purple_first=True,
            mistakes=0,
            won=True,
            raw_text="",
        ),
        ConnectionsPlay(
            game_number=todays_game_number,
            username="user1",
            score=90,
            purple_first=True,
            mistakes=0,
            won=True,
            raw_text="",
        ),
        ConnectionsPlay(
            game_number=todays_game_number,
            username="user2",
            score=80,
            purple_first=True,
            mistakes=0,
            won=True,
            raw_text="",
        ),
        ConnectionsPlay(
            game_number=todays_game_number - 1,
            username="user1",
            score=70,
            purple_first=True,
            mistakes=0,
            won=True,
            raw_text="",
        ),
        ConnectionsPlay(
            game_number=todays_game_number + 1,
            username="user2",
            score=60,
            purple_first=True,
            mistakes=0,
            won=True,
            raw_text="",
        ),
    ]
    for obj in con_game_objs:
        await obj.save()
    leaderboard = await ConnectionsGame.todays_data(override_date=test_date)
    assert leaderboard == {
        "game_type": "connections",
        "game_number": 770,
        "leaderboard": [
            {"username": "user3", "score": 100},
            {"username": "user1", "score": 90},
            {"username": "user2", "score": 80},
        ],
    }
