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
    ExplorerOp, ExplorerOpList,
    ExplorerPoint, ExplorerPointList,
    ExplorerSource, ExplorerSourceList,
)


def test_project(client):
    p = client.project()
    assert isinstance(p, Project)
    assert isinstance(p.proj_id, int)
    assert isinstance(p.proj_name, str)
    assert isinstance(p.area, int)
    assert isinstance(p.tz, str)
    assert isinstance(p.max_trend_years, int)


def test_assets(client, proj_id):
    res = client.assets()
    assert isinstance(res, AssetList)
    assert res.proj_id == proj_id
    assert isinstance(res.currency, str)
    for a in res:
        assert isinstance(a, Asset)
        assert isinstance(a.id, str)
        assert isinstance(a.name, str)
        assert isinstance(a.type, str)


def test_spaces(client, proj_id):
    res = client.spaces()
    assert isinstance(res, SpaceList)
    assert res.proj_id == proj_id
    for s in res:
        assert isinstance(s, Space)
        assert isinstance(s.id, str)
        assert isinstance(s.name, str)
        assert isinstance(s.type, str)


def test_zones(client, proj_id):
    res = client.zones()
    assert isinstance(res, ZoneList)
    assert res.proj_id == proj_id
    for z in res:
        assert isinstance(z, Zone)
        assert isinstance(z.id, str)
        assert isinstance(z.name, str)
        assert isinstance(z.type, str)


def test_sources(client, proj_id):
    res = client.sources()
    assert isinstance(res, SourceList)
    assert res.proj_id == proj_id
    for s in res:
        assert isinstance(s, Source)
        assert isinstance(s.id, str)
        assert isinstance(s.name, str)
        assert isinstance(s.type, str)


def test_sources_bound_only(client, proj_id):
    res = client.sources(bound_only=True)
    assert isinstance(res, SourceList)
    assert res.proj_id == proj_id
    for s in res:
        assert s.bound is True


def test_points_by_source(client, proj_id, any_source_id):
    res = client.points(source_id=any_source_id)
    assert isinstance(res, PointList)
    assert res.proj_id == proj_id
    assert res.source_id == any_source_id
    for p in res:
        assert isinstance(p, Point)
        assert isinstance(p.id, str)
        assert isinstance(p.kind, str)
        assert isinstance(p.writable, bool)


def test_points_by_space(client, proj_id):
    spaces = client.spaces()
    if len(spaces) == 0:
        pytest.skip("test project has no spaces")
    space_id = next(iter(spaces)).id
    res = client.points(space_id=space_id)
    assert isinstance(res, PointList)
    assert res.proj_id == proj_id
    assert res.space_id == space_id


def test_points_with_point_types_filter(client, proj_id, any_source_id):
    res = client.points(
        source_id=any_source_id,
        point_types=["zone_air_temp_sensor", "discharge_air_temp_sensor"],
    )
    assert isinstance(res, PointList)
    assert res.proj_id == proj_id


def test_values_by_source(client, proj_id, any_source_id):
    res = client.values(source_id=any_source_id)
    assert isinstance(res, ValueList)
    assert res.proj_id == proj_id
    assert res.source_id == any_source_id
    for v in res:
        assert isinstance(v, PointValue)
        assert isinstance(v.id, str)
        assert isinstance(v.status, str)


def test_values_by_space(client, proj_id):
    spaces = client.spaces()
    if len(spaces) == 0:
        pytest.skip("test project has no spaces")
    space_id = next(iter(spaces)).id
    res = client.values(space_id=space_id)
    assert isinstance(res, ValueList)
    assert res.proj_id == proj_id
    assert res.space_id == space_id


def test_values_with_point_types_filter(client, proj_id, any_source_id):
    res = client.values(
        source_id=any_source_id,
        point_types=["zone_air_temp_sensor"],
    )
    assert isinstance(res, ValueList)
    assert res.proj_id == proj_id


def test_trends(client, proj_id, any_source_id):
    points = client.points(source_id=any_source_id)
    if len(points) == 0:
        pytest.skip("test source has no points")
    point_id = next(iter(points)).id
    today = date.today().isoformat()
    res = client.trends(point_ids=[point_id], date=today)
    assert isinstance(res, TrendData)
    assert res.proj_id == proj_id
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


# explorer_scan and explorer_learn are not covered here: they queue real
# work on an edge node and take minutes to complete.

def test_explorer_ops(client, proj_id):
    res = client.explorer_ops()
    assert isinstance(res, ExplorerOpList)
    assert res.proj_id == proj_id
    for o in res:
        assert isinstance(o, ExplorerOp)
        assert isinstance(o.id, str)
        assert isinstance(o.op, str)
        assert o.state in ("queued", "active", "ok", "error")
        assert o.done == (o.state in ("ok", "error"))


def test_explorer_sources(client, proj_id):
    res = client.explorer_sources()
    assert isinstance(res, ExplorerSourceList)
    assert res.proj_id == proj_id
    for s in res:
        assert isinstance(s, ExplorerSource)
        assert isinstance(s.id, str)
        assert isinstance(s.name, str)
        assert isinstance(s.type, str)


def test_explorer_points(client, proj_id):
    sources = client.explorer_sources()
    learned = [s for s in sources if s.last_learn is not None]
    if not learned:
        pytest.skip("test project has no learned explorer sources")
    source_id = learned[0].id
    res = client.explorer_points(source_id=source_id)
    assert isinstance(res, ExplorerPointList)
    assert res.proj_id == proj_id
    assert isinstance(res.source, ExplorerSource)
    assert res.source.id == source_id
    assert res.source.point_count == len(res)
    for p in res:
        assert isinstance(p, ExplorerPoint)
        assert isinstance(p.name, str)
        assert isinstance(p.addr, str)
