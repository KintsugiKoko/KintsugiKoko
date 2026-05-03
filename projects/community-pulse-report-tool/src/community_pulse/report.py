from __future__ import annotations

from community_pulse.models import AnalysisResult, FeedbackItem


def generate_markdown_report(analysis: AnalysisResult) -> str:
    lines: list[str] = [
        "# Weekly Community Sentiment Report",
        "",
        "> Portfolio-safe prototype report generated from fictional sample data.",
        "",
        "## Executive Summary",
        "",
        f"- Total feedback items reviewed: **{analysis.total_items}**",
        _summary_theme_line("Strongest positive area", analysis.positive_areas),
        _summary_theme_line("Strongest negative area", analysis.negative_areas),
        "- This report is a draft aid for human review, not an automated community decision.",
        "",
        "## Sentiment Snapshot",
        "",
        _count_table("Sentiment", analysis.sentiment_counts),
        "",
        "## Feedback Sources",
        "",
        _count_table("Source", analysis.source_counts),
        "",
        "## Top Mentioned Game Areas",
        "",
        _count_table("Game Area", analysis.game_area_counts),
        "",
        "## Positive Themes",
        "",
        *_theme_lines(analysis.positive_areas, "positive"),
        "",
        "## Negative Themes",
        "",
        *_theme_lines(analysis.negative_areas, "negative"),
        "",
        "## Representative Quotes",
        "",
        *_quote_lines(analysis.representative_quotes),
        "",
        "## Suggested Follow-ups",
        "",
        *_suggested_followups(analysis),
        "",
        "## Method / Limitations",
        "",
        "- Uses fictional sample data only.",
        "- Sentiment is read from the `sentiment` column; the tool does not infer sentiment with AI or machine learning.",
        "- Counts are simple summaries meant to support review, not replace community judgment.",
        "- Representative quotes are selected deterministically from the sample rows.",
        "- No external community platforms, private APIs, internal tools, or proprietary data are used.",
        "",
    ]

    return "\n".join(lines)


def _summary_theme_line(label: str, areas: list[tuple[str, int]]) -> str:
    if not areas:
        return f"- {label}: **No matching feedback in this sample.**"

    area, count = areas[0]
    return f"- {label}: **{area}** ({count} item{_plural(count)})"


def _count_table(label: str, counts: dict[str, int]) -> str:
    if not counts:
        return "_No feedback items found._"

    rows = [f"| {label} | Count |", "| --- | ---: |"]
    rows.extend(f"| {name} | {count} |" for name, count in counts.items())
    return "\n".join(rows)


def _theme_lines(areas: list[tuple[str, int]], sentiment_label: str) -> list[str]:
    if not areas:
        return [f"- No {sentiment_label} themes found in this sample."]

    return [
        f"- **{area}**: {count} {sentiment_label} item{_plural(count)}"
        for area, count in areas
    ]


def _quote_lines(quotes: list[FeedbackItem]) -> list[str]:
    if not quotes:
        return ["- No representative quotes available."]

    return [
        (
            f'- "{quote.text}" '
            f"({quote.sentiment}, {quote.game_area}, {quote.source}, {quote.date})"
        )
        for quote in quotes
    ]


def _suggested_followups(analysis: AnalysisResult) -> list[str]:
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

    return followups


def _plural(count: int) -> str:
    return "" if count == 1 else "s"
