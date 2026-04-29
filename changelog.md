# Changelog

## Version 0.2 (working)
* Add `space_id` and `point_types` options to `points()` and `values()`
* Fix `PointList` and `ValueList` parsing to handle responses scoped by
  `asset_id` or `space_id` (parent metadata fields are now optional, and
  `asset_id`, `asset_name`, `space_id`, `space_name`, `source_ids` are
  exposed)
* Add integration test suite under `tests/` (run with `pytest`)

## Version 0.1 (9-Mar-2026)
* Initial MVP
