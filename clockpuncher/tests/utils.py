""" Contains utilities and constants for testing """
from clockpuncher.models import Entry, Project
from hypothesis.strategies import builds, datetimes, integers, none, text

INT8_RANGE = dict(min_value=-9223372036854775807, max_value=9223372036854775807)
PROJECT_HYPOTHESIS = dict(
    id=none(),
    rate=integers(**INT8_RANGE),
    monthly_frequency=integers(**INT8_RANGE),
    weekly_hour_allotment=integers(**INT8_RANGE),
)
ENTRY_HYPOTHESIS = {
    "id": none(),
    "project_name": text(),
    "description": text(),
    "start_time": datetimes(),
    "end_time": datetimes(),
}
project_build_strategy = builds(Project, **PROJECT_HYPOTHESIS)
entry_build_strategy = builds(Entry, **ENTRY_HYPOTHESIS)
