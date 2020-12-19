""" Tests for database.py """
import pytest

from hypothesis import given
from hypothesis.strategies import datetimes, integers, text
from src.database import Database
from src.models import Project

INT8_RANGE = dict(min_value=-9223372036854775807, max_value=9223372036854775807)
PROJECT_HYPOTHESIS = dict(
    name=text(),
    client=text(),
    rate=integers(**INT8_RANGE),
    freq=integers(**INT8_RANGE),
    hours=integers(**INT8_RANGE),
)


@pytest.fixture
def db():
    return Database(development=True)


def test_intialization(db):
    """
    Tests that on creation a dataabase with projects and entries table is created
    """
    assert db.db.url == "sqlite:///data/development.db"

    assert db.projects == db.db.get_table("projects")
    assert db.entries == db.db.get_table("entries")
    assert db.db.get_table("projects").count() == 3
    assert db.db.get_table("entries").count() == 0


def test_get_project_names(db):
    """
    Asserts the get_project_names returns a list and that the length of the list matches the length entries
    """
    assert isinstance(db.get_project_names(), list)
    assert len(db.get_project_names()) == db.db.get_table("projects").count()
    for name in db.get_project_names():
        assert isinstance(name, str)


@given(**PROJECT_HYPOTHESIS)
def test_create_valid_project(db, name, client, rate, freq, hours):
    project_to_add = Project(
        id=None,
        project_name=name,
        client=client,
        rate=rate,
        monthly_frequency=freq,
        weekly_hour_allotment=hours,
    )
    result = db.add_project(project_to_add, return_value=False)
    assert isinstance(result, int)
    assert result != project_to_add.id


@given(name=text(), client=text())
def test_bad_int_raises_value_error(db, name, client):
    pass
