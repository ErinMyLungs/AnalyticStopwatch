""" Tests for local storage """
from unittest.mock import MagicMock, patch

from clockpuncher.platform_local_storage import (
    _check_if_file_exists_or_create, initialize_development_files,
    initialize_production_files)


def test_file_not_created_if_exists():
    MockedPath = MagicMock()
    MockedPath.exists.return_value = True

    _check_if_file_exists_or_create(MockedPath)

    MockedPath.exists.assert_called_once()
    MockedPath.parents.mkdir.assert_not_called()
    MockedPath.touch.assert_not_called()

    MockedPath.exists.return_value = False
    MockedPath.exists.reset_mock()

    _check_if_file_exists_or_create(MockedPath)
    MockedPath.exists.assert_called_once()
    MockedPath.parent.mkdir.assert_called_once()
    MockedPath.touch.assert_called_once()


def test_init_files():
    with patch("platform_local_storage.DEVELOPMENT_DB_PATH") as MockDevelopmentPath:
        MockDevelopmentPath.exists.return_value = False
        initialize_development_files()
        MockDevelopmentPath.exists.assert_called_once()
        MockDevelopmentPath.parent.mkdir.assert_called_once()
        MockDevelopmentPath.touch.assert_called_once()

    with patch("platform_local_storage.PRODUCTION_DB_PATH") as MockProductionPath:
        MockProductionPath.exists.return_value = False
        initialize_production_files()
        MockProductionPath.exists.assert_called_once()
        MockProductionPath.parent.mkdir.assert_called_once()
        MockProductionPath.touch.assert_called_once()
