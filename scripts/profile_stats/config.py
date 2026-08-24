"""Configuration loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "username": "trsdn",
    "top_n": 12,
    "include_private": False,
    "repo": {"include": [], "exclude": []},
    "cards": {
        "repo": ["repo-card"],
        "account": ["overview", "activity", "language", "repos-table", "now-building"],
    },
    "themes": {},
}


def _merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    cfg = dict(DEFAULT_CONFIG)
    config_path = Path(path) if path else Path(__file__).with_name("config.yml")
    if config_path.exists():
        loaded = yaml.safe_load(config_path.read_text()) or {}
        if not isinstance(loaded, dict):
            raise ValueError("configuration root must be a mapping")
        cfg = _merge(cfg, loaded)
    if not isinstance(cfg.get("username"), str) or not cfg["username"]:
        raise ValueError("username must be a non-empty string")
    top_n = cfg.get("top_n")
    if not isinstance(top_n, int) or top_n < 1 or top_n > 100:
        raise ValueError("top_n must be an integer between 1 and 100")
    repo = cfg.get("repo", {})
    for key in ("include", "exclude"):
        if key in repo and not isinstance(repo[key], list):
            raise ValueError(f"repo.{key} must be a list")
    return cfg
