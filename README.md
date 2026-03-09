# novant-python

Python SDK for the [Novant](https://novant.io) API.

## Installation

```bash
pip install novant
```

Or install from source:

```bash
git clone https://github.com/novant-io/novant-python.git
cd novant-python
pip install -e .
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

## Pandas & NumPy

Install with optional pandas support:

```bash
pip install novant[pandas]
```

Convert values and trends directly to DataFrames:

```python
# Values as DataFrame
result = client.values(source_id="s.2")
df = result.to_dataframe()

# Trends as DataFrame with DatetimeIndex
trends = client.trends(point_ids=["s.2.4", "s.2.5"], date="2026-03-09")
df = trends.to_dataframe()

# Trends as NumPy array
arr = trends.to_numpy()
```

## API

### Client

```python
client = NovantClient(api_key="ak_xxx", timeout=30)
```

Client arguments:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `api_key` | — | API key string |
| `timeout` | `30` | Request timeout in seconds |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `project()` | `Project` | Get project metadata |
| `assets(asset_ids=None)` | `AssetList` | List assets |
| `spaces(space_ids=None)` | `SpaceList` | List spaces |
| `zones(zone_ids=None)` | `ZoneList` | List zones |
| `sources(source_ids=None, bound_only=False)` | `SourceList` | List sources |
| `points(source_id=None, asset_id=None, point_ids=None)` | `PointList` | List points for a source or asset |
| `values(source_id=None, asset_id=None, point_ids=None)` | `ValueList` | Get current values |
| `trends(point_ids, ...)` | `TrendData` | Get historical trend data |
| `write(point_id, value, level=None)` | `WriteResult` | Write a value to a point |
| `import_zones(csv_data)` | `dict` | Import zones from CSV |
| `import_spaces(csv_data)` | `dict` | Import spaces from CSV |
| `import_assets(csv_data)` | `dict` | Import assets from CSV |
| `import_sources(csv_data)` | `dict` | Import sources from CSV |
| `import_source_map(csv_data)` | `dict` | Import source point mappings from CSV |
| `import_trends(csv_data, mode=None)` | `dict` | Import trend data from CSV |

See the [Novant API docs](https://docs.novant.io/api) for full parameter details.

## Error Handling

API errors raise `NovantErr`:

```python
from novant import NovantClient, NovantErr

client = NovantClient(api_key="ak_xxx")
try:
    client.project()
except NovantErr as e:
    print(e.code)     # HTTP status code
    print(e.message)  # Error message
```