""" Holds baseclass for GUI with helpers and logger methods """
from pathlib import Path
from typing import Tuple

from dearpygui import core as c

from clockpuncher.gui.dev_gui import start_development_windows


class BaseGUI:
    """
    Base GUI class with logging help functions and base screen initializations.
    """

    def __init__(
        self,
        development: bool = False,
        *,
        dev_window_size: Tuple[int, int] = (1000, 800),
        prod_window_size: Tuple[int, int] = (700, 800),
        title: str = "Clock Puncher!",
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
        # font = list(Path("").absolute().parent.glob("**/InputMono-Black.ttf"))
        check_pipx = Path().home() / ".local/pipx/venvs/clockpuncher"
        if check_pipx.exists() is True:
            font = list(check_pipx.glob("**/fonts/InputMono-Black.ttf"))

            if font and font[0].exists():
                c.add_additional_font(file=str(font[0]), size=16)
        elif check_pipx.exists() is False:
            font = list(
                Path(__file__).resolve().parents[2].glob("**/fonts/InputMono-Black.ttf")
            )
            if font and font[0].exists():

                c.add_additional_font(str(font[0].absolute()), size=16)

        else:
            print("Cannot load font")
        c.set_main_window_title(self.title)
        c.set_main_window_size(*self.window_size)
        c.set_style_window_rounding(0)
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
