from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import unittest

from profile_stats.collect import collect_account_stats, collect_repo_stats


class FakeClient:
    def graphql(self, query, variables):
        if "RepoStats" in query:
            return {"repository": repo_node("trsdn/OpenLens")}
        if "AccountProfile" in query:
            return {
                "user": {
                    "login": "trsdn",
                    "followers": {"totalCount": 7},
                    "contributionsCollection": {
                        "contributionCalendar": {
                            "weeks": [
                                {
                                    "contributionDays": [
                                        {"date": "2026-08-21", "contributionCount": 1},
                                        {"date": "2026-08-22", "contributionCount": 0},
                                        {"date": "2026-08-23", "contributionCount": 2},
                                        {"date": "2026-08-24", "contributionCount": 3},
                                    ]
                                }
                            ]
                        }
                    },
                }
            }
        return {
            "user": {
                "repositories": {
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                    "nodes": [repo_node("trsdn/OpenLens"), repo_node("trsdn/fork", is_fork=True)],
                }
            }
        }

    def count_paginated(self, path, params=None):
        return 3

    def stats_commit_activity(self, owner, repo):
        return [0, 1, 2]

    def search_count(self, query):
        return 4


def repo_node(full_name, is_fork=False):
    owner, name = full_name.split("/")
    return {
        "name": name,
        "nameWithOwner": full_name,
        "description": "Example & repo",
        "isPrivate": False,
        "isFork": is_fork,
        "isArchived": False,
        "stargazerCount": 5,
        "forkCount": 2,
        "diskUsage": 123,
        "updatedAt": "2026-08-24T10:00:00Z",
        "watchers": {"totalCount": 1},
        "issues": {"totalCount": 6},
        "pullRequests": {"totalCount": 1},
        "releases": {"totalCount": 2},
        "latestRelease": {
            "tagName": "v1.0.0",
            "publishedAt": "2026-08-20T00:00:00Z",
            "releaseAssets": {"nodes": [{"downloadCount": 9}]},
        },
        "licenseInfo": {"name": "MIT License", "spdxId": "MIT"},
        "primaryLanguage": {"name": "Python", "color": "#3572A5"},
        "languages": {
            "totalSize": 100,
            "edges": [
                {"size": 80, "node": {"name": "Python", "color": "#3572A5"}},
                {"size": 20, "node": {"name": "Shell", "color": "#89e051"}},
            ],
        },
        "defaultBranchRef": {
            "name": "main",
            "target": {
                "history": {
                    "totalCount": 42,
                    "nodes": [
                        {
                            "committedDate": "2026-08-24T09:00:00Z",
                            "messageHeadline": "Update <stats>",
                        }
                    ],
                }
            },
        },
        "owner": {"login": owner},
    }


class CollectTests(unittest.TestCase):
    def test_collect_repo_stats_maps_fields(self) -> None:
        stats = collect_repo_stats(FakeClient(), "trsdn/OpenLens")
        self.assertEqual(stats.full_name, "trsdn/OpenLens")
        self.assertEqual(stats.commits, 42)
        self.assertEqual(stats.contributors, 3)
        self.assertEqual(stats.latest_release.asset_downloads, 9)
        self.assertEqual(stats.commit_activity, [0, 1, 2])

    def test_collect_account_stats_filters_forks_and_builds_language_weights(self) -> None:
        stats = collect_account_stats(FakeClient(), "trsdn")
        self.assertEqual(len(stats.repos), 1)
        self.assertEqual(stats.total_commits, 42)
        self.assertEqual(stats.total_stars, 5)
        self.assertEqual(stats.followers, 7)
        self.assertEqual(stats.current_streak, 2)
        self.assertEqual(stats.longest_streak, 2)
        self.assertEqual(stats.weighted_languages[0].name, "Python")


if __name__ == "__main__":
    unittest.main()
