import os

import pytest

# Local test database
os.environ["DATABASE_URL"] = "mysql+pymysql://root:Laxmi@localhost:3307/jobportal"

from app import create_app


@pytest.fixture
def client():
    app = create_app()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client