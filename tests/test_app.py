import os

import app
import pytest
from mockupdb import MockupDB, OpMsg

from tests.mock_data import items


@pytest.fixture
def client():
    server = MockupDB(auto_ismaster=True)
    server.run()
    server.autoresponds(
        OpMsg("find", "todos"), cursor={"id": 0, "firstBatch": items.json_data}
    )
    mongo_uri = f"{server.uri}/test"

    # Create the new app.
    os.environ["SECRET_KEY"] = "SECRET_KEY"
    os.environ["LOGIN_DISABLED"] = "1"
    test_app = app.create_app(mongo_uri)
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get("/")
    html = str(response.data)

    assert "To Do" in html
    assert "Doing" in html
    assert "Done" in html
    assert "non existant task" not in html
    assert "Test 7" in html
    assert response.status == "200 OK"
