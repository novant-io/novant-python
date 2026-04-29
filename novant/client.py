#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# History:
#   9 Mar 2026  Andy Frank  Creation
#

import json
import urllib.request
import urllib.parse
import urllib.error
import base64
import gzip

from . import __version__
from .err import NovantErr
from .models import (
    Project, AssetList, SpaceList, ZoneList, SourceList,
    PointList, ValueList, TrendData, WriteResult,
)

#############################################################################
# NovantClient
#############################################################################

class NovantClient:
    """Client for the Novant REST API."""

    def __init__(self, api_key, timeout=30):
        """Create a new NovantClient instance.

        Args:
            api_key: API key string (e.g. 'ak_xxx')
            timeout: request timeout in seconds (default 30)
        """
        self.api_key = api_key
        self.base_url = "https://api.novant.io/v1"
        self.timeout = timeout

    ######
    # Project
    ######

    def project(self):
        """Get project metadata.

        Returns:
            Project
        """
        return Project._from_dict(self._get("/project"))

    ######
    # Assets
    ######

    def assets(self, asset_ids=None):
        """List assets for this project.

        Args:
            asset_ids: optional list of asset id strings to filter

        Returns:
            AssetList
        """
        params = {}
        if asset_ids is not None:
            params["asset_ids"] = ",".join(asset_ids)
        return AssetList._from_dict(self._get("/assets", params))

    ######
    # Spaces
    ######

    def spaces(self, space_ids=None):
        """List spaces for this project.

        Args:
            space_ids: optional list of space id strings to filter

        Returns:
            SpaceList
        """
        params = {}
        if space_ids is not None:
            params["space_ids"] = ",".join(space_ids)
        return SpaceList._from_dict(self._get("/spaces", params))

    ######
    # Zones
    ######

    def zones(self, zone_ids=None):
        """List zones for this project.

        Args:
            zone_ids: optional list of zone id strings to filter

        Returns:
            ZoneList
        """
        params = {}
        if zone_ids is not None:
            params["zone_ids"] = ",".join(zone_ids)
        return ZoneList._from_dict(self._get("/zones", params))

    ######
    # Sources
    ######

    def sources(self, source_ids=None, bound_only=False):
        """List sources for this project.

        Args:
            source_ids: optional list of source id strings to filter
            bound_only: if True only return bound sources

        Returns:
            SourceList
        """
        params = {}
        if source_ids is not None:
            params["source_ids"] = ",".join(source_ids)
        if bound_only:
            params["bound_only"] = "true"
        return SourceList._from_dict(self._get("/sources", params))

    ######
    # Points
    ######

    def points(self, source_id=None, asset_id=None, space_id=None,
               point_ids=None, point_types=None):
        """List points for a source, asset, or space.

        Args:
            source_id: parent source id (one of source_id, asset_id, or space_id required)
            asset_id: parent asset id (one of source_id, asset_id, or space_id required)
            space_id: parent space id (one of source_id, asset_id, or space_id required)
            point_ids: optional list of point id strings to filter
            point_types: optional list of point type strings to filter

        Returns:
            PointList
        """
        params = {}
        if source_id is not None:
            params["source_id"] = source_id
        if asset_id is not None:
            params["asset_id"] = asset_id
        if space_id is not None:
            params["space_id"] = space_id
        if point_ids is not None:
            params["point_ids"] = ",".join(point_ids)
        if point_types is not None:
            params["point_types"] = ",".join(point_types)
        return PointList._from_dict(self._get("/points", params))

    ######
    # Values
    ######

    def values(self, source_id=None, asset_id=None, space_id=None,
               point_ids=None, point_types=None):
        """Get current values for points.

        Args:
            source_id: parent source id (one of source_id, asset_id, or space_id required)
            asset_id: parent asset id (one of source_id, asset_id, or space_id required)
            space_id: parent space id (one of source_id, asset_id, or space_id required)
            point_ids: optional list of point id strings to filter
            point_types: optional list of point type strings to filter

        Returns:
            ValueList
        """
        params = {}
        if source_id is not None:
            params["source_id"] = source_id
        if asset_id is not None:
            params["asset_id"] = asset_id
        if space_id is not None:
            params["space_id"] = space_id
        if point_ids is not None:
            params["point_ids"] = ",".join(point_ids)
        if point_types is not None:
            params["point_types"] = ",".join(point_types)
        return ValueList._from_dict(self._get("/values", params))

    ######
    # Trends
    ######

    def trends(self, point_ids, start_date=None, end_date=None, date=None,
               tz=None, interval=None, aggregate=None):
        """Get historical trend data for points.

        Args:
            point_ids: list of point id strings
            start_date: start date as YYYY-MM-DD (required unless date is set)
            end_date: end date as YYYY-MM-DD (required unless date is set)
            date: single date as YYYY-MM-DD (takes precedence over start/end)
            tz: timezone for results (defaults to project timezone)
            interval: resample interval - auto|5min|15min|30min|1hr|1day|1mo|raw
            aggregate: aggregation function - auto|mean|sum|min|max|diff

        Returns:
            TrendData
        """
        params = {"point_ids": ",".join(point_ids)}
        if date is not None:
            params["date"] = date
        else:
            if start_date is not None:
                params["start_date"] = start_date
            if end_date is not None:
                params["end_date"] = end_date
        if tz is not None:
            params["tz"] = tz
        if interval is not None:
            params["interval"] = interval
        if aggregate is not None:
            params["aggregate"] = aggregate
        return TrendData._from_dict(self._get("/trends", params))

    ######
    # Write
    ######

    def write(self, point_id, value, level=None):
        """Write a value to a point.

        Args:
            point_id: point id string
            value: numeric value or None to clear priority hold
            level: optional BACnet priority level (defaults to 16)

        Returns:
            WriteResult
        """
        params = {"point_id": point_id}
        if value is None:
            params["value"] = "null"
        else:
            params["value"] = str(value)
        if level is not None:
            params["level"] = str(level)
        return WriteResult._from_dict(self._post("/write", params))

    ######
    # Import
    ######

    def import_zones(self, csv_data):
        """Import zones from CSV data.

        Args:
            csv_data: CSV string content

        Returns:
            dict with status
        """
        return self._post_csv("/import/zones", csv_data)

    def import_spaces(self, csv_data):
        """Import spaces from CSV data.

        Args:
            csv_data: CSV string content

        Returns:
            dict with status
        """
        return self._post_csv("/import/spaces", csv_data)

    def import_assets(self, csv_data):
        """Import assets from CSV data.

        Args:
            csv_data: CSV string content

        Returns:
            dict with status
        """
        return self._post_csv("/import/assets", csv_data)

    def import_sources(self, csv_data):
        """Import sources from CSV data.

        Args:
            csv_data: CSV string content

        Returns:
            dict with status
        """
        return self._post_csv("/import/sources", csv_data)

    def import_source_map(self, csv_data):
        """Import source map from CSV data.

        Args:
            csv_data: CSV string content

        Returns:
            dict with status
        """
        return self._post_csv("/import/source-map", csv_data)

    def import_trends(self, csv_data, mode=None):
        """Import trend data from CSV data.

        CSV must have 'ts' as the first column (ISO 8601 timestamps)
        followed by point id columns. Max 50 columns and 10,000 rows.

        Args:
            csv_data: CSV string content
            mode: merge (default), append, or prepend

        Returns:
            dict with status
        """
        params = {}
        if mode is not None:
            params["mode"] = mode
        return self._post_csv("/import/trends", csv_data, params)

    ##########################################################################
    # Private
    ##########################################################################

    def _get(self, path, params=None):
        """Perform a GET request."""
        url = self.base_url + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url)
        self._add_headers(req)
        return self._send(req)

    def _post(self, path, params):
        """Perform a POST request with form-encoded body."""
        url = self.base_url + path
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        self._add_headers(req)
        return self._send(req)

    def _post_csv(self, path, csv_data, params=None):
        """Perform a POST request with CSV body."""
        url = self.base_url + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = csv_data.encode("utf-8") if isinstance(csv_data, str) else csv_data
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "text/csv")
        self._add_headers(req)
        return self._send(req)

    def _add_headers(self, req):
        """Add auth, compression, and user-agent headers."""
        creds = base64.b64encode(
            (self.api_key + ":").encode("utf-8")
        ).decode("utf-8")
        req.add_header("Authorization", "Basic " + creds)
        req.add_header("Accept-Encoding", "gzip")
        req.add_header("User-Agent", "novant-python/" + __version__)

    def _send(self, req):
        """Send request and return parsed JSON response."""
        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout)
            return self._read_json(resp)
        except urllib.error.HTTPError as e:
            # attempt to parse error body
            try:
                body = self._read_json(e)
            except Exception:
                body = None
            raise NovantErr(e.code, body) from None

    def _read_json(self, resp):
        """Read and decode a response body."""
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        return json.loads(raw.decode("utf-8"))
