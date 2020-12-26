""" Module for pie chart and table GUI elements """
import datetime
from collections import defaultdict
from typing import List

import dearpygui.core as c
from clockpuncher.models import Entry


class Chart:
    """
    Defines a simple pie-chart for project task breakdown visualization
    """

    def __init__(self):
        self.data = [(0.4), (0.1), (0.5)]
        self.labels = ["one", "two", "three"]
        self.plot_label = "##TaskChart"
        self.chart = lambda: c.add_pie_series(
            self.plot_label, "TaskPieChart", self.data, self.labels, 0.5, 0.4, 0.4
        )
        self.prior_id = None

    def render(self, entries: List[Entry]) -> None:
        """
        Render method that checks for ID change before rerunning calculations
        :param entries: List of entries to display
        :return: None but calls update chart on change
        """

        if id(entries) == self.prior_id:
            return

        self.prior_id = id(entries)
        project_dict = defaultdict(datetime.timedelta)
        total_duration = datetime.timedelta()
        for entry in entries:
            total_duration += entry.duration
            project_dict[entry.project_name] += entry.duration

        labels, data = list(), list()
        for project, time in project_dict.items():
            labels.append(project)
            data.append((time / total_duration))

        self.update_chart(data, labels)

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

    def create_chart(self, data: List[float] = None, labels: List[str] = None) -> None:
        """
        Creates task chart window using base data
        :return: None
        """
        # c.
        if data is not None:
            self.data = data
        if labels is not None:
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

    def __init__(self):
        self.prior_id = None
        self.table_name = "Entries##table"

    def render(self, entries: List[Entry]) -> None:
        """
        Checks if entries in parent have updated
        If so it'll clear and re-render the table
        :param entries: Entries passed in parent class
        :return: Updated table with new data
        """

        if id(entries) == self.prior_id:
            return
        self.prior_id = id(entries)
        c.clear_table(self.table_name)
        for entry in entries:
            self.add_row_to_entry_table(entry)

    def create_table(self, input_data: List[Entry]) -> None:
        """
        Creates table widget with name Entries##table
        :param input_data: Initial data to create table with
        :return: Table loaded with entries
        """
        self.prior_id = id(input_data)
        c.add_table(
            self.table_name,
            headers=["Project", "Description", "Duration", "Start", "End"],
        )
        for single_entry in input_data:
            self.add_row_to_entry_table(single_entry)

    def add_row_to_entry_table(self, entry: Entry) -> None:
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
        c.add_row(self.table_name, row_data)


task_chart = Chart()
entry_table = EntryTable()
