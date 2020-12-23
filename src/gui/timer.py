""" Contains module for timer face """
import datetime
from enum import Enum
from typing import List, Union

import dearpygui.core as c
import dearpygui.simple as s
from src.gui.base_gui import BaseGUI


class Direction(str, Enum):
    """
    An enum to indicate which of the 5 line types should be rendered
    """

    up = "up"
    down = "down"
    left = "left"
    right = "right"
    center = "center"


class Digit(set, Enum):
    """
    An enum that contains all the render commands for each number
    """

    num_1 = {"top_right", "bottom_right"}
    num_2 = {"top", "top_right", "center", "bottom_left", "bottom"}
    num_3 = {"top", "top_right", "center", "bottom_right", "bottom"}
    num_4 = {"top_left", "center", "top_right", "bottom_right"}
    num_5 = {"top", "top_left", "center", "bottom_right", "bottom"}
    num_6 = num_5.union({"bottom_left"})
    num_7 = {"top"}.union(num_1)
    num_8 = num_6.union({"top_right"})
    num_9 = num_7.union({"center", "top_left"})
    num_0 = num_8.difference({"center"})


class Number:
    """
    Class for creating a single 'digital' number display
    """

    def __init__(self, canvas="Drawing", color=None):
        self.canvas = canvas
        self.prior_num = None
        self.nums = Digit
        if not color:
            self.color = [120, 255, 120]
        else:
            self.color = color

        self.line_trigger = {
            "top": lambda: self.regular_line(x=3, direction=Direction.up, tag="top"),
            "top_left": lambda: self.regular_line(y=3, tag="top_left"),
            "top_right": lambda: self.regular_line(
                x=126, y=3, direction=Direction.right, tag="top_right"
            ),
            "center": lambda: self.regular_line(
                x=-12, y=81, direction=Direction.center, tag="center"
            ),
            "bottom_left": lambda: self.regular_line(y=100, tag="bottom_left"),
            "bottom_right": lambda: self.regular_line(
                x=126, y=100, direction=Direction.right, tag="bottom_right"
            ),
            "bottom": lambda: self.regular_line(
                x=123, y=224, direction=Direction.down, tag="bottom"
            ),
        }

    def render(self, new_lines, num):
        """
        Takes in draw commands and a number value, if the number is new, render new lines
        :param new_lines: New lines to render
        :param num: Prior number rendered - this is the rendered number but it could be an ID
        :return: updated canvas to render the new_lines
        """

        if num == self.prior_num:
            return
        self.clear()
        for line in new_lines:
            self.line_trigger[line]()
        self.prior_num = num

    def clear(self):
        """
        Clears the canvas drawing
        """
        c.clear_drawing(self.canvas)

    def regular_line(
        self, x=0, y=0, direction: Direction = Direction.left, tag: str = None
    ):
        """
        Creates a line in the number box in the digital clock format
        :param x: base x-coord
        :param y: base y-coord
        :param direction: Which type of line to render
        :param tag: string to tag the line with
        :return: drawn polygon on self.canvas
        """
        if tag is None:
            tag = str(direction.value)
        translate = lambda coords: [coords[0] + x, coords[1] + y]
        position = [[0, 0], [30, 30], [30, 90], [0, 120]]

        if direction == Direction.left:
            position = [[0, 0], [30, 30], [30, 90], [0, 120]]
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
            self.canvas,
            points=list(map(translate, position)),
            color=[255, 255, 255, 0],
            fill=self.color,
            tag=tag,
        )

    def build_number_box(self, group="timergroup"):
        """
        Creates a single number drawing
        :param group: Group to put drawing in
        :return: Drawing number box ready to render
        """
        c.add_drawing(self.canvas, width=125, height=225, parent=group)


class Timer:
    """
    Creates a 6 cell timer display with create_window, render, and run commands
    """

    def __init__(self):
        self.sec_0 = Number(canvas="sec_0")
        self.sec_1 = Number(canvas="sec_1")
        self.min_0 = Number(canvas="min_0")
        self.min_1 = Number(canvas="min_1")
        self.hour_0 = Number(canvas="hour_0")
        self.hour_1 = Number(canvas="hour_1")
        self.display = [
            (self.hour_0, self.hour_1),
            (self.min_0, self.min_1),
            (self.sec_0, self.sec_1),
        ]

    @staticmethod
    def process_timedelta(timedelta: datetime.timedelta) -> List[str]:
        """
        Returns a length 8 str ready for processing
        :param timedelta: Timedelta to render
        :return: 8 len string to render
        """
        time_str = str(timedelta)
        if len(time_str) > 8:
            time_str = time_str.split(" ")[-1]

        result_list = time_str.split(":")

        if len(time_str) == 7:
            result_list[0] = "0" + result_list[0]

        return result_list

    def render(
        self, *args, time_to_render: Union[datetime.datetime, datetime.timedelta]
    ):
        """
        Renders timedelta or datetime onto the display
        :return: Updated timer display
        """
        select_num = lambda number: f"num_{number}"
        if isinstance(time_to_render, datetime.timedelta):
            time_string = self.process_timedelta(time_to_render)
        else:
            time_string = time_to_render.strftime("%H_%M_%S").split("_")
        for digits_in_time, display_numbers in zip(time_string, self.display):
            for single_digit, single_cell in zip(digits_in_time, display_numbers):
                single_cell.render(Digit[select_num(single_digit)], single_digit)

    def create_timer(self, **kwargs):
        """
        Creates timer window for composing into other classes
        :param kwargs: Key words for s.window
        :return: Create timer window plus timergroup
        """
        window_args = dict(
            autosize=False,
            height=250,
            width=900,
            x_pos=0,
            y_pos=0,
            no_title_bar=True,
            no_resize=True,
            no_move=True,
            no_background=True,
        )

        for kwarg, value in kwargs.items():
            window_args[kwarg] = value

        with s.window("timer", **window_args):
            with s.group(name="timergroup", horizontal=True):
                for section in self.display:
                    for cell in section:
                        cell.build_number_box()

    def run(self, *_args, **kwargs):
        """
        Runs stand-alone timer window with render callback.
        Mostly for demo purposes
        :return: Full development window with most basic setup to run a timer
        """
        base = BaseGUI(development=True)
        base.initialize_base_screens()
        self.create_timer(**kwargs)

        # A simple render callback that sends the current time
        render_callback = lambda sender, data: self.render(
            sender, data, time_to_render=datetime.datetime.today()
        )

        c.set_render_callback(render_callback)

        c.start_dearpygui()


if __name__ == "__main__":
    Timer().run()
