#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# Unit tests for write param encoding. These stub _post so they do not
# hit the live API or mutate any project state.
#

from novant import NovantClient
from novant.models import WriteResult


def _stub_post(client, captured):
    """Replace _post to capture args and return a fake WriteResult dict."""
    def fake(path, params):
        captured["path"] = path
        captured["params"] = params
        return {
            "point_id": params.get("point_id"),
            "level": 16,
            "source_id": "s.1",
            "value": params.get("value"),
            "status": "ok",
        }
    client._post = fake


def test_write_basic():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_post(client, captured)
    res = client.write("s.1.3", 25.0)
    assert isinstance(res, WriteResult)
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
