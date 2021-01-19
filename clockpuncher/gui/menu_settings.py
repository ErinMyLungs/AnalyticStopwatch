""" Contains settings menu component class """
import subprocess
import sys
from typing import Optional

import dearpygui.core as c
import dearpygui.simple as s

from clockpuncher.platform_local_storage import DATA_DIR_PATH


class SettingMenu:
    """
    Creates a settings menu with callbacks
    """

    def __init__(self, menu_bar_name: Optional[str] = None) -> None:
        """
        For manual menu bar settings
        :param menu_bar_name: menu bar to add menu to
        """
        if menu_bar_name is None:
            self.menu_bar_name = "Main Menu Bar"
        else:
            self.menu_bar_name = menu_bar_name

    def create_menu(self):
        """
        Creates menu with menu items
        :return: Menu
        """
        with s.menu(name="Settings##menu", parent=self.menu_bar_name):
            c.add_menu_item(
                name="ShowDataOption##Settings",
                label="Show local data storage",
                callback=self.show_local_storage,
            )
            c.add_menu_item(
                name="AdjustSettings##Settings", label="Change Settings", enabled=False
            )

    @staticmethod
    def show_local_storage(*_args):
        """
        Helper for Show Local Data Storage menu option
        :param _args:  sender/data args
        :return: Opens the file GUI explorer hopefully
        """
        path_str = DATA_DIR_PATH.as_posix()
        open_functions = {
            "linux": lambda: subprocess.check_call(["xdg-open", path_str]),
            "win32": lambda: subprocess.check_call(["explorer", "/select", path_str]),
            "darwin": lambda: subprocess.check_call(["open", "--", path_str]),
        }
        open_file_explorer = open_functions.get(sys.platform, None)

        if open_file_explorer is None:
            raise OSError("Your platform is not supported for this function")
        try:
            open_file_explorer()
        except subprocess.CalledProcessError as open_error:
            raise open_error


settings_menu = SettingMenu()
