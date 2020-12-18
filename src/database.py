""" Contains database mixin class """
import json
from pathlib import Path
from typing import Dict, List, Tuple, Union

import dataset
from models import Entry, Project


def as_project(query):
    """
    Decorator to load query results up as Project
    """

    def wrapper(*args, **kwargs):
        query_result = query(*args, **kwargs)
        for result in query_result:
            yield Project(**result)

    return wrapper


def as_entry(query):
    """
    Decorator to return entries loaded as Entry dataclasses
    """

    def wrapper(*args, **kwargs):
        query_result = query(*args, **kwargs)
        for result in query_result:
            yield Entry(**result)

    return wrapper


class Database:
    def __init__(
        self, db_uri: str = "sqlite:///data/timer.db", development: bool = False
    ):
        """
        :param db_uri: path to sqlite db file. Either path or URI
        :type db_uri: str
        :param development: Flag that wipes and re-inits the database
        :type development: bool
        """
        self._db_uri = f"sqlite://{db_uri}" if db_uri.find("sqlite://") else db_uri
        self.db: dataset.database.Database = dataset.connect(self._db_uri)
        self.development = development
        self.projects, self.entries = self.init_db()

    def init_db(self) -> Tuple[dataset.table.Table, dataset.table.Table]:
        """
        Initializes the database and creates the tables if they don't exist.
        :return: returns the projects and entry tables
        """
        if self.development is True:
            """ Wipes DB before recreating for development """
            for file in Path().glob("**/timer.db*"):
                file.unlink()

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
            return Entry(**self.entries.find_one(id=inserted_id))

    def add_project(
        self, project: Union[Dict, Project], return_value: bool = False
    ) -> Union[int, Project]:
        """
        Insert project into project table
        :param project: Project dataclass to insert
        :type project: Dict or Project dataclass
        :param return_value: If True return updated Project
        :type return_value: bool
        :return: db ID or Project if return_value is True
        """
        if isinstance(project, Project):
            project = project.to_dict()

        inserted_id = self.projects.insert(project)

        if not return_value:
            return inserted_id
        else:
            project_in_db = self.projects.find_one(id=inserted_id)
            return project_in_db if project_in_db else None

    @staticmethod
    def _eager_loader(query: callable, eager_loading: bool, **kwargs):
        query_result = query(**kwargs)
        if eager_loading:
            query_result = list(query_result)
            if len(query_result) == 1:
                return query_result[0]
            else:
                return query_result
        else:
            return query_result

    @as_project
    def get_all_projects(self, eager_loading: bool = False):
        return self._eager_loader(self.get_multi_projects, eager_loading=eager_loading)

    @as_project
    def _get_multi_projects(self, **kwargs):
        return self.projects.find(**kwargs)

    def get_multi_projects(self, eager_loading: bool = False, **kwargs):
        """
        Returns project query fetched matching kwarg values
        :param eager_loading: if True returns value in memory, else generator
        :param kwargs: id, weekly_hour_allotment, monthly_frequency, client, and project_name
        :return: Generator, list, or single instance of Project
        """
        return self._eager_loader(
            self._get_multi_projects, eager_loading=eager_loading, **kwargs
        )

    @as_entry
    def _get_multi_entries(self, **kwargs):
        return self.entries.find(**kwargs)

    def get_all_entries(self, eager_loading: bool = False):
        return self._eager_loader(self._get_multi_entries, eager_loading=eager_loading)

    def get_multi_entries(self, eager_loading: bool = False, **kwargs):
        return self._eager_loader(
            self._get_multi_entries, eager_loading=eager_loading, **kwargs
        )

    def get_project_names(self) -> List[str]:
        """
        Returns all project names in DB
        :return: List of project names
        """
        project_names = list()
        for project in self.projects.distinct("project_name"):
            project_names.append(project["project_name"])
        return project_names


if __name__ == "__main__":
    db = Database()
