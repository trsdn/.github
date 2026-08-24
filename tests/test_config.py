from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from profile_stats.config import load_config


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.out = Path('out')
        self.out.mkdir(exist_ok=True)

    def tearDown(self) -> None:
        for path in self.out.glob('test-config*.yml'):
            path.unlink(missing_ok=True)
        try:
            self.out.rmdir()
        except OSError:
            pass

    def write_config(self, name: str, text: str) -> Path:
        path = self.out / name
        path.write_text(text)
        return path

    def test_load_config_merges_defaults(self) -> None:
        path = self.write_config(
            'test-config.yml',
            'username: trsdn\ntop_n: 5\nrepo:\n  exclude:\n    - old\n',
        )
        cfg = load_config(path)
        self.assertEqual(cfg['username'], 'trsdn')
        self.assertEqual(cfg['top_n'], 5)
        self.assertEqual(cfg['repo']['exclude'], ['old'])
        self.assertEqual(cfg['cards']['repo'], ['repo-card'])

    def test_config_rejects_invalid_top_n(self) -> None:
        path = self.write_config('test-config-invalid.yml', 'top_n: 0\n')
        with self.assertRaises(ValueError):
            load_config(path)

    def test_default_config_loads_without_third_party_yaml(self) -> None:
        cfg = load_config('scripts/profile_stats/config.yml')
        self.assertEqual(cfg['cards']['account'][0], 'overview')
        self.assertEqual(cfg['repo']['include'], [])


if __name__ == "__main__":
    unittest.main()
