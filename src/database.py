""" Contains database mixin class """
from typing import Tuple, Union

import dataset
from .models import Entry, Project
from pathlib import Path
import json


class DatabaseMixin:
    def __init__(self, db_uri: str = "sqlite:///data/timer.db"):
        """
        :param db_uri: path to sqlite db file. Either path or URI
        :type db_uri: str
        """
        self._db_uri = f"sqlite://{db_uri}" if db_uri.find("sqlite://") else db_uri
        self.db: dataset.database.Database = dataset.connect(self._db_uri)
        self.projects, self.entries = self.init_db()

    def init_db(self) -> Tuple[dataset.table.Table, dataset.table.Table]:
        """
        Initializes the database and creates the tables if they don't exist.
        :return: returns the projects and entry tables
        """
        tables = self.db.tables

        seed_db = False

        for table_name in ["entries", "projects"]:
            if table_name not in tables:
                seed_db = table_name == "projects"  # pre-seed if new
                self.db.create_table(table_name=table_name)

        projects_table: dataset.table.Table = self.db.get_table("projects")
        entries_table = self.db.get_table("entries")

        if not seed_db:
            return projects_table, entries_table

        # Pre-seeding the project database. See example_project_data.json for example values
        project_starter_data_path = Path("./data/project_data.json")
        if project_starter_data_path.exists():
            with project_starter_data_path.open() as f:
                project_starter_data = json.load(f)

            for project in project_starter_data:
                projects_table.insert(project)

        return projects_table, entries_table

    def add_entry(self, entry: Entry, return_value: bool = False) -> Union[int, Entry]:
        """
        Adds entry to entries tables
        :param entry: Entry to insert
        :type entry: Entry
        :param return_value: If to return the updated entry
        :type return_value: bool
        :return: created ID or entry if return_value is True
        """
        inserted_id = self.entries.insert(entry.to_dict())
        if not return_value:
            return inserted_id
        else:
            return self.entries.find_one(id=inserted_id)

    def add_project(
        self, project: Project, return_value: bool = False
    ) -> Union[int, Project]:
        """
        Insert project into project table
        :param project: Project dataclass to insert
        :type project: Project
        :param return_value: If True return updated Project
        :type return_value: bool
        :return: db ID or Project if return_value is True
        """
        inserted_id = self.entries.insert(project.to_dict())

        if not return_value:
            return inserted_id
        else:
            return self.projects.find_one(id=inserted_id)
