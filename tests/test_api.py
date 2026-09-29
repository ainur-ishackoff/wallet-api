import asyncio
import pytest

pytestmark = pytest.mark.asyncio


async def test_get_wallet_balance_ok(client, wallet_id):
    response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["wallet_uuid"] == str(wallet_id)
    assert data["balance"] == 0


async def test_get_wallet_balance_404(client):
    resp = await client.get("/api/v1/wallets/11111111-1111-1111-1111-111111111111")
    assert resp.status_code == 404


async def test_deposit_increases_balance(client, wallet_id):
    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000}
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 1000


async def test_withdraw_decreases_balance(client, wallet_id):
    await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000}
    )

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 400}
    )

    assert response.status_code == 200
    assert response.json()["balance"] == 600


async def test_withdraw_insufficient_funds_returns_409(client, wallet_id):
    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 10000}
    )
    assert response.status_code == 409


async def test_concurrent_withdraw_is_atomic(client, wallet_id):
    await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000}
    )

    async def withdraw_700():
        return await client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "WITHDRAW", "amount": 700},
        )
    response1, response2 = await asyncio.gather(withdraw_700(), withdraw_700())
    statuses = sorted([response1.status_code, response2.status_code])
    assert statuses == [200, 409]

    final_response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert final_response.status_code == 200
    assert final_response.json()["balance"] == 300