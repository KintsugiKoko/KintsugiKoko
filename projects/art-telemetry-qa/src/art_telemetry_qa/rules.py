from __future__ import annotations

from art_telemetry_qa.schemas import (
    ArtTelemetryRecord,
    AssetValidationRecord,
    Finding,
    ScanInputs,
    SoakResult,
)


TEXTURE_BUDGET_PX = 4096
CRITICAL_TEXTURE_PX = 8192
HIGH_DENSITY_TRIANGLES = 100000
MATERIAL_SLOT_THRESHOLD = 6
VFX_PARTICLE_THRESHOLD = 2000
SUSPICIOUS_BOUNDS_M = 45.0
LOAD_WARNING_MS = 2500
SOAK_WARNING_SPIKE_THRESHOLD = 3
SOAK_HITCH_THRESHOLD = 8


def evaluate_rules(inputs: ScanInputs) -> list[Finding]:
    validation_by_asset = {record.asset_id: record for record in inputs.asset_validation}
    soak_by_asset = {record.asset_id: record for record in inputs.soak_results}

    findings: list[Finding] = []
    for record in inputs.telemetry:
        validation = validation_by_asset.get(record.asset_id)
        soak = soak_by_asset.get(record.asset_id)
        findings.extend(_telemetry_rules(record))
        if validation is not None:
            findings.extend(_validation_rules(record, validation))
        if soak is not None:
            findings.extend(_soak_rules(record, soak))

    return findings


def _telemetry_rules(record: ArtTelemetryRecord) -> list[Finding]:
    findings: list[Finding] = []

    if record.texture_size_px >= CRITICAL_TEXTURE_PX:
        findings.append(
            _finding(
                record,
                "ART-TEX-001",
                "Texture size over critical review budget",
                "Critical",
                "Tech Art",
                f"Texture size is {record.texture_size_px}px, which needs immediate budget review.",
                "Compare texture size, compression, mip behavior, and platform target before sign-off.",
            )
        )
    elif record.texture_size_px > TEXTURE_BUDGET_PX:
        findings.append(
            _finding(
                record,
                "ART-TEX-001",
                "Texture size over review budget",
                "High",
                "Tech Art",
                f"Texture size is {record.texture_size_px}px, above the {TEXTURE_BUDGET_PX}px review budget.",
                "Confirm whether the texture size is justified by camera distance and asset priority.",
            )
        )

    if (
        record.triangle_count >= HIGH_DENSITY_TRIANGLES
        and record.translucent_material_count > 0
        and record.alpha_coverage_pct >= 25
    ):
        findings.append(
            _finding(
                record,
                "ART-ALPHA-001",
                "Alpha/translucency on high-density asset",
                "High",
                "Tech Art",
                (
                    f"{record.translucent_material_count} translucent material(s), "
                    f"{record.alpha_coverage_pct:.1f}% alpha coverage, and "
                    f"{record.triangle_count:,} triangles were captured together."
                ),
                "Review overdraw, material setup, camera overlap, and whether a cheaper presentation is acceptable.",
            )
        )

    if record.material_slot_count > MATERIAL_SLOT_THRESHOLD:
        findings.append(
            _finding(
                record,
                "ART-MAT-002",
                "Material slot count over threshold",
                "Medium",
                "Tech Art",
                f"Material slot count is {record.material_slot_count}, above the review threshold of {MATERIAL_SLOT_THRESHOLD}.",
                "Check whether material consolidation can reduce draw-call and maintenance risk.",
            )
        )

    if _is_vfx(record) and record.particle_count > VFX_PARTICLE_THRESHOLD:
        findings.append(
            _finding(
                record,
                "VFX-PART-001",
                "VFX particle count over threshold",
                "High",
                "VFX",
                f"Particle count is {record.particle_count}, above the review threshold of {VFX_PARTICLE_THRESHOLD}.",
                "Review spawn rate, lifetime, LOD behavior, and expected camera density.",
            )
        )

    if record.bounds_extent_m > SUSPICIOUS_BOUNDS_M:
        findings.append(
            _finding(
                record,
                "ART-BOUNDS-001",
                "Suspiciously large bounds",
                "Medium",
                "QA",
                f"Bounds extent is {record.bounds_extent_m:.1f}m.",
                "Validate pivot, bounds setup, culling behavior, collision, and map placement.",
            )
        )

    if record.load_warning_count > 0 or record.asset_load_ms > LOAD_WARNING_MS:
        severity = "High" if record.load_warning_count >= 3 else "Medium"
        findings.append(
            _finding(
                record,
                "PERF-LOAD-001",
                "Asset load warning",
                severity,
                "Performance",
                (
                    f"{record.load_warning_count} load warning(s), "
                    f"{record.asset_load_ms:.0f} ms asset load time."
                ),
                "Compare warm/cold load captures and check whether streaming or asset dependency cost changed.",
            )
        )

    if not record.naming_valid or not record.path_valid:
        findings.append(
            _finding(
                record,
                "QA-NAME-001",
                "Invalid naming or path convention",
                "Low",
                "QA",
                f"Naming valid: {record.naming_valid}; path valid: {record.path_valid}.",
                "Confirm naming and folder rules before content review or bug handoff.",
            )
        )

    return findings


def _validation_rules(
    record: ArtTelemetryRecord,
    validation: AssetValidationRecord,
) -> list[Finding]:
    findings: list[Finding] = []

    if validation.missing_material_slots:
        findings.append(
            _finding(
                record,
                "ART-MAT-001",
                "Missing material slot assignment",
                "High",
                "Art",
                "Missing material slot(s): " + ", ".join(validation.missing_material_slots),
                "Open the asset in Unreal and verify slot assignment, defaults, and intended material overrides.",
            )
        )

    if _is_skeletal(record) and validation.skeletal_weighting_warnings > 0:
        findings.append(
            _finding(
                record,
                "ANIM-WEIGHT-001",
                "Skeletal mesh weighting warning",
                "High",
                "Animation",
                f"{validation.skeletal_weighting_warnings} weighting warning(s) were captured.",
                "Check deformation poses, vertex influence, affected bones, and animation preview coverage.",
            )
        )

    if _needs_lods(record) and validation.lod_count < 2:
        findings.append(
            _finding(
                record,
                "ART-LOD-001",
                "Missing or insufficient LODs",
                "Medium",
                "Tech Art",
                f"LOD count is {validation.lod_count}.",
                "Verify imported LODs, screen-size transitions, and expected viewing distance.",
            )
        )

    if validation.gameplay_asset and not validation.has_collision:
        findings.append(
            _finding(
                record,
                "ENG-COLL-001",
                "Missing collision on gameplay asset",
                "High",
                "Engineering",
                "Asset is marked as gameplay-facing but collision is missing.",
                "Validate collision setup in PIE and confirm player, camera, projectile, or interaction expectations.",
            )
        )

    if validation.naming_warnings or validation.path_warnings:
        warnings = validation.naming_warnings + validation.path_warnings
        findings.append(
            _finding(
                record,
                "QA-NAME-002",
                "Validation naming/path warning",
                "Low",
                "QA",
                "; ".join(warnings),
                "Clean up naming/path convention before filing higher-cost technical issues.",
            )
        )

    return findings


def _soak_rules(record: ArtTelemetryRecord, soak: SoakResult) -> list[Finding]:
    if soak.warning_spikes <= SOAK_WARNING_SPIKE_THRESHOLD and soak.hitch_count <= SOAK_HITCH_THRESHOLD:
        return []

    severity = "Critical" if soak.warning_spikes >= 8 or soak.hitch_count >= 15 else "High"
    return [
        _finding(
            record,
            "SOAK-WARN-001",
            "Soak test warning spike",
            severity,
            "Performance",
            (
                f"{soak.warning_spikes} warning spike(s), {soak.hitch_count} hitch(es), "
                f"{soak.memory_growth_mb:.1f} MB memory growth over {soak.duration_minutes} minutes."
            ),
            "Review timestamped soak evidence, streaming behavior, VFX loops, memory growth, and repeatability.",
        )
    ]


def _finding(
    record: ArtTelemetryRecord,
    rule_id: str,
    title: str,
    severity: str,
    likely_owner: str,
    message: str,
    suggested_validation: str,
) -> Finding:
    return Finding(
        asset_id=record.asset_id,
        asset_name=record.asset_name,
        asset_path=record.asset_path,
        rule_id=rule_id,
        title=title,
        severity=severity,
        likely_owner=likely_owner,
        message=message,
        evidence=(
            f"{record.asset_type} captured on {record.platform} in {record.map_name} "
            f"from build {record.build_label}."
        ),
        suggested_validation=suggested_validation,
    )


def _is_vfx(record: ArtTelemetryRecord) -> bool:
    return "vfx" in record.asset_type.lower() or "particle" in record.asset_type.lower()


def _is_skeletal(record: ArtTelemetryRecord) -> bool:
    return "skeletal" in record.asset_type.lower()


def _needs_lods(record: ArtTelemetryRecord) -> bool:
    return any(kind in record.asset_type.lower() for kind in ("static mesh", "skeletal mesh", "vfx"))
