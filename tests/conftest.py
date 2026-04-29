#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#

import os
import pytest

from novant import NovantClient

KEY_PATH = os.path.join(
    os.path.dirname(__file__), "..", "secret", "test.key"
)


@pytest.fixture(scope="session")
def client():
    if not os.path.exists(KEY_PATH):
        pytest.skip(f"test API key not found at {KEY_PATH}")
    with open(KEY_PATH) as f:
        api_key = f.read().strip()
    return NovantClient(api_key=api_key)


@pytest.fixture(scope="session")
def any_source_id(client):
    """Pick any source id from the test project, preferring bound sources."""
    sources = client.sources(bound_only=True)
    if len(sources) == 0:
        sources = client.sources()
    if len(sources) == 0:
        pytest.skip("test project has no sources")
    return next(iter(sources)).id
