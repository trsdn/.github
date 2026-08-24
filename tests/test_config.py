from pathlib import Path

import pytest

from profile_stats.config import load_config


def _workspace_file(name: str, text: str) -> Path:
    path = Path('out') / name
    path.parent.mkdir(exist_ok=True)
    path.write_text(text)
    return path


def test_load_config_merges_defaults():
    path = _workspace_file('test-config.yml', 'username: trsdn\ntop_n: 5\nrepo:\n  exclude:\n    - old\n')
    try:
        cfg = load_config(path)
        assert cfg['username'] == 'trsdn'
        assert cfg['top_n'] == 5
        assert cfg['repo']['exclude'] == ['old']
        assert cfg['cards']['repo'] == ['repo-card']
    finally:
        path.unlink(missing_ok=True)


def test_config_rejects_invalid_top_n():
    path = _workspace_file('test-config-invalid.yml', 'top_n: 0\n')
    try:
        with pytest.raises(ValueError):
            load_config(path)
    finally:
        path.unlink(missing_ok=True)
