import pytest

from app.airports.models import Airport
from app import create_app, db


@pytest.fixture(scope='module')
def test_client():
    app = create_app(settings_module='config.testing')
    testing_client = app.test_client()

    with app.app_context():
        db.create_all()

        yield testing_client
        db.session.remove()
        db.drop_all()


@pytest.fixture
def airport():
    app = create_app(settings_module='config.testing')
    with app.app_context():
        yield Airport
