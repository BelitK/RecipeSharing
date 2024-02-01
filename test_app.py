import pytest
from app import app
from environs import Env


env = Env()
env.read_env()

Secret = env("SECRET")

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Recipe Sharing" in response.data


def test_add_delete_recipe_route(client):
    test_data={
            "title": "test mojito",
            "username": "test_user",
            "instructions": "Test instructions",
            "ingredients": ["ingredient1", "ingredient2"],
            "weight": ["100", "200"],
        }
    response = client.post(
        "/add_recipe",
        data=test_data,
        follow_redirects=False,
    )
    assert response.status_code == 302
    id = response.location.split('/')[-1]
    response = client.get(response.location, follow_redirects=True)
    assert test_data['title'] in response.text
    response = client.get(f"/delete/{id}/secret={Secret}",follow_redirects=True)
    assert response.status_code in [200,404]



def test_show_recipe_route(client):
    response = client.get("/recipe/1", follow_redirects=True)
    assert response.status_code in [200, 404]
    assert b"Publish date" in response.data or b"404" in response.data


def test_search_route(client):
    response = client.get("/search", data={"search": "mojito"}, follow_redirects=True)
    assert response.status_code == 200
    print(response.text)
    assert "mojito" in response.text
