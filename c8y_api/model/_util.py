# Copyright (c) 2020 Software AG,
# Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA,
# and/or its subsidiaries and/or its affiliates and/or their licensors.
# Use, reproduction, transfer, publication or disclosure is prohibited except
# as specifically provided for in your License Agreement with Software AG.

from datetime import datetime, timedelta, timezone
from dateutil import parser


class _DateUtil(object):

    @staticmethod
    def now_timestring() -> str:
        """Provide an ISO timestring for the current time."""
        return _DateUtil.to_timestring(_DateUtil.now())

    @staticmethod
    def to_timestring(dt: datetime):
        """Format a datetime as ISO timestring."""
        return dt.isoformat(timespec='milliseconds')

    @staticmethod
    def to_datetime(string):
        """Parse an ISO timestring as datetime object."""
        return parser.parse(string)

    @staticmethod
    def now():
        """Provide the current time as datetime object."""
        return datetime.now(timezone.utc)

    @staticmethod
    def ensure_timestring(time):
        """Ensure that a given timestring reflects a proper, timezone aware date/time.
        A static string 'now' will be converted to the current datetime in UTC."""
        if isinstance(time, datetime):
            if not time.tzinfo:
                raise ValueError("A specified datetime needs to be timezone aware.")
            return _DateUtil.to_timestring(time)
        if time == 'now':
            return _DateUtil.now_timestring()
        return time  # assuming it is a timestring

    @staticmethod
    def ensure_timedelta(time):
        """Ensure that a given object is a timedelta object."""
        if not isinstance(time, timedelta):
            raise ValueError("A specified duration needs to be a timedelta object.")
        return time
