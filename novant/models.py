#
# Copyright (c) 2026, Novant LLC
# Licensed under the MIT License
#
# History:
#   9 Mar 2026  Andy Frank  Creation
#

from dataclasses import dataclass, field
from typing import Any, Optional

#############################################################################
# Ontology
#############################################################################

@dataclass
class Ontology:
    """Ontology classification for an entity."""
    brick: Optional[str] = None
    haystack: Optional[str] = None
    vbis: Optional[str] = None
    rec: Optional[str] = None

    @classmethod
    def _from_dict(cls, d):
        if d is None:
            return None
        return cls(
            brick=d.get("brick"),
            haystack=d.get("haystack"),
            vbis=d.get("vbis"),
            rec=d.get("rec"),
        )

#############################################################################
# EnumState
#############################################################################

@dataclass
class EnumState:
    """Enumeration state for a point."""
    val: int
    name: str

    @classmethod
    def _from_dict(cls, d):
        return cls(val=d["val"], name=d["name"])

#############################################################################
# Project
#############################################################################

@dataclass
class Project:
    """Project metadata."""
    proj_id: int
    proj_name: str
    city: str
    tz: str
    usage: int
    capacity: int

    @classmethod
    def _from_dict(cls, d):
        return cls(
            proj_id=d["proj_id"],
            proj_name=d["proj_name"],
            city=d["city"],
            tz=d["tz"],
            usage=d["usage"],
            capacity=d["capacity"],
        )

#############################################################################
# Asset
#############################################################################

@dataclass
class Asset:
    """A project asset."""
    id: str
    name: str
    type: str
    props: Optional[dict] = None
    ontology: Optional[Ontology] = None
    source_ids: list[str] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            type=d["type"],
            props=d.get("props"),
            ontology=Ontology._from_dict(d.get("ontology")),
            source_ids=d.get("source_ids", []),
        )

@dataclass
class AssetList:
    """Response from the assets endpoint."""
    currency: str
    assets: list[Asset]

    def __iter__(self):
        return iter(self.assets)

    def __len__(self):
        return len(self.assets)

    def asset(self, id):
        """Lookup an asset by id.

        Args:
            id: asset id string

        Returns:
            Asset or None if not found
        """
        for a in self.assets:
            if a.id == id:
                return a
        return None

    @classmethod
    def _from_dict(cls, d):
        return cls(
            currency=d["currency"],
            assets=[Asset._from_dict(a) for a in d["assets"]],
        )

#############################################################################
# Space
#############################################################################

@dataclass
class Space:
    """A building space."""
    id: str
    name: str
    type: str
    parent_space_id: Optional[str] = None
    parent_zone_id: Optional[str] = None
    contains_asset_ids: list[str] = field(default_factory=list)
    props: Optional[dict] = None
    ontology: Optional[Ontology] = None

    @classmethod
    def _from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            type=d["type"],
            parent_space_id=d.get("parent_space_id"),
            parent_zone_id=d.get("parent_zone_id"),
            contains_asset_ids=d.get("contains_asset_ids", []),
            props=d.get("props"),
            ontology=Ontology._from_dict(d.get("ontology")),
        )

@dataclass
class SpaceList:
    """Response from the spaces endpoint."""
    spaces: list[Space]

    def __iter__(self):
        return iter(self.spaces)

    def __len__(self):
        return len(self.spaces)

    def space(self, id):
        """Lookup a space by id.

        Args:
            id: space id string

        Returns:
            Space or None if not found
        """
        for s in self.spaces:
            if s.id == id:
                return s
        return None

    @classmethod
    def _from_dict(cls, d):
        return cls(
            spaces=[Space._from_dict(s) for s in d["spaces"]],
        )

#############################################################################
# Zone
#############################################################################

@dataclass
class Zone:
    """A thermal or control zone."""
    id: str
    name: str
    type: str
    fed_by_asset_ids: list[str] = field(default_factory=list)
    feeds_space_ids: list[str] = field(default_factory=list)
    ontology: Optional[Ontology] = None

    @classmethod
    def _from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            type=d["type"],
            fed_by_asset_ids=d.get("fed_by_asset_ids", []),
            feeds_space_ids=d.get("feeds_space_ids", []),
            ontology=Ontology._from_dict(d.get("ontology")),
        )

@dataclass
class ZoneList:
    """Response from the zones endpoint."""
    zones: list[Zone]

    def __iter__(self):
        return iter(self.zones)

    def __len__(self):
        return len(self.zones)

    def zone(self, id):
        """Lookup a zone by id.

        Args:
            id: zone id string

        Returns:
            Zone or None if not found
        """
        for z in self.zones:
            if z.id == id:
                return z
        return None

    @classmethod
    def _from_dict(cls, d):
        return cls(
            zones=[Zone._from_dict(z) for z in d["zones"]],
        )

#############################################################################
# Source
#############################################################################

@dataclass
class Source:
    """A data source."""
    id: str
    name: str
    type: str
    addr: Optional[str] = None
    device_id: Optional[int] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    enabled: bool = False
    bound: bool = False
    parent_asset_id: Optional[str] = None

    @classmethod
    def _from_dict(cls, d):
        return cls(
            id=d["id"],
            name=d["name"],
            type=d["type"],
            addr=d.get("addr"),
            device_id=d.get("device_id"),
            vendor=d.get("vendor"),
            model=d.get("model"),
            enabled=d.get("enabled", False),
            bound=d.get("bound", False),
            parent_asset_id=d.get("parent_asset_id"),
        )

@dataclass
class SourceList:
    """Response from the sources endpoint."""
    sources: list[Source]

    def __iter__(self):
        return iter(self.sources)

    def __len__(self):
        return len(self.sources)

    def source(self, id):
        """Lookup a source by id.

        Args:
            id: source id string

        Returns:
            Source or None if not found
        """
        for s in self.sources:
            if s.id == id:
                return s
        return None

    @classmethod
    def _from_dict(cls, d):
        return cls(
            sources=[Source._from_dict(s) for s in d["sources"]],
        )

#############################################################################
# Point
#############################################################################

@dataclass
class Point:
    """A sensor or control point."""
    id: str
    name: str
    type: str
    addr: str
    kind: str
    writable: bool
    unit: Optional[str] = None
    schedule: Optional[str] = None
    mode: Optional[str] = None
    limit: Optional[str] = None
    enum: Optional[str] = None
    enum_states: Optional[list[EnumState]] = None
    ontology: Optional[Ontology] = None

    @classmethod
    def _from_dict(cls, d):
        enum_states = None
        if d.get("enum_states"):
            enum_states = [EnumState._from_dict(e) for e in d["enum_states"]]
        return cls(
            id=d["id"],
            name=d["name"],
            type=d["type"],
            addr=d["addr"],
            kind=d["kind"],
            writable=d["writable"],
            unit=d.get("unit"),
            schedule=d.get("schedule"),
            mode=d.get("mode"),
            limit=d.get("limit"),
            enum=d.get("enum"),
            enum_states=enum_states,
            ontology=Ontology._from_dict(d.get("ontology")),
        )

@dataclass
class PointList:
    """Response from the points endpoint."""
    source_id: str
    source_name: str
    source_bound: bool
    source_enabled: bool
    points: list[Point]

    def __iter__(self):
        return iter(self.points)

    def __len__(self):
        return len(self.points)

    def point(self, id):
        """Lookup a point by id.

        Args:
            id: point id string

        Returns:
            Point or None if not found
        """
        for p in self.points:
            if p.id == id:
                return p
        return None

    @classmethod
    def _from_dict(cls, d):
        return cls(
            source_id=d["source_id"],
            source_name=d["source_name"],
            source_bound=d["source_bound"],
            source_enabled=d["source_enabled"],
            points=[Point._from_dict(p) for p in d["points"]],
        )

#############################################################################
# PointValue
#############################################################################

@dataclass
class PointValue:
    """A current point value."""
    id: str
    val: Any
    status: str

    @classmethod
    def _from_dict(cls, d):
        return cls(id=d["id"], val=d["val"], status=d["status"])

@dataclass
class ValueList:
    """Response from the values endpoint."""
    source_id: str
    values: list[PointValue]

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def point(self, id):
        """Lookup a point value by id.

        Args:
            id: point id string

        Returns:
            PointValue or None if not found
        """
        for v in self.values:
            if v.id == id:
                return v
        return None

    def to_dataframe(self):
        """Convert to a pandas DataFrame.

        Returns:
            DataFrame with columns: id, val, status
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for to_dataframe(). "
                "Install it with: pip install novant[pandas]"
            )
        df = pd.DataFrame([
            {"id": v.id, "val": v.val, "status": v.status}
            for v in self.values
        ])
        df["val"] = pd.to_numeric(df["val"], errors="coerce")
        return df

    @classmethod
    def _from_dict(cls, d):
        return cls(
            source_id=d["source_id"],
            values=[PointValue._from_dict(v) for v in d["values"]],
        )

#############################################################################
# TrendRow / TrendData
#############################################################################

@dataclass
class TrendRow:
    """A single trend data row."""
    ts: str
    values: dict[str, Any]

    @classmethod
    def _from_dict(cls, d):
        ts = d["ts"]
        values = {k: v for k, v in d.items() if k != "ts"}
        return cls(ts=ts, values=values)

@dataclass
class TrendData:
    """Response from the trends endpoint."""
    start: str
    end: str
    tz: str
    interval: str
    aggregate: str
    point_ids: list[str]
    trends: list[TrendRow]

    def __iter__(self):
        return iter(self.trends)

    def __len__(self):
        return len(self.trends)

    def to_dataframe(self):
        """Convert to a pandas DataFrame with DatetimeIndex.

        Returns:
            DataFrame with ts as DatetimeIndex and point_ids as columns
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for to_dataframe(). "
                "Install it with: pip install novant[pandas]"
            )
        rows = [{"ts": r.ts, **r.values} for r in self.trends]
        df = pd.DataFrame(rows)
        df["ts"] = pd.to_datetime(df["ts"])
        df = df.set_index("ts")
        df = df.replace("na", pd.NA)
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    @classmethod
    def _from_dict(cls, d):
        return cls(
            start=d["start"],
            end=d["end"],
            tz=d["tz"],
            interval=d["interval"],
            aggregate=d["aggregate"],
            point_ids=d["point_ids"],
            trends=[TrendRow._from_dict(r) for r in d["trends"]],
        )

#############################################################################
# WriteResult
#############################################################################

@dataclass
class WriteResult:
    """Response from the write endpoint."""
    point_id: str
    level: int
    source_id: Any
    value: str
    status: str

    @classmethod
    def _from_dict(cls, d):
        return cls(
            point_id=d["point_id"],
            level=d["level"],
            source_id=d["source_id"],
            value=d["value"],
            status=d["status"],
        )
