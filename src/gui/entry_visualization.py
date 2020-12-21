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
        self.chart = lambda: c.add_pie_series(
            "##PieChart1##demo", "PieChart1", self.data, self.labels, 0.5, 0.5, 0.5
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

        c.clear_plot("##PieChart1##demo")
        self.chart()

    def task_chart(self, data: List[float], labels: List[str]) -> None:
        """
        Creates task chart window using base data
        :return: None
        """
        # c.
        self.data = data
        self.labels = labels
        self.chart()
        c.add_same_line()

        c.set_plot_xlimits("##PieChart1##demo", 0, 1)
        c.set_plot_ylimits("##PieChart1##demo", 0, 1)
