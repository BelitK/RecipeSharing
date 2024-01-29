import pytest
from app import app, db, Recipe, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Recipe Sharing' in response.data

def test_add_recipe_route(client):
    response = client.post('/add_recipe', data={
        'title': 'test mojito',
        'username': 'test_user',
        'instructions': 'Test instructions',
        'ingredients': ['ingredient1', 'ingredient2'],
        'weight': ['100', '200']
    }, follow_redirects=True)
    assert response.status_code == 200

def test_show_recipe_route(client):
    response = client.get('/recipe/1'
    , follow_redirects=True)
    assert response.status_code == 200
    assert b'Publish date' in response.data

def test_search_route(client):
    response = client.get('/search',data={'search':'mojito'}
    , follow_redirects=True)
    assert response.status_code == 200
    print(response.text)
    assert 'mojito' in response.text