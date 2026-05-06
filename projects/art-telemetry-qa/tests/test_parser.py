from __future__ import annotations

from pathlib import Path

import pytest

from art_telemetry_qa.parser import (
    load_scan_inputs,
    parse_art_telemetry_csv,
    parse_asset_validation_json,
    parse_soak_results_json,
)


def test_load_scan_inputs_loads_all_sample_files() -> None:
    inputs = load_scan_inputs("samples")

    assert len(inputs.telemetry) == 6
    assert len(inputs.soak_results) == 3
    assert len(inputs.asset_validation) == 6
    assert inputs.telemetry[0].asset_name == "SM_Starwell_Blockout"


def test_parse_art_telemetry_validates_required_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "bad.csv"
    csv_path.write_text("asset_id,asset_name\nART001,SM_Test\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        parse_art_telemetry_csv(csv_path)


def test_parse_soak_results_requires_json_list(tmp_path: Path) -> None:
    json_path = tmp_path / "bad.json"
    json_path.write_text('{"asset_id": "ART001"}', encoding="utf-8")

    with pytest.raises(ValueError, match="must contain a list"):
        parse_soak_results_json(json_path)


def test_parse_asset_validation_reads_warning_lists() -> None:
    records = parse_asset_validation_json("samples/sample_asset_validation.json")
    caravan = next(record for record in records if record.asset_id == "ART005")

    assert caravan.missing_material_slots
    assert caravan.path_warnings
