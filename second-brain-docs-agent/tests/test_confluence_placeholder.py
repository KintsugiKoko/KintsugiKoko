from src.publish.confluence import is_publish_enabled, publish_draft


def test_confluence_publishing_defaults_disabled_and_dry_run():
    result = publish_draft("Draft", "# Draft", env={})

    assert is_publish_enabled({}) is False
    assert result.enabled is False
    assert result.dry_run is True
    assert result.published is False
    assert "disabled" in result.message.lower()
    assert "CONFLUENCE_API_TOKEN" in result.missing_env_vars


def test_confluence_enabled_still_dry_runs():
    env = {
        "CONFLUENCE_PUBLISH_ENABLED": "true",
        "CONFLUENCE_BASE_URL": "https://example.atlassian.net/wiki",
        "CONFLUENCE_SPACE_KEY": "DOCS",
        "CONFLUENCE_PARENT_PAGE_ID": "123",
        "CONFLUENCE_EMAIL": "sample@example.com",
        "CONFLUENCE_API_TOKEN": "sample-token",
    }

    result = publish_draft("Draft", "# Draft", env=env, dry_run=True)

    assert result.enabled is True
    assert result.dry_run is True
    assert result.published is False
    assert result.missing_env_vars == ()
