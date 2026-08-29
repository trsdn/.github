"""Tests for the internal link checker.

The checker is only worth having if it fails on a real break and stays quiet on
everything that merely looks like one. Both halves are asserted here: the false
negatives it must catch, and the false positives it must not raise.
"""

from __future__ import annotations

from support import ScriptTestCase


class LinkTests(ScriptTestCase):
    def write(self, name: str, text: str) -> None:
        path = self.repository / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_links(self):
        return self.run_script("links.py")

    def test_resolvable_links_are_accepted(self) -> None:
        self.write("README.md", "# Title\n\n[docs](docs/guide.md)\n")
        self.write("docs/guide.md", "# Guide\n")
        self.assertAccepts(self.run_links())

    def test_missing_file_is_rejected(self) -> None:
        self.write("README.md", "# Title\n\n[gone](docs/missing.md)\n")
        self.assertRejects(self.run_links(), "link target does not exist")

    def test_missing_anchor_in_another_file_is_rejected(self) -> None:
        self.write("README.md", "# Title\n\n[see](docs/guide.md#absent)\n")
        self.write("docs/guide.md", "# Guide\n")
        self.assertRejects(self.run_links(), "anchor not found")

    def test_missing_anchor_in_the_same_file_is_rejected(self) -> None:
        self.write("README.md", "# Title\n\n[see](#absent)\n")
        self.assertRejects(self.run_links(), "anchor not found")

    def test_heading_anchor_is_resolved(self) -> None:
        self.write("README.md", "# Title\n\n## Some Section\n\n[see](#some-section)\n")
        self.assertAccepts(self.run_links())

    def test_explicit_html_anchor_is_resolved(self) -> None:
        """The standard's criteria are addressed this way, not by heading text."""
        self.write("README.md", '# Title\n\n[see](docs/guide.md#s05)\n')
        self.write("docs/guide.md", '# Guide\n\n| <a id="s05"></a>S05 | Requirement |\n')
        self.assertAccepts(self.run_links())

    def test_repeated_headings_get_numbered_anchors(self) -> None:
        self.write(
            "README.md",
            "# Title\n\n## Notes\n\n## Notes\n\n[first](#notes)\n[second](#notes-1)\n",
        )
        self.assertAccepts(self.run_links())

    def test_external_links_are_not_checked(self) -> None:
        self.write(
            "README.md",
            "# Title\n\n[site](https://example.invalid/nowhere)\n"
            "[mail](mailto:someone@example.invalid)\n",
        )
        self.assertAccepts(self.run_links())

    def test_links_inside_code_fences_are_ignored(self) -> None:
        """Documentation shows examples whose paths exist elsewhere, not here."""
        self.write(
            "README.md",
            "# Title\n\n```md\n[example](.github/stats/repo-card.svg)\n```\n",
        )
        self.assertAccepts(self.run_links())

    def test_html_src_attributes_are_checked(self) -> None:
        self.write("README.md", '# Title\n\n<img src="assets/missing.svg">\n')
        self.assertRejects(self.run_links(), "link target does not exist")

    def test_reference_style_definitions_are_checked(self) -> None:
        self.write("README.md", "# Title\n\n[text][ref]\n\n[ref]: docs/missing.md\n")
        self.assertRejects(self.run_links(), "link target does not exist")

    def test_root_relative_targets_resolve_from_the_repository_root(self) -> None:
        self.write("docs/guide.md", "# Guide\n\n[readme](/README.md)\n")
        self.write("README.md", "# Title\n")
        self.assertAccepts(self.run_links())

    def test_anchors_on_non_markdown_targets_are_not_checked(self) -> None:
        self.write("README.md", "# Title\n\n[part](assets/thing.svg#layer)\n")
        self.write("assets/thing.svg", "<svg></svg>")
        self.assertAccepts(self.run_links())

    def test_every_broken_link_is_reported_not_just_the_first(self) -> None:
        self.write(
            "README.md",
            "# Title\n\n[one](docs/a.md)\n[two](docs/b.md)\n[three](docs/c.md)\n",
        )
        result = self.run_links()
        self.assertRejects(result, "3 broken internal link(s)")
