from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from datetime import UTC, datetime
from xml.etree import ElementTree
import unittest

from profile_stats.models import AccountStats, ContributionDay, LanguageShare, ReleaseStats, RepoStats
from profile_stats.render.account import render_activity_card, render_language_card, render_now_building_card, render_overview_card, render_repos_table_card
from profile_stats.render.repo import render_repo_card
from profile_stats.render.theme import LIGHT


def repo_stats():
    return RepoStats(
        owner='trsdn', name='demo', full_name='trsdn/demo', description='Demo <repo>', default_branch='main', is_private=False,
        stars=12, forks=3, watchers=4, open_issues=1, open_prs=2, releases=1,
        latest_release=ReleaseStats('v1.0.0', datetime(2026, 8, 20, tzinfo=UTC), 5), commits=99,
        last_commit_at=datetime(2026, 8, 24, tzinfo=UTC), last_commit_message='Fix & ship', contributors=4,
        primary_language='Python', primary_language_color='#3572A5', languages=[LanguageShare('Python', 90, '#3572A5'), LanguageShare('Shell', 10, '#89e051')],
        language_total=100, disk_usage_kb=2048, license_name='MIT', commit_activity=[0, 1, 3] * 18,
        updated_at=datetime(2026, 8, 24, tzinfo=UTC),
    )


def account_stats():
    days = [ContributionDay(datetime(2026, 8, d, tzinfo=UTC).date(), d % 4) for d in range(1, 25)]
    return AccountStats('trsdn', datetime(2026, 8, 24, tzinfo=UTC), [repo_stats()], 99, 12, 7, 8, 9, 10, 1, days, 2, 8, [LanguageShare('Python', 90, '#3572A5')])


class RenderTests(unittest.TestCase):
    def assert_well_formed(self, svg: str) -> None:
        ElementTree.fromstring(svg)
        self.assertNotIn('<script', svg)
        self.assertNotIn('<foreignObject', svg)

    def test_repo_card_is_well_formed(self) -> None:
        self.assert_well_formed(render_repo_card(repo_stats(), LIGHT, datetime(2026, 8, 24, tzinfo=UTC)))

    def test_account_cards_are_well_formed(self) -> None:
        stats = account_stats()
        for svg in [
            render_overview_card(stats, LIGHT),
            render_activity_card(stats, LIGHT),
            render_language_card(stats, LIGHT),
            render_repos_table_card(stats, LIGHT),
            render_now_building_card(stats, LIGHT),
        ]:
            with self.subTest(svg=svg[:40]):
                self.assert_well_formed(svg)


if __name__ == "__main__":
    unittest.main()
