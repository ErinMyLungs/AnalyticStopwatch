from dearpygui.core import (
    log_info,
    get_value,
    log_debug,
    get_windows,
    get_item_configuration,
    add_doc_window,
    end,
    add_debug_window,
    add_logger,
    add_button,
    add_input_text,
    set_item_callback,
    set_log_level,
    mvTRACE,
    add_text,
add_checkbox
)
from dearpygui.simple import window



def debug_get_window_pos(sender, data):
    """
    Debug setup for getting location configs of windows
    """
    log_info(sender, logger="log")
    window_name = get_value("Window Name##input")
    show_invisible = get_value("Print invisible")
    log_info(window_name, logger="log")
    log_info(show_invisible, logger="log")
    window_list = list()

    if window_name:
        log_debug((window_name), logger="log")
        for window in get_windows():
            if window_name.lower() in window.lower():
                window_list.append(window)
    else:
        window_list = get_windows()

    for window in window_list:
        config = get_item_configuration(window)
        if show_invisible is False:
            if config.get('show') is False:
                continue

        x_pos = config.get("x_pos", 0)
        y_pos = config.get("y_pos", 0)
        name = config.get("name")

        if len(name) > 6:
            name = name[:5]
        log_debug(f"{name} : {x_pos}, {y_pos}", logger="log")


def debug_get_location_gui():
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
            name="Window Name##input", callback=debug_get_window_pos, on_enter=True
        )
        add_checkbox("Print invisible", default_value=False)



def start_development_windows():
    """
    Starts doc, debug, and logger window
    Note that logger name is "log"
    """
    add_doc_window(name="Core Documentation", x_pos=0, y_pos=800)
    end()

    add_debug_window(name="Debug", x_pos=0, y_pos=300)
    end()

    with window(name="Logger", width=300, height=300, x_pos=500, y_pos=0):
        add_logger(name="log", width=300, height=300, parent="Logger")
        # debug_get_location_gui()
    set_log_level(mvTRACE, logger="log")