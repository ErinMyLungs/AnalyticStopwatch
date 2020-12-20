""" GUI module, contains BaseGUI class and PyTogglGUI subclass """
import datetime
from typing import Optional, Tuple

import dearpygui.core as c
import dearpygui.simple as s
from src.database import Database
from src.dev_gui import start_development_windows
from src.models import Entry, Project


class BaseGUI:
    """
    Base GUI class with logging help functions and base screen initializations.
    """

    def __init__(
        self,
        development: bool = False,
        *,
        dev_window_size: Tuple[int, int] = (800, 800),
        prod_window_size: Tuple[int, int] = (300, 300),
        title: str = "PyToggl",
        logger: str = "",
    ):
        """
        Base parameters for GUI
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
        self.development = development
        self.title = title
        self.logger = logger
        if self.development:
            self.window_size = dev_window_size
        else:
            self.window_size = prod_window_size

        self.initialize_base_screens()

    def initialize_base_screens(self):
        """
        Loads up input font and sets up development windows.
        """
        c.add_additional_font(file="./fonts/InputMono-Black.ttf", size=16)
        c.set_main_window_title(self.title)
        c.set_main_window_size(*self.window_size)
        if self.development:
            c.set_main_window_pos(x=1120, y=0)
            start_development_windows(self.logger)

        else:
            c.set_main_window_resizable(False)

    def _log(self, message: str, log_fun: callable):
        """
        Generic logging function
        :param message: Message for console
        :param log_fun: base log function
        :return: Message in console
        """
        if self.development:
            log_fun(message=message, logger=self.logger)

    def log(self, message: str):
        """
        This is a short-hand for log_info. Literally calls the same thing.
        :param message: Message to send to logger
        :return: Message in show_logger() window
        """
        return self.log_info(message)

    def log_info(self, message: str):
        """
        Adds message to logger in info level
        :param message: message to log
        :return: Message in logger
        """
        self._log(message, log_fun=c.log_info)

    def log_debug(self, message: str):
        """
        Adds message to logger at debug level
        :param message: message to log
        :return: Debug message in logger
        """
        self._log(message=message, log_fun=c.log_debug)

    def log_warning(self, message: str):
        """
        Adds message to logger at warning level
        :param message: Message to log
        :return: Warning message in logger
        """
        self._log(message=message, log_fun=c.log_warning)

    def log_error(self, message: str):
        """
        Adds error message to logger. Does not raise error
        :param message: Message to log
        :return: Error message in logger
        """
        self._log(message=message, log_fun=c.log_error)

    def run(self):
        """
        A minimum run function would be c.start_dearpygui()
        """
        raise NotImplementedError


class PyTogglGUI(BaseGUI):
    """
    Stopwatch class, builds out the GUI portion of PyToggl
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
    def project(self) -> str:
        """
        Gets selected project from dropdown

        :return: Selected project_name
        """
        return c.get_value("Project")

    @property
    def description(self) -> str:
        """
        Property for description input value
        :return: Str description of task
        """
        return c.get_value("Description")

    def flip_timer_state(self, *_args):
        """
        Flips tracking bool, sets starting time, and flips button label
        :arg sender: Callback widget name in pos 0
        :arg data: callback_data setting in widget in pos 1
        """
        if self.tracking:
            label = "Start Timer"
            self.save_new_entry()
        else:
            label = "End Timer"

        s.set_item_label("Start Timer", label=label)
        self.set_tracking()
        self.set_start_time()

    def save_new_entry(self) -> None:
        """
        Inserts timer entry to entries table
        :param return_value: Option to return the created entry
        :type return_value: bool
        :return: None or created entry in db.
        """
        entry_to_insert = Entry(
            id=None,
            project_name=self.project,
            description=self.description,
            start_time=self.start_time,
            end_time=datetime.datetime.now(),
        )
        entry = self.db.add_entry(entry_to_insert, return_value=True)
        self.add_row_to_entry_table(entry)

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
        c.configure_item("Project", items=self.db.get_project_names())
        c.delete_item("Create New Project")

    def create_new_project(self, *_args):
        """
        Defines a simple window that takes inputs for creating a new project
        :return: On save inserts project data into database
        """
        with s.window("Create New Project"):
            c.add_input_text("project_name##new_project")
            c.add_input_text("client##new_project")
            c.add_input_int("rate##new_project")
            c.add_input_int("monthly_frequency##new_project")
            c.add_input_int("weekly_hour_allotment##new_project")
            c.add_button("Save##SaveProject", callback=self.save_new_project)

    @staticmethod
    def add_row_to_entry_table(entry: Entry) -> None:
        """
        Helper to add entry to the table
        :param entry: A single entry to convert to entries table
        :return: New row attached to the Entries##table
        """
        row_data = [
            entry.project_name,
            entry.description,
            str(entry.duration)[:10],
            entry.start_time.time().strftime("%I:%M"),
            entry.end_time.time().strftime("%I:%M"),
        ]
        c.add_row("Entries##table", row_data)

    def entries_table(self):
        """
        Creates entries table and fills with all entries
        :return: Entry table?
        """

        c.add_table(
            "Entries##table",
            headers=["Project", "Description", "Duration", "Start", "End"],
        )
        for entry in self.db.get_all_entries():
            self.add_row_to_entry_table(entry)

    def render(self, *_args):
        """
        Updates timer text continuously
        """
        if self.tracking:
            c.set_value("timer_text", str(self.time_delta))
        else:
            c.set_value(
                "timer_text",
                datetime.time.strftime(datetime.datetime.now().time(), "%H:%M:%S"),
            )

    def run(self, width: int = 600, height: int = 600, **kwargs):
        # pylint: disable=arguments-differ
        """
        GUI definition and runs dearpygui
        :param width: pixel width of main window
        :param height: pixel height of main window
        :param kwargs: any simple.window kwargs
        :return:GUI although more probably 'void'
        """
        with s.window(
            name="Timer",
            x_pos=0,
            y_pos=0,
            width=width,
            height=height,
            no_close=True,
            no_title_bar=True,
            no_resize=not self.development,
            no_move=not self.development,
            **kwargs,
        ):
            c.set_value(
                "timer_text",
                datetime.time.strftime(datetime.datetime.now().time(), "%H:%M:%S"),
            )
            c.add_text(name="TimerText", source="timer_text")
            c.add_combo(name="Project", items=self.db.get_project_names(), width=200)
            c.add_input_text(
                name="Description", default_value="coding", label="Description"
            )
            c.add_button(name="Start Timer", callback=self.flip_timer_state)
            c.add_same_line()
            c.add_button(name="Add Project", callback=self.create_new_project)
            c.add_same_line()

            c.add_spacing()
            self.entries_table()

        c.set_render_callback(self.render)
        c.start_dearpygui()


if __name__ == "__main__":
    gui = PyTogglGUI(development=True)
    gui.run()
