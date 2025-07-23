from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "connections_play" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "game_number" INT NOT NULL,
    "score" INT NOT NULL,
    "raw_text" TEXT NOT NULL,
    "purple_first" INT NOT NULL,
    "mistakes" INT NOT NULL,
    "won" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "queens_play" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "game_number" INT NOT NULL,
    "score" INT NOT NULL,
    "raw_text" TEXT NOT NULL,
    "time_taken" INT NOT NULL,
    "flawless" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
