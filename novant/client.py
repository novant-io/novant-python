#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# History:
#   9 Mar 2026  Andy Frank  Creation
#

import base64
import gzip
import json
import urllib.error
import urllib.parse
import urllib.request

from . import __version__
from .err import NovantErr
from .models import (
    AssetList,
    ExplorerOpList,
    ExplorerPointList,
    ExplorerSourceList,
    OrgProjectList,
    PointList,
    Project,
    SceneList,
    ScheduleList,
    SourceList,
    SpaceList,
    TrendData,
    ValueList,
    ZoneList,
)

#############################################################################
# NovantClient
#############################################################################


class NovantClient:
    """Client for the Novant REST API."""

    def __init__(self, api_key, timeout=30, proj_id=None):
        """Create a new NovantClient instance.

        Project keys ('ak_xxx') are bound to a single project and do not
        require proj_id. Org keys ('ak_org_xxx') can access any project in
        the organization, and must specify proj_id on every project request,
        either here as a default or per call.

        Args:
            api_key: API key string (e.g. 'ak_xxx' or 'ak_org_xxx')
            timeout: request timeout in seconds (default 30)
            proj_id: optional default project id for all project requests
        """
        self.api_key = api_key
        self.base_url = "https://api.novant.io/v1"
        self.timeout = timeout
        self.proj_id = proj_id

    ######
    # Org
    ######

    def org_projects(self):
        """List all projects in the organization.

        Requires an org key ('ak_org_xxx'); project keys fail with 403. Use
        the returned proj_id values to target project requests.

        Returns:
            OrgProjectList
        """
        return OrgProjectList._from_dict(self._get("/org/projects"))

    ######
    # Project
    ######

    def project(self, proj_id=None):
        """Get project metadata.

        Args:
            proj_id: project id; required for org keys unless set on the client

        Returns:
            Project
        """
        return Project._from_dict(self._get("/project", self._proj_params(proj_id)))

    ######
    # Assets
    ######

    def assets(self, asset_ids=None, proj_id=None):
        """List assets for this project.

        Args:
            asset_ids: optional list of asset id strings to filter
            proj_id: project id; required for org keys unless set on the client

        Returns:
            AssetList
        """
        params = self._proj_params(proj_id)
        if asset_ids is not None:
            params["asset_ids"] = ",".join(asset_ids)
        return AssetList._from_dict(self._get("/assets", params))

    ######
    # Spaces
    ######

    def spaces(self, space_ids=None, proj_id=None):
        """List spaces for this project.

        Args:
            space_ids: optional list of space id strings to filter
            proj_id: project id; required for org keys unless set on the client

        Returns:
            SpaceList
        """
        params = self._proj_params(proj_id)
        if space_ids is not None:
            params["space_ids"] = ",".join(space_ids)
        return SpaceList._from_dict(self._get("/spaces", params))

    ######
    # Zones
    ######

    def zones(self, zone_ids=None, proj_id=None):
        """List zones for this project.

        Args:
            zone_ids: optional list of zone id strings to filter
            proj_id: project id; required for org keys unless set on the client

        Returns:
            ZoneList
        """
        params = self._proj_params(proj_id)
        if zone_ids is not None:
            params["zone_ids"] = ",".join(zone_ids)
        return ZoneList._from_dict(self._get("/zones", params))

    ######
    # Sources
    ######

    def sources(self, source_ids=None, bound_only=False, proj_id=None):
        """List sources for this project.

        Args:
            source_ids: optional list of source id strings to filter
            bound_only: if True only return bound sources
            proj_id: project id; required for org keys unless set on the client

        Returns:
            SourceList
        """
        params = self._proj_params(proj_id)
        if source_ids is not None:
            params["source_ids"] = ",".join(source_ids)
        if bound_only:
            params["bound_only"] = "true"
        return SourceList._from_dict(self._get("/sources", params))

    ######
    # Points
    ######

    def points(
        self,
        source_id=None,
        asset_id=None,
        space_id=None,
        point_ids=None,
        point_types=None,
        proj_id=None,
    ):
        """List points for a source, asset, or space.

        Args:
            source_id: parent source id (one of source_id, asset_id, or space_id required)
            asset_id: parent asset id (one of source_id, asset_id, or space_id required)
            space_id: parent space id (one of source_id, asset_id, or space_id required)
            point_ids: optional list of point id strings to filter
            point_types: optional list of point type strings to filter
            proj_id: project id; required for org keys unless set on the client

        Returns:
            PointList
        """
        params = self._proj_params(proj_id)
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

    def values(
        self,
        source_id=None,
        source_ids=None,
        asset_id=None,
        space_id=None,
        point_ids=None,
        point_types=None,
        proj_id=None,
    ):
        """Get current values for points.

        One of source_id, source_ids, asset_id, or space_id is required. If
        multiple are specified, precedence is source_id, then source_ids,
        then asset_id, then space_id.

        Args:
            source_id: parent source id
            source_ids: list of parent source id strings (max 10)
            asset_id: parent asset id
            space_id: parent space id
            point_ids: optional list of point id strings to filter
            point_types: optional list of point type strings to filter
            proj_id: project id; required for org keys unless set on the client

        Returns:
            ValueList
        """
        params = self._proj_params(proj_id)
        if source_id is not None:
            params["source_id"] = source_id
        if source_ids is not None:
            params["source_ids"] = ",".join(source_ids)
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

    def trends(
        self,
        point_ids,
        start_date=None,
        end_date=None,
        date=None,
        tz=None,
        interval=None,
        aggregate=None,
        proj_id=None,
    ):
        """Get historical trend data for points.

        Args:
            point_ids: list of point id strings
            start_date: start date as YYYY-MM-DD (required unless date is set)
            end_date: end date as YYYY-MM-DD (required unless date is set)
            date: single date as YYYY-MM-DD (takes precedence over start/end)
            tz: timezone for results (defaults to project timezone)
            interval: resample interval - auto|5min|15min|30min|1hr|1day|1mo|raw
            aggregate: aggregation function - auto|mean|sum|min|max|diff
            proj_id: project id; required for org keys unless set on the client

        Returns:
            TrendData
        """
        params = self._proj_params(proj_id)
        params["point_ids"] = ",".join(point_ids)
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
    # Scenes
    ######

    def scenes(self, scene_id=None, proj_id=None):
        """List scenes for this project.

        Args:
            scene_id: optional scene id string to fetch a single scene
            proj_id: project id; required for org keys unless set on the client

        Returns:
            SceneList
        """
        params = self._proj_params(proj_id)
        if scene_id is not None:
            params["scene_id"] = scene_id
        return SceneList._from_dict(self._get("/scenes", params))

    ######
    # Schedules
    ######

    def schedules(self, schedule_id=None, proj_id=None):
        """List schedules for this project.

        Args:
            schedule_id: optional schedule id string to fetch a single schedule
            proj_id: project id; required for org keys unless set on the client

        Returns:
            ScheduleList
        """
        params = self._proj_params(proj_id)
        if schedule_id is not None:
            params["schedule_id"] = schedule_id
        return ScheduleList._from_dict(self._get("/schedules", params))

    ######
    # Write
    ######

    def write(self, point_id, value, level=None, expires=None, proj_id=None):
        """Write a value to a point.

        Args:
            point_id: point id string
            value: numeric value or None to clear priority hold
            level: optional priority level (defaults to 16)
            expires: optional auto-release duration, e.g. "1hr", "30min", "1day"
            proj_id: project id; required for org keys unless set on the client

        Returns:
            dict with status, e.g. {"status": "ok"}
        """
        params = self._proj_params(proj_id)
        params["point_id"] = point_id
        if value is None:
            params["value"] = "null"
        else:
            params["value"] = str(value)
        if level is not None:
            params["level"] = str(level)
        if expires is not None:
            params["expires"] = str(expires)
        return self._post("/write", params)

    def write_batch(self, writes, proj_id=None):
        """Write values to multiple points in a single request.

        Validation is all-or-nothing: if any entry is invalid the entire
        request is rejected and no writes are committed.

        Args:
            writes: list of dicts, each with keys:
                point_id (required): point id string
                value (required): numeric value or None to clear priority hold
                level (optional): priority level (defaults to 16)
                expires (optional): auto-release duration, e.g. "1hr", "1day"
            proj_id: project id; required for org keys unless set on the client

        Returns:
            dict with status, e.g. {"status": "ok"}
        """
        if not writes:
            raise ValueError("writes must be a non-empty list")
        params = self._proj_params(proj_id)
        for i, w in enumerate(writes):
            if "point_id" not in w:
                raise ValueError(f"writes[{i}] missing required 'point_id'")
            if "value" not in w:
                raise ValueError(f"writes[{i}] missing required 'value'")
            params[f"writes[{i}][point_id]"] = w["point_id"]
            value = w["value"]
            params[f"writes[{i}][value]"] = "null" if value is None else str(value)
            if w.get("level") is not None:
                params[f"writes[{i}][level]"] = str(w["level"])
            if w.get("expires") is not None:
                params[f"writes[{i}][expires]"] = str(w["expires"])
        return self._post("/write", params)

    ######
    # Explorer
    ######

    def explorer_scan(self, op, node_id=None, proj_id=None, **params):
        """Queue a discovery operation on an edge node.

        Scans run asynchronously: this returns an op_id once the operation
        is queued. Poll explorer_ops() no faster than once every 30 seconds
        until the op is done, then read results from explorer_sources().

        Each op accepts its own parameters, passed as keyword args. Any
        parameter not specified falls back to its default:

            bacnet-scan    broadcast across a range of device instance ids
                port       UDP port to scan (default 47808)
                range_low  lowest device instance id, 0-4194303 (default 0)
                range_high highest device instance id (default 4194303)

            bacnet-find    probe an explicit list of addresses
                ip_addrs   required, list or comma separated IP addresses
                port       UDP port to probe (default 47808)
                max_time   max time to search, 1min-15min (default 5min)

            jasper-scan    scan a Niagara instance for Jasper sources
                ip_addr    required, IP address of the Niagara instance
                credential required, name of credential used to connect
                port       TCP port for the Niagara WebService (default 443)
                tls        use TLS as a bool; defaults to True for ports
                           ending in 443 and False otherwise

            kaiterra-find  find Kaiterra sources by device identifier
                uuids      required, list or comma separated device UDIDs
                credential required, name of credential used for device data

        Credentials are referenced by name, not id - the same name shown in
        Project Settings.

        Args:
            op: discovery operation to run, i.e.: "bacnet-scan"
            node_id: optional edge node serial number (defaults to the
                first node in the project)
            proj_id: project id; required for org keys unless set on the client
            **params: op specific parameters as documented above; list
                values are joined with commas and bools sent as true/false

        Returns:
            dict with status and op id, e.g. {"status": "ok", "op_id": "0a1b"}
        """
        args = self._proj_params(proj_id)
        args["op"] = op
        if node_id is not None:
            args["node_id"] = node_id
        for k, v in params.items():
            if v is not None:
                args[k] = self._encode_param(v)
        return self._post("/explorer/scan", args)

    def explorer_learn(self, source_id, node_id=None, proj_id=None):
        """Queue a learn operation to read a discovered source's point list.

        Learns run asynchronously: this returns an op_id once the operation
        is queued. Poll explorer_ops() no faster than once every 30 seconds
        until the op is done, then read results from explorer_points().

        Everything else is derived from the source itself - its protocol,
        address, device id, and any credential used to discover it. Learning
        a source that has already been learned replaces its previous results.

        Args:
            source_id: discovery id of the source to learn, as returned by
                explorer_sources()
            node_id: optional edge node serial number (defaults to the node
                that discovered the source)
            proj_id: project id; required for org keys unless set on the client

        Returns:
            dict with status and op id, e.g. {"status": "ok", "op_id": "0a1b"}
        """
        params = self._proj_params(proj_id)
        params["source_id"] = source_id
        if node_id is not None:
            params["node_id"] = node_id
        return self._post("/explorer/learn", params)

    def explorer_ops(self, proj_id=None):
        """Get the status of explorer operations in this project.

        Returns every queued and active operation, plus those completed in
        the last 24 hours. A single request covers all outstanding ops, so
        there is no need to poll per op id. Do not poll faster than once
        every 30 seconds.

        Args:
            proj_id: project id; required for org keys unless set on the client

        Returns:
            ExplorerOpList
        """
        params = self._proj_params(proj_id)
        return ExplorerOpList._from_dict(self._get("/explorer/ops", params))

    def explorer_sources(self, proj_id=None):
        """List the sources discovered in this project.

        Sources accumulate across scans, so compare last_scan to identify
        what the most recent scan found.

        Args:
            proj_id: project id; required for org keys unless set on the client

        Returns:
            ExplorerSourceList
        """
        params = self._proj_params(proj_id)
        return ExplorerSourceList._from_dict(self._get("/explorer/sources", params))

    def explorer_points(self, source_id, proj_id=None):
        """List the points advertised by a discovered source.

        The point list reflects the source's last learn, so it is empty
        until the source has been learned; see explorer_learn().

        Args:
            source_id: discovery id of the source, i.e.: "23a769452950"
            proj_id: project id; required for org keys unless set on the client

        Returns:
            ExplorerPointList
        """
        params = self._proj_params(proj_id)
        params["source_id"] = source_id
        return ExplorerPointList._from_dict(self._get("/explorer/points", params))

    ######
    # Import
    ######

    def import_zones(self, csv_data, proj_id=None):
        """Import zones from CSV data.

        Args:
            csv_data: CSV string content
            proj_id: project id; required for org keys unless set on the client

        Returns:
            dict with status
        """
        params = self._proj_params(proj_id)
        return self._post_csv("/import/zones", csv_data, params)

    def import_spaces(self, csv_data, proj_id=None):
        """Import spaces from CSV data.

        Args:
            csv_data: CSV string content
            proj_id: project id; required for org keys unless set on the client

        Returns:
            dict with status
        """
        params = self._proj_params(proj_id)
        return self._post_csv("/import/spaces", csv_data, params)

    def import_assets(self, csv_data, proj_id=None):
        """Import assets from CSV data.

        Args:
            csv_data: CSV string content
            proj_id: project id; required for org keys unless set on the client

        Returns:
            dict with status
        """
        params = self._proj_params(proj_id)
        return self._post_csv("/import/assets", csv_data, params)

    def import_sources(self, csv_data, proj_id=None):
        """Import sources from CSV data.

        Args:
            csv_data: CSV string content
            proj_id: project id; required for org keys unless set on the client

        Returns:
            dict with status
        """
        params = self._proj_params(proj_id)
        return self._post_csv("/import/sources", csv_data, params)

    def import_source_map(self, csv_data, proj_id=None):
        """Import source map from CSV data.

        Args:
            csv_data: CSV string content
            proj_id: project id; required for org keys unless set on the client

        Returns:
            dict with status
        """
        params = self._proj_params(proj_id)
        return self._post_csv("/import/source-map", csv_data, params)

    def import_trends(self, csv_data, mode=None, proj_id=None):
        """Import trend data from CSV data.

        CSV must have 'ts' as the first column (ISO 8601 timestamps)
        followed by point id columns. Max 50 columns and 10,000 rows.

        Args:
            csv_data: CSV string content
            mode: merge (default), append, or prepend
            proj_id: project id; required for org keys unless set on the client

        Returns:
            dict with status
        """
        params = self._proj_params(proj_id)
        if mode is not None:
            params["mode"] = mode
        return self._post_csv("/import/trends", csv_data, params)

    ##########################################################################
    # Private
    ##########################################################################

    def _proj_params(self, proj_id):
        """Return a new params dict with proj_id if set, else an empty dict."""
        if proj_id is None:
            proj_id = self.proj_id
        return {} if proj_id is None else {"proj_id": proj_id}

    def _encode_param(self, val):
        """Encode a param value: lists join with commas, bools as true/false."""
        if isinstance(val, bool):
            return "true" if val else "false"
        if isinstance(val, (list, tuple)):
            return ",".join(str(v) for v in val)
        return str(val)

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
        creds = base64.b64encode((self.api_key + ":").encode("utf-8")).decode("utf-8")
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
