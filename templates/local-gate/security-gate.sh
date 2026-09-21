#!/usr/bin/env bash
# security-gate.sh: the two checks criterion R09 asks for before a release, run
# locally, for a repository that has no hosted Actions minutes to run them on.
#
# Run it from a clean checkout of the release commit:
#
#   scripts/security-gate.sh                     # print a result block
#   scripts/security-gate.sh --record FILE       # and append it to FILE
#
# It scans the tree and the history for secrets with gitleaks, and audits the
# lockfiles and manifests it finds with osv-scanner, falling back to npm audit and
# pip-audit. It never reports a pass for a check it could not run: a missing tool
# is "not run" and the exit code says so.
#
# Exit codes: 0 every check passed or does not apply, 1 a check found something,
# 2 a check could not run because its tool is missing.
#
# TODO(tools): install what it reports missing, for example
#   brew install gitleaks osv-scanner
#   pipx install pip-audit        # only if you use it instead of osv-scanner

set -uo pipefail

record_file=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --record)
      record_file="${2:-}"
      [[ -n "$record_file" ]] || { echo "--record needs a file" >&2; exit 64; }
      shift 2
      ;;
    -h | --help)
      sed -n '2,20p' "$0"
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 64
      ;;
  esac
done

root="$(git rev-parse --show-toplevel)" || { echo "not a git repository" >&2; exit 64; }
cd "$root" || exit 64
commit="$(git rev-parse HEAD)"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "warning: the working tree has uncommitted changes; the record names commit ${commit:0:12}, so commit or stash first." >&2
fi

have() { command -v "$1" > /dev/null 2>&1; }

secret_result=""
secret_detail=""
dependency_result=""
dependency_detail=""
worst=0
note_status() { [[ "$1" -gt "$worst" ]] && worst="$1"; return 0; }

# --- Secret scan -------------------------------------------------------------
if have gitleaks; then
  version="$(gitleaks version 2> /dev/null | head -1)"
  if gitleaks git --help > /dev/null 2>&1; then
    gitleaks git --no-banner --redact --exit-code 1 . > /dev/null 2>&1
  else
    gitleaks detect --source . --no-banner --redact --exit-code 1 > /dev/null 2>&1
  fi
  code=$?
  case "$code" in
    0)
      secret_result="pass"
      secret_detail="gitleaks ${version}, tree and history"
      ;;
    1)
      secret_result="fail"
      secret_detail="gitleaks ${version} reported findings; run it without redirection to see them"
      note_status 1
      ;;
    *)
      secret_result="not run"
      secret_detail="gitleaks ${version} failed with exit code ${code}"
      note_status 2
      ;;
  esac
else
  secret_result="not run"
  secret_detail="gitleaks is not installed"
  note_status 2
fi

# --- Dependency vulnerability check -----------------------------------------
lockfiles="$(git ls-files | grep -E '(^|/)(Package\.resolved|package-lock\.json|yarn\.lock|pnpm-lock\.yaml|poetry\.lock|uv\.lock|Pipfile\.lock|requirements[^/]*\.txt|Cargo\.lock|go\.sum|packages\.lock\.json|Gemfile\.lock|composer\.lock)$' || true)"

if [[ -z "$lockfiles" ]]; then
  dependency_result="not applicable"
  dependency_detail="no lockfile or dependency manifest is tracked"
elif have osv-scanner; then
  version="$(osv-scanner --version 2> /dev/null | head -1)"
  json="$(mktemp)"
  trap 'rm -f "$json"' EXIT
  if osv-scanner scan source --help > /dev/null 2>&1; then
    osv-scanner scan source -r . --format json > "$json" 2> /dev/null
  else
    osv-scanner -r . --format json > "$json" 2> /dev/null
  fi
  code=$?
  case "$code" in
    0 | 1)
      # osv-scanner exits 1 for any advisory. R09 asks about high and critical
      # ones, so count those (CVSS 7.0 or above) and treat an unrated advisory as
      # high, because nobody has said it is not.
      counts="$(
        python3 - "$json" 2> /dev/null << 'PY'
import json, sys

data = json.load(open(sys.argv[1]))
total = high = 0
for result in data.get("results") or []:
    for package in result.get("packages") or []:
        for group in package.get("groups") or []:
            total += 1
            try:
                score = float(group.get("max_severity", ""))
            except ValueError:
                high += 1
                continue
            if score >= 7.0:
                high += 1
print(total, high)
PY
      )"
      if [[ -z "$counts" ]]; then
        if [[ $code -eq 0 ]]; then
          dependency_result="pass"
          dependency_detail="${version}, no advisories"
        else
          dependency_result="fail"
          dependency_detail="${version} reported advisories and python3 is missing to rate them; run it to see them"
          note_status 1
        fi
      else
        total="${counts% *}"
        high="${counts#* }"
        if [[ "$high" -gt 0 ]]; then
          dependency_result="fail"
          dependency_detail="${version}, ${high} advisory at high severity or unrated, ${total} in all; run osv-scanner to see them"
          note_status 1
        else
          dependency_result="pass"
          dependency_detail="${version}, no high or critical advisory (${total} lower-severity in all)"
        fi
      fi
      ;;
    128)
      dependency_result="not applicable"
      dependency_detail="${version} found no packages in the tracked files"
      ;;
    *)
      dependency_result="not run"
      dependency_detail="${version} failed with exit code ${code}"
      note_status 2
      ;;
  esac
else
  # Without osv-scanner, use the native audit for each ecosystem present.
  ran_any=0
  failed=0
  if echo "$lockfiles" | grep -q 'package-lock\.json' && have npm; then
    ran_any=1
    npm audit --audit-level=high > /dev/null 2>&1 || failed=1
  fi
  if echo "$lockfiles" | grep -q 'requirements' && have pip-audit; then
    ran_any=1
    while IFS= read -r file; do
      pip-audit -r "$file" > /dev/null 2>&1 || failed=1
    done < <(echo "$lockfiles" | grep 'requirements')
  fi
  if [[ $ran_any -eq 0 ]]; then
    dependency_result="not run"
    dependency_detail="osv-scanner is not installed, and no native audit tool matches the lockfiles found"
    note_status 2
  elif [[ $failed -eq 1 ]]; then
    dependency_result="fail"
    dependency_detail="a native audit reported advisories at high severity or above"
    note_status 1
  else
    dependency_result="pass"
    dependency_detail="native audit (npm audit or pip-audit) only; osv-scanner would cover more"
  fi
fi

# --- Result block ------------------------------------------------------------
block="$(
  cat << EOF
## Security gate: $(date +%Y-%m-%d)

- Commit: ${commit}
- Secret scan: ${secret_result} (${secret_detail})
- Dependencies: ${dependency_result} (${dependency_detail})
EOF
)"

echo "$block"
if [[ -n "$record_file" ]]; then
  { echo; echo "$block"; } >> "$record_file"
  echo "appended to ${record_file}" >&2
fi

exit "$worst"
