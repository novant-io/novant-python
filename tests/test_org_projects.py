#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# Unit tests for the org projects endpoint and error parsing. These stub
# _get so they do not hit the live API.
#

from novant import NovantClient, NovantErr
from novant.models import OrgProject, OrgProjectList

SAMPLE = {
    "projects": [
        {
            "proj_id": 4821,
            "proj_name": "Lumon Industries",
            "city": "Denver, CO",
            "tz": "Denver",
            "area": 145000,
        },
        {
            "proj_id": 5307,
            "proj_name": "Lumon Annex",
            "city": "Boulder, CO",
            "tz": "Denver",
        },
    ]
}


def _stub_get(client, captured, resp):
    def fake(path, params=None):
        captured["path"] = path
        captured["params"] = params
        return resp
    client._get = fake


def test_org_projects_request():
    client = NovantClient(api_key="x")
    captured = {}
    _stub_get(client, captured, SAMPLE)
    res = client.org_projects()
    assert isinstance(res, OrgProjectList)
    assert captured["path"] == "/org/projects"
    assert captured["params"] is None


def test_org_projects_ignores_client_proj_id():
    client = NovantClient(api_key="x", proj_id=4821)
    captured = {}
    _stub_get(client, captured, SAMPLE)
    client.org_projects()
    assert captured["params"] is None


def test_org_projects_parsing():
    client = NovantClient(api_key="x")
    _stub_get(client, {}, SAMPLE)
    res = client.org_projects()
    assert len(res) == 2
    p = res.project(4821)
    assert isinstance(p, OrgProject)
    assert p.proj_name == "Lumon Industries"
    assert p.city == "Denver, CO"
    assert p.tz == "Denver"
    assert p.area == 145000
    # area is optional
    assert res.project(5307).area is None


def test_org_projects_iteration_and_index_access():
    client = NovantClient(api_key="x")
    _stub_get(client, {}, SAMPLE)
    res = client.org_projects()
    assert [p.proj_id for p in res] == [4821, 5307]
    assert res[1].proj_name == "Lumon Annex"
    assert [p.proj_id for p in res[0:2]] == [4821, 5307]


def test_org_projects_lookup_miss_returns_none():
    client = NovantClient(api_key="x")
    _stub_get(client, {}, SAMPLE)
    assert client.org_projects().project(9999) is None


def test_err_message_from_msg():
    e = NovantErr(400, {"msg": "Organization API keys require proj_id argument."})
    assert e.code == 400
    assert e.message == "Organization API keys require proj_id argument."
    assert str(e) == e.message


def test_err_message_fallbacks():
    assert NovantErr(500, {"message": "boom"}).message == "boom"
    assert NovantErr(500, {"error": "boom"}).message == "boom"
    assert NovantErr(502, None).message == "HTTP 502"
