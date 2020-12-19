""" Tests for database.py """
import datetime

import pytest
from hypothesis import assume, given
from hypothesis.strategies import (
    builds,
    composite,
    data,
    datetimes,
    integers,
    none,
    text,
)

from src.database import Database
from src.models import Entry, Project

INT8_RANGE = dict(min_value=-9223372036854775807, max_value=9223372036854775807)
PROJECT_HYPOTHESIS = dict(
    id=none(),
    rate=integers(**INT8_RANGE),
    monthly_frequency=integers(**INT8_RANGE),
    weekly_hour_allotment=integers(**INT8_RANGE),
)
ENTRY_HYPOTHESIS = {
    "id": none(),
    "project_name": text(),
    "description": text(),
    "start_time": datetimes(),
    "end_time": datetimes(),
}
project_build_strategy = builds(Project, **PROJECT_HYPOTHESIS)
entry_build_strategy = builds(Entry, **ENTRY_HYPOTHESIS)


@pytest.fixture(scope="module")
def db() -> Database:
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


@given(project_to_add=project_build_strategy)
def test_create_valid_project(db, project_to_add):
    result = db.add_project(project_to_add, return_value=False)
    assert isinstance(result, int)
    assert result != project_to_add.id


@given(project=project_build_strategy)
def test_get_created_project(db, project):
    added_id = db.add_project(project, return_value=False)

    assert added_id != project.id
    project_in_db = db.get_multi_projects(eager_loading=True, id=added_id)

    assert len(project_in_db) == 1
    assert isinstance(project_in_db, list)

    project_in_db = project_in_db[0]

    for key, value in project.to_dict().items():
        assert project_in_db.get(key) == value
    assert project_in_db.id == added_id


@given(project_1=project_build_strategy, project_2=project_build_strategy)
def test_get_multiple_projects(db, project_1: Project, project_2: Project):
    for key, value in project_1.to_dict().items():
        if key == "project_name":
            continue
        assume(value != project_2.get(key))
    project_2.project_name = project_1.project_name
    added_id = db.add_project(project_1, return_value=False)

    project_with_differ_values = db.add_project(project_2, return_value=False)

    assert added_id != project_with_differ_values

    projects_with_same_name = db.get_multi_projects(
        project_name=project_1.project_name, eager_loading=True
    )

    assert len(projects_with_same_name) > 1
    project_unique_names = {project.project_name for project in projects_with_same_name}
    assert len(project_unique_names) == 1
    assert project_1.project_name in project_unique_names

    for key in project_1.to_dict().keys():
        if key == "project_name":
            continue
        else:
            assert len({proj.get(key) for proj in projects_with_same_name}) != 1


def test_add_wrong_type_project(db):
    bad_data_examples = [
        "a string",
        ["a", "list", "of", "str"],
        {key: val for (key, val) in [("test", 1), ("weird", "values")]},
        {i for i in range(10)},
        ("a", "tuple"),
        Entry(
            id=None,
            project_name="foo",
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
            description="foo",
        ),
    ]

    for bad_data in bad_data_examples:
        error_message = f"Project must be a Project dataclass, not {type(bad_data)}"
        with pytest.raises(ValueError, match=error_message):
            db.add_project(bad_data)


@given(entry=entry_build_strategy)
def test_create_valid_entry(db, entry):
    result = db.add_entry(entry, return_value=False)
    assert isinstance(result, int)
    assert result != entry.id


@given(entry=entry_build_strategy)
def test_get_entry(db, entry):
    inserted_id = db.add_entry(entry, return_value=False)
    entries_in_db = db.get_multi_entries(eager_loading=True, id=inserted_id)
    assert isinstance(entries_in_db, list)

    assert len(entries_in_db) == 1
    entry_in_db = entries_in_db[0]
    for key, value in entry_in_db.to_dict().items():
        if key == "id":
            assert entry.get(key) != value
        else:
            assert entry.get(key) == value


@given(entry_1=entry_build_strategy, entry_2=entry_build_strategy)
def test_get_multi_entry(db, entry_1: Entry, entry_2: Entry):
    entry_2.project_name = entry_1.project_name

    for key, value in entry_1.to_dict().items():
        if key in {"id", "project_name"}:
            continue
        assume(value != entry_2.get(key))

    entry_1_id = db.add_entry(entry_1, False)
    entry_2_id = db.add_entry(entry_2, False)

    assert entry_1_id != entry_2_id

    all_entries = db.get_multi_entries(
        eager_loading=True, project_name=entry_1.project_name
    )

    assert len(all_entries) > 1
    id_mix = {entry_dat.id for entry_dat in all_entries}
    assert len(id_mix) > 1
    assert entry_1_id in id_mix
    assert entry_2_id in id_mix


@given(project=project_build_strategy)
def test_bad_data_entry(db: Database, project: Project):
    bad_data_list = [
        "a string",
        ["a", "list", "of", "str"],
        {key: val for (key, val) in [("test", 1), ("weird", "values")]},
        {i for i in range(10)},
        ("a", "tuple"),
        project,
    ]

    for bad_data in bad_data_list:
        error_message = f"Entry must be an Entry dataclass, not {type(bad_data)}"
        with pytest.raises(ValueError, match=error_message):
            db.add_entry(bad_data, False)
