""" Contains development GUI helpers """
from dearpygui.core import (
    add_checkbox,
    add_debug_window,
    add_doc_window,
    add_input_text,
    add_text,
    end,
    get_item_configuration,
    get_value,
    get_windows,
    log_debug,
    log_info,
    show_logger,
)
from dearpygui.simple import window


def start_development_windows(logger: str):
    """
    Starts doc, debug, and logger window
    """
    add_doc_window(name="Core Documentation", x_pos=0, y_pos=800)
    end()

    show_logger()

    # for some reason the default logger doesn't show the first
    # log_info call so this clears that out.
    log_info("Clearing out initial issue with logger", logger=logger)

    add_debug_window(name="Debug", x_pos=0, y_pos=300)
    end()


def debug_get_window_pos(sender, data):
    """
    Debug setup for getting location configs of windows
    """
    log_info(sender, logger=data)
    window_name_to_search = get_value("Window Name##input")
    show_invisible = get_value("Print invisible")
    log_info(window_name_to_search, logger=data)
    log_info(show_invisible, logger=data)
    window_list = list()

    if window_name_to_search:
        log_debug(window_name_to_search, logger=data)
        for window_name in get_windows():
            if window_name_to_search.lower() in window_name.lower():
                window_list.append(window_name)
    else:
        window_list = get_windows()

    for window_name in window_list:
        config = get_item_configuration(window_name)
        if show_invisible is False:
            if config.get("show") is False:
                continue

        x_pos = config.get("x_pos", 0)
        y_pos = config.get("y_pos", 0)
        name = config.get("name")

        if len(name) > 6:
            name = name[:5]
        log_debug(f"{name} : {x_pos}, {y_pos}", logger=data)


def debug_get_location_gui(logger="log"):
    """
    Simple text input + location window for checking default config x/y pos
    """

    with window("Location", autosize=True, y_pos=0):
        add_text(
            """
On enter will give all window config locations.
Window name will look for all windows that name contains the string, caps insensitive.
"""
        )
        add_input_text(
            name="Window Name##input",
            callback=debug_get_window_pos,
            on_enter=True,
            callback_data=logger,
        )
        add_checkbox("Print invisible", default_value=False)
