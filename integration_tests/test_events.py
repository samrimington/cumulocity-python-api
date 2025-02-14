# Copyright (c) 2020 Software AG,
# Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA,
# and/or its subsidiaries and/or its affiliates and/or their licensors.
# Use, reproduction, transfer, publication or disclosure is prohibited except
# as specifically provided for in your License Agreement with Software AG.

# pylint: disable=redefined-outer-name

from __future__ import annotations

from logging import Logger
from typing import List

import pytest

from c8y_api import CumulocityApi
from c8y_api.model import Event, Device
from tests import RandomNameGenerator


@pytest.fixture(scope='session')
def sample_device(logger: Logger, live_c8y: CumulocityApi) -> Device:
    """Provide an sample device, jsut for testing purposes."""

    typename = RandomNameGenerator.random_name()
    device = Device(live_c8y, type=typename, name=typename).create()
    logger.info(f"Created test device #{device.id}, name={device.name}")

    yield device

    device.delete()
    logger.info(f"Deleted test device #{device.id}")


@pytest.fixture(scope='session')
def sample_events(factory, sample_device) -> List[Event]:
    """Provide a set of sample Event instances that will automatically
    be removed after the test function."""
    typename = RandomNameGenerator.random_name()
    result = []
    for i in range(1, 6):
        event = Event(type=f'{typename}_{i}', text=f'{typename} text', source=sample_device.id,
                      time='2020-12-31T11:33:55Z')
        result.append(factory(event))
    return result


def test_CRUD(live_c8y: CumulocityApi, sample_device: Device):  # noqa (case)
    """Verify that basic CRUD functionality works."""

    typename = RandomNameGenerator.random_name()
    event = Event(c8y=live_c8y, type=typename, text=f'{typename} text', time='now', source=sample_device.id)

    created_event = event.create()
    try:
        # 1) assert correct creation
        assert created_event.id
        assert created_event.type == typename
        assert typename in created_event.text
        assert created_event.time  # auto generated by API
        assert created_event.creation_time  # auto generated by Cumulocity

        # 2) update updatable fields
        created_event.text = f'{typename} updated'
        updated_event = created_event.update()
        # -> text should be updated in db
        assert updated_event.text == created_event.text

        # 3) use apply_to
        model_event = Event(c8y=live_c8y, text='some text')
        model_event.apply_to(created_event.id)
        # -> text should be updated in db
        updated_event = live_c8y.events.get(created_event.id)
        assert updated_event.text == 'some text'

    finally:
        created_event.delete()

    # 4) assert deletion
    with pytest.raises(KeyError) as e:
        live_c8y.events.get(created_event.id)
        assert created_event.id in str(e)


def test_CRUD_2(live_c8y: CumulocityApi, sample_device: Device):  # noqa (case)
    """Verify that basic CRUD functionality via the API works."""

    typename = RandomNameGenerator.random_name()
    event1 = Event(c8y=live_c8y, type=typename, text=f'{typename} text', source=sample_device.id)
    event2 = Event(c8y=live_c8y, type=typename, text=f'{typename} text', source=sample_device.id)

    # 1) create multiple events and read from Cumulocity
    live_c8y.events.create(event1, event2)
    events = live_c8y.events.get_all(type=typename)
    event_ids = [e.id for e in events]
    assert len(events) == 2

    try:
        # 2) assert correct creation
        for event in events:
            assert event.id
            assert event.type == typename
            assert typename in event.text
            assert event.time  # auto generated by API
            assert event.creation_time  # auto generated by Cumulocity

        # 3) update updatable fields
        for event in events:
            event.text = 'new text'
        live_c8y.events.update(*events)
        events = live_c8y.events.get_all(type=typename)
        assert len(events) == 2

        # 4) assert updates
        for event in events:
            assert event.text == 'new text'

        # 5) apply updates
        model = Event(text='another update', simple_attribute='value')
        live_c8y.events.apply_to(model, *event_ids)

        # -> the new text should be in all events
        events = live_c8y.events.get_all(type=typename)
        assert len(events) == 2
        assert all(e.text == 'another update' for e in events)

    finally:
        live_c8y.events.delete(*event_ids)

    # 6) assert deletion
    assert not live_c8y.events.get_all(type=typename)


def test_filter_by_update_time(live_c8y: CumulocityApi, sample_device, sample_events: List[Event]):
    """Verify that filtering by lastUpdatedTime works as expected."""

    event = sample_events[0]

    # created events should all have different update times
    # -> we use the middle/pivot element for queries
    updated_datetimes = [a.updated_datetime for a in sample_events]
    updated_datetimes.sort()
    pivot = updated_datetimes[len(updated_datetimes)//2]

    before_events = live_c8y.events.get_all(source=event.source, updated_before=pivot)
    after_events = live_c8y.events.get_all(source=event.source, updated_after=pivot)

    # -> selected events should match the update times from 'before'
    # upper boundary, i.e. before/to timestamp is exclusive -> does not include pivot
    before_datetimes = list(filter(lambda x: x < pivot, updated_datetimes))
    result_datetimes = [a.updated_datetime for a in before_events]
    assert sorted(result_datetimes) == sorted(before_datetimes)

    # -> selected events should match the update times from 'after'
    # lower boundary, i.e. after/from timestamp is inclusive -> includes pivot
    after_datetimes = list(filter(lambda x: x >= pivot, updated_datetimes))
    result_datetimes = [a.updated_datetime for a in after_events]
    assert sorted(result_datetimes) == sorted(after_datetimes)
