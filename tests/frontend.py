import tempfile
import unittest
import pytest
import os
from pathlib import PurePath
from application import create_app

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class TestLogin(unittest.TestCase):

    def test_signup(client):
        response = client.get("/signup")
        assert response.status_code == 200
 


if __name__ == '__main__':
    unittest.main()