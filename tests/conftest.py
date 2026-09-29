import uuid
import pytest_asyncio

from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.models.database import AsyncSessionLocal, engine
from app.main import app


@pytest_asyncio.fixture(autouse=True)
async def clean_wallets_table():
    async with engine.begin() as conn:
        await conn.exec_driver_sql("TRUNCATE TABLE wallets")
    yield

    await engine.dispose()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def wallet_id() -> uuid.UUID:
    wall_id = uuid.uuid4()
    async with AsyncSessionLocal() as session:
        await session.execute(
            text("INSERT INTO wallets (id, balance) VALUES (:id, :balance)"),
            {"id": str(wall_id), "balance": 0},
        )
        await session.commit()
    return wall_id






