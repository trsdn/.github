"""Account-level SVG card renderers."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from math import ceil

from .svg import esc, iso_date, n, relative_time, svg_root, truncate
from .theme import Theme, card_bg, defs
from ..languages import color_for
from ..models import AccountStats, LanguageShare, RepoStats


def _metric(x: int, y: int, label: str, value: object) -> str:
    return f'<text x="{x}" y="{y}" class="label">{esc(label)}</text><text x="{x}" y="{y + 24}" class="value">{esc(value)}</text>'


def render_overview_card(stats: AccountStats, theme: Theme) -> str:
    width, height = 820, 300
    body = [defs(theme), card_bg(width, height, theme)]
    body.append(f'<text x="28" y="44" class="title">{esc(stats.username)} account overview</text>')
    body.append(f'<text x="28" y="68" class="subtitle">Public GitHub activity and repository health snapshot</text>')
    metrics = [
        (28, 116, "Total commits", n(stats.total_commits)),
        (188, 116, "Stars", n(stats.total_stars)),
        (328, 116, "Merged PRs", n(stats.merged_prs)),
        (488, 116, "Issues", n(stats.authored_issues)),
        (638, 116, "Reviews", n(stats.code_reviews)),
        (28, 196, "Followers", n(stats.followers)),
        (188, 196, "Active repos", n(stats.active_repos)),
        (328, 196, "Current streak", f"{stats.current_streak}d"),
        (488, 196, "Longest streak", f"{stats.longest_streak}d"),
        (638, 196, "Repositories", n(len(stats.repos))),
    ]
    body.extend(_metric(*m) for m in metrics)
    body.append(f'<text x="792" y="272" text-anchor="end" class="small">auto-generated · {stats.generated_at.replace(microsecond=0).isoformat()}</text>')
    return svg_root(width, height, "".join(body))


def _heat_color(count: int, theme: Theme) -> str:
    if count <= 0:
        return theme.track
    if count < 2:
        return "#93c5fd"
    if count < 5:
        return theme.accent2
    if count < 10:
        return theme.accent
    return theme.good


def render_activity_card(stats: AccountStats, theme: Theme) -> str:
    width, height = 820, 250
    body = [defs(theme), card_bg(width, height, theme)]
    body.append(f'<text x="28" y="44" class="title">Contribution activity</text>')
    body.append(f'<text x="28" y="68" class="subtitle">Last 12 months · current streak {stats.current_streak}d · longest streak {stats.longest_streak}d</text>')
    days = stats.contribution_days[-371:]
    cell, gap = 10, 3
    start_x, start_y = 28, 96
    for i, day in enumerate(days):
        week = i // 7
        dow = i % 7
        x = start_x + week * (cell + gap)
        y = start_y + dow * (cell + gap)
        body.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{_heat_color(day.count, theme)}"><title>{day.day.isoformat()}: {day.count}</title><animate attributeName="opacity" from="0" to="1" dur="500ms" fill="freeze"/></rect>')
    body.append(f'<text x="792" y="224" text-anchor="end" class="small">auto-generated · {stats.generated_at.replace(microsecond=0).isoformat()}</text>')
    return svg_root(width, height, "".join(body))


def _language_bar(langs: list[LanguageShare], total: int, x: int, y: int, width: int, theme: Theme) -> str:
    if total <= 0:
        return f'<rect x="{x}" y="{y}" width="{width}" height="18" rx="9" fill="{theme.track}"/>'
    parts = []
    offset = 0.0
    for lang in langs[:10]:
        w = max(3, width * lang.size / total)
        parts.append(f'<rect x="{x + offset:.2f}" y="{y}" width="{w:.2f}" height="18" rx="9" fill="{color_for(lang.name, lang.color)}"><animate attributeName="width" from="0" to="{w:.2f}" dur="650ms" fill="freeze"/></rect>')
        offset += w
    return "".join(parts)


def render_language_card(stats: AccountStats, theme: Theme) -> str:
    width, height = 820, 300
    total = sum(l.size for l in stats.weighted_languages)
    body = [defs(theme), card_bg(width, height, theme)]
    body.append(f'<text x="28" y="44" class="title">Language distribution</text>')
    body.append('<text x="28" y="68" class="subtitle">Weighted by repository language bytes; forks excluded</text>')
    body.append(_language_bar(stats.weighted_languages, total, 28, 98, 764, theme))
    for i, lang in enumerate(stats.weighted_languages[:12]):
        col = i % 3
        row = i // 3
        x = 28 + col * 255
        y = 150 + row * 32
        pct = (lang.size / total * 100) if total else 0
        body.append(f'<circle cx="{x + 5}" cy="{y - 5}" r="5" fill="{color_for(lang.name, lang.color)}"/><text x="{x + 18}" y="{y}" class="mono">{esc(truncate(lang.name, 18))}</text><text x="{x + 185}" y="{y}" class="small">{pct:.1f}%</text>')
    body.append(f'<text x="792" y="272" text-anchor="end" class="small">auto-generated · {stats.generated_at.replace(microsecond=0).isoformat()}</text>')
    return svg_root(width, height, "".join(body))


def render_repos_table_card(stats: AccountStats, theme: Theme, top_n: int = 12) -> str:
    repos = sorted(stats.repos, key=lambda r: r.last_commit_at or r.updated_at or datetime(1970, 1, 1, tzinfo=UTC), reverse=True)[:top_n]
    row_h = 34
    width, height = 980, 94 + row_h * len(repos)
    body = [defs(theme), card_bg(width, height, theme)]
    body.append(f'<text x="28" y="44" class="title">Recently active repositories</text>')
    body.append(f'<text x="28" y="68" class="subtitle">Top {len(repos)} sorted by last activity</text>')
    headers = [(28, "Repo"), (338, "Stars"), (420, "Commits"), (520, "Last commit"), (660, "Release"), (830, "Issues"), (900, "Lang")]
    for x, label in headers:
        body.append(f'<text x="{x}" y="100" class="label">{esc(label)}</text>')
    for i, repo in enumerate(repos):
        y = 130 + i * row_h
        fill = theme.track if i % 2 else theme.panel
        body.append(f'<rect x="20" y="{y - 21}" width="940" height="30" rx="7" fill="{fill}" opacity=".42"/>')
        release = repo.latest_release.tag if repo.latest_release and repo.latest_release.tag else "—"
        if repo.latest_release and repo.latest_release.published_at:
            release = f"{release} {repo.latest_release.published_at.date().isoformat()}"
        body.append(f'<text x="28" y="{y}" class="mono">{esc(truncate(repo.full_name, 34))}</text>')
        body.append(f'<text x="338" y="{y}" class="small">{esc(n(repo.stars))}</text><text x="420" y="{y}" class="small">{esc(n(repo.commits))}</text><text x="520" y="{y}" class="small">{esc(relative_time(repo.last_commit_at, stats.generated_at))}</text><text x="660" y="{y}" class="small">{esc(truncate(release, 21))}</text><text x="830" y="{y}" class="small">{esc(n(repo.open_issues))}</text><circle cx="906" cy="{y - 5}" r="5" fill="{color_for(repo.primary_language, repo.primary_language_color)}"/><text x="918" y="{y}" class="small">{esc(truncate(repo.primary_language or "—", 8))}</text>')
    body.append(f'<text x="960" y="{height - 20}" text-anchor="end" class="small">auto-generated · {stats.generated_at.replace(microsecond=0).isoformat()}</text>')
    return svg_root(width, height, "".join(body))


def render_now_building_card(stats: AccountStats, theme: Theme) -> str:
    repos = sorted(stats.repos, key=lambda r: r.last_commit_at or r.updated_at or datetime(1970, 1, 1, tzinfo=UTC), reverse=True)[:3]
    width, height = 820, 270
    body = [defs(theme), card_bg(width, height, theme)]
    body.append(f'<text x="28" y="44" class="title">Now building</text>')
    body.append('<text x="28" y="68" class="subtitle">The three repositories with the most recent commits</text>')
    for i, repo in enumerate(repos):
        y = 112 + i * 54
        body.append(f'<circle cx="38" cy="{y - 7}" r="7" fill="{color_for(repo.primary_language, repo.primary_language_color)}"/><text x="56" y="{y - 12}" class="mono">{esc(truncate(repo.full_name, 45))}</text><text x="56" y="{y + 10}" class="small">{esc(relative_time(repo.last_commit_at, stats.generated_at))} · {esc(truncate(repo.last_commit_message or "—", 78))}</text>')
    body.append(f'<text x="792" y="244" text-anchor="end" class="small">auto-generated · {stats.generated_at.replace(microsecond=0).isoformat()}</text>')
    return svg_root(width, height, "".join(body))
