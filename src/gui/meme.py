""" Meme module """
from pathlib import Path

import dearpygui.core as c
import dearpygui.simple as s
from src.gui.base_gui import BaseGUI


class Meme(BaseGUI):
    def __init__(self, **kwargs):
        super().__init__(title="Meme", **kwargs)

    def run(self, width=700, height=700, **kwargs):
        window_args = dict(
            autosize=True,
            no_resize=True,
            no_title_bar=True,
            no_close=True,
            no_background=True,
            no_scrollbar=True,
        )
        font_path = list(Path().glob("**/*Input*"))
        c.add_additional_font(str(font_path[0]), size=50)
        with s.window(name="foo", x_pos=112, y_pos=0, width=475, **window_args):
            c.add_text(name="What Gives People")
            c.add_drawing(name="underline##1", width=460, height=5)
            c.draw_line(
                drawing="underline##1",
                p1=[0, 5],
                p2=[475, 5],
                color=[255, 255, 255, 255],
                thickness=20,
            )
        with s.window(
            name="second line", x_pos=112, y_pos=75, width=475, **window_args
        ):
            c.add_text("Feelings of Power")
            c.add_drawing(name="underline##2", width=460, height=5)
            c.draw_line(
                drawing="underline##2",
                p1=[0, 5],
                p2=[475, 5],
                color=[255, 255, 255, 255],
                thickness=20,
            )
        with s.window(
            "labels", x_pos=0, y_pos=150, width=300, height=550, **window_args
        ):
            c.add_text("Money")
            c.add_text("Status")
            c.add_text("Making a meme in DPG")

        window_args["autosize"] = False
        with s.window(
            name="chart", x_pos=0, y_pos=150, width=700, height=550, **window_args
        ):
            c.add_plot(
                name="##meme",
                no_legend=True,
                no_mouse_pos=True,
                xaxis_no_gridlines=True,
                yaxis_no_gridlines=True,
                xaxis_no_tick_labels=True,
                xaxis_no_tick_marks=True,
                yaxis_no_tick_labels=True,
                show_annotations=True,
                show_drag_points=False,
                scale_max=100,
            )

            c.add_annotation(
                "##meme", text="Money", x=-1.4, y=2.8, xoffset=-1, yoffset=0
            )
            c.add_annotation(
                "##meme", text="Status", x=-1.4, y=2, xoffset=-1, yoffset=0
            )
            c.add_annotation(
                "##meme", text="Making", x=-1.4, y=1.4, xoffset=-1, yoffset=0
            )
            c.add_annotation(
                "##meme", text="A meme", x=-1.4, y=1.2, xoffset=-1, yoffset=0
            )
            c.add_annotation(
                "##meme", text="in DPG", x=-1.4, y=1.0, xoffset=-1, yoffset=0
            )
            c.set_plot_xlimits("##meme", xmin=-30, xmax=80)
            c.set_plot_ylimits("##meme", ymin=0.6, ymax=3.3)
            c.add_bar_series(
                plot="##meme", name="dpg", x=[20], y=[2], horizontal=True, weight=0.5
            )
            c.add_bar_series(
                plot="##meme",
                name="status",
                x=[75],
                y=[1.2],
                horizontal=True,
                weight=0.5,
            )
            c.add_bar_series(
                plot="##meme", name="DPG", x=[15], y=[2.8], horizontal=True, weight=0.5
            )
            c.add_drag_line(plot="##meme", name="", thickness=4, show_label=False)
        c.start_dearpygui()


if __name__ == "__main__":
    meme = Meme()
    meme.run()
