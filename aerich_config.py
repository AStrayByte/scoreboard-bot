from secret import DB_URL

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["orm.models", "aerich.models"],  # Include aerich.models
            "default_connection": "default",
        },
    },
}
