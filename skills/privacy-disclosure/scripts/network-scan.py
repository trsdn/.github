"""Find what a product talks to, stores, and reports, so it can be disclosed.

Evidence for `Y01`-`Y05`: outbound hosts in source, telemetry and crash-reporting
SDKs, third-party and AI providers, and local storage locations. It reports what
is in the source with file and line, and decides nothing: whether a host is a
*product* destination or a build-time one, and whether a disclosure is adequate,
are readings this deliberately leaves to whoever runs it.

Read-only.

Usage:
    python3 network-scan.py --path /path/to/checkout [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import defaultdict

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".build",
    "build",
    "dist",
    ".venv",
    "venv",
    "Pods",
    "Carthage",
    "vendor",
    "third_party",
    ".next",
    "target",
    "DerivedData",
    "__pycache__",
}

CODE_SUFFIXES = {
    ".swift",
    ".m",
    ".mm",
    ".h",
    ".c",
    ".cc",
    ".cpp",
    ".py",
    ".js",
    ".mjs",
    ".ts",
    ".tsx",
    ".jsx",
    ".go",
    ".rs",
    ".rb",
    ".java",
    ".kt",
    ".cs",
}

CONFIG_SUFFIXES = {".yml", ".yaml", ".json", ".toml", ".plist", ".xml", ".sh"}

DOC_SUFFIXES = {".md", ".html", ".css"}

SOURCE_SUFFIXES = CODE_SUFFIXES | CONFIG_SUFFIXES | DOC_SUFFIXES

URL = re.compile(r"https?://([A-Za-z0-9.\-]+\.[A-Za-z]{2,})(?::\d+)?")

# Hosts that belong to developing rather than running the product. They are
# reported separately rather than dropped, because which is which is a reading
# and not a fact.
BUILD_TIME_HINTS = (
    "github.com",
    "api.github.com",
    "raw.githubusercontent.com",
    "objects.githubusercontent.com",
    "pypi.org",
    "files.pythonhosted.org",
    "registry.npmjs.org",
    "crates.io",
    "golang.org",
    "proxy.golang.org",
    "nuget.org",
    "maven.apache.org",
    "schema.org",
    "www.w3.org",
    "docs.github.com",
    "developer.apple.com",
    "swift.org",
    "json-schema.org",
    "spdx.org",
)

TELEMETRY = {
    "Sentry": ("sentry-", "SentrySDK", "sentry.io", "sentry_sdk"),
    "Crashlytics": ("Crashlytics", "firebase-crashlytics"),
    "Firebase": ("FirebaseCore", "firebase/app", "firebaseio.com"),
    "Google Analytics": ("google-analytics.com", "gtag(", "googletagmanager"),
    "Mixpanel": ("Mixpanel", "mixpanel.com"),
    "Amplitude": ("Amplitude", "amplitude.com"),
    "PostHog": ("PostHog", "posthog.com"),
    "Matomo": ("Matomo", "matomo."),
    "App Center": ("AppCenter", "appcenter.ms"),
    "TelemetryDeck": ("TelemetryDeck", "telemetrydeck.com"),
    "Bugsnag": ("Bugsnag", "bugsnag.com"),
    "MetricKit": ("MetricKit", "MXMetricManager"),
    "Plausible": ("plausible.io",),
}

PROVIDERS = {
    "OpenAI": ("api.openai.com", "openai.com", "OpenAI("),
    "Anthropic": ("api.anthropic.com", "anthropic.com"),
    "Azure OpenAI": ("openai.azure.com", "cognitiveservices.azure.com"),
    "Google AI": ("generativelanguage.googleapis.com", "aiplatform.googleapis.com"),
    "Mistral": ("api.mistral.ai",),
    "Hugging Face": ("huggingface.co",),
    "AWS": ("amazonaws.com",),
}

STORAGE = {
    "Application Support": ("Application Support", "applicationSupportDirectory"),
    "UserDefaults": ("UserDefaults", "NSUserDefaults", "standardUserDefaults"),
    "Keychain": ("SecItemAdd", "Keychain", "kSecClass"),
    "Core Data": ("NSPersistentContainer", "NSManagedObject"),
    "SQLite": ("sqlite3", ".sqlite"),
    "Caches": ("cachesDirectory", "/Library/Caches"),
    "Documents": ("documentDirectory", "FileManager.default.urls"),
    "Temporary": ("NSTemporaryDirectory", "tempfile.", "mkstemp"),
}


def source_files(root: pathlib.Path, limit: int = 4000) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for path in root.rglob("*"):
        if len(files) >= limit:
            break
        if not path.is_file() or set(path.parts) & SKIP_DIRS:
            continue
        if path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        try:
            if path.stat().st_size > 1_000_000:
                continue
        except OSError:
            continue
        files.append(path)
    return files


def classify(path: pathlib.Path, root: pathlib.Path) -> str:
    """Code, config, or documentation — which decides what a match means.

    A telemetry SDK named in a Markdown file is usually a sentence saying it is
    *not* used, so matching there produces exactly the wrong finding. Only code
    and configuration are searched for SDKs and storage.
    """
    relative = path.relative_to(root)
    if relative.parts[:2] == (".github", "workflows"):
        return "build"
    if path.suffix.lower() in CODE_SUFFIXES:
        return "code"
    if path.suffix.lower() in CONFIG_SUFFIXES:
        return "config"
    return "doc"


def scan(root: pathlib.Path) -> dict:
    hosts: dict[str, dict[str, list[str]]] = {
        "code": defaultdict(list),
        "config": defaultdict(list),
        "doc": defaultdict(list),
        "build": defaultdict(list),
    }
    telemetry: dict[str, list[str]] = defaultdict(list)
    providers: dict[str, list[str]] = defaultdict(list)
    storage: dict[str, list[str]] = defaultdict(list)

    for path in source_files(root):
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        relative = str(path.relative_to(root))
        kind = classify(path, root)
        for number, line in enumerate(text.splitlines(), start=1):
            where = f"{relative}:{number}"
            for match in URL.finditer(line):
                host = match.group(1).lower()
                # A plist or XML doctype is a schema reference, not a destination.
                if "DTD" in line or "!DOCTYPE" in line or "xmlns" in line:
                    continue
                if where not in hosts[kind][host]:
                    hosts[kind][host].append(where)
            if kind == "doc":
                continue
            for name, markers in TELEMETRY.items():
                if any(marker in line for marker in markers):
                    telemetry[name].append(where)
            for name, markers in PROVIDERS.items():
                if any(marker in line for marker in markers):
                    providers[name].append(where)
            for name, markers in STORAGE.items():
                if any(marker in line for marker in markers):
                    storage[name].append(where)

    def split(group: dict[str, list[str]]) -> tuple[dict, list[str]]:
        product = {h: p[:5] for h, p in sorted(group.items()) if h not in BUILD_TIME_HINTS}
        known = sorted(h for h in group if h in BUILD_TIME_HINTS)
        return product, known

    runtime = defaultdict(list)
    for kind in ("code", "config"):
        for host, places in hosts[kind].items():
            runtime[host].extend(places)
    product_hosts, build_like = split(runtime)
    doc_hosts, _ = split(hosts["doc"])

    return {
        "path": str(root),
        "product_hosts": product_hosts,
        "documentation_hosts": doc_hosts,
        "build_or_schema_hosts": build_like,
        "telemetry": {name: places[:5] for name, places in sorted(telemetry.items())},
        "providers": {name: places[:5] for name, places in sorted(providers.items())},
        "storage": {name: places[:3] for name, places in sorted(storage.items())},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()

    root = arguments.path.resolve()
    if not root.is_dir():
        print(f"privacy: {root} is not a directory", file=sys.stderr)
        return 1

    report = scan(root)
    if arguments.json:
        print(json.dumps(report, indent=2))
        return 0

    print("Y02 — outbound hosts in code and configuration")
    if report["product_hosts"]:
        for host, places in report["product_hosts"].items():
            print(f"  {host}")
            for place in places:
                print(f"      {place}")
    else:
        print("  none found. If the product contacts nothing, Y02 is met by saying so")
    if report["build_or_schema_hosts"]:
        print(
            "  (build, schema or platform hosts, usually not product destinations: "
            + ", ".join(report["build_or_schema_hosts"])
            + ")"
        )
    if report["documentation_hosts"]:
        print(
            "\n  Hosts in the README, site or docs only. These are not Y02 destinations, "
            "but a site loading them is what W07 asks about:"
        )
        for host in report["documentation_hosts"]:
            print(f"      {host}")

    print("\nY03 — telemetry, analytics, crash reporting")
    if report["telemetry"]:
        for name, places in report["telemetry"].items():
            print(f"  {name}: {places[0]}")
        print("  → each must be off by default or opt-in, and disclosed")
    else:
        print("  none found. Y03 is met by a source review showing none is present")

    print("\nY05 — third-party and AI providers receiving user content")
    if report["providers"]:
        for name, places in report["providers"].items():
            print(f"  {name}: {places[0]}")
    else:
        print("  none found")

    print("\nY04 and Y06 — local storage the product writes")
    if report["storage"]:
        for name, places in report["storage"].items():
            print(f"  {name}: {places[0]}")
        print("  → document where it lives, and how a user finds, exports, or deletes it")
    else:
        print("  none found. If nothing outlives the process, say so for Y04 and Y06")

    print(
        "\nThis lists what is in the source. Whether a host is a product destination, "
        "and whether the disclosure is adequate, is yours to decide."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
