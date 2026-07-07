#!/usr/bin/env bash
# Preflight checks for Nova nightly screenshot capture on macOS.
set -euo pipefail

FIREFOX_APP="${FIREFOX_APP:-/Applications/Firefox Nightly.app}"
FAIL=0

echo "Nova nightly capture — preflight"
echo ""
echo "Before capture: quit Firefox Nightly completely (Cmd+Q), so no translocated copy is running."
echo ""

if [[ ! -d "$FIREFOX_APP" ]]; then
  echo "✗ Firefox Nightly not found at: $FIREFOX_APP"
  exit 1
fi
echo "✓ Firefox Nightly installed"

if [[ ! -f "$FIREFOX_APP/Contents/Info.plist" ]]; then
  echo "✗ Firefox Nightly app bundle is incomplete (missing Contents/Info.plist)"
  if [[ -d "$FIREFOX_APP/updating" ]]; then
    echo "  Cause: Nightly is mid-update. Open Firefox Nightly from Finder once to finish,"
    echo "  or reinstall from https://www.mozilla.org/firefox/nightly/"
  else
    echo "  Cause: damaged install. Reinstall Nightly from https://www.mozilla.org/firefox/nightly/"
  fi
  echo ""
  echo "  Workaround: point shots.json firefox_binary at a healthy build, e.g.:"
  for candidate in \
    "$HOME/VibeCoding_BK/mozilla/firefox"/obj-*/dist/Nightly.app \
    "$HOME/mozilla/firefox"/obj-*/dist/Nightly.app; do
    if [[ -f "$candidate/Contents/Info.plist" ]]; then
      echo "    $candidate"
    fi
  done
  FAIL=1
else
  echo "✓ Firefox Nightly app bundle looks healthy"
fi

QUAR=$(xattr -p com.apple.quarantine "$FIREFOX_APP" 2>&1) || true
if [[ "$QUAR" == *"Operation not permitted"* ]]; then
  echo "⚠ Could not read quarantine flag (Terminal may need Full Disk Access — optional)"
  echo "  If you see 'Open existing Nightly application?' during capture, click Open existing once."
elif xattr -p com.apple.quarantine "$FIREFOX_APP" >/dev/null 2>&1; then
  echo "⚠ Quarantine flag on Firefox Nightly (may show 'Open existing' dialog)"
  echo "  Easiest fix: click Open existing when the dialog appears during the first shot."
  echo "  Optional: xattr -rd com.apple.quarantine '$FIREFOX_APP' (needs Full Disk Access)"
else
  echo "✓ No quarantine flag on Firefox Nightly"
fi

TEST_IMG="/tmp/pd-os-screen-recording-test.png"
rm -f "$TEST_IMG"
if screencapture -x "$TEST_IMG" 2>/dev/null && [[ -s "$TEST_IMG" ]]; then
  echo "✓ Screen Recording permission OK"
  rm -f "$TEST_IMG"
else
  echo "✗ Screen Recording not granted for this app (Terminal / iTerm / Cursor)"
  echo "  Fix: System Settings → Privacy & Security → Screen Recording → enable your terminal"
  FAIL=1
fi

if osascript -e 'tell application "System Events" to get name of processes' >/dev/null 2>&1; then
  echo "✓ Accessibility permission OK"
else
  echo "⚠ Accessibility not granted (keyboard shortcuts may fail; most shots use prefs/CLI)"
  echo "  Fix: System Settings → Privacy & Security → Accessibility → enable your terminal"
fi

echo ""
if [[ "$FAIL" -ne 0 ]]; then
  echo "Fix the items above, then re-run ./setup/bin/run-nightly-nova-screenshots.sh"
  exit 1
fi

echo "Ready to capture."
