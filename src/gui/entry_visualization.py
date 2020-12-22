""" Module for pie chart and table GUI elements """
from typing import List

import dearpygui.core as c

from models import Entry


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

    # def

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

    def create_chart(self, data: List[float], labels: List[str]) -> None:
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


class EntryTable:
    """
    Table for Listing most recent time entries
    """

    def create_table(self, input_data: List[Entry]) -> None:
        """
        Creates table widget with name Entries##table
        :param input_data: Initial data to create table with
        :return: Table loaded with entries
        """
        c.add_table(
            "Entries##table",
            headers=["Project", "Description", "Duration", "Start", "End"],
        )
        for single_entry in input_data:
            self.add_row_to_entry_table(single_entry)

    @staticmethod
    def add_row_to_entry_table(entry: Entry) -> None:
        """
        Helper to add entry to the table
        :param entry: A single entry to convert to entries table
        :return: New row attached to the Entries##table
        """
        row_data = [
            entry.project_name,
            entry.description,
            str(entry.duration)[:10],
            entry.start_time.time().strftime("%I:%M"),
            entry.end_time.time().strftime("%I:%M"),
        ]
        c.add_row("Entries##table", row_data)


task_chart = Chart()
entry_table = EntryTable()
