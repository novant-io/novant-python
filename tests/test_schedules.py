#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# Unit tests for the schedules endpoint and schedule-string decoding.
# These stub _get so they do not hit the live API.
#

import datetime

import pytest

from novant import NovantClient
from novant.models import (
    Schedule, ScheduleList, ScheduleRule, _parse_schedule,
)

SAMPLE = {
    "schedules": [
        {
            "id": "sch.1",
            "name": "Business Hours",
            "schedule": "weekdays 8:00-17:00, sat 9:00-12:00",
            "active_mode_ids": ["sn.1.1", "sn.2.1"],
            "inactive_mode_ids": ["sn.1.2", "sn.2.2"],
        }
    ]
}

# reference weekdays for the dates used below
WED = datetime.date(2026, 6, 24)   # weekday() == 2
SAT = datetime.date(2026, 6, 27)   # weekday() == 5
SUN = datetime.date(2026, 6, 28)   # weekday() == 6


def _stub_get(client, captured, resp):
    def fake(path, params=None):
        captured["path"] = path
        captured["params"] = params
        return resp
    client._get = fake


def _client():
    client = NovantClient(api_key="x")
    _stub_get(client, {}, SAMPLE)
    return client


def _dt(date, h, m):
    return datetime.datetime(date.year, date.month, date.day, h, m)


# -- request / parsing -------------------------------------------------------

def test_schedules_request_with_and_without_id():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SAMPLE)
    res = client.schedules()
    assert isinstance(res, ScheduleList)
    assert captured["path"] == "/schedules"
    assert captured["params"] == {}
    client.schedules(schedule_id="sch.1")
    assert captured["params"] == {"schedule_id": "sch.1"}


def test_schedule_fields_and_raw_string_preserved():
    sched = _client().schedules().schedule("sch.1")
    assert isinstance(sched, Schedule)
    assert sched.name == "Business Hours"
    assert sched.schedule == "weekdays 8:00-17:00, sat 9:00-12:00"
    assert sched.active_mode_ids == ["sn.1.1", "sn.2.1"]
    assert sched.inactive_mode_ids == ["sn.1.2", "sn.2.2"]


def test_schedule_decodes_rules():
    sched = _client().schedules()[0]
    assert len(sched) == 2
    weekdays, sat = sched.rules
    assert weekdays.start_day == 0 and weekdays.end_day == 4
    assert weekdays.start == datetime.time(8, 0)
    assert weekdays.end == datetime.time(17, 0)
    assert weekdays.days == frozenset({0, 1, 2, 3, 4})
    assert sat.start_day == 5 and sat.end_day == 5
    assert sat.start == datetime.time(9, 0)
    assert sat.end == datetime.time(12, 0)


# -- active() ---------------------------------------------------------------

def test_active_within_weekday_window():
    sched = _client().schedules()[0]
    assert sched.active(_dt(WED, 10, 0)) is True


def test_inactive_before_start_and_at_exclusive_end():
    sched = _client().schedules()[0]
    assert sched.active(_dt(WED, 7, 59)) is False   # before 8:00
    assert sched.active(_dt(WED, 17, 0)) is False    # end is exclusive


def test_active_within_saturday_window():
    sched = _client().schedules()[0]
    assert sched.active(_dt(SAT, 10, 0)) is True
    assert sched.active(_dt(SAT, 12, 0)) is False    # exclusive end


def test_inactive_on_unscheduled_day():
    sched = _client().schedules()[0]
    assert sched.active(_dt(SUN, 10, 0)) is False


def test_active_defaults_current_time_to_now():
    sched = _client().schedules()[0]
    # omitting current_time resolves None -> datetime.now() before evaluating;
    # returning a bool (rather than raising on None.date()) proves the default
    # path ran. Correctness against specific times is covered by other tests.
    assert isinstance(sched.active(), bool)
    # rule-level matches() also defaults to now
    assert isinstance(sched.rules[0].matches(), bool)


def test_tolerance_shifts_start_earlier():
    sched = _client().schedules()[0]
    tol = datetime.timedelta(minutes=30)
    # 7:30 is outside 8:00-17:00 normally, but in-window with 30m tolerance
    assert sched.active(_dt(WED, 7, 30)) is False
    assert sched.active(_dt(WED, 7, 30), tolerance=tol) is True
    assert sched.active(_dt(WED, 7, 29), tolerance=tol) is False
    # tolerance never extends the end
    assert sched.active(_dt(WED, 17, 0), tolerance=tol) is False


# -- day-range wrap ---------------------------------------------------------

def test_day_range_wraps_across_weekend():
    (rule,) = _parse_schedule("fri-mon 8:00-9:00")
    assert rule.start_day == 4 and rule.end_day == 0
    assert rule.days == frozenset({4, 5, 6, 0})
    assert rule._day_contains(SAT.weekday()) is True   # sat
    assert rule._day_contains(SUN.weekday()) is True   # sun
    assert rule._day_contains(0) is True               # mon
    assert rule._day_contains(2) is False              # wed


# -- parsing errors ---------------------------------------------------------

@pytest.mark.parametrize("bad", [
    "",                      # empty
    "weekdays",              # missing time range
    "funday 8:00-9:00",      # bad weekday
    "weekdays 8-9",          # bad time format
    "weekdays 25:00-9:00",   # hour out of range
])
def test_invalid_schedule_strings_raise(bad):
    with pytest.raises(ValueError):
        _parse_schedule(bad)


# -- lookup / iteration -----------------------------------------------------

def test_lookup_and_index():
    res = _client().schedules()
    assert res.schedule("sch.1").id == "sch.1"
    assert res.schedule("nope") is None
    assert res[0].id == "sch.1"
    assert [r.start for r in res[0]] == [datetime.time(8, 0), datetime.time(9, 0)]
