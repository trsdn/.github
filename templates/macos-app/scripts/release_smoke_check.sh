#!/usr/bin/env bash
# Checks a published release the way a consumer receives it, on your own Mac,
# for an app whose repository has no hosted Actions minutes to run smoke-test.yml.
# Copy to scripts/release_smoke_check.sh, make it executable, and replace every
# TODO(...) marker below.
#
# For each asset it downloads the release asset and its checksum with `gh`,
# verifies the checksum, unpacks a ZIP or mounts a DMG read-only into a temporary
# directory, and checks that the bundle carries the release's version, that its
# Developer ID signature verifies, that Gatekeeper accepts it, and that the
# notarization ticket is stapled. It removes everything it created.
#
# It never starts the app, uses no credentials beyond `gh` access to the
# repository, and needs no elevated privileges. What it does not cover: that the
# app starts and works, which needs a person at a logged-in desktop.
#
# Usage:
#   scripts/release_smoke_check.sh 1.2.3
#
# Exit codes: 0 every check passed, 1 a check failed, 2 a tool is missing,
# 64 the arguments are wrong.

set -uo pipefail

# TODO(repo): the OWNER/NAME of the repository that holds the release.
repo="TODO(repo)"
# TODO(assets): one entry per asset to check, as BUNDLE_NAME:ASSET_FILE_NAME.
# `@VERSION@` is replaced by the version. The extension decides how the asset is
# opened: .zip is unpacked, .dmg is mounted read-only. Every asset needs a
# matching `.sha256` file beside it in the release.
assets=(
  "TODO(app-name):TODO(app-name)-v@VERSION@-macOS-arm64.dmg"
)

version="${1:-}"
if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "usage: $0 MAJOR.MINOR.PATCH" >&2
  exit 64
fi
for tool in gh shasum unzip hdiutil ditto codesign spctl xcrun sw_vers; do
  command -v "$tool" > /dev/null 2>&1 || { echo "missing tool: $tool" >&2; exit 2; }
done
plist="/usr/libexec/PlistBuddy"
[[ -x "$plist" ]] || { echo "missing tool: $plist" >&2; exit 2; }

work="$(mktemp -d)"
mounted=""
cleanup() {
  if [[ -n "$mounted" ]]; then
    hdiutil detach "$mounted" > /dev/null 2>&1 || true
  fi
  rm -rf "$work"
}
trap cleanup EXIT
failed=0

# Run one named check, print its result, and keep going after a failure so one
# run reports every problem.
check() {
  local name="$1"
  shift
  if "$@" > "$work/out.log" 2>&1; then
    printf '  pass  %s\n' "$name"
  else
    printf '  FAIL  %s\n' "$name"
    sed 's/^/        /' "$work/out.log"
    failed=1
  fi
}

bundle_version() { [[ "$("$plist" -c 'Print :CFBundleShortVersionString' "$1/Contents/Info.plist")" == "$2" ]]; }
has_executable() { [[ -x "$1/Contents/MacOS/$("$plist" -c 'Print :CFBundleExecutable' "$1/Contents/Info.plist")" ]]; }
checksum_ok() { (cd "$1" && shasum -a 256 -c "$2"); }

for entry in "${assets[@]}"; do
  bundle="${entry%%:*}"
  file="${entry#*:}"
  file="${file//@VERSION@/$version}"
  dir="$work/$bundle"
  mkdir -p "$dir"
  echo "$bundle $version ($file)"

  if ! gh release download "v${version}" --repo "$repo" --dir "$dir" \
    --pattern "$file" --pattern "${file}.sha256" > /dev/null 2>&1; then
    printf '  FAIL  download of %s\n' "$file"
    failed=1
    continue
  fi
  check "checksum" checksum_ok "$dir" "${file}.sha256"

  app=""
  case "$file" in
    *.zip)
      if unzip -q "$dir/$file" -d "$dir/unpacked"; then
        app="$dir/unpacked/${bundle}.app"
      fi
      ;;
    *.dmg)
      mount="$dir/mount"
      mkdir -p "$mount"
      if hdiutil attach "$dir/$file" -nobrowse -readonly -mountpoint "$mount" > /dev/null 2>&1; then
        mounted="$mount"
        mkdir -p "$dir/unpacked"
        ditto "$mount/${bundle}.app" "$dir/unpacked/${bundle}.app" || true
        hdiutil detach "$mount" > /dev/null 2>&1 || true
        mounted=""
        app="$dir/unpacked/${bundle}.app"
      fi
      ;;
    *)
      printf '  FAIL  unsupported asset type: %s\n' "$file"
      failed=1
      continue
      ;;
  esac
  if [[ -z "$app" || ! -d "$app" ]]; then
    printf '  FAIL  could not open %s or it holds no %s.app\n' "$file" "$bundle"
    failed=1
    continue
  fi

  check "bundle version is $version" bundle_version "$app" "$version"
  check "executable is present" has_executable "$app"
  check "codesign verifies" codesign --verify --deep --strict --verbose=2 "$app"
  check "Gatekeeper accepts" spctl --assess --type execute --verbose=2 "$app"
  check "notarization ticket is stapled" xcrun stapler validate "$app"
done

echo
if [[ "$failed" -eq 0 ]]; then
  echo "Release smoke check v${version}: pass ($(date +%F), macOS $(sw_vers -productVersion), $(uname -m))"
else
  echo "Release smoke check v${version}: FAIL"
  exit 1
fi
