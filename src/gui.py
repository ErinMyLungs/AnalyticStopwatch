import datetime

import dearpygui.core as core
import dearpygui.simple as simple
from src.dev_gui import start_development_windows


def render(sender, data):
    if core.get_data("tracking"):
        start_time = core.get_data("start_time")
        current_time = datetime.datetime.now()
        core.set_value("timer_text", str(current_time - start_time))
    else:
        core.set_value(
            "timer_text",
            datetime.time.strftime(datetime.datetime.now().time(), "%H:%M:%S"),
        )


def initialize_values(development: bool = False):
    core.add_data("tracking", False)
    core.add_data("start_time", datetime.datetime.now())
    core.add_additional_font(file="./fonts/InputMono-Black.ttf", size=16)
    core.set_main_window_title("Py Toggl")

    if development:
        core.set_main_window_size(800, 800)
        core.set_main_window_pos(2400, 0)
        start_development_windows()
    else:
        core.set_main_window_size(300, 300)
        core.set_main_window_resizable(False)
def flip_toggle(sender, data):
    tracking = core.get_data("tracking")
    if tracking is True:

        core.add_data("start_time", datetime.datetime.now())
        core.add_data("tracking", False)
        simple.set_item_label("Start Timer", label="Start Timer")
    else:
        core.add_data("tracking", True)
        core.add_data("start_time", datetime.datetime.now())
        simple.set_item_label("Start Timer", label="End Timer")


def main(development: bool = False):

    initialize_values(development)


    with simple.window(
        name="Timer",
        x_pos=0,
        y_pos=0,
        width=300,
        height=300,
        no_close=True,
        no_title_bar=True,
        no_resize=not development,
        no_move=not development,
    ):
        core.set_value(
            "timer_text",
            datetime.time.strftime(datetime.datetime.now().time(), "%H:%M:%S"),
        )
        core.add_text(name="TimerText", source="timer_text")
        core.add_button(name="Start Timer", callback=flip_toggle)
        core.add_combo(
            name="Project", items=["CEO School", "Set Tracker", "Type Two Tech"]
        )

    core.set_render_callback(render)
    core.start_dearpygui()


if __name__ == "__main__":
    main(development=True)
