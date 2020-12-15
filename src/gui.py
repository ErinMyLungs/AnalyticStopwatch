import dearpygui.core as core
import dearpygui.simple as simple
from src.dev_gui import start_development_windows


def main(development: bool = False):
    core.set_main_window_size(800, 800)
    core.set_main_window_pos(2400,0)
    if development:
        start_development_windows()

    core.start_dearpygui()


if __name__ == "__main__":
    main(development=True)
