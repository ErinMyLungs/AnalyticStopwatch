# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import dataclasses

from hypothesis import given
from hypothesis import strategies as st

import clockpuncher.models as models
from clockpuncher.tests.utils import INT8_RANGE


@given(
    _cls=st.none(),
    init=st.booleans(),
    repr=st.booleans(),
    eq=st.booleans(),
    order=st.booleans(),
    unsafe_hash=st.booleans(),
    frozen=st.booleans(),
)
def test_fuzz_dataclass(_cls, init, repr, eq, order, unsafe_hash, frozen):
    dataclasses.dataclass(
        _cls=_cls,
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        frozen=frozen,
    )


@given(
    id=st.one_of(st.none(), st.integers()),
    project_name=st.text(),
    description=st.text(),
    start_time=st.datetimes(),
    end_time=st.datetimes(),
)
def test_fuzz_Entry(id, project_name, description, start_time, end_time):
    models.Entry(
        id=id,
        project_name=project_name,
        description=description,
        start_time=start_time,
        end_time=end_time,
    )


@given(id=st.one_of(st.none(), st.integers()))
def test_fuzz_ModelHelperMixin(id):
    result_model = models.BaseModelClass(id=id)
    assert result_model.id == id


@given(
    id=st.one_of(st.none(), st.integers(**INT8_RANGE)),
    weekly_hour_allotment=st.integers(**INT8_RANGE),
    monthly_frequency=st.integers(**INT8_RANGE),
    rate=st.integers(**INT8_RANGE),
    client=st.text(),
    project_name=st.text(),
)
def test_fuzz_Project_valid(
    id, weekly_hour_allotment, monthly_frequency, rate, client, project_name
):
    models.Project(
        id=id,
        weekly_hour_allotment=weekly_hour_allotment,
        monthly_frequency=monthly_frequency,
        rate=rate,
        client=client,
        project_name=project_name,
    )
