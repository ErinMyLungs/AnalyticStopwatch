""" Tests for database.py """
import datetime
import json
import pickle
from collections.abc import Generator
from pathlib import Path

import pytest
from hypothesis import assume, given
from clockpuncher.platform_local_storage import (
    DEVELOPMENT_DB_PATH,
    PRODUCTION_DB_PATH,
    destroy_development_files,
    initialize_development_files,
)

from clockpuncher.database import Database
from clockpuncher.models import Entry, Project
from clockpuncher.tests.utils import entry_build_strategy, project_build_strategy


@pytest.fixture()
def db() -> Database:
    initialize_development_files()
    yield Database(development=True)
    destroy_development_files()


@pytest.fixture()
def seed_data():
    project_seed_data = Path("./clockpuncher/data/project_data.json")
    entries_seed_data = Path("./clockpuncher/data/entries")
    project_data = None
    entry_data = None

    if project_seed_data.exists():
        with project_seed_data.open() as f:
            project_data = json.load(f)

    if entries_seed_data.exists():
        with entries_seed_data.open("rb") as f:
            entry_data = pickle.load(f)
    if project_data is None:
        project_data = list()
    if entry_data is None:
        entry_data = list()
    return project_data, entry_data


def test_intialization(db, seed_data):
    """
    Tests that on creation a database with projects and entries table is created
    """

    assert db.db.url == f"sqlite:///{DEVELOPMENT_DB_PATH.as_posix()}"

    assert db.projects == db.db.get_table("projects")
    assert db.entries == db.db.get_table("entries")

    # Define seed data possible location
    seed_project_data, seed_entry_data = seed_data
    num_of_projects = len(seed_project_data)
    num_of_entries = len(seed_entry_data)

    assert db.db.get_table("entries").count() == num_of_entries
    assert db.db.get_table("projects").count() == num_of_projects


def test_production_flag():
    db = Database()
    assert db._db_uri != f"sqlite:///{DEVELOPMENT_DB_PATH.as_posix()}"
    assert db._db_uri == f"sqlite:///{PRODUCTION_DB_PATH.as_posix()}"


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


@given(project=project_build_strategy)
def test_insert_return_value(db, project):
    project_output: Project = db.add_project(project, return_value=True)

    assert isinstance(project_output, Project)

    assert project.id != project_output.id

    for key, value in project.to_dict().items():
        if key == "id":
            continue
        assert project_output.get(key) == value


def test_get_all_projects(seed_data):
    db = Database(development=True)
    seed_project_data, _ = seed_data

    all_projects_eager = db.get_all_projects(eager_loading=True)
    all_projects_generator = db.get_all_projects(eager_loading=False)

    assert isinstance(all_projects_eager, list)
    assert isinstance(all_projects_generator, Generator)

    assert len(seed_project_data) == len(all_projects_eager)

    idx = 0
    for gen_project in all_projects_generator:
        assert idx + 1 <= len(seed_project_data)
        seed_project = seed_project_data[idx]
        eager_project = all_projects_eager[idx]
        for key, value in seed_project.items():
            if key == "id":
                assert gen_project.get(key) != value
                assert eager_project.get(key) != value
                assert eager_project.id == gen_project.id
            else:
                assert gen_project.get(key) == value
                assert eager_project.get(key) == value
        idx += 1
    assert idx == len(all_projects_eager)


@given(entry=entry_build_strategy)
def test_create_valid_entry(db, entry):
    result = db.add_entry(entry, return_value=False)
    assert isinstance(result, int)
    assert result != entry.id


@given(entry=entry_build_strategy)
def test_insert_entry_with_return_value(db, entry):
    result = db.add_entry(entry, return_value=True)
    assert isinstance(result, Entry)
    assert entry.id != result.id
    for key, value in result.to_dict().items():
        if key == "id":
            continue
        assert entry.get(key) == value


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


def test_get_all_entries(seed_data):
    db = Database(development=True)
    _, seed_entry_data = seed_data

    all_entries_eager = db.get_all_entries(eager_loading=True)
    assert isinstance(all_entries_eager, list)
    assert len(all_entries_eager) == len(seed_entry_data)

    for seed_entry, entry in zip(seed_entry_data, all_entries_eager):
        assert isinstance(entry, Entry)
        for key, value in seed_entry.to_dict().items():
            if key == "id":
                assert entry.get(key) != value
            else:
                assert entry.get(key) == value

    all_entries_gen = db.get_all_entries(eager_loading=False)

    assert isinstance(all_entries_gen, Generator)

    idx = 0
    for gen_entry in all_entries_gen:
        assert idx + 1 <= len(all_entries_eager)
        assert gen_entry == all_entries_eager[idx]
        idx += 1

    assert idx == len(all_entries_eager)
