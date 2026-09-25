#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# Unit tests for the explorer endpoints. These stub _get and _post so
# they do not hit the live API.
#

from novant import NovantClient
from novant.models import (
    ExplorerOp,
    ExplorerOpList,
    ExplorerPoint,
    ExplorerPointList,
    ExplorerSource,
    ExplorerSourceList,
)

OPS = {
    "proj_id": 4821,
    "ops": [
        {
            "id": "0a1b2c3d4e5f6a7b",
            "op": "bacnet-scan",
            "state": "active",
            "node_id": "NA00000000V1",
            "started": "2026-08-08T14:22:08Z",
        },
        {
            "id": "1b2c3d4e5f6a7b8c",
            "op": "bacnet-learn",
            "state": "queued",
            "node_id": "NA00000000V1",
            "source_id": "c1578fe370e4",
        },
        {
            "id": "2c3d4e5f6a7b8c9d",
            "op": "bacnet-scan",
            "state": "ok",
            "node_id": "NA00000000V1",
            "started": "2026-08-08T13:55:02Z",
            "finished": "2026-08-08T13:56:14Z",
            "summary": "Found 12 sources",
        },
        {
            "id": "3d4e5f6a7b8c9d0e",
            "op": "jasper-scan",
            "state": "error",
            "node_id": "NA00000000V1",
            "started": "2026-08-08T13:40:11Z",
            "finished": "2026-08-08T13:40:53Z",
            "err_code": "E12",
        },
    ]
}

SOURCES = {
    "proj_id": 4821,
    "sources": [
        {
            "id": "c1578fe370e4",
            "name": "ECB-600-3",
            "type": "bacnet",
            "addr": "10.0.1.3:47808",
            "device_id": 102,
            "path": None,
            "vendor": "ACME",
            "model": "AHU-B15",
            "version": "2.07",
            "firmware": "1.0.12",
            "desc": "AHU-3",
            "last_scan": "2026-07-13T22:02:18.193Z",
            "last_learn": None,
            "point_count": None,
        },
        {
            "id": "e1ca7fadc524",
            "name": "ECB-VAV-01",
            "type": "bacnet",
            "addr": "10.0.2.1:47808",
            "device_id": 200,
            "path": None,
            "vendor": "ACME",
            "model": "VAV-HX1",
            "version": "1.25",
            "firmware": "1.3.40",
            "desc": "VAV-01",
            "last_scan": "2026-07-13T22:02:18.193Z",
            "last_learn": None,
            "point_count": None,
        },
    ]
}

POINTS = {
    "proj_id": 4821,
    "source": {
        "id": "23a769452950",
        "name": "ECB-600-1",
        "type": "bacnet",
        "addr": "10.0.1.1:47808",
        "device_id": 100,
        "path": None,
        "vendor": "ACME",
        "model": "AHU-B15",
        "version": "2.07",
        "firmware": "1.0.12",
        "desc": "AHU-1",
        "last_scan": "2026-07-13T22:02:18.193Z",
        "last_learn": "2026-07-13T22:09:47.95Z",
        "point_count": 3,
    },
    "points": [
        {
            "name": "Discharge Air Temperature",
            "addr": "ai.1",
            "type": "generic",
            "unit": "°F",
            "enum": None,
            "desc": None,
            "sample": None,
        },
        {
            "name": "Discharge Air Pressure",
            "addr": "av.2",
            "type": "generic",
            "unit": "inH₂O",
            "enum": None,
            "desc": None,
            "sample": None,
        },
        {
            "name": "Cooling",
            "addr": "av.3",
            "type": "generic",
            "unit": "%",
            "enum": None,
            "desc": None,
            "sample": None,
        },
    ],
}

QUEUED = {"status": "ok", "op_id": "0a1b2c3d4e5f6a7b"}


def _stub_get(client, captured, resp):
    def fake(path, params=None):
        captured["path"] = path
        captured["params"] = params
        return resp
    client._get = fake


def _stub_post(client, captured, resp):
    def fake(path, params):
        captured["path"] = path
        captured["params"] = params
        return resp
    client._post = fake


######
# Scan
######

def test_explorer_scan_request():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured, QUEUED)
    res = client.explorer_scan(op="bacnet-scan")
    assert captured["path"] == "/explorer/scan"
    assert captured["params"] == {"op": "bacnet-scan"}
    assert res == QUEUED


def test_explorer_scan_with_node_id():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured, QUEUED)
    client.explorer_scan(op="bacnet-scan", node_id="NA00000000V1")
    assert captured["params"] == {
        "op": "bacnet-scan",
        "node_id": "NA00000000V1",
    }


def test_explorer_scan_op_params_encoded_as_strings():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured, QUEUED)
    client.explorer_scan(
        op="bacnet-scan", port=47808, range_low=0, range_high=4194303,
    )
    assert captured["params"] == {
        "op": "bacnet-scan",
        "port": "47808",
        "range_low": "0",
        "range_high": "4194303",
    }


def test_explorer_scan_list_params_join_with_commas():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured, QUEUED)
    client.explorer_scan(
        op="bacnet-find",
        ip_addrs=["10.0.1.1", "10.0.1.2"],
        max_time="5min",
    )
    assert captured["params"] == {
        "op": "bacnet-find",
        "ip_addrs": "10.0.1.1,10.0.1.2",
        "max_time": "5min",
    }
    # a pre-joined string passes through unchanged
    client.explorer_scan(op="kaiterra-find", uuids="aaaa,bbbb", credential="kt")
    assert captured["params"] == {
        "op": "kaiterra-find",
        "uuids": "aaaa,bbbb",
        "credential": "kt",
    }


def test_explorer_scan_bool_params_encoded_as_true_false():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured, QUEUED)
    client.explorer_scan(
        op="jasper-scan", ip_addr="10.0.0.5", credential="niagara", tls=True,
    )
    assert captured["params"]["tls"] == "true"
    client.explorer_scan(
        op="jasper-scan", ip_addr="10.0.0.5", credential="niagara", tls=False,
    )
    assert captured["params"]["tls"] == "false"


def test_explorer_scan_omits_none_params():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured, QUEUED)
    client.explorer_scan(op="bacnet-scan", port=None, range_low=0)
    assert captured["params"] == {"op": "bacnet-scan", "range_low": "0"}


######
# Learn
######

def test_explorer_learn_request():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured, QUEUED)
    res = client.explorer_learn(source_id="c1578fe370e4")
    assert captured["path"] == "/explorer/learn"
    assert captured["params"] == {"source_id": "c1578fe370e4"}
    assert res["op_id"] == "0a1b2c3d4e5f6a7b"


def test_explorer_learn_with_node_id():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured, QUEUED)
    client.explorer_learn(source_id="c1578fe370e4", node_id="NA00000000V1")
    assert captured["params"] == {
        "source_id": "c1578fe370e4",
        "node_id": "NA00000000V1",
    }


######
# Ops
######

def test_explorer_ops_request():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, OPS)
    res = client.explorer_ops()
    assert isinstance(res, ExplorerOpList)
    assert captured["path"] == "/explorer/ops"
    assert captured["params"] is None


def test_explorer_ops_parsing():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, OPS)
    res = client.explorer_ops()
    assert res.proj_id == 4821
    assert len(res) == 4
    op = res.op("2c3d4e5f6a7b8c9d")
    assert isinstance(op, ExplorerOp)
    assert op.op == "bacnet-scan"
    assert op.state == "ok"
    assert op.node_id == "NA00000000V1"
    assert op.started == "2026-08-08T13:55:02Z"
    assert op.finished == "2026-08-08T13:56:14Z"
    assert op.summary == "Found 12 sources"
    assert op.err_code is None


def test_explorer_op_learn_carries_source_id():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, OPS)
    op = client.explorer_ops().op("1b2c3d4e5f6a7b8c")
    assert op.op == "bacnet-learn"
    assert op.source_id == "c1578fe370e4"
    # queued ops have not started or finished
    assert op.started is None
    assert op.finished is None


def test_explorer_op_state_helpers():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, OPS)
    res = client.explorer_ops()
    active = res.op("0a1b2c3d4e5f6a7b")
    queued = res.op("1b2c3d4e5f6a7b8c")
    ok = res.op("2c3d4e5f6a7b8c9d")
    err = res.op("3d4e5f6a7b8c9d0e")
    # only ok and error are terminal
    assert [o.done for o in (queued, active, ok, err)] == [
        False, False, True, True,
    ]
    assert [o.ok for o in (queued, active, ok, err)] == [
        False, False, True, False,
    ]
    assert [o.error for o in (queued, active, ok, err)] == [
        False, False, False, True,
    ]
    # err_code is set only on failures
    assert err.err_code == "E12"
    assert ok.err_code is None


def test_explorer_ops_iteration_and_index_access():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, OPS)
    res = client.explorer_ops()
    assert [o.state for o in res] == ["active", "queued", "ok", "error"]
    assert res[0].id == "0a1b2c3d4e5f6a7b"
    assert [o.id for o in res[0:2]] == [
        "0a1b2c3d4e5f6a7b", "1b2c3d4e5f6a7b8c",
    ]


def test_explorer_ops_lookup_miss_returns_none():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, OPS)
    assert client.explorer_ops().op("nope") is None


def test_explorer_ops_empty():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, {"proj_id": 4821, "ops": []})
    res = client.explorer_ops()
    assert len(res) == 0
    assert res.op("0a1b2c3d4e5f6a7b") is None


######
# Sources
######

def test_explorer_sources_request():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SOURCES)
    res = client.explorer_sources()
    assert isinstance(res, ExplorerSourceList)
    assert captured["path"] == "/explorer/sources"
    assert captured["params"] is None


def test_explorer_sources_parsing():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SOURCES)
    res = client.explorer_sources()
    assert res.proj_id == 4821
    assert len(res) == 2
    s = res.source("c1578fe370e4")
    assert isinstance(s, ExplorerSource)
    assert s.name == "ECB-600-3"
    assert s.type == "bacnet"
    assert s.addr == "10.0.1.3:47808"
    assert s.device_id == 102
    assert s.vendor == "ACME"
    assert s.model == "AHU-B15"
    assert s.version == "2.07"
    assert s.firmware == "1.0.12"
    assert s.desc == "AHU-3"
    assert s.last_scan == "2026-07-13T22:02:18.193Z"
    # not yet learned
    assert s.path is None
    assert s.last_learn is None
    assert s.point_count is None


def test_explorer_sources_missing_metadata_defaults_to_none():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, {
        "proj_id": 4821,
        "sources": [{"id": "abc123", "name": "Dev", "type": "bacnet"}]
    })
    s = client.explorer_sources().source("abc123")
    assert s.addr is None
    assert s.device_id is None
    assert s.vendor is None
    assert s.last_scan is None
    assert s.point_count is None


def test_explorer_sources_iteration_and_index_access():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SOURCES)
    res = client.explorer_sources()
    assert [s.name for s in res] == ["ECB-600-3", "ECB-VAV-01"]
    assert res[1].id == "e1ca7fadc524"
    assert [s.id for s in res[0:1]] == ["c1578fe370e4"]


def test_explorer_sources_lookup_miss_returns_none():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SOURCES)
    assert client.explorer_sources().source("nope") is None


######
# Points
######

def test_explorer_points_request():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, POINTS)
    res = client.explorer_points(source_id="23a769452950")
    assert isinstance(res, ExplorerPointList)
    assert captured["path"] == "/explorer/points"
    assert captured["params"] == {"source_id": "23a769452950"}


def test_explorer_points_parsing():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, POINTS)
    res = client.explorer_points(source_id="23a769452950")
    assert res.proj_id == 4821
    assert len(res) == 3
    p = res.point("ai.1")
    assert isinstance(p, ExplorerPoint)
    assert p.name == "Discharge Air Temperature"
    assert p.type == "generic"
    assert p.unit == "°F"
    assert p.enum is None
    assert p.desc is None
    assert p.sample is None


def test_explorer_points_includes_source_metadata():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, POINTS)
    res = client.explorer_points(source_id="23a769452950")
    assert isinstance(res.source, ExplorerSource)
    assert res.source.id == "23a769452950"
    assert res.source.name == "ECB-600-1"
    # learned sources carry last_learn and point_count
    assert res.source.last_learn == "2026-07-13T22:09:47.95Z"
    assert res.source.point_count == len(res)


def test_explorer_points_iteration_and_index_access():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, POINTS)
    res = client.explorer_points(source_id="23a769452950")
    assert [p.addr for p in res] == ["ai.1", "av.2", "av.3"]
    assert res[2].name == "Cooling"
    assert [p.addr for p in res[0:2]] == ["ai.1", "av.2"]


def test_explorer_points_lookup_miss_returns_none():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, POINTS)
    assert client.explorer_points(source_id="23a769452950").point("nope") is None


def test_explorer_points_empty_until_learned():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, {
        "proj_id": 4821,
        "source": {
            "id": "23a769452950",
            "name": "ECB-600-1",
            "type": "bacnet",
            "last_learn": None,
            "point_count": None,
        },
        "points": [],
    })
    res = client.explorer_points(source_id="23a769452950")
    assert len(res) == 0
    assert res.source.last_learn is None
    assert res.source.point_count is None
