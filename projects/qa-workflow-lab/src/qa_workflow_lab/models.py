"""Small evidence contracts shared by tools, agents, and reports."""

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
import re


class InputError(ValueError):
    """The evidence cannot be evaluated under this contract."""


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


@dataclass
class Finding:
    id: str
    title: str
    kind: str
    risk: str
    owner: str
    observation: str
    expected: str
    next_action: str
    evidence: list[str]


@dataclass
class Result:
    workflow: str
    title: str
    status: str = "complete"
    product_verdict: str = "review_required"
    findings: list[Finding] = field(default_factory=list)
    details: dict = field(default_factory=dict)
    trace: list[dict] = field(default_factory=list)
    model_notes: list[dict] = field(default_factory=list)
    stop_reason: str = "contract_complete"
    review_status: str = "pending"

    def to_dict(self):
        return asdict(self)


@dataclass
class Bundle:
    metadata: dict
    records: list[dict]

    @classmethod
    def load(cls, path):
        path = Path(path)
        if path.stat().st_size > 2_000_000:
            raise InputError("Evidence bundle exceeds the 2 MB local review limit.")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise InputError("Evidence must be a UTF-8 JSON object.") from exc
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or set(data) != {"metadata", "records"}:
            raise InputError("Expected metadata and records fields.")
        meta, records = data["metadata"], data["records"]
        required = ("feature", "build", "baseline", "platforms", "rule_version", "owner", "fictional")
        if not isinstance(meta, dict) or any(k not in meta for k in required):
            raise InputError("Missing run identity, owner, or configuration.")
        if meta["fictional"] is not True:
            raise InputError("This demo accepts explicitly fictional evidence bundles only.")
        for key in ("feature", "build", "baseline", "rule_version", "owner"):
            if not isinstance(meta[key], str) or not meta[key].strip():
                raise InputError(f"Metadata {key} must be nonempty text.")
        if not isinstance(meta["platforms"], list) or not meta["platforms"] or any(not isinstance(p, str) or not p for p in meta["platforms"]):
            raise InputError("At least one named platform is required.")
        if not isinstance(records, list) or len(records) > 2000:
            raise InputError("Records must be a list of at most 2000 entries.")
        ids = set()
        for record in records:
            if not isinstance(record, dict) or set(record) != {"id", "kind", "build", "platform", "data"}:
                raise InputError("Each record needs id, kind, build, platform, and data.")
            if not isinstance(record["id"], str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", record["id"]):
                raise InputError("Record IDs must contain only letters, numbers, underscores, or hyphens.")
            if record["id"] in ids:
                raise InputError(f"Duplicate record ID: {record['id']}")
            ids.add(record["id"])
            if not isinstance(record["data"], dict):
                raise InputError("Record data must be an object.")
            if any(not isinstance(record[k], str) or not record[k] for k in ("kind", "build", "platform")):
                raise InputError("Record kind, build and platform must be nonempty text.")
        return cls(meta, records)

    def select(self, kind):
        return [r for r in self.records if r["kind"] == kind]

    def get(self, record_id):
        for record in self.records:
            if record["id"] == record_id:
                return record
        raise InputError(f"Unknown evidence ID: {record_id}")

    @property
    def fingerprint(self):
        return digest({"metadata": self.metadata, "records": self.records})


def finding(record, suffix, title, observation, expected, next_action, *, kind="observation", risk="High", owner="QA"):
    return Finding(f"{record['id']}-{suffix}", title, kind, risk, owner, observation, expected, next_action, [record["id"]])
