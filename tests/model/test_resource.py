# Copyright (c) 2020 Software AG,
# Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA,
# and/or its subsidiaries and/or its affiliates and/or their licensors.
# Use, reproduction, transfer, publication or disclosure is prohibited except
# as specifically provided for in your License Agreement with Software AG.

import random
from unittest.mock import Mock

from c8y_api.model import CumulocityResource
from tests import RandomNameGenerator


def test_build_base_query():
    """Verify that query parameters for object selection are mapped correctly."""
    # pylint: disable=protected-access

    # supported query parameters
    base = RandomNameGenerator.random_name(1)
    kwargs = {
        # some of the below are mapped from python naming
        'type': base + '_type',
        'name': base + '_name',
        'owner': base + '_owner',
        'source': str(random.randint(1000, 9999)),
        'fragment': base + '_fragment',
        'status': base + '_status',
        'severity': base + '_severity',
        'resolved': 'True',
        'before': base + '_before',
        'after': base + '_after',
        'created_before': base + '_created_after',
        'created_after': base + '_created_after',
        'updated_before': base + '_updated_after',
        'updated_after': base + '_updated_after',
        'reverse': True,
        'page_size': random.randint(0, 10000),
        # random parameters are supported as well and will be mapped 1:1
        'random_' + base: True,
    }

    # mapped parameters (python name to API name)
    mapping = {
        'fragment': 'fragmentType',
        'created_before': 'createdTo',
        'created_after': 'createdFrom',
        'updated_before': 'lastUpdatedTo',
        'updated_after': 'lastUpdatedFrom',
        'before': 'dateTo',
        'after': 'dateFrom',
        'reverse': 'revert',
        'page_size': 'pageSize',
    }

    # expected parameters, kwargs combined with mapping
    expected_params = kwargs.copy()
    for py_key, api_key in mapping.items():
        expected_params[api_key] = expected_params.pop(py_key)

    # (1) init mock resource and build query
    resource = CumulocityResource(Mock(), 'res')
    base_query = resource._build_base_query(**kwargs)

    # -> all expected params are there
    for key, value in expected_params.items():
        assert f'{key}={value}' in base_query

    # -> query string ends with currentPage param
    assert base_query.endswith('currentPage=')
