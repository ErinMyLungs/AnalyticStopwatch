""" Contains module for timer face """
import datetime
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


class Digit(set, Enum):
    one = {"top_right", "bottom_right"}
    two = {"top", "top_right", "center", "bottom_left", "bottom"}
    three = {"top", "top_right", "center", "bottom_right", "bottom"}
    four = {"top_left", "center", "top_right", "bottom_right"}
    five = {"top", "top_left", "center", "bottom_right", "bottom"}
    six = five.union({"bottom_left"})
    seven = {"top"}.union(one)
    eight = six.union({"top_right"})
    nine = seven.union({"center", "top_left"})
    zero = eight.difference({"center"})

    def get(self, attribute):
        return getattr(self, attribute)


class Number:
    """
    Class for creating a single 'digital' number display
    """

    def __init__(self, canvas="Drawing"):
        self.canvas = canvas
        self.prior_num = None
        self.nums = Digit

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
        self.active = set()

    def render(self, new_lines, num):

        if num == self.prior_num:
            return
        self.clear()
        for line in new_lines:
            self.line_trigger[line]()
        self.prior_num = num

    def clear(self):
        c.clear_drawing(self.canvas)

    def regular_line(
        self, x=0, y=0, direction: Direction = Direction.left, tag: str = None
    ):
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
            fill=[120, 255, 120],
            tag=tag,
        )

    def send_command(self, *_args):
        command = c.get_value("TextInput")

        exec(command)

    def build_number_box(self, x_pos=0, y_pos=0):
        # with s.window(
        #     f"{self.canvas}_window",
        #     width=0,
        #     height=0,
        #     x_pos=x_pos,
        #     y_pos=y_pos,
        #     autosize=True,
        #     no_title_bar=True,
        #     no_background=True,
        #     no_scrollbar=True,
        # ):
        # with s.group("group"):
        #     c.add_button("foo")
        #     c.add_button("foo2")
        #     c.add_same_line()

        c.add_drawing(self.canvas, width=125, height=225, parent="timergroup")

    # def run(self):
    #     with s.window(
    #         f"{self.canvas}_window",
    #         width=0,
    #         height=0,
    #         x_pos=0,
    #         y_pos=0,
    #         autosize=True,
    #         no_title_bar=True,
    #         no_background=True,
    #         no_scrollbar=True,
    #     ):
    #         # with s.group("group"):
    #         #     c.add_button("foo")
    #         #     c.add_button("foo2")
    #         #     c.add_same_line()
    #
    #         c.add_drawing(self.canvas, width=125, height=225)
    #     with s.window("commands", x_pos=600, y_pos=0, width=400, height=500):
    #         c.add_input_text(
    #             name="TextInput",
    #             label="",
    #             default_value="self.render(Digit.nine)",
    #             multiline=True,
    #             on_enter=True,
    #             callback=self.send_command,
    #             width=400,
    #             height=500,
    #         )
    #
    #     c.start_dearpygui()


class Timer(BaseGUI):
    pass

    def __init__(self):
        super().__init__(development=True)
        self.sec_0 = Number(canvas="sec_0")
        self.sec_1 = Number(canvas="sec_1")
        self.min_0 = Number(canvas="min_0")
        self.min_1 = Number(canvas="min_1")
        self.hour_0 = Number(canvas="hour_0")
        self.hour_1 = Number(canvas="hour_1")

    def render(self, *args):
        time = datetime.datetime.now().strftime("%H_%M_%S")
        (hour_0, hour_1), (min_0, min_1), (sec_0, sec_1) = time.split("_")

        units = [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]

        num_to_word = {str(idx): word for idx, word in enumerate(units)}
        self.sec_0.render(Digit[num_to_word.get(sec_0, 0)], sec_0)
        self.sec_1.render(Digit[num_to_word.get(sec_1, 0)], sec_1)
        self.min_0.render(Digit[num_to_word.get(min_0, 0)], min_0)
        self.min_1.render(Digit[num_to_word.get(min_1, 0)], min_1)
        self.hour_0.render(Digit[num_to_word.get(hour_0, 0)], hour_0)
        self.hour_1.render(Digit[num_to_word.get(hour_1, 0)], hour_1)

    def run(self, *_args):
        with s.window("timer", autosize=False, height=250, width=900):
            with s.group(name="timergroup", horizontal=True):
                self.hour_0.build_number_box()
                self.hour_1.build_number_box()
                self.min_0.build_number_box()
                self.min_1.build_number_box()
                self.sec_0.build_number_box()
                self.sec_1.build_number_box()

            # self.left.render(Digit.eight, 8)
        c.set_render_callback(self.render)
        c.start_dearpygui()


if __name__ == "__main__":
    Timer().run()
