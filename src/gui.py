import datetime

import dearpygui.core as core
import dearpygui.simple as simple
from src.dev_gui import start_development_windows

def render(sender, data):

    core.set_value("timer_text", datetime.time.strftime(datetime.datetime.now().time(), "%H:%M:%S"))


def main(development: bool = False):
    core.set_main_window_size(800, 800)
    core.set_main_window_pos(2400, 0)
    if development:
        start_development_windows()
    with simple.window(name="Timer", x_pos=0, y_pos=0, width=300, height=300):
        # core.add_additional_font(file="./fonts/InputMono-Black.ttf", size=25)
        core.set_value("timer_text", datetime.time.strftime(datetime.datetime.now().time(), "%H:%M:%S"))
        core.add_text(name="TimerText", source="timer_text")

    core.set_render_callback(render)
    core.start_dearpygui()


if __name__ == "__main__":
    main(development=True)
