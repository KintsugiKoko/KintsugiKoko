"""Dry-run-only Confluence publishing placeholder.

Real publishing is intentionally not implemented in the MVP.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


REQUIRED_ENV_VARS = (
    "CONFLUENCE_BASE_URL",
    "CONFLUENCE_SPACE_KEY",
    "CONFLUENCE_PARENT_PAGE_ID",
    "CONFLUENCE_EMAIL",
    "CONFLUENCE_API_TOKEN",
)


@dataclass(frozen=True)
class PublishResult:
    """Result from a dry-run publish attempt."""

    enabled: bool
    dry_run: bool
    published: bool
    message: str
    missing_env_vars: tuple[str, ...] = ()


def is_publish_enabled(env: Mapping[str, str] | None = None) -> bool:
    """Return whether external publishing has been explicitly enabled."""

    values = env or os.environ
    return values.get("CONFLUENCE_PUBLISH_ENABLED", "false").lower() == "true"


def missing_required_env_vars(env: Mapping[str, str] | None = None) -> tuple[str, ...]:
    """List missing future Confluence environment variables."""

    values = env or os.environ
    return tuple(name for name in REQUIRED_ENV_VARS if not values.get(name))


def publish_draft(
    title: str,
    markdown: str,
    env: Mapping[str, str] | None = None,
    dry_run: bool = True,
) -> PublishResult:
    """Return a dry-run result without publishing externally."""

    values = env or os.environ
    enabled = is_publish_enabled(values)
    missing = missing_required_env_vars(values)

    if not enabled:
        return PublishResult(
            enabled=False,
            dry_run=True,
            published=False,
            message=f"Confluence publishing is disabled. Draft '{title}' was not published.",
            missing_env_vars=missing,
        )

    if dry_run:
        return PublishResult(
            enabled=True,
            dry_run=True,
            published=False,
            message=f"Dry run only. Draft '{title}' would be prepared for Confluence, but no request was sent.",
            missing_env_vars=missing,
        )

    return PublishResult(
        enabled=True,
        dry_run=True,
        published=False,
        message="Real Confluence publishing is not implemented in this MVP.",
        missing_env_vars=missing,
    )
