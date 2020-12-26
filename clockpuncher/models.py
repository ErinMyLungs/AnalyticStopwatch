""" database models used in database.py """
import datetime
import inspect
import struct
from dataclasses import asdict, dataclass
from typing import Generator, Optional, Any


@dataclass
class BaseModelClass:
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

    def get(self, attribute: str):
        """
        Simple wrap around getattr to mirror dictionary .get accessing
        :param attribute: Attribute name as a str to get
        :return: Attribute value
        """
        return getattr(self, attribute)

    def set(self, attribute: str, value: Any):
        """
        Simple wrapper for setattr for easy updating
        :param attribute: attribute name as str
        :param value: value to update with
        :return: Attribute updated to value
        """
        return setattr(self, attribute, value)

    def _check_if_annotation_matches(self) -> Generator:
        """
        Basic generator to iterate through attributes and check for match.

        This is so if overriding __post_init__ with class specific validation it'll be more modular
        :return: generator of attribute_name, type_annotation, and if the attribute value matches
        """
        for attribute_name, type_annotation in inspect.getfullargspec(
            self.__class__
        ).annotations.items():
            if attribute_name in {"return", "id"}:
                continue
            yield attribute_name, type_annotation, isinstance(
                self.get(attribute_name), type_annotation
            )

    def __post_init__(self):
        """
        Validates that all attributes except ID match their type annotation
        :return: None or raises error with count, list, and info about attribute problems
        """

        create_type_error_str = lambda attr, type_anno: (
            f"\tAttribute {attr} must match type {type_anno}"
            f"\n\t\tReceived: {self.get(attr)} of type {type(self.get(attr))} type!"
        )
        create_int8_error_str = lambda attr, int8error: (
            f"\t Attribute {attr} cannot be converted to int8 (value: {self.get(attr)})"
            f"\n\t\t struct.error - {int8error.args[0]}"
        )

        attribute_fail_list = list()
        for (
            attribute_name,
            type_annotation,
            type_match_check,
        ) in self._check_if_annotation_matches():
            if type_match_check is False:
                if (type_annotation is datetime.datetime) and (
                    isinstance(self.get(attribute_name), str)
                ):
                    try:
                        coerced_datetime_check = datetime.datetime.fromisoformat(
                            self.get(attribute_name)
                        )
                        if isinstance(coerced_datetime_check, datetime.datetime):
                            self.set(attribute_name, coerced_datetime_check)
                            continue
                    except ValueError:
                        pass

                attribute_fail_list.append(
                    create_type_error_str(attribute_name, type_annotation)
                )
            elif type_annotation is int:
                try:
                    struct.pack("q", self.get(attribute_name))
                except struct.error as int8error:
                    attribute_fail_list.append(
                        create_int8_error_str(attribute_name, int8error)
                    )

        if attribute_fail_list:
            final_error_str = "\n\n".join(
                (
                    f"{len(attribute_fail_list)} invalid attributes:",
                    *attribute_fail_list,
                )
            )
            raise AttributeError(final_error_str)


@dataclass
class Entry(BaseModelClass):
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
class Project(BaseModelClass):
    """
    Defines a simple projects dataclass, has attributes -
    id, project_name, client, rate, monthly_frequency, weekly_hour_allotment
    """

    weekly_hour_allotment: int
    monthly_frequency: int
    rate: int
    client: str
    project_name: str
