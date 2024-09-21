import pytest
from .conf_test import client

@pytest.mark.asyncio
async def test_create_note(client):
    response = await client.post(
        "/notes/create",
        auth=("testuser", "testpassword"),
        json={
            "title": "Купить тестовое тесто",
            "description": "У тестировщика"
        })
    assert response.status_code == 200
    assert response.json()["title"] == "Купить тестовое тесто"
    assert response.json()["description"] == "У тестировщика"

@pytest.mark.asyncio
async def test_create_note_wrong_words(client):
    response = await client.post(
        "/notes/create",
        auth=("testuser", "testpassword"),
        json={
            "title": "Кпуить тсетовое тсето еще",
            "description": "У тсетировщика"
        })
    assert response.status_code == 200
    assert response.json()["title"] == "Купить тестовое тесто еще"
    assert response.json()["description"] == "У тестировщика"

@pytest.mark.asyncio
async def test_get_all_notes(client):
    await client.post(
        "/notes/create",
        auth=("testuser", "testpassword"),
        json={
            "title": "Больше теста",
            "description": "У того же тестировщика"
        })

    response = await client.get("/notes/get_all", auth=("testuser", "testpassword"))

    assert response.status_code == 200
    notes = response.json()
    assert len(notes) == 3
    assert notes[0]["title"] == "Купить тестовое тесто"