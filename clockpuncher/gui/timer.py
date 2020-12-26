""" Contains module for timer face """
import datetime
from enum import Enum
from typing import Dict, List, Union

import dearpygui.core as c
import dearpygui.simple as s

from clockpuncher.gui.base_gui import BaseGUI


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

        self.line_trigger = self._line_trigger()

        for key, value in self.line_trigger.items():
            setattr(self, key, value)

    def _line_trigger(
        self,
    ) -> Dict[str, callable]:
        """
        This holds the specific values to render all lines for the numbers
        :return: callable dict
        """
        return {
            "top": lambda: self.regular_line(
                x_offset=3, direction=Direction.up, tag="top"
            ),
            "top_left": lambda: self.regular_line(y_offset=3, tag="top_left"),
            "top_right": lambda: self.regular_line(
                x_offset=66, y_offset=3, direction=Direction.right, tag="top_right"
            ),
            "center": lambda: self.regular_line(
                x_offset=13, y_offset=64.5, direction=Direction.center, tag="center"
            ),
            "bottom_left": lambda: self.regular_line(y_offset=66.6, tag="bottom_left"),
            "bottom_right": lambda: self.regular_line(
                x_offset=66,
                y_offset=66.6,
                direction=Direction.right,
                tag="bottom_right",
            ),
            "bottom": lambda: self.regular_line(
                x_offset=3, y_offset=129.6, direction=Direction.down, tag="bottom"
            ),
        }

    def get(self, attribute: str):
        """
        Fetches attribute by string name
        :param attribute: attribute name
        :return: the attribute value
        """
        return getattr(self, attribute)

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
            draw_line = self.get(line)
            draw_line()
        self.prior_num = num

    def clear(self):
        """
        Clears the canvas drawing
        """
        c.clear_drawing(self.canvas)

    def regular_line(
        self,
        x_offset=0,
        y_offset=0,
        direction: Direction = Direction.left,
        tag: str = None,
    ):
        """
        Creates a line in the number box in the digital clock format
        :param x_offset: x translation magnitude, as x gets larger, the line shifts right
        :param y_offset: y translation magnitude, as y increases the line shifts down
        :param direction: Which type of line to render
        :param tag: string to tag the line with
        :return: drawn polygon on self.canvas
        """
        if tag is None:
            tag = str(direction.value)
        translate = lambda coords: [coords[0] + x_offset, coords[1] + y_offset]

        if direction == Direction.left:
            position = [(0.0, 0.0), (20.0, 20.0), (20.0, 60.0), (0.0, 80.0)]
        elif direction == Direction.up:
            position = [(0.0, 0.0), (20.0, 20.0), (60.0, 20.0), (80.0, 0.0)]
        elif direction == Direction.down:
            position = [(80.0, 20.0), (60.0, 0.0), (20.0, 0.0), (0.0, 20.0)]
        elif direction == Direction.right:
            position = [(20.0, 0.0), (0.0, 20.0), (0.0, 60.0), (20.0, 80.0)]
        else:
            position = [
                (0.0, 10.0),
                (10.0, 0.0),
                (50.0, 0.0),
                (60.0, 10.0),
                (50.0, 20.0),
                (10.0, 20.0),
                (0.0, 10.0),
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
        c.add_drawing(self.canvas, width=90, height=150, parent=group)

    def run(self):
        """
        A very basic stand-aloen run method to show what this looks like by default
        :return: General number display example
        """
        base = BaseGUI(development=True)
        base.initialize_base_screens()
        window_args = dict(
            autosize=False,
            height=250,
            width=900,
            x_pos=0,
            y_pos=0,
            no_title_bar=True,
            no_resize=True,
            no_move=True,
            no_background=False,
        )
        with s.window("single_cell", **window_args):
            with s.group(name="timergroup", horizontal=True):
                self.build_number_box()

        self.render(Digit.num_8, 8)

        c.start_dearpygui()


class Timer:
    """
    Creates a 6 cell timer display with create_window, render, and run commands
    """

    def __init__(self, color=None):
        if color is None:
            color = [120, 255, 120]
        self.sec_0 = Number(canvas="sec_0", color=color)
        self.sec_1 = Number(canvas="sec_1", color=color)
        self.min_0 = Number(canvas="min_0", color=color)
        self.min_1 = Number(canvas="min_1", color=color)
        self.hour_0 = Number(canvas="hour_0", color=color)
        self.hour_1 = Number(canvas="hour_1", color=color)
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
            # Handles > 24 hour timedelta
            time_str = time_str.split(" ")[-1]

        if 14 <= len(time_str) <= 15:
            # handles sub-second resolution
            time_str = time_str.split(".")[0]
        result_list = time_str.split(":")

        if len(time_str) == 7:
            # Handles sub 10 hour timers
            result_list[0] = "0" + result_list[0]

        return result_list

    def render(
        self, *_args, time_to_render: Union[datetime.datetime, datetime.timedelta]
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
            autosize=True,
            height=150,
            width=540,
            x_pos=0,
            y_pos=0,
            no_title_bar=True,
            no_resize=True,
            no_move=True,
            no_background=True,
            no_scrollbar=True,
        )

        for kwarg, value in kwargs.items():
            window_args[kwarg] = value

        with s.window("timer##display", **window_args):
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


timer_display = Timer()
number = Number()

if __name__ == "__main__":
    Timer().run()
    # Number().run()
