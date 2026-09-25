#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# Unit tests for proj_id handling. These stub _get, _post, and _post_csv
# so they do not hit the live API.
#

import pytest

from novant import NovantClient

# Minimal response bodies so each endpoint parses.
RESP = {
    "/project": {
        "proj_id": 4821, "proj_name": "Lumon", "area": 1, "city": "Denver, CO",
        "tz": "Denver", "usage": 0, "capacity": 0, "max_trend_years": 1,
    },
    "/assets":           {"proj_id": 4821, "currency": "USD", "assets": []},
    "/spaces":           {"proj_id": 4821, "spaces": []},
    "/zones":            {"proj_id": 4821, "zones": []},
    "/sources":          {"proj_id": 4821, "sources": []},
    "/points":           {"proj_id": 4821, "points": []},
    "/values":           {"proj_id": 4821, "values": []},
    "/trends": {
        "proj_id": 4821, "start": "", "end": "", "tz": "", "interval": "",
        "aggregate": "", "point_ids": [], "trends": [],
    },
    "/scenes":           {"proj_id": 4821, "scenes": []},
    "/schedules":        {"proj_id": 4821, "schedules": []},
    "/explorer/ops":     {"proj_id": 4821, "ops": []},
    "/explorer/sources": {"proj_id": 4821, "sources": []},
    "/explorer/points":  {"proj_id": 4821, "points": []},
}

# Every project endpoint method, invoked with its minimum required args.
CALLS = [
    ("project",           lambda c, **kw: c.project(**kw)),
    ("assets",            lambda c, **kw: c.assets(**kw)),
    ("spaces",            lambda c, **kw: c.spaces(**kw)),
    ("zones",             lambda c, **kw: c.zones(**kw)),
    ("sources",           lambda c, **kw: c.sources(**kw)),
    ("points",            lambda c, **kw: c.points(source_id="s.1", **kw)),
    ("values",            lambda c, **kw: c.values(source_id="s.1", **kw)),
    ("trends",            lambda c, **kw: c.trends(["s.1.1"], date="2026-01-01", **kw)),
    ("scenes",            lambda c, **kw: c.scenes(**kw)),
    ("schedules",         lambda c, **kw: c.schedules(**kw)),
    ("write",             lambda c, **kw: c.write("s.1.1", 72, **kw)),
    ("write_batch",       lambda c, **kw: c.write_batch([{"point_id": "s.1.1", "value": 72}], **kw)),
    ("explorer_scan",     lambda c, **kw: c.explorer_scan("bacnet-scan", **kw)),
    ("explorer_learn",    lambda c, **kw: c.explorer_learn("abc123", **kw)),
    ("explorer_ops",      lambda c, **kw: c.explorer_ops(**kw)),
    ("explorer_sources",  lambda c, **kw: c.explorer_sources(**kw)),
    ("explorer_points",   lambda c, **kw: c.explorer_points("abc123", **kw)),
    ("import_zones",      lambda c, **kw: c.import_zones("id\n", **kw)),
    ("import_spaces",     lambda c, **kw: c.import_spaces("id\n", **kw)),
    ("import_assets",     lambda c, **kw: c.import_assets("id\n", **kw)),
    ("import_sources",    lambda c, **kw: c.import_sources("id\n", **kw)),
    ("import_source_map", lambda c, **kw: c.import_source_map("id\n", **kw)),
    ("import_trends",     lambda c, **kw: c.import_trends("ts\n", **kw)),
]


def _stub(client, captured):
    """Replace all transport methods to capture params."""
    def fake_get(path, params=None):
        captured["params"] = params
        return RESP[path]
    def fake_post(path, params):
        captured["params"] = params
        return {"status": "ok"}
    def fake_post_csv(path, csv_data, params=None):
        captured["params"] = params
        return {"status": "ok"}
    client._get = fake_get
    client._post = fake_post
    client._post_csv = fake_post_csv


def test_all_project_methods_covered():
    public = {
        n for n in dir(NovantClient)
        if not n.startswith(("_", "org_")) and callable(getattr(NovantClient, n))
    }
    assert public == {name for name, _ in CALLS}


@pytest.mark.parametrize("name,call", CALLS)
def test_proj_id_omitted_by_default(name, call):
    client = NovantClient(api_key="x")
    captured = {}
    _stub(client, captured)
    call(client)
    assert "proj_id" not in (captured["params"] or {})


@pytest.mark.parametrize("name,call", CALLS)
def test_proj_id_per_call(name, call):
    client = NovantClient(api_key="x")
    captured = {}
    _stub(client, captured)
    call(client, proj_id=4821)
    assert captured["params"]["proj_id"] == 4821


@pytest.mark.parametrize("name,call", CALLS)
def test_proj_id_client_default(name, call):
    client = NovantClient(api_key="x", proj_id=4821)
    captured = {}
    _stub(client, captured)
    call(client)
    assert captured["params"]["proj_id"] == 4821


@pytest.mark.parametrize("name,call", CALLS)
def test_proj_id_per_call_overrides_client_default(name, call):
    client = NovantClient(api_key="x", proj_id=4821)
    captured = {}
    _stub(client, captured)
    call(client, proj_id=5307)
    assert captured["params"]["proj_id"] == 5307


def test_proj_id_does_not_leak_between_calls():
    client = NovantClient(api_key="x", proj_id=4821)
    captured = {}
    _stub(client, captured)
    client.zones(proj_id=5307)
    client.zones()
    assert captured["params"] == {"proj_id": 4821}


def test_proj_id_with_other_params():
    client = NovantClient(api_key="x")
    captured = {}
    _stub(client, captured)
    client.write("s.1.3", 25.0, level=8, proj_id=4821)
    assert captured["params"] == {
        "proj_id": 4821, "point_id": "s.1.3", "value": "25.0", "level": "8",
    }
