from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ArtTelemetryRecord:
    asset_id: str
    asset_name: str
    asset_path: str
    asset_type: str
    map_name: str
    platform: str
    build_label: str
    texture_size_px: int
    triangle_count: int
    material_slot_count: int
    translucent_material_count: int
    alpha_coverage_pct: float
    particle_count: int
    bounds_extent_m: float
    load_warning_count: int
    asset_load_ms: float
    naming_valid: bool
    path_valid: bool


@dataclass(frozen=True)
class SoakResult:
    asset_id: str
    duration_minutes: int
    warning_spikes: int
    hitch_count: int
    memory_growth_mb: float
    average_frame_ms: float
    p95_frame_ms: float
    notes: str = ""


@dataclass(frozen=True)
class AssetValidationRecord:
    asset_id: str
    gameplay_asset: bool
    has_collision: bool
    lod_count: int
    missing_material_slots: list[str] = field(default_factory=list)
    skeletal_weighting_warnings: int = 0
    naming_warnings: list[str] = field(default_factory=list)
    path_warnings: list[str] = field(default_factory=list)
    validation_notes: str = ""


@dataclass(frozen=True)
class ScanInputs:
    telemetry: list[ArtTelemetryRecord]
    soak_results: list[SoakResult]
    asset_validation: list[AssetValidationRecord]


@dataclass(frozen=True)
class Finding:
    asset_id: str
    asset_name: str
    asset_path: str
    rule_id: str
    title: str
    severity: str
    likely_owner: str
    message: str
    evidence: str
    suggested_validation: str
    risk_points: int = 0


@dataclass(frozen=True)
class ScanResult:
    total_assets: int
    findings: list[Finding]
    risk_by_asset: dict[str, int]
    severity_counts: dict[str, int]
    owner_counts: dict[str, int]
