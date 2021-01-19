""" Entrypoint and GUI definition for the Clockpuncher app """
import datetime
from typing import Optional

import dearpygui.core as c
import dearpygui.simple as s

from clockpuncher.database import Database
from clockpuncher.gui import entry_table, settings_menu, task_chart, timer_display
from clockpuncher.gui.base_gui import BaseGUI
from clockpuncher.models import Entry, Project
from clockpuncher.platform_local_storage import (
    destroy_development_files,
    initialize_development_files,
    initialize_production_files,
)


class ClockPuncher(BaseGUI):
    """
    Stopwatch class, builds out the GUI portion of ClockPuncher
    """

    def __init__(self, **kwargs):
        """
        :keyword development: If True launches logger + debugger
        :type development: bool
        :keyword dev_window_size: Dev window size, typically larger to accommodate dev tools
        :type dev_window_size: Tuple[int, int]
        :keyword prod_window_size: Size if dev == False, usually the size of the main window
        :type prod_window_size: Tuple[int, int]
        :keyword title: Title for Window
        :type title: str
        :keyword logger: Name for logger
        :type logger: str
        """
        super().__init__(**kwargs)

        self.db = Database(development=self.development)

        self.entries = self.db.get_all_entries(True)
        self.selected_project = None
        self.initialize_tracking_data()

    @staticmethod
    def initialize_tracking_data():
        """
        Initializes data objects tracking and start_time
        """
        c.add_data("tracking", False)
        c.add_data("start_time", datetime.datetime.now())

    @property
    def tracking(self):
        """
        Bool of if the stopwatch should be active
        """
        return c.get_data("tracking")

    def set_tracking(self, value: Optional[bool] = None):
        """
        Flips tracking data bool by default or sets to exact value
        :param value:
        """
        if value is None:
            c.add_data("tracking", not self.tracking)
        elif isinstance(value, bool):
            c.add_data("tracking", value)
        else:
            raise ValueError

    @property
    def start_time(self) -> datetime.datetime:
        """
        Property for start_time stored in DearPyGUI
        :return:  datetime of prior start_time
        """
        # noinspection PyTypeChecker
        return c.get_data("start_time")

    @staticmethod
    def set_start_time(manual_time: Optional[datetime.datetime] = None):
        """
        Sets start_time property to either now or a manual entry
        :param manual_time: datetime object manual setting
        """
        if manual_time is None:
            c.add_data("start_time", datetime.datetime.now())
        elif isinstance(manual_time, datetime.datetime):
            c.add_data("start_time", manual_time)
        else:
            raise ValueError

    @property
    def time_delta(self):
        """
        Gives delta between now and start time of timer.
        """
        return datetime.datetime.now() - self.start_time

    @property
    def description(self) -> str:
        """
        Property for description input value
        :return: Str description of task
        """
        return c.get_value("Description")

    def switch_task(self, *_args) -> None:
        """
        Saves entry but maintains timer so updating description is inline
        :param _args: sender, data in 0, 1 tuple position
        :return: None
        """
        self.save_new_entry()
        self.set_start_time()
        c.set_value("Description", "")

    def flip_timer_state(self, *_args):
        """
        Flips tracking bool, sets starting time, and flips button label
        :arg sender: Callback widget name in pos 0
        :arg data: callback_data setting in widget in pos 1
        """
        if self.tracking:
            label = "Start Timer"
            c.configure_item("Switch Task", show=False)
            self.save_new_entry()
        else:
            label = "End Timer"
            c.configure_item("Switch Task", show=True)

        s.set_item_label("Start Timer", label=label)
        self.set_tracking()
        self.set_start_time()

    def save_new_entry(self) -> None:
        """
        Inserts timer entry to entries table
        """
        entry_to_insert = Entry(
            id=None,
            project_name=self.selected_project if self.selected_project else "",
            description=self.description,
            start_time=self.start_time,
            end_time=datetime.datetime.now(),
        )
        entry = self.db.add_entry(entry_to_insert, return_value=True)
        self.entries = [*self.entries, entry]

    def save_new_project(self, *_args):
        """
        Fetches data from the create new project window and inserts into db and then refreshes the
        combo dropdown values
        """
        project_data = dict()
        # pylint: disable=no-member
        for val in Project.__annotations__:
            project_data[val] = c.get_value(f"{val}##new_project")
        self.db.add_project(Project(**project_data, id=None))
        c.delete_item("Projects##ProjectMenu", children_only=True)
        for name in self.db.get_project_names():
            c.add_menu_item(
                name=name,
                callback=self.select_project,
                callback_data=name,
                parent="Projects##ProjectMenu",
            )

        c.add_menu_item(
            "Add project",
            parent="Projects##ProjectMenu",
            callback=self.create_new_project,
        )
        c.delete_item("Create New Project")

    def create_new_project(self, *_args):
        """
        Defines a simple window that takes inputs for creating a new project
        :return: On save inserts project data into database
        """
        with s.window("Create New Project", autosize=True):
            c.add_input_text("project_name##new_project", label="Project Name")
            c.add_input_text("client##new_project", label="Client")
            c.add_slider_int(
                "rate##new_project",
                label="Billing Rate per hour",
                max_value=100,
                tip="ctrl+click to directly type the number",
            )
            c.add_slider_int(
                "monthly_frequency##new_project",
                label="Pay Frequency per Month",
                default_value=2,
                max_value=8,
                tip="How frequently pay is given, default twice a month",
            )
            c.add_slider_int(
                "weekly_hour_allotment##new_project",
                label="Weekly Hours",
                max_value=80,
                default_value=20,
                tip="Hours per week for project.",
            )

            c.add_button("Save##SaveProject", callback=self.save_new_project)

    def select_project(self, _sender, data: str):
        """
        Selects project in menu
        :param _sender: Menu item clicked
        :param data: data which contains selected project name
        :return: Sets main window title and self.selected_project
        """
        if self.selected_project is not None:
            c.configure_item(self.selected_project, check=False)
        self.selected_project = data
        c.set_main_window_title(f"{self.title} - {data}")
        c.configure_item(data, check=True)

    def run(self, width: int = 700, height: int = 800, **kwargs):
        # pylint: disable=arguments-differ
        """
        GUI definition and runs dearpygui
        :param width: pixel width of main window
        :param height: pixel height of main window
        :param kwargs: any simple.window kwargs
        :return:GUI although more probably 'void'
        """
        if self.development:
            x_pos = 300
        else:
            x_pos = 0

        with s.window(
            name="Timer",
            x_pos=x_pos,
            y_pos=0,
            width=width,
            height=height,
            no_close=True,
            no_title_bar=True,
            no_resize=not self.development,
            no_move=not self.development,
            no_bring_to_front_on_focus=True,
            **kwargs,
        ):
            with s.menu_bar("Main Menu Bar"):
                with s.menu("Projects##ProjectMenu"):
                    for name in self.db.get_project_names():
                        c.add_menu_item(
                            name=name, callback=self.select_project, callback_data=name
                        )
                    c.add_menu_item("Add project", callback=self.create_new_project)
                with s.menu("Range##FilterMenu"):
                    c.add_menu_item(
                        name="Today", callback=self.filter_entries, check=False
                    )
                    c.add_menu_item(
                        name="All Time", callback=self.filter_entries, check=True
                    )
                settings_menu.create_menu()

            c.add_spacing(count=40)
            c.add_input_text(
                name="Description", default_value="coding", label="Description"
            )
            c.add_button(name="Start Timer", callback=self.flip_timer_state)
            c.add_same_line()
            c.add_button(name="Switch Task", callback=self.switch_task, show=False)

            c.add_spacing()
            entry_table.create_table(input_data=self.entries)
            c.add_spacing()
            task_chart.create_chart(
                data=[0.2, 0.5, 0.3], labels=self.db.get_project_names()
            )
        timer_display.create_timer(x_pos=(x_pos + 60), y_pos=20)
        c.set_render_callback(self.render)
        c.start_dearpygui()

    def render(self, *_args):
        """
        Updates timer text continuously and updates task_chart on entries update
        """
        task_chart.render(self.entries)
        entry_table.render(self.entries)
        if self.tracking:
            timer_display.render(time_to_render=self.time_delta)
        else:
            timer_display.render(time_to_render=datetime.datetime.now())

    def filter_entries(self, sender, _data):
        """
        Filters entries into this week or just today for display
        :param sender: Sender to call this
        :return: self.entries is updated to reflect entries from today
        """
        if sender == "All Time":
            self.entries = self.db.get_all_entries(True)
            c.configure_item("All Time", check=True)
            c.configure_item("Today", check=False)

        elif sender == "Today":
            new_entries = self.db.get_entries_today(True)
            self.entries = new_entries
            c.configure_item("All Time", check=False)
            c.configure_item("Today", check=True)


def main(development=False):
    """
    Entrypoint function to run the GUI
    :return: None
    """
    # Setup Data Files
    if development:
        initialize_development_files()
    else:
        initialize_production_files()

    # Create GUI
    gui = ClockPuncher(development=development)
    gui.run()

    # Teardown Development Files
    if development:
        destroy_development_files()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Start ClockPuncher to track your hours."
    )
    parser.add_argument(
        "-X",
        "--development",
        default=False,
        action="store_true",
        help="Launch in development mode with a fresh database that is wiped on next launch.",
    )
    args = parser.parse_args()

    main(development=args.development)
