""" gui for visualizing entries """
from typing import List

import dearpygui.core as c


class Chart:
    """
    Defines a simple pie-chart for project task breakdown visualization
    """

    def __init__(self):
        self.data = [(0.4), (0.1), (0.5)]
        self.labels = ["one", "two", "three"]
        self.plot_label = "##TaskChart"
        self.chart = lambda: c.add_pie_series(
            self.plot_label, "TaskPieChart", self.data, self.labels, 0.5, 0.5, 0.5
        )

    def update_chart(self, data: List[float], labels: List[str]) -> None:
        """
        Updates data and labels and updates Pie chart
        :param data: List of floats
        :param labels: List of labels
        :return: None but updates chart
        """
        self.data = data
        self.labels = labels

        c.clear_plot(self.plot_label)
        self.chart()

    def task_chart(self, data: List[float], labels: List[str]) -> None:
        """
        Creates task chart window using base data
        :return: None
        """
        # c.
        self.data = data
        self.labels = labels
        c.add_plot(
            self.plot_label,
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

        c.set_plot_xlimits(self.plot_label, 0, 1)
        c.set_plot_ylimits(self.plot_label, 0, 1)
