import datetime
from typing import Tuple, Optional

import dearpygui.core as c
import dearpygui.simple as s
from dev_gui import start_development_windows


class BaseGUI:
    def __init__(
        self,
        development: bool = False,
        dev_window_size: Tuple[int, int] = (800, 800),
        prod_window_size: Tuple[int, int] = (300, 300),
        title: str = "Py Toggl",
        logger: str = "",
    ):
        """
        Base parameters for GUI
        :param development: If True launches logger + debugger
        :param dev_window_size: Dev window size, typically larger to accommodate dev tools
        :param prod_window_size: Size if dev == False, usually the size of the main window
        :param title: Title for Window
        :param logger: Name for logger
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
        return self.log_info(message)

    def log_info(self, message: str):
        self._log(message, log_fun=c.log_info)

    def log_debug(self, message: str):
        self._log(message=message, log_fun=c.log_debug)

    def log_warning(self, message: str):
        self._log(message=message, log_fun=c.log_warning)

    def log_error(self, message: str):
        self._log(message=message, log_fun=c.log_error)

    def run(self):
        """
        A minimum run function would be c.start_dearpygui()
        """
        raise NotImplemented


class PyTogglGUI(BaseGUI):
    def __init__(self, db_uri: str, **kwargs):
        """
        :param db_uri: Local sqlite database for saving data to
        :param kwargs: accepts base class arguments
        """
        super().__init__(**kwargs)
        self.db_uri = db_uri

        self.initialize_tracking_data()

    def initialize_tracking_data(self):
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
        # noinspection PyTypeChecker
        return c.get_data("start_time")

    def set_start_time(self, manual_time: Optional[datetime.datetime] = None):
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

    def flip_timer_state(self, caller, data):
        """
        Flips tracking bool, sets starting time, and flips button label
        :return:
        """
        if self.tracking:
            label = "Start Timer"
        else:
            label = "End Timer"
        s.set_item_label("Start Timer", label=label)
        self.set_tracking()
        self.set_start_time()

    def render(self, sender, data):
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

    def run(self, width: int = 300, height: int = 300, **kwargs):
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
            **kwargs
        ):
            c.set_value(
                "timer_text",
                datetime.time.strftime(datetime.datetime.now().time(), "%H:%M:%S"),
            )
            c.add_text(name="TimerText", source="timer_text")
            c.add_button(name="Start Timer", callback=self.flip_timer_state)
            c.add_combo(
                name="Project", items=["CEO School", "Set Tracker", "Type Two Tech"]
            )

        c.set_render_callback(self.render)
        c.start_dearpygui()


if __name__ == "__main__":
    gui = PyTogglGUI(development=False, db_uri="")
    gui.run()
