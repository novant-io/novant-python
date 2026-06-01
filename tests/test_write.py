#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# Unit tests for write param encoding. These stub _post so they do not
# hit the live API or mutate any project state.
#

import pytest

from novant import NovantClient


def _stub_post(client, captured):
    """Replace _post to capture args and return a {"status": "ok"} response."""
    def fake(path, params):
        captured["path"] = path
        captured["params"] = params
        return {"status": "ok"}
    client._post = fake


def test_write_basic():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured)
    res = client.write("s.1.3", 25.0)
    assert res == {"status": "ok"}
    assert captured["path"] == "/write"
    assert captured["params"] == {"point_id": "s.1.3", "value": "25.0"}


def test_write_with_level():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured)
    client.write("s.1.3", 25.0, level=8)
    assert captured["params"] == {
        "point_id": "s.1.3", "value": "25.0", "level": "8",
    }


def test_write_with_expires():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured)
    client.write("s.1.4", 20.0, expires="1hr")
    assert captured["params"] == {
        "point_id": "s.1.4", "value": "20.0", "expires": "1hr",
    }


def test_write_with_level_and_expires():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured)
    client.write("s.1.3", 25.0, level=8, expires="30min")
    assert captured["params"] == {
        "point_id": "s.1.3", "value": "25.0", "level": "8", "expires": "30min",
    }


def test_write_null_clears_hold():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured)
    client.write("s.1.3", None)
    assert captured["params"] == {"point_id": "s.1.3", "value": "null"}


def test_write_batch_encodes_bracket_notation():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured)
    res = client.write_batch([
        {"point_id": "s.1.3", "value": 25.0, "level": 8},
        {"point_id": "s.1.4", "value": 20.0, "expires": "1hr"},
    ])
    assert captured["path"] == "/write"
    assert captured["params"] == {
        "writes[0][point_id]": "s.1.3",
        "writes[0][value]": "25.0",
        "writes[0][level]": "8",
        "writes[1][point_id]": "s.1.4",
        "writes[1][value]": "20.0",
        "writes[1][expires]": "1hr",
    }
    assert res == {"status": "ok"}


def test_write_batch_null_clears_hold():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured)
    client.write_batch([{"point_id": "s.1.3", "value": None}])
    assert captured["params"] == {
        "writes[0][point_id]": "s.1.3",
        "writes[0][value]": "null",
    }


def test_write_batch_empty_raises():
    client = NovantClient(api_key="x")
    with pytest.raises(ValueError):
        client.write_batch([])


def test_write_batch_missing_point_id_raises():
    client = NovantClient(api_key="x")
    with pytest.raises(ValueError):
        client.write_batch([{"value": 1.0}])


def test_write_batch_missing_value_raises():
    client = NovantClient(api_key="x")
    with pytest.raises(ValueError):
        client.write_batch([{"point_id": "s.1.3"}])
