import pytest

from core.config import settings
from .conf_test import client

user_urls = settings.user

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        url=f'{user_urls.prefix}{user_urls.create}',
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_register_existing_user(client):
    response = await client.post(
        url=f'{user_urls.prefix}{user_urls.create}',
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

