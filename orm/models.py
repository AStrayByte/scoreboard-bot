from tortoise import fields
from tortoise.models import Model


class Play(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=255)
    game_number = fields.IntField()
    score = fields.IntField()
    raw_text = fields.TextField()

    class Meta:
        abstract = True


class ConnectionsPlay(Play):
    purple_first = fields.BooleanField()
    mistakes = fields.IntField()
    won = fields.BooleanField()

    class Meta:
        table = "connections_play"
        default_connection = "default"


class QueensPlay(Play):
    seconds = fields.IntField()
    flawless = fields.BooleanField()

    class Meta:
        table = "queens_play"
        default_connection = "default"


class TangoPlay(Play):
    seconds = fields.IntField()
    flawless = fields.BooleanField()

    class Meta:
        table = "tango_play"
        default_connection = "default"


class ZipPlay(Play):
    seconds = fields.IntField()
    backtracks = fields.IntField()
    flawless = fields.BooleanField()

    class Meta:
        table = "zip_play"
        default_connection = "default"

class MiniCrosswordPlay(Play):
    game_date = fields.DateField()
    seconds = fields.IntField()


# class MiniCrossword(Play):
#     ...
#     # game_number somehow needs to be date as there is no game_number for MiniCrossword

#     class Meta:
#         table = "minicrossword_play"
#         default_connection = "default"

# Save a game instance
# Show leaderboard for day
# Show User Stats
#   - Total Games Played
#   - Per Game
#         - Total Games Played
#         - Total Win/loss

# Different games
# Connections - score, purples first
# Queens - time and flawless
# Tango - time
# Zip - time and backtracks
# MiniCrossword - time
