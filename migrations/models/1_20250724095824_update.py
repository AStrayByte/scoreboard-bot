from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "queens_play" RENAME COLUMN "time_taken" TO "seconds";
        CREATE TABLE IF NOT EXISTS "tango_play" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "game_number" INT NOT NULL,
    "score" INT NOT NULL,
    "raw_text" TEXT NOT NULL,
    "seconds" INT NOT NULL,
    "flawless" INT NOT NULL
);
        CREATE TABLE IF NOT EXISTS "zip_play" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "game_number" INT NOT NULL,
    "score" INT NOT NULL,
    "raw_text" TEXT NOT NULL,
    "seconds" INT NOT NULL,
    "backtracks" INT NOT NULL,
    "flawless" INT NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "queens_play" RENAME COLUMN "seconds" TO "time_taken";
        DROP TABLE IF EXISTS "zip_play";
        DROP TABLE IF EXISTS "tango_play";"""
