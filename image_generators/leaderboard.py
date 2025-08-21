from html import escape
import requests

# import BROWSERLESS_URL if not running pytest otherwise use mock
if "pytest" in __import__("sys").modules:
    BROWSERLESS_URL = "http://10.0.0.69:3000"
else:
    from secret import BROWSERLESS_URL


def generate_leaderboard_payload(games_data, viewport_width=1000, viewport_height=390):
    def get_rank_class(index):
        return ["gold", "silver", "bronze"][index] if index < 3 else "plain"

    board_count = len(games_data)
    single_column = board_count == 1
    grid_class = "grid single-column" if single_column else "grid"

    # Calculate height based on number of boards
    viewport_height = 360 * (board_count // 2 + board_count % 2)

    # Style + HTML head
    style = """
    <style>
    body {
        margin: 0;
        padding: 40px;
        background: linear-gradient(to bottom, #eaf0ff, #ffffff);
        font-family: 'Segoe UI', sans-serif;
        color: #222;
    }
    .grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 32px;
    }
    .grid.single-column {
        grid-template-columns: 1fr;
    }
    .game-block {
        background: #fff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    .game-title {
        font-size: 22px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 18px;
        color: #0041c4;
        letter-spacing: 0.5px;
    }
    .entry {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 12px;
        background: linear-gradient(to right, #f9f9f9, #f2f7ff);
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .entry:nth-child(2) {
        background: linear-gradient(to right, #e6f2ff, #ffffff);
    }
    .entry:nth-child(3) {
        background: linear-gradient(to right, #f3f3f3, #ffffff);
    }
    .entry:nth-child(4) {
        background: linear-gradient(to right, #f7f7f7, #ffffff);
    }
    .rank-circle {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ffcc00, #ff9900);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 0 6px rgba(0,0,0,0.15);
    }
    .rank-circle.silver {
        background: linear-gradient(135deg, #d8d8d8, #b0b0b0);
    }
    .rank-circle.bronze {
        background: linear-gradient(135deg, #cd7f32, #a64f00);
    }
    .rank-circle.plain {
        background: #ccc;
    }
    .name {
        font-size: 18px;
        font-weight: 700;
        margin-left: 12px;
        color: #222;
        flex-grow: 1;
    }
    .score {
        font-size: 18px;
        font-weight: bold;
        color: #0041c4;
        text-align: right;
        min-width: 70px;
    }
    </style>
    """

    # Build HTML content
    game_blocks = ""
    for game in games_data:
        if not game:
            continue
        title = escape(game["game_type"].capitalize())
        game_number = game.get("game_number")
        if game_number is not None:
            title += f" #{game_number}"

        entries_html = ""
        for idx, entry in enumerate(game["leaderboard"]):
            rank = idx + 1
            rank_class = get_rank_class(idx)
            entries_html += f"""
            <div class='entry'>
                <div class='rank-circle {rank_class}'>{rank}</div>
                <div class='name'>{escape(entry["username"])}</div>
                <div class='score'>{escape(str(entry["score"]))}</div>
            </div>
            """

        game_blocks += f"""
        <div class='game-block'>
            <div class='game-title'>{title}</div>
            {entries_html}
        </div>
        """

    html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'>{style}</head><body><div class='{grid_class}'>{game_blocks}</div></body></html>"

    return {
        "html": html,
        "viewport": {"width": viewport_width, "height": viewport_height},
        "options": {"type": "png", "fullPage": True},
    }


async def generate_leaderboard_image(games_data: list[dict]) -> bytes:
    """
    Generates a leaderboard image from the provided game data.

    Args:
        games_data (list[dict]): List of game data dictionaries containing leaderboard information.

    Returns:
        bytes: The generated image in PNG format.
    """
    payload = generate_leaderboard_payload(games_data)
    response = requests.post(
        f"{BROWSERLESS_URL}/screenshot",
        json=payload,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        raise Exception(f"Failed to generate image: {response.text}")

    return response.content
