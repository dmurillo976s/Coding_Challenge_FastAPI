import pytest

from httpx import AsyncClient
from api.modules.database.mock_database_handler import MockErrorDBHandler
from api import app


# Override production database_handler dependency for mock error test interactions
@pytest.fixture(scope="module")
def configure_mock_error_dependency():
    app.app.dependency_overrides[app.database_dependency] = MockErrorDBHandler


@pytest.mark.asyncio
async def test_create_user_error(configure_mock_error_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/users", json={"id": "mock_id", "name": "my_name", "email": "my_email",
                                                 "password": "12345"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_user_error(configure_mock_error_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.put("/users/mock_id",
                                json={"name": "my_name", "email": "my_email", "password": "12345"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_team_error(configure_mock_error_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/teams",
                                 json={"id": "mock_id", "name": "my_name", "description": "my_description"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_team_error(configure_mock_error_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.put("/teams/mock_id", json={"name": "my_name", "description": "my_description"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_add_team_member_error(configure_mock_error_dependency):
    async with AsyncClient(app=app.app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/teams/mock_team_id/members", json={"user_id": "mock_user_id"})
    assert response.status_code == 400

