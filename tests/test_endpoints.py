#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# Integration tests run against the live API. Tests verify response shape
# (types and required-field presence via model parsing) rather than
# specific values.
#

from datetime import date

import pytest

from novant.models import (
    Project,
    Asset, AssetList,
    Space, SpaceList,
    Zone, ZoneList,
    Source, SourceList,
    Point, PointList,
    PointValue, ValueList,
    TrendData, TrendRow,
)


def test_project(client):
    p = client.project()
    assert isinstance(p, Project)
    assert isinstance(p.proj_id, int)
    assert isinstance(p.proj_name, str)
    assert isinstance(p.tz, str)


def test_assets(client):
    res = client.assets()
    assert isinstance(res, AssetList)
    assert isinstance(res.currency, str)
    for a in res:
        assert isinstance(a, Asset)
        assert isinstance(a.id, str)
        assert isinstance(a.name, str)
        assert isinstance(a.type, str)


def test_spaces(client):
    res = client.spaces()
    assert isinstance(res, SpaceList)
    for s in res:
        assert isinstance(s, Space)
        assert isinstance(s.id, str)
        assert isinstance(s.name, str)
        assert isinstance(s.type, str)


def test_zones(client):
    res = client.zones()
    assert isinstance(res, ZoneList)
    for z in res:
        assert isinstance(z, Zone)
        assert isinstance(z.id, str)
        assert isinstance(z.name, str)
        assert isinstance(z.type, str)


def test_sources(client):
    res = client.sources()
    assert isinstance(res, SourceList)
    for s in res:
        assert isinstance(s, Source)
        assert isinstance(s.id, str)
        assert isinstance(s.name, str)
        assert isinstance(s.type, str)


def test_sources_bound_only(client):
    res = client.sources(bound_only=True)
    assert isinstance(res, SourceList)
    for s in res:
        assert s.bound is True


def test_points_by_source(client, any_source_id):
    res = client.points(source_id=any_source_id)
    assert isinstance(res, PointList)
    assert res.source_id == any_source_id
    for p in res:
        assert isinstance(p, Point)
        assert isinstance(p.id, str)
        assert isinstance(p.kind, str)
        assert isinstance(p.writable, bool)


def test_points_by_space(client):
    spaces = client.spaces()
    if len(spaces) == 0:
        pytest.skip("test project has no spaces")
    space_id = next(iter(spaces)).id
    res = client.points(space_id=space_id)
    assert isinstance(res, PointList)
    assert res.space_id == space_id


def test_points_with_point_types_filter(client, any_source_id):
    res = client.points(
        source_id=any_source_id,
        point_types=["zone_air_temp_sensor", "discharge_air_temp_sensor"],
    )
    assert isinstance(res, PointList)


def test_values_by_source(client, any_source_id):
    res = client.values(source_id=any_source_id)
    assert isinstance(res, ValueList)
    assert res.source_id == any_source_id
    for v in res:
        assert isinstance(v, PointValue)
        assert isinstance(v.id, str)
        assert isinstance(v.status, str)


def test_values_by_space(client):
    spaces = client.spaces()
    if len(spaces) == 0:
        pytest.skip("test project has no spaces")
    space_id = next(iter(spaces)).id
    res = client.values(space_id=space_id)
    assert isinstance(res, ValueList)
    assert res.space_id == space_id


def test_values_with_point_types_filter(client, any_source_id):
    res = client.values(
        source_id=any_source_id,
        point_types=["zone_air_temp_sensor"],
    )
    assert isinstance(res, ValueList)


def test_trends(client, any_source_id):
    points = client.points(source_id=any_source_id)
    if len(points) == 0:
        pytest.skip("test source has no points")
    point_id = next(iter(points)).id
    today = date.today().isoformat()
    res = client.trends(point_ids=[point_id], date=today)
    assert isinstance(res, TrendData)
    assert isinstance(res.start, str)
    assert isinstance(res.end, str)
    assert isinstance(res.tz, str)
    assert isinstance(res.interval, str)
    assert isinstance(res.aggregate, str)
    assert isinstance(res.point_ids, list)
    for row in res:
        assert isinstance(row, TrendRow)
        assert isinstance(row.ts, str)
        assert isinstance(row.values, dict)
