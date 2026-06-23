#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# Unit tests for the scenes endpoint. These stub _get so they do not
# hit the live API.
#

from novant import NovantClient
from novant.models import Scene, SceneList, SceneMode

SAMPLE = {
    "scenes": [
        {
            "id": "sn.5",
            "name": "Lobby HVAC",
            "point_ids": ["s.5.9", "s.5.12"],
            "modes": [
                {
                    "id": "sn.5.1",
                    "name": "occupied",
                    "vals": {"s.5.9": 72.0, "s.5.12": 1.0},
                },
                {
                    "id": "sn.5.2",
                    "name": "unoccupied",
                    "vals": {"s.5.9": 55.0, "s.5.12": 0.0},
                },
            ],
        }
    ]
}


def _stub_get(client, captured, resp):
    def fake(path, params=None):
        captured["path"] = path
        captured["params"] = params
        return resp
    client._get = fake


def test_scenes_request_no_filter():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SAMPLE)
    res = client.scenes()
    assert isinstance(res, SceneList)
    assert captured["path"] == "/scenes"
    assert captured["params"] == {}


def test_scenes_request_with_scene_id():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SAMPLE)
    client.scenes(scene_id="sn.5")
    assert captured["params"] == {"scene_id": "sn.5"}


def test_scenes_parsing():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SAMPLE)
    res = client.scenes()
    assert len(res) == 1
    scene = res.scene("sn.5")
    assert isinstance(scene, Scene)
    assert scene.name == "Lobby HVAC"
    assert scene.point_ids == ["s.5.9", "s.5.12"]
    assert len(scene.modes) == 2


def test_scene_mode_vals_is_point_id_to_value_map():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SAMPLE)
    scene = client.scenes().scene("sn.5")
    occ = scene.mode("sn.5.1")
    assert isinstance(occ, SceneMode)
    assert occ.name == "occupied"
    # vals is a plain map of point id -> value
    assert occ.vals == {"s.5.9": 72.0, "s.5.12": 1.0}
    # value access via .vals[...] or item access on the mode
    assert occ.vals["s.5.9"] == 72.0
    assert occ["s.5.12"] == 1.0
    # mapping protocol: iterate point ids, len, None-safe get
    assert set(occ) == {"s.5.9", "s.5.12"}
    assert len(occ) == 2
    assert occ.vals.get("nope") is None


def test_scene_mode_lookup_by_id_or_int_suffix():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SAMPLE)
    scene = client.scenes().scene("sn.5")
    # full id string
    assert scene.mode("sn.5.1").name == "occupied"
    assert scene.mode("sn.5.2").name == "unoccupied"
    # integer id suffix
    assert scene.mode(1).id == "sn.5.1"
    assert scene.mode(2).id == "sn.5.2"
    # same mode resolved both ways
    assert scene.mode(1) is scene.mode("sn.5.1")
    # misses
    assert scene.mode(9) is None
    assert scene.mode("sn.5.9") is None


def test_scenes_iteration():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SAMPLE)
    scene = next(iter(client.scenes()))
    mode_names = [m.name for m in scene]
    assert mode_names == ["occupied", "unoccupied"]


def test_scenes_index_and_slice_access():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SAMPLE)
    res = client.scenes()
    # scenes and modes index positionally
    assert res[0].id == "sn.5"
    assert res[0][0].name == "occupied"
    # mode vals index by point id (map access) -> raw value
    assert res[0][0]["s.5.9"] == 72.0
    # slicing returns a plain list
    assert [s.id for s in res[0:1]] == ["sn.5"]
    assert [m.name for m in res[0][0:2]] == ["occupied", "unoccupied"]


def test_scenes_lookup_miss_returns_none():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SAMPLE)
    res = client.scenes()
    assert res.scene("nope") is None
    assert res.scene("sn.5").mode("nope") is None
    assert res.scene("sn.5").mode("sn.5.1").vals.get("nope") is None
