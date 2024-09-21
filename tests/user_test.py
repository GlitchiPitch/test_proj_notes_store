import pytest
from .conf_test import client


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/user/register", json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_register_existing_user(client):
    response = await client.post(
        "/user/register", json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

