import pytest_asyncio
from tortoise import Tortoise


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_tortoise():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["orm.models"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
