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
result = client.assets()
for asset in result.assets:
    print(asset.name, asset.type)

# Read current values
result = client.values(source_id="s.2")
for v in result.values:
    print(v.id, v.val, v.status)

# Get trend data
trends = client.trends(
    point_ids=["s.2.4", "s.2.5"],
    date="2026-03-09"
)
for row in trends.trends:
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

### NovantClient(api_key)

Create a new client with your API key.

### Project

- `project()` → `Project` — Get project metadata

### Assets, Spaces, Zones, Sources

- `assets(asset_ids=None)` → `AssetList` — List assets
- `spaces(space_ids=None)` → `SpaceList` — List spaces
- `zones(zone_ids=None)` → `ZoneList` — List zones
- `sources(source_ids=None, bound_only=False)` → `SourceList` — List sources

### Points & Values

- `points(source_id=None, asset_id=None, point_ids=None)` → `PointList` — List points for a source or asset
- `values(source_id=None, asset_id=None, point_ids=None)` → `ValueList` — Get current values for points

### Trends

- `trends(point_ids, start_date=None, end_date=None, date=None, tz=None, interval=None, aggregate=None)` → `TrendData` — Get historical trend data

Interval options: `auto`, `5min`, `15min`, `30min`, `1hr`, `1day`, `1mo`, `raw`

Aggregate options: `auto`, `mean`, `sum`, `min`, `max`, `diff`

### Write

- `write(point_id, value, level=None)` → `WriteResult` — Write a value to a point. Pass `value=None` to clear a priority hold.

### Import

- `import_zones(csv_data)` — Import zones from CSV
- `import_spaces(csv_data)` — Import spaces from CSV
- `import_assets(csv_data)` — Import assets from CSV
- `import_sources(csv_data)` — Import sources from CSV
- `import_source_map(csv_data)` — Import source point mappings from CSV
- `import_trends(csv_data, mode=None)` — Import trend data from CSV (`merge`, `append`, or `prepend`)

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