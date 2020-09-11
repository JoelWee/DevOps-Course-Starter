import pytest
from dotenv import load_dotenv

import app
from tests.mock_trello_requests import cards, lists


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version file_path = find_dotenv('.env.test')
    load_dotenv(".env.test", override=True)
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


def test_index_page(requests_mock, client):
    requests_mock.get("https://api.trello.com/1/boards/id/lists", json=lists.json)
    requests_mock.get("https://api.trello.com/1/boards/id/cards", json=cards.json)
    response = client.get("/")
    html = str(response.data)

    assert "To Do" in html
    assert "Doing" in html
    assert "Done" in html
    assert "non existant task" not in html
    assert "Test 7" in html
    assert response.status == "200 OK"
