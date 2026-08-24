"""Repo stats card renderer."""

from __future__ import annotations

from datetime import UTC, datetime

from .svg import bytesize, esc, iso_date, n, relative_time, svg_root, truncate
from .theme import Theme, card_bg, defs
from ..models import RepoStats
from ..languages import color_for


def _metric(x: int, y: int, label: str, value: object) -> str:
    return f'<text x="{x}" y="{y}" class="label">{esc(label)}</text><text x="{x}" y="{y + 23}" class="value">{esc(value)}</text>'


def _language_bar(stats: RepoStats, x: int, y: int, width: int) -> str:
    if not stats.languages or stats.language_total <= 0:
        return f'<rect x="{x}" y="{y}" width="{width}" height="10" rx="5" fill="#8b949e" opacity=".35"/>'
    parts = []
    offset = 0.0
    for lang in stats.languages[:8]:
        w = max(2.0, width * lang.size / stats.language_total)
        parts.append(f'<rect x="{x + offset:.2f}" y="{y}" width="{w:.2f}" height="10" rx="5" fill="{color_for(lang.name, lang.color)}"><animate attributeName="width" from="0" to="{w:.2f}" dur="600ms" fill="freeze"/></rect>')
        offset += w
    legend = []
    lx = x
    ly = y + 26
    for lang in stats.languages[:4]:
        pct = lang.size / stats.language_total * 100
        legend.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="4" fill="{color_for(lang.name, lang.color)}"/><text x="{lx + 14}" y="{ly}" class="small">{esc(truncate(lang.name, 12))} {pct:.0f}%</text>')
        lx += 115
    return "".join(parts + legend)


def _activity_bars(stats: RepoStats, x: int, y: int, width: int, height: int, theme: Theme) -> str:
    values = (stats.commit_activity or [])[-52:]
    if not values:
        values = [0] * 52
    max_value = max(values) or 1
    gap = 2
    bar_w = (width - gap * (len(values) - 1)) / len(values)
    parts = [f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="6" fill="{theme.track}" opacity=".42"/>']
    for i, value in enumerate(values):
        h = max(2, height * value / max_value) if value else 2
        bx = x + i * (bar_w + gap)
        by = y + height - h
        opacity = .35 + .65 * (value / max_value if max_value else 0)
        parts.append(f'<rect x="{bx:.2f}" y="{by:.2f}" width="{bar_w:.2f}" height="{h:.2f}" rx="2" fill="{theme.accent}" opacity="{opacity:.2f}"><animate attributeName="height" from="0" to="{h:.2f}" dur="700ms" fill="freeze"/><animate attributeName="y" from="{y + height}" to="{by:.2f}" dur="700ms" fill="freeze"/></rect>')
    return "".join(parts)


def render_repo_card(stats: RepoStats, theme: Theme, generated_at: datetime | None = None) -> str:
    generated_at = generated_at or datetime.now(UTC)
    width, height = 820, 480
    release = stats.latest_release
    release_text = "—"
    if release and release.tag:
        release_text = f"{release.tag} · {iso_date(release.published_at)} · {n(release.asset_downloads)} dl"
    body = [defs(theme), card_bg(width, height, theme)]
    body.append(f'<text x="28" y="44" class="title">{esc(truncate(stats.full_name, 54))}</text>')
    body.append(f'<text x="28" y="68" class="subtitle">{esc(truncate(stats.description or "No description", 112))}</text>')
    body.append(f'<circle cx="774" cy="40" r="7" fill="{color_for(stats.primary_language, stats.primary_language_color)}"/><text x="754" y="64" text-anchor="end" class="small">{esc(stats.primary_language or "Unknown")}</text>')
    metrics = [
        (28, 114, "Commits", n(stats.commits)),
        (158, 114, "Last commit", relative_time(stats.last_commit_at, generated_at)),
        (306, 114, "Stars", n(stats.stars)),
        (416, 114, "Forks", n(stats.forks)),
        (526, 114, "Watchers", n(stats.watchers)),
        (646, 114, "Contributors", n(stats.contributors)),
        (28, 186, "Open issues", n(stats.open_issues)),
        (158, 186, "Open PRs", n(stats.open_prs)),
        (306, 186, "Releases", n(stats.releases)),
        (416, 186, "Size", bytesize(stats.disk_usage_kb)),
        (526, 186, "License", truncate(stats.license_name or "—", 16)),
        (646, 186, "Branch", truncate(stats.default_branch, 15)),
    ]
    body.extend(_metric(*m) for m in metrics)
    body.append(f'<text x="28" y="258" class="label">Latest release</text><text x="28" y="281" class="mono">{esc(truncate(release_text, 58))}</text>')
    body.append(f'<text x="416" y="258" class="label">Last message</text><text x="416" y="281" class="mono">{esc(truncate(stats.last_commit_message or "—", 48))}</text>')
    body.append(f'<text x="28" y="326" class="label">Language distribution</text>')
    body.append(_language_bar(stats, 28, 342, 764))
    body.append(f'<text x="28" y="410" class="label">Commit activity · 52 weeks</text>')
    body.append(_activity_bars(stats, 28, 424, 764, 30, theme))
    body.append(f'<text x="792" y="466" text-anchor="end" class="small">auto-generated · {generated_at.replace(microsecond=0).isoformat()}</text>')
    return svg_root(width, height, "".join(body))
