#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# Unit tests for values param encoding. These stub _get so they do not
# hit the live API.
#

from novant import NovantClient
from novant.models import ValueList


def _stub_get(client, captured):
    """Replace _get to capture args and return an empty values response."""
    def fake(path, params=None):
        captured["path"] = path
        captured["params"] = params
        return {"values": []}
    client._get = fake


def test_values_by_source_id():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured)
    res = client.values(source_id="s.2")
    assert isinstance(res, ValueList)
    assert captured["path"] == "/values"
    assert captured["params"] == {"source_id": "s.2"}


def test_values_by_source_ids():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured)
    client.values(source_ids=["s.2", "s.3"])
    assert captured["params"] == {"source_ids": "s.2,s.3"}


def test_values_source_ids_with_point_types():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured)
    client.values(source_ids=["s.2", "s.3"], point_types=["zone_air_temp_sensor"])
    assert captured["params"] == {
        "source_ids": "s.2,s.3",
        "point_types": "zone_air_temp_sensor",
    }
