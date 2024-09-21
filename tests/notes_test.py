import pytest

from core.config import settings
from .conf_test import client

notes_urls = settings.notes

@pytest.mark.asyncio
async def test_create_note(client):
    response = await client.post(
        url=f'{notes_urls.prefix}{notes_urls.create}',
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
        url=f'{notes_urls.prefix}{notes_urls.create}',
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
    response = await client.get(
        url=f'{notes_urls.prefix}{notes_urls.get_all}',
        auth=("testuser", "testpassword")
    )

    assert response.status_code == 200
    notes = response.json()
    assert len(notes) == 2
    assert notes[0]["title"] == "Купить тестовое тесто"