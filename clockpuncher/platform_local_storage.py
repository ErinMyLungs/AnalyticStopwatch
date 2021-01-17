""" A simple module to provide paths to files in Clockpuncher """
from pathlib import Path

from appdirs import AppDirs

local_application_directories = AppDirs(appname="Clockpuncher", appauthor="ISAC")

DATA_DIR_PATH = Path(local_application_directories.user_data_dir)

DEVELOPMENT_DB_PATH = DATA_DIR_PATH / "development.db"

PRODUCTION_DB_PATH = DATA_DIR_PATH / "timer.db"


def _check_if_file_exists_or_create(file_to_init: Path) -> None:
    """
    Helper method to check if file exists and if not to create it.
    :param file_to_init: File path to check
    """
    if file_to_init.exists() is False:
        file_to_init.parent.mkdir(parents=True, exist_ok=True)
        file_to_init.touch()


def _delete_sqlite_wal_and_shm_files(file_to_delete: Path) -> None:
    """
    Deletes shm and wal files that are created for sqlite
    :param file_to_delete: database path to find wal and shm files
    :return: None, unlinks -shm and -wal files at same path as file_to_delete
    """
    posix_path = file_to_delete.as_posix()
    for extension in ["-shm", "-wal"]:
        specific_file_to_delete = Path(posix_path + extension)
        if specific_file_to_delete.exists():
            specific_file_to_delete.unlink()


def initialize_development_files() -> None:
    """
    Initializes development db file if it doesn't exist
    """
    _check_if_file_exists_or_create(DEVELOPMENT_DB_PATH)


def destroy_development_files() -> None:
    """
    Destroys development database
    """
    if DEVELOPMENT_DB_PATH.exists():
        DEVELOPMENT_DB_PATH.unlink()
    _delete_sqlite_wal_and_shm_files(DEVELOPMENT_DB_PATH)


def initialize_production_files() -> None:
    """
    Initializes production user files if does not exist
    """
    _check_if_file_exists_or_create(PRODUCTION_DB_PATH)
