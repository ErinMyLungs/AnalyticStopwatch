""" Contains database mixin class """
import json
import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Union

import dataset

from src.models import Entry, Project


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
    """
    This class structures the database with initialization, access and insert methods
    """

    def __init__(
        self, db_uri: str = "sqlite:///src/data/timer.db", development: bool = False
    ):
        """
        :param db_uri: path to sqlite db file. Either path or URI
        :type db_uri: str
        :param development: Flag that wipes and re-inits the database
        :type development: bool
        """
        self.development = development
        if development is True:
            self._db_uri = "sqlite:///data/development.db"
            # clear db_path

            for db_path in Path(".").glob("**/development.db*"):
                db_path.unlink()

        else:
            self._db_uri = f"sqlite://{db_uri}" if db_uri.find("sqlite://") else db_uri

        self.db: dataset.database.Database = dataset.connect(self._db_uri)
        self.projects, self.entries = self.init_db()

    def init_db(self) -> Tuple[dataset.table.Table, dataset.table.Table]:
        """
        Initializes the database and creates the tables if they don't exist.
        :return: returns the projects and entry tables
        """
        projects_table = self.db.get_table("projects")
        entries_table = self.db.get_table("entries")

        if self.development is False:
            return projects_table, entries_table

        self._pre_seed_db()

        return projects_table, entries_table

    def _pre_seed_db(
        self,
        project_starter_data_path: Path = Path("./data/project_data.json"),
        entries_pickle_path: Path = Path("./data/entries"),
    ) -> None:
        """
        Pre-seeding the database with projects and entries. Projects can be stored as json, entries
        are stored as a pickle due to datetime not converting nicely to json.
        :param project_starter_data_path: By default /data/project_data.json
        :type project_starter_data_path: Path
        :param entries_pickle_path: Default /data/entries pickle
        :type entries_pickle_path: Path
        :return: None but database is seeded with data.
        """
        if project_starter_data_path.exists():
            with project_starter_data_path.open() as file:
                project_starter_data = json.load(file)

            for project in project_starter_data:
                self.db["projects"].insert(project)
        if entries_pickle_path.exists():
            with entries_pickle_path.open("rb") as file:
                entries = pickle.load(file)
            for entry in entries:
                self.db["entries"].insert(entry.to_dict())

    def add_entry(self, entry: Entry, return_value: bool = False) -> Union[int, Entry]:
        """
        Adds entry to entries tables
        :param entry: Entry to insert
        :type entry: Entry
        :param return_value: If to return the updated entry
        :type return_value: bool
        :return: created ID or entry if return_value is True
        """
        if isinstance(entry, Entry):
            entry: Dict = entry.to_dict()
        else:
            raise ValueError(f"Entry must be an Entry dataclass, not {type(entry)}")
        inserted_id = self.entries.insert(entry)
        if not return_value:
            return inserted_id
        entry_in_db = self.entries.find_one(id=inserted_id)
        return Entry(**entry_in_db)

    def add_project(
        self, project: Project, return_value: bool = False
    ) -> Union[int, Project]:
        """
        Insert project into project table
        :param project: Project dataclass to insert
        :type project: Project dataclass
        :param return_value: If True return updated Project
        :type return_value: bool
        :return: db ID or Project if return_value is True
        """
        if isinstance(project, Project):
            project: Dict = project.to_dict()
        else:
            raise ValueError(
                f"Project must be a Project dataclass, not {type(project)}"
            )

        inserted_id = self.projects.insert(project)

        if not return_value:
            return inserted_id

        project_in_db = self.projects.find_one(id=inserted_id)
        return Project(**project_in_db)

    @staticmethod
    def _eager_loader(query: callable, eager_loading: bool, **kwargs):
        query_result = query(**kwargs)
        if eager_loading:
            return list(query_result)
        return query_result

    def get_all_projects(self, eager_loading: bool = False):
        """
        Gets all projects in the projects table
        :param eager_loading: on True loads all projects into a list
        :return: Generator or List of Projects
        """
        return self.get_multi_projects(eager_loading=eager_loading)

    @as_project
    def _get_multi_projects(self, **kwargs):
        """
        Internal method for calling .find with kwargs
        :param kwargs: Column names to match on
        :return: Results processed into a list or single entity
        """
        return self.projects.find(**kwargs)

    def get_multi_projects(
        self, eager_loading: bool = False, **kwargs
    ) -> List[Project]:
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
        """
        Internal query of get entries with decorator to auto-convert to entry dataclass
        :return: Dataset result iterator -> generator that unpacks results into entries.
        """
        return self.entries.find(**kwargs)

    def get_all_entries(self, eager_loading: bool = False):
        """
        Fetches all entries in database. Essentially calling get_multi_entries with no kwargs
        :param eager_loading: if True load everything into a list in memory
        :return: Generator or List of entries
        """
        return self._eager_loader(self._get_multi_entries, eager_loading=eager_loading)

    def get_multi_entries(self, eager_loading: bool = False, **kwargs):
        """
        Get all timer entries matching kwargs passed in.
        :param eager_loading: On True returns a list else returns a generator
        :param kwargs: id, project, description are likely candidates for searching
        :return: Generator or List of Entries
        """
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
    db = Database(development=True)
