from __future__ import annotations

from community_pulse.models import AnalysisResult, FeedbackItem

DEFAULT_MAX_FOLLOW_UPS = 5
DEFAULT_MAX_QUOTES = 8
DEFAULT_MAX_THEMES = 5
DEFAULT_MAX_TOPICS = 10


def generate_markdown_report(
    analysis: AnalysisResult,
    max_quotes: int = DEFAULT_MAX_QUOTES,
    max_topics: int = DEFAULT_MAX_TOPICS,
    max_themes: int = DEFAULT_MAX_THEMES,
    max_follow_ups: int = DEFAULT_MAX_FOLLOW_UPS,
) -> str:
    lines: list[str] = [
        "# Weekly Community Feedback Review Report",
        "",
        "> Portfolio-safe prototype report generated from fictional sample data.",
        "",
        "## Executive Summary",
        "",
        f"- Total local feedback records reviewed: **{analysis.total_items}**",
        _summary_theme_line("Strongest positive area", analysis.positive_areas),
        _summary_theme_line("Strongest mixed area", analysis.mixed_areas),
        _summary_theme_line("Strongest negative area", analysis.negative_areas),
        "- This report is a draft aid for human review, not an automated community decision.",
        "",
        "## Filters Applied",
        "",
        *_filter_lines(analysis.applied_filters),
        "",
        *_processing_note_section(analysis.processing_notes),
        "## Sentiment Snapshot",
        "",
        _count_table("Sentiment", analysis.sentiment_counts),
        "",
        "## Local Feedback Inputs",
        "",
        _count_table(
            "Local Input",
            analysis.source_counts,
            limit=max_topics,
            limit_label="local feedback inputs",
        ),
        "",
        *_optional_count_section(
            "Accounts Represented",
            "Account",
            analysis.account_counts,
            limit=max_topics,
            limit_label="accounts",
        ),
        *_optional_count_section(
            "Posts Represented",
            "Post ID",
            analysis.post_counts,
            limit=max_topics,
            limit_label="posts",
        ),
        "## Top Mentioned Topics / Game Areas",
        "",
        _count_table(
            "Topic or Game Area",
            analysis.topic_counts,
            limit=max_topics,
            limit_label="topics by mention count",
        ),
        "",
        "## Topic Opinion Splits",
        "",
        *_opinion_split_lines(analysis, max_topics),
        "",
        "## Positive Themes",
        "",
        *_theme_lines(analysis.positive_areas, "positive", max_themes),
        "",
        "## Mixed Themes",
        "",
        *_theme_lines(analysis.mixed_areas, "mixed", max_themes),
        "",
        "## Negative Themes",
        "",
        *_theme_lines(analysis.negative_areas, "negative", max_themes),
        "",
        "## Representative Quotes Copied From CSV",
        "",
        *_quote_lines(analysis.representative_quotes),
        *_quote_limit_note(analysis, max_quotes),
        "",
        "## Suggested Follow-ups",
        "",
        *_suggested_followups(analysis, max_follow_ups),
        "",
        "## Method / Limitations",
        "",
        "- Generated from local CSV data only.",
        "- Built-in sample data is fictional and created for portfolio practice.",
        "- Optional `account`, `post_id`, `keyword`, `topic`, and `conversation_id` columns model local demo metadata only.",
        "- Sentiment is read from the `sentiment` column; the tool does not infer sentiment with AI or machine learning.",
        "- Counts summarize only the provided local records and are meant to support review, not replace community judgment.",
        "- Representative quotes are selected deterministically, copied exactly from the CSV `text` field, and not paraphrased or rewritten.",
        "- The tool does not scrape, monitor, fetch, discover, or ingest live community conversations.",
        "- The tool does not connect to private APIs, proprietary systems, internal tools, or live community platforms.",
        "- The tool does not perform automated moderation, automated player decisions, or product direction decisions.",
        "- The tool does not generate screenshots, visual evidence, art, avatars, or media.",
        "- User-provided screenshots or media references should remain untouched and require human review before sharing.",
        "- A human reviewer should validate context before routing feedback to QA, design, production, community, or External QA partners.",
        "",
    ]

    return "\n".join(lines)


def _summary_theme_line(label: str, areas: list[tuple[str, int]]) -> str:
    if not areas:
        return f"- {label}: **No matching feedback in this sample.**"

    area, count = areas[0]
    return f"- {label}: **{area}** ({count} item{_plural(count)})"


def _count_table(
    label: str,
    counts: dict[str, int],
    limit: int | None = None,
    limit_label: str | None = None,
) -> str:
    if not counts:
        return "_No feedback items found._"

    visible_counts = _limit_count_dict(counts, limit)
    rows = [f"| {label} | Count |", "| --- | ---: |"]
    rows.extend(f"| {name} | {count} |" for name, count in visible_counts.items())
    if limit is not None and len(counts) > limit:
        label_text = limit_label or label.lower()
        rows.extend(["", f"_Showing top {limit} {label_text}._"])
    return "\n".join(rows)


def _optional_count_section(
    heading: str,
    label: str,
    counts: dict[str, int],
    limit: int | None = None,
    limit_label: str | None = None,
) -> list[str]:
    if not counts:
        return []

    return [
        f"## {heading}",
        "",
        _count_table(label, counts, limit=limit, limit_label=limit_label),
        "",
    ]


def _filter_lines(filters: dict[str, str]) -> list[str]:
    if not filters:
        return ["_No filters applied._"]

    return [f"- **{name}**: {value}" for name, value in filters.items()]


def _processing_note_section(notes: list[str]) -> list[str]:
    if not notes:
        return []

    return [
        "## Report Scope Notes",
        "",
        *[f"- {note}" for note in notes],
        "",
    ]


def _theme_lines(
    areas: list[tuple[str, int]],
    sentiment_label: str,
    limit: int,
) -> list[str]:
    if not areas:
        return [f"- No {sentiment_label} themes found in this sample."]

    lines = [
        f"- **{area}**: {count} {sentiment_label} item{_plural(count)}"
        for area, count in areas[:limit]
    ]
    if len(areas) > limit:
        lines.append(f"_Showing top {limit} {sentiment_label} themes by mention count._")
    return lines


def _quote_lines(quotes: list[FeedbackItem]) -> list[str]:
    if not quotes:
        return ["- No representative quotes available."]

    return [
        (
            f'- "{quote.text}" '
            f"({_quote_metadata(quote)})"
        )
        for quote in quotes
    ]


def _quote_limit_note(analysis: AnalysisResult, max_quotes: int) -> list[str]:
    if analysis.total_items <= len(analysis.representative_quotes):
        return []

    return [f"_Representative quotes limited to {max_quotes} for readability._"]


def _opinion_split_lines(analysis: AnalysisResult, limit: int) -> list[str]:
    if not analysis.opinion_splits:
        return ["- No conflicting sentiment splits found in this sample."]

    lines = [
        f"- **{split.label}**: {_sentiment_split_summary(split.counts)}"
        for split in analysis.opinion_splits[:limit]
    ]
    if len(analysis.opinion_splits) > limit:
        lines.append(f"_Showing top {limit} topic opinion splits by mention count._")
    return lines


def _sentiment_split_summary(counts: dict[str, int]) -> str:
    return ", ".join(
        f"{count} {sentiment}" for sentiment, count in counts.items()
    )


def _quote_metadata(quote: FeedbackItem) -> str:
    parts = [quote.sentiment, quote.topic or quote.game_area, quote.source, quote.date]
    if quote.account:
        parts.append(f"account: {quote.account}")
    if quote.post_id:
        parts.append(f"post: {quote.post_id}")
    return ", ".join(parts)


def _suggested_followups(analysis: AnalysisResult, limit: int) -> list[str]:
    followups = [
        "- Have a human reviewer confirm whether the selected quotes fairly represent the week.",
        "- Compare the report with QA notes or support patterns before deciding on next actions.",
    ]

    if analysis.negative_areas:
        top_area, _ = analysis.negative_areas[0]
        followups.insert(
            0,
            f"- Review **{top_area}** feedback first because it has the most negative items in this sample.",
        )

    if analysis.positive_areas:
        top_area, _ = analysis.positive_areas[0]
        followups.append(
            f"- Preserve what is working in **{top_area}** when planning changes."
        )

    if analysis.mixed_areas:
        top_area, _ = analysis.mixed_areas[0]
        followups.append(
            f"- Review **{top_area}** for tradeoffs because mixed feedback is present."
        )

    if analysis.opinion_splits:
        followups.append(
            "- Use the topic opinion splits to decide where follow-up questions or QA checks are needed."
        )

    if len(followups) <= limit:
        return followups

    return [
        *followups[:limit],
        f"_Suggested follow-ups limited to {limit} for readability._",
    ]


def _limit_count_dict(counts: dict[str, int], limit: int | None) -> dict[str, int]:
    if limit is None:
        return counts

    return dict(list(counts.items())[:limit])


def _plural(count: int) -> str:
    return "" if count == 1 else "s"
