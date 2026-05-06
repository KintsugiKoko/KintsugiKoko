from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from art_telemetry_qa.schemas import (
    ArtTelemetryRecord,
    AssetValidationRecord,
    ScanInputs,
    SoakResult,
)


TELEMETRY_FILE = "sample_art_telemetry.csv"
SOAK_FILE = "sample_soak_results.json"
VALIDATION_FILE = "sample_asset_validation.json"

TELEMETRY_COLUMNS = {
    "asset_id",
    "asset_name",
    "asset_path",
    "asset_type",
    "map_name",
    "platform",
    "build_label",
    "texture_size_px",
    "triangle_count",
    "material_slot_count",
    "translucent_material_count",
    "alpha_coverage_pct",
    "particle_count",
    "bounds_extent_m",
    "load_warning_count",
    "asset_load_ms",
    "naming_valid",
    "path_valid",
}


def load_scan_inputs(input_dir: str | Path) -> ScanInputs:
    base = Path(input_dir)
    return ScanInputs(
        telemetry=parse_art_telemetry_csv(base / TELEMETRY_FILE),
        soak_results=parse_soak_results_json(base / SOAK_FILE),
        asset_validation=parse_asset_validation_json(base / VALIDATION_FILE),
    )


def parse_art_telemetry_csv(path: str | Path) -> list[ArtTelemetryRecord]:
    csv_path = Path(path)
    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("Art telemetry CSV is empty or missing a header row.")

        missing = TELEMETRY_COLUMNS.difference(reader.fieldnames)
        if missing:
            raise ValueError(
                "Art telemetry CSV is missing required columns: "
                + ", ".join(sorted(missing))
            )

        return [_telemetry_record(row, line_number) for line_number, row in enumerate(reader, start=2)]


def parse_soak_results_json(path: str | Path) -> list[SoakResult]:
    data = _load_json_list(path, "soak results")
    return [
        SoakResult(
            asset_id=_text(row, "asset_id", index),
            duration_minutes=_int(row, "duration_minutes", index),
            warning_spikes=_int(row, "warning_spikes", index),
            hitch_count=_int(row, "hitch_count", index),
            memory_growth_mb=_float(row, "memory_growth_mb", index),
            average_frame_ms=_float(row, "average_frame_ms", index),
            p95_frame_ms=_float(row, "p95_frame_ms", index),
            notes=str(row.get("notes", "")).strip(),
        )
        for index, row in enumerate(data, start=1)
    ]


def parse_asset_validation_json(path: str | Path) -> list[AssetValidationRecord]:
    data = _load_json_list(path, "asset validation")
    return [
        AssetValidationRecord(
            asset_id=_text(row, "asset_id", index),
            gameplay_asset=_bool(row, "gameplay_asset", index),
            has_collision=_bool(row, "has_collision", index),
            lod_count=_int(row, "lod_count", index),
            missing_material_slots=_string_list(row, "missing_material_slots", index),
            skeletal_weighting_warnings=_int(row, "skeletal_weighting_warnings", index),
            naming_warnings=_string_list(row, "naming_warnings", index),
            path_warnings=_string_list(row, "path_warnings", index),
            validation_notes=str(row.get("validation_notes", "")).strip(),
        )
        for index, row in enumerate(data, start=1)
    ]


def _telemetry_record(row: dict[str, str], line_number: int) -> ArtTelemetryRecord:
    return ArtTelemetryRecord(
        asset_id=_required_cell(row, "asset_id", line_number),
        asset_name=_required_cell(row, "asset_name", line_number),
        asset_path=_required_cell(row, "asset_path", line_number),
        asset_type=_required_cell(row, "asset_type", line_number),
        map_name=_required_cell(row, "map_name", line_number),
        platform=_required_cell(row, "platform", line_number),
        build_label=_required_cell(row, "build_label", line_number),
        texture_size_px=_int_cell(row, "texture_size_px", line_number),
        triangle_count=_int_cell(row, "triangle_count", line_number),
        material_slot_count=_int_cell(row, "material_slot_count", line_number),
        translucent_material_count=_int_cell(row, "translucent_material_count", line_number),
        alpha_coverage_pct=_float_cell(row, "alpha_coverage_pct", line_number),
        particle_count=_int_cell(row, "particle_count", line_number),
        bounds_extent_m=_float_cell(row, "bounds_extent_m", line_number),
        load_warning_count=_int_cell(row, "load_warning_count", line_number),
        asset_load_ms=_float_cell(row, "asset_load_ms", line_number),
        naming_valid=_bool_cell(row, "naming_valid", line_number),
        path_valid=_bool_cell(row, "path_valid", line_number),
    )


def _load_json_list(path: str | Path, label: str) -> list[dict[str, Any]]:
    json_path = Path(path)
    with json_path.open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"{label} JSON must contain a list of objects.")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError(f"{label} JSON entries must be objects.")
    return data


def _required_cell(row: dict[str, str], field: str, line_number: int) -> str:
    value = row.get(field, "").strip()
    if not value:
        raise ValueError(f"Line {line_number}: `{field}` is required.")
    return value


def _int_cell(row: dict[str, str], field: str, line_number: int) -> int:
    value = _required_cell(row, field, line_number)
    try:
        return int(value)
    except ValueError as error:
        raise ValueError(f"Line {line_number}: `{field}` must be an integer.") from error


def _float_cell(row: dict[str, str], field: str, line_number: int) -> float:
    value = _required_cell(row, field, line_number)
    try:
        return float(value)
    except ValueError as error:
        raise ValueError(f"Line {line_number}: `{field}` must be a number.") from error


def _bool_cell(row: dict[str, str], field: str, line_number: int) -> bool:
    value = _required_cell(row, field, line_number)
    return _parse_bool(value, f"Line {line_number}: `{field}`")


def _text(row: dict[str, Any], field: str, index: int) -> str:
    value = str(row.get(field, "")).strip()
    if not value:
        raise ValueError(f"JSON entry {index}: `{field}` is required.")
    return value


def _int(row: dict[str, Any], field: str, index: int) -> int:
    try:
        return int(row[field])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"JSON entry {index}: `{field}` must be an integer.") from error


def _float(row: dict[str, Any], field: str, index: int) -> float:
    try:
        return float(row[field])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"JSON entry {index}: `{field}` must be a number.") from error


def _bool(row: dict[str, Any], field: str, index: int) -> bool:
    if field not in row:
        raise ValueError(f"JSON entry {index}: `{field}` is required.")
    return _parse_bool(row[field], f"JSON entry {index}: `{field}`")


def _string_list(row: dict[str, Any], field: str, index: int) -> list[str]:
    value = row.get(field, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"JSON entry {index}: `{field}` must be a list of strings.")
    return [item.strip() for item in value if item.strip()]


def _parse_bool(value: Any, label: str) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "yes", "1"}:
        return True
    if normalized in {"false", "no", "0"}:
        return False
    raise ValueError(f"{label} must be true or false.")
