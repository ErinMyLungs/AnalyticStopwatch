""" gui for visualizing entries """

import numpy as np

import dearpygui.core as c
import dearpygui.simple as s


class Chart:
    def __init__(self):
        self.data = [(0.4), (0.1), (0.5)]
        self.labels = ["one", "two", "three"]
        self.chart = lambda: c.add_pie_series(
            "##PieChart1##demo", "PieChart1", self.data, self.labels, 0.5, 0.5, 0.5
        )

    def update_chart(self, data, labels):
        self.data = data
        self.labels = labels

        c.clear_plot("##PieChart1##demo")
        self.chart()

    def task_chart(self, data, labels):
        """
        Creates task chart window
        :return:
        """
        # c.
        self.data = data
        self.labels = labels
        c.add_plot(
            "##PieChart1##demo",
            no_mouse_pos=True,
            xaxis_no_gridlines=True,
            xaxis_no_tick_marks=True,
            xaxis_no_tick_labels=True,
            yaxis_no_gridlines=True,
            yaxis_no_tick_marks=True,
            yaxis_no_tick_labels=True,
            width=300,
            height=300,
        )
        c.add_same_line()

        c.set_plot_xlimits("##PieChart1##demo", 0, 1)
        c.set_plot_ylimits("##PieChart1##demo", 0, 1)


class TimerDebug:
    def create_win(self):
        with s.window("Timer info"):
            c.add_button(name="timerinfo##button", label="Get Timer Info")

    pass
