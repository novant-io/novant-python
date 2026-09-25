#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# Integration tests for org keys against the live API. The test org must
# contain the test project bound to secret/test.key.
#

import pytest

from novant import NovantClient, NovantErr
from novant.models import Project, ZoneList


def test_org_key_requires_proj_id(org_client):
    with pytest.raises(NovantErr) as e:
        org_client.zones()
    assert e.value.code == 400


def test_org_key_per_call_proj_id(org_client, proj_id):
    p = org_client.project(proj_id=proj_id)
    assert isinstance(p, Project)
    assert p.proj_id == proj_id
    res = org_client.zones(proj_id=proj_id)
    assert isinstance(res, ZoneList)
    assert res.proj_id == proj_id


def test_org_key_client_default_proj_id(org_client, proj_id):
    client = NovantClient(api_key=org_client.api_key, proj_id=proj_id)
    assert client.zones().proj_id == proj_id
    assert client.explorer_ops().proj_id == proj_id


def test_org_key_unknown_proj_id(org_client):
    with pytest.raises(NovantErr) as e:
        org_client.zones(proj_id=1)
    assert e.value.code == 404


def test_project_key_own_proj_id(client, proj_id):
    assert client.zones(proj_id=proj_id).proj_id == proj_id


def test_project_key_other_proj_id(client, proj_id):
    with pytest.raises(NovantErr) as e:
        client.zones(proj_id=proj_id + 1)
    assert e.value.code in (403, 404)
