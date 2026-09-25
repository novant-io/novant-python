# novant-python

Python SDK for the [Novant](https://novant.io) API.

Full documentation at [docs.novant.io/sdk/python](https://docs.novant.io/sdk/python).

## Installation

```bash
pip install novant
```

## Quick Start

```python
from novant import NovantClient

client = NovantClient(api_key="ak_xxx")

# Get project info
proj = client.project()
print(proj.city)        # "Richmond, VA"
print(proj.tz)          # "New_York"

# List assets
for asset in client.assets():
    print(asset.name, asset.type)

# Read current values
for v in client.values(source_id="s.2"):
    print(v.id, v.val, v.status)

# Get trend data
for row in client.trends(point_ids=["s.2.4", "s.2.5"], date="2026-03-09"):
    print(row.ts, row.values)
```

## Organization Keys

Project keys (`ak_xxx`) are bound to a single project. Organization keys
(`ak_org_xxx`) can access any project in the organization, and must specify
which project to act on with `proj_id`:

```python
client = NovantClient(api_key="ak_org_xxx")

# List all projects in the organization
for p in client.org_projects():
    print(p.proj_id, p.proj_name)

# Pass proj_id per call
zones = client.zones(proj_id=4821)

# Or set a default proj_id for all calls
client = NovantClient(api_key="ak_org_xxx", proj_id=4821)
zones = client.zones()
```

All responses from project endpoints include the `proj_id` they were
served from:

```python
print(zones.proj_id)    # 4821
```

## Development

```bash
git clone https://github.com/novant-io/novant-python.git
cd novant-python
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

The `dev` extra installs `pytest`, `build`, and `twine` — everything
needed for testing and publishing.

## Testing

Tests are integration tests that run against the live Novant API. Place a
test project's API key at `secret/test.key`, then:

```bash
pytest
```

Tests are skipped automatically if `secret/test.key` is missing.

Organization key tests additionally require an org key at
`secret/test.org_key`, for an organization that contains the test project.
These tests are skipped if the key is missing.