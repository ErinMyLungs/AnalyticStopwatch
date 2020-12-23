""" Contains module for timer face """
from enum import Enum

import dearpygui.core as c
import dearpygui.simple as s

from src.gui.base_gui import BaseGUI


class Direction(str, Enum):
    up = "up"
    down = "down"
    left = "left"
    right = "right"
    center = "center"


class Timer(BaseGUI):
    def __init__(self):
        super().__init__(development=True)
        self.all_commands = list()

    def draw_everything(self):

        # top left
        self.regular_line()
        # bottom left
        self.regular_line(y=200)
        # top right
        self.regular_line(x=205, direction=Direction.right)
        # Bottom right
        self.regular_line(x=205, y=200, direction=Direction.right)
        # top line
        self.regular_line(x=108, y=95, direction=Direction.up)
        # center line
        self.regular_line(x=78, y=166, direction=Direction.center)
        # bottom line
        self.regular_line(x=197, y=296, direction=Direction.down)

    def regular_line(self, x=100, y=100, direction: Direction = Direction.left):
        translate = lambda coords: [coords[0] + x, coords[1] + y]
        position = [[0, 0], [30, 30], [30, 60], [0, 90]]

        if direction == Direction.left:
            position = [[0, 0], [30, 30], [30, 60], [0, 90]]
        elif direction == Direction.up:
            position = list(map(lambda coord: [coord[1], coord[0]], position))
        elif direction == Direction.down:
            position = list(map(lambda coord: [-coord[1], -coord[0]], position))
        elif direction == Direction.right:
            position = list(map(lambda coord: [-coord[0], coord[1]], position))
        else:
            position = [
                [30, 30],
                [45, 15],
                [105, 15],
                [120, 30],
                [105, 45],
                [45, 45],
                [30, 30],
            ]
        c.draw_polygon(
            "Drawing",
            points=list(map(translate, position)),
            color=[255, 255, 255, 0],
            fill=[120, 255, 120],
        )

    def send_command(self, *_args):
        command = c.get_value("TextInput")
        c.clear_drawing("Drawing")

        exec(command)

    def run(self):
        with s.window("Drawing", width=600, height=500, x_pos=0, y_pos=0):
            c.add_drawing("Drawing", width=500, height=500)
        with s.window("commands", x_pos=600, y_pos=0, width=400, height=500):
            c.add_input_text(
                name="TextInput",
                label="",
                default_value="self.draw_everything()",
                multiline=True,
                on_enter=True,
                callback=self.send_command,
                width=400,
                height=500,
            )
        c.start_dearpygui()


if __name__ == "__main__":
    Timer().run()
