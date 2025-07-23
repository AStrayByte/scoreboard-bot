from image_generators.leaderboard import generate_leaderboard_payload, generate_leaderboard_image

# from orm.models import ConnectionsPlay
from rich import print  # noqa: E402 F401
import pytest
# from datetime import date
import vcr


@pytest.mark.asyncio
async def test_image():
    games = [
        {
            "game_type": "connections",
            "game_number": 770,
            "leaderboard": [
                {"username": "meg", "score": 99},
                {"username": "user1", "score": 90},
                {"username": "user2", "score": 80},
                {"username": "user5", "score": 80},
                {"username": "user6", "score": 80},
                {"username": "user7", "score": 80},
            ],
        },
        {
            "game_type": "wordle",
            "game_number": 120,
            "leaderboard": [
                {"username": "alice", "score": 6},
                {"username": "bob", "score": 5},
                {"username": "carol", "score": 4},
            ],
        },
        {
            "game_type": "wordle2",
            "game_number": 120,
            "leaderboard": [
                {"username": "alice", "score": 6},
                {"username": "bob", "score": 5},
                {"username": "carol", "score": 4},
            ],
        },
    ]

    with vcr.use_cassette("tests/cassettes/test_leaderboard.yaml"):
        image = await generate_leaderboard_image(games)
    # Save the image to a file for verification
    with open("test_leaderboard_image.png", "wb") as f:
        f.write(image)
    print("Image generated and saved as test_leaderboard_image.png")
