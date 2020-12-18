""" database models used in database.py """
import datetime
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class ModelHelperMixin:
    """
    A simple helper class that defines ID and the to_dict method for inserting into DB
    """
    id: Optional[int]

    def to_dict(self):
        """
        Simple wrapper for asdict from dataclass module
        :return: dataclass as dictionary representation
        """
        class_dict = asdict(self)
        if self.id is None:
            class_dict.pop("id")

        return class_dict


@dataclass
class Entry(ModelHelperMixin):
    """
    Defines a simple entry dataclass for db handling
    :parameter project: Project name
    :parameter description: Task description string
    :parameter start_time: start time in datetime format
    :parameter end_time: end_time, default is creation time
    """

    @property
    def duration(self):
        """
        Calculates time delta of entry
        :return: Duration of timed entry
        :type return: datetime.timedelta
        """
        return self.end_time - self.start_time

    project_name: str
    description: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    _duration = duration


@dataclass
class Project(ModelHelperMixin):
    """
    Defines a simple projects dataclass
    """

    weekly_hour_allotment: int
    monthly_frequency: int
    rate: int
    client: str
    project_name: str
