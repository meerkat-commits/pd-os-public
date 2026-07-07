"""Capture Nova punch-QA screenshots from Firefox Nightly on macOS."""

from __future__ import annotations

import json
import plistlib
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from pd_os.paths import repo_root_from_here

PRODUCT_VERSIONS_URL = "https://product-details.mozilla.org/1.0/firefox_versions.json"
NIGHTLY_DOWNLOAD_URL = (
    "https://download.mozilla.org/?product=firefox-nightly-latest-ssl&os=osx&lang=en-US"
)

DEFAULT_FIREFOX_PATH = Path(
    "/Applications/Firefox Nightly.app/Contents/MacOS/firefox"
)
DEFAULT_FIREFOX_APP = "Firefox Nightly"
DEFAULT_PROJECT_SLUG = "2026-06-nova-nightly-screenshots"
DEFAULT_WINDOW = (1440, 900)
MARIONETTE_PORT = 2828

# Shared Nova baseline (match your about:config Nova toggles).
BASE_PREFS: dict[str, bool | int | str] = {
    "browser.nova.enabled": True,
    "browser.newtabpage.enabled": True,
    "browser.newtabpage.activity-stream.nova.enabled": True,
    "browser.urlbar.quicksuggest.ampTopPickUseNovaIconSize": True,
    "browser.smartwindow.enabled": True,
    "browser.shell.checkDefaultBrowser": False,
    "datareporting.policy.dataSubmissionPolicyBypassNotification": True,
    "toolkit.telemetry.reportingpolicy.firstRun": False,
    "app.update.disabledForTesting": True,
    "app.update.auto": False,
    "browser.startup.homepage_override.mstone": "ignore",
    "browser.bookmarks.restore_on_load": False,
    "toolkit.crashreporter.enabled": False,
    "browser.sessionstore.resume_from_crash": False,
}

SKIP_ONBOARDING_PREFS: dict[str, bool | int | str] = {
    "browser.aboutwelcome.enabled": False,
    "trailhead.firstrun.didSeeAboutWelcome": True,
    "browser.profiles.created": True,
    "browser.laterrun.enabled": False,
}

FIRST_RUN_PREFS: dict[str, bool | int | str] = {
    "browser.aboutwelcome.enabled": True,
    "trailhead.firstrun.didSeeAboutWelcome": False,
    "browser.profiles.created": False,
}

CONTINUOUS_ONBOARDING_PREFS: dict[str, bool | int | str] = {
    **SKIP_ONBOARDING_PREFS,
    # Best-effort: surface deferred Nova prompts (Nimbus may still gate).
    "browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features": True,
}

_NEW_TAB_URLS = frozenset({"about:newtab", "about:home"})


@dataclass
class ShotSpec:
    id: str
    filename: str
    profile: str = "nova"
    url: str = "about:blank"
    prefs: dict[str, bool | int | str] = field(default_factory=dict)
    firefox_args: list[str] = field(default_factory=list)
    keys: list[str] = field(default_factory=list)
    type_text: str = ""
    open_tabs: list[str] = field(default_factory=list)
    tab_group: bool = False
    tab_group_collapsed: bool = False
    customize_toolbar: bool = False
    sidebar_panel: str = ""
    background_tab_url: str = ""
    scroll_vertical_tabs: bool = False
    wait_ms: int = 2500
    notes: str = ""
    automation: str = "automated"  # automated | hybrid | best_effort | manual
    requires_no_marionette: bool = False  # Marionette suppresses about:newtab Activity Stream


DEFAULT_SHOTS: list[ShotSpec] = [
    ShotSpec(
        id="chrome",
        filename="01-chrome.png",
        url="https://example.com",
        notes="Default Nova chrome on a loaded page.",
    ),
    ShotSpec(
        id="sidebar",
        filename="02-sidebar.png",
        url="https://example.com",
        prefs={"sidebar.revamp": True, "sidebar.visibility": "always-show"},
        notes="Bookmarks sidebar open via sidebar.visibility pref.",
    ),
    ShotSpec(
        id="vertical-tabs",
        filename="03-vertical-tabs.png",
        url="https://example.com",
        prefs={"sidebar.verticalTabs": True},
        notes="Vertical tabs via sidebar.verticalTabs pref.",
    ),
    ShotSpec(
        id="tab-grouping",
        filename="04-tab-grouping.png",
        url="https://example.com",
        prefs={"browser.tabs.groups.enabled": True},
        open_tabs=["https://example.com", "https://mozilla.org", "https://firefox.com"],
        tab_group=True,
        wait_ms=3500,
        notes="Three tabs; best-effort tab group via chrome script.",
    ),
    ShotSpec(
        id="new-tab",
        filename="05-new-tab.png",
        url="about:newtab",
        prefs={
            "sidebar.revamp": True,
            "sidebar.visibility": "always-show",
        },
        wait_ms=8000,
        notes="Nova new tab page (no-marionette: Activity Stream is suppressed under Marionette).",
        automation="hybrid",
        requires_no_marionette=True,
    ),
    ShotSpec(
        id="private-window",
        filename="06-private-window.png",
        url="about:privatebrowsing",
        firefox_args=["-private-window"],
        notes="Private browsing window.",
    ),
    ShotSpec(
        id="smart-window",
        filename="07-smart-window.png",
        url="about:newtab",
        prefs={
            "browser.smartwindow.tos.consentTime": 1,
        },
        firefox_args=["-new-instance"],
        wait_ms=6000,
        notes="Smart Window enabled; consent pref bypassed for capture (no-marionette: shares about:newtab path).",
        automation="hybrid",
        requires_no_marionette=True,
    ),
    ShotSpec(
        id="search",
        filename="08-search.png",
        url="about:blank",
        keys=["Meta+l"],
        type_text="firefox nova",
        wait_ms=3000,
        notes="Urlbar focused with query text (Nova search suggestions if available).",
    ),
    ShotSpec(
        id="first-run",
        filename="09-first-run.png",
        profile="first-run",
        url="about:home",
        firefox_args=["-new-instance"],
        wait_ms=5000,
        notes="Fresh profile — About Welcome / first-run onboarding.",
    ),
    ShotSpec(
        id="continuous",
        filename="10-continuous.png",
        profile="continuous",
        url="https://example.com",
        firefox_args=["-new-instance"],
        wait_ms=4000,
        notes="Post-first-run profile for deferred / continuous onboarding prompts.",
    ),
]


def project_dir(root: Path, slug: str) -> Path:
    return root / "data" / "projects" / slug


def shots_config_path(root: Path, slug: str) -> Path:
    return project_dir(root, slug) / "shots.json"


def captures_dir(root: Path, slug: str) -> Path:
    return project_dir(root, slug) / "captures"


def state_path(root: Path, slug: str) -> Path:
    return project_dir(root, slug) / ".state" / "last-run.json"


def profiles_cache(root: Path, slug: str) -> Path:
    return project_dir(root, slug) / ".profiles"


def fetch_nightly_version(firefox_binary: Path | None = None) -> str:
    """Return the installed Nightly version.

    Prefers the local Firefox.app `Info.plist` (`CFBundleShortVersionString`) so
    capture works offline / on flaky networks. Falls back to the product-details
    JSON, and finally to "unknown" so a run can still produce a dated folder.
    """
    if firefox_binary is not None:
        try:
            bundle = resolve_firefox_bundle(firefox_binary)
            info = _bundle_info_plist(bundle)
            local = info.get("CFBundleShortVersionString")
            if local:
                return str(local)
        except Exception:
            pass
    try:
        req = urllib.request.Request(
            PRODUCT_VERSIONS_URL,
            headers={"User-Agent": "pd-os-nightly-screenshots/1.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        version = data.get("FIREFOX_NIGHTLY")
        if version:
            return str(version)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"  ! Could not fetch Nightly version from product-details: {exc}")
    return "unknown"


def resolve_firefox_binary(config: dict[str, Any]) -> Path:
    env = config.get("firefox_binary")
    if env:
        path = Path(str(env)).expanduser()
        if path.is_dir():
            path = path / "Contents" / "MacOS" / "firefox"
        if not path.exists():
            raise FileNotFoundError(f"firefox_binary not found: {path}")
        return path
    if DEFAULT_FIREFOX_PATH.exists():
        return DEFAULT_FIREFOX_PATH
    raise FileNotFoundError(
        "Firefox Nightly not found at "
        f"{DEFAULT_FIREFOX_PATH}. Install Nightly or set firefox_binary in shots.json."
    )


def resolve_firefox_bundle(firefox_binary: Path) -> Path:
    bundle = firefox_binary.parent.parent.parent
    if bundle.suffix != ".app":
        raise FileNotFoundError(f"Firefox app bundle not found for binary: {firefox_binary}")
    return bundle


def _bundle_info_plist(bundle: Path) -> dict[str, Any]:
    plist_path = bundle / "Contents" / "Info.plist"
    if not plist_path.is_file():
        return {}
    with plist_path.open("rb") as handle:
        return plistlib.load(handle)


def bundle_health_error(bundle: Path) -> str | None:
    """Return a user-facing error when Launch Services cannot open the .app bundle."""
    plist_path = bundle / "Contents" / "Info.plist"
    if plist_path.is_file():
        return None
    if (bundle / "updating").is_dir():
        return (
            f"Firefox at {bundle} is mid-update (missing Contents/Info.plist). "
            "Open Nightly from Finder once to finish updating, or reinstall from "
            "https://www.mozilla.org/firefox/nightly/"
        )
    return (
        f"Firefox app bundle at {bundle} is incomplete (missing Contents/Info.plist). "
        "Reinstall Nightly or set firefox_binary in shots.json to a valid .app path."
    )


def resolve_firefox_app(config: dict[str, Any], firefox_binary: Path | None = None) -> str:
    if config.get("firefox_app"):
        return str(config["firefox_app"])
    if firefox_binary is not None:
        info = _bundle_info_plist(resolve_firefox_bundle(firefox_binary))
        name = info.get("CFBundleName") or info.get("CFBundleDisplayName")
        if name:
            return str(name)
    return DEFAULT_FIREFOX_APP


def discover_local_nightly_apps() -> list[Path]:
    """Best-effort search for healthy mozilla-central dist/Nightly.app builds."""
    home = Path.home()
    candidates: list[Path] = []
    for base in (
        home / "mozilla" / "firefox",
        home / "VibeCoding_BK" / "mozilla" / "firefox",
    ):
        if not base.is_dir():
            continue
        for objdir in sorted(base.glob("obj-*")):
            app = objdir / "dist" / "Nightly.app"
            if app.is_dir() and (app / "Contents" / "Info.plist").is_file():
                candidates.append(app)
    return candidates


def load_config(root: Path, slug: str) -> dict[str, Any]:
    path = shots_config_path(root, slug)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "project": slug,
        "firefox_binary": str(DEFAULT_FIREFOX_PATH.parent.parent),
        "window": {"width": DEFAULT_WINDOW[0], "height": DEFAULT_WINDOW[1]},
        "base_prefs": BASE_PREFS,
        "shots": [shot.__dict__ for shot in DEFAULT_SHOTS],
    }


def parse_shots(config: dict[str, Any]) -> list[ShotSpec]:
    raw = config.get("shots")
    if not raw:
        return list(DEFAULT_SHOTS)
    shots: list[ShotSpec] = []
    for item in raw:
        shots.append(ShotSpec(**item))
    return shots


def filter_shots_for_run(
    shots: list[ShotSpec],
    *,
    only: list[str] | None,
    include_manual: bool,
    include_best_effort: bool,
) -> tuple[list[ShotSpec], list[ShotSpec]]:
    if only:
        wanted = {s.strip() for s in only}
        selected = [s for s in shots if s.id in wanted]
        if not selected:
            raise ValueError(f"No shots matched --only {only!r}")
        return selected, []

    selected: list[ShotSpec] = []
    skipped: list[ShotSpec] = []
    for shot in shots:
        if shot.automation == "manual" and not include_manual:
            skipped.append(shot)
        elif shot.automation == "best_effort" and not include_best_effort:
            skipped.append(shot)
        else:
            # "automated" and "hybrid" both run by default
            selected.append(shot)
    return selected, skipped


def write_user_js(profile_dir: Path, prefs: dict[str, bool | int | str]) -> None:
    profile_dir.mkdir(parents=True, exist_ok=True)
    lines = [f'user_pref("{key}", {json.dumps(value)});' for key, value in prefs.items()]
    (profile_dir / "user.js").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _clear_session_state(profile_dir: Path) -> None:
    """Drop saved window/sidebar/tab state so shots do not bleed into each other."""
    for name in (
        "sessionstore.json",
        "sessionstore.jsonlz4",
        "sessionCheckpoints.json",
        "recovery.jsonlz4",
    ):
        path = profile_dir / name
        if path.exists():
            path.unlink()
    backups = profile_dir / "sessionstore-backups"
    if backups.is_dir():
        shutil.rmtree(backups)


def _clear_extension_state(profile_dir: Path) -> None:
    """Drop cached addon/theme state so user.js activeThemeID wins on launch."""
    for name in ("extensions.json", "addonStartup.json.lz4"):
        path = profile_dir / name
        if path.exists():
            path.unlink()


def profile_prefs_for_template(template: str) -> dict[str, bool | int | str]:
    if template == "first-run":
        return dict(FIRST_RUN_PREFS)
    if template == "continuous":
        return dict(CONTINUOUS_ONBOARDING_PREFS)
    return dict(SKIP_ONBOARDING_PREFS)


def ensure_profile(
    root: Path,
    slug: str,
    template: str,
    extra_prefs: dict[str, bool | int | str],
    base_prefs: dict[str, bool | int | str],
    *,
    reset: bool,
) -> Path:
    cache = profiles_cache(root, slug) / template
    if reset and cache.exists():
        shutil.rmtree(cache)
    merged = {**base_prefs, **profile_prefs_for_template(template), **extra_prefs}
    write_user_js(cache, merged)
    _clear_session_state(cache)
    _clear_extension_state(cache)
    # prefs.js overrides user.js from prior runs — remove so this shot's user.js wins.
    prefs_js = cache / "prefs.js"
    if prefs_js.exists():
        prefs_js.unlink()
    return cache


def _applescript_list(items: list[str]) -> str:
    """Format strings as an AppleScript list literal."""
    return "{" + ", ".join(json.dumps(item) for item in items) + "}"


def _run_applescript(script: str, *, required: bool = True) -> str:
    result = subprocess.run(
        ["osascript", "-e", script],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if required:
            err = (result.stderr or result.stdout or "").strip()
            raise subprocess.CalledProcessError(
                result.returncode,
                result.args,
                output=result.stdout,
                stderr=err,
            )
        return ""
    return result.stdout.strip()


def _activate_firefox(app_name: str) -> None:
    proc_list = _applescript_list(_firefox_process_names(app_name))
    _run_applescript(
        f"""
        tell application "System Events"
            repeat with procName in {proc_list}
                if exists process procName then
                    tell process procName to set frontmost to true
                    exit repeat
                end if
            end repeat
        end tell
        delay 0.6
        """,
        required=False,
    )


def _launch_failure_message(firefox_binary: Path, *, used_direct_binary: bool) -> str:
    bundle = resolve_firefox_bundle(firefox_binary)
    health = bundle_health_error(bundle)
    if health:
        return (
            f"Firefox Nightly did not start Marionette within 90s. {health} "
            "The script fell back to launching the binary directly."
        )
    if used_direct_binary:
        return (
            "Firefox Nightly did not start Marionette within 90s. "
            "If you see 'Open existing Nightly application?', click Open existing once "
            "or quit all Firefox windows and re-run."
        )
    return (
        "Firefox Nightly did not start Marionette within 90s. "
        "Quit all Firefox windows and re-run."
    )


def _launch_url_for_shot(shot: ShotSpec) -> str:
    """Defer about:newtab until Marionette can enable Activity Stream prefs.

    Hybrid (no-marionette) shots bypass this deferral: we want Firefox to load
    the real about:newtab on startup so Activity Stream hydrates normally.
    """
    if shot.requires_no_marionette:
        return shot.url
    if shot.url in _NEW_TAB_URLS:
        return "about:blank"
    return shot.url


def _launch_firefox_process(
    firefox_binary: Path,
    profile_dir: Path,
    window: tuple[int, int],
    shot: ShotSpec,
) -> tuple[subprocess.Popen[bytes], str]:
    """Launch Firefox; returns (process, launch_mode)."""
    bundle = resolve_firefox_bundle(firefox_binary)
    width, height = window
    # Marionette suppresses Activity Stream / about:newtab content on connect.
    # For shots that need real NTP content, launch without -marionette and skip
    # the Marionette session entirely in capture_shot (see requires_no_marionette).
    base_args: list[str]
    if shot.requires_no_marionette:
        base_args = ["-no-remote"]
    else:
        base_args = ["-marionette", "-remote-allow-system-access", "-no-remote"]
    firefox_args = [
        *base_args,
        "-profile",
        str(profile_dir),
        f"-width={width}",
        f"-height={height}",
        *shot.firefox_args,
    ]
    if shot.open_tabs:
        firefox_args.append(shot.open_tabs[0])
        for tab_url in shot.open_tabs[1:]:
            firefox_args.extend(["-new-tab", tab_url])
    else:
        firefox_args.append(_launch_url_for_shot(shot))

    # Hybrid shots: launch the binary directly. `open -na` goes through Launch
    # Services and (on some setups) silently swallows `-no-remote` / `-profile`,
    # which can land us on a stale session instead of the automation profile.
    # Direct-binary launch matches manual `firefox -no-remote -profile ...`.
    if shot.requires_no_marionette or bundle_health_error(bundle) is not None:
        cmd = [str(firefox_binary), *firefox_args]
        return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), "binary"

    cmd = ["open", "-na", str(bundle), "--args", *firefox_args]
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), "open"


def _try_dismiss_open_existing_dialog() -> None:
    """Click through Mozilla's 'Open existing' prompt if it appears (Accessibility)."""
    script = """
    tell application "System Events"
        repeat with procName in {"firefox", "Nightly", "Firefox Nightly"}
            if exists process procName then
                tell process procName
                    repeat with w in windows
                        try
                            if exists (button "Open existing" of w) then
                                click button "Open existing" of w
                                return
                            end if
                        end try
                    end repeat
                end tell
            end if
        end repeat
    end tell
    """
    try:
        _run_applescript(script, required=False)
    except subprocess.CalledProcessError:
        pass


def _wait_for_port(port: int, timeout: int = 90) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        _try_dismiss_open_existing_dialog()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(1)
    return False


def _import_marionette():
    try:
        from marionette_driver.marionette import Marionette
    except ImportError as exc:
        raise RuntimeError(
            "marionette-driver is required. Install with: pip install marionette-driver"
        ) from exc
    return Marionette


def _key_action_sequence(marionette: Any) -> Any:
    return marionette.actions.sequence("key", "keyboard")


def send_key_chords(marionette: Any, chords: list[str]) -> None:
    from marionette_driver.keys import Keys

    modifier_map = {
        "Meta": Keys.META,
        "Alt": Keys.ALT,
        "Control": Keys.CONTROL,
        "Shift": Keys.SHIFT,
    }
    for chord in chords:
        parts = chord.split("+")
        actions = _key_action_sequence(marionette)
        mods = parts[:-1]
        key = parts[-1]
        for mod in mods:
            actions.key_down(modifier_map.get(mod, mod))
        if key == "Enter":
            actions.key_down(Keys.ENTER).key_up(Keys.ENTER)
        elif len(key) == 1:
            actions.send_keys(key)
        else:
            for char in key:
                actions.send_keys(char)
        for mod in reversed(mods):
            actions.key_up(modifier_map.get(mod, mod))
        actions.perform()
        time.sleep(0.3)


_URLBAR_TYPE_SCRIPT = """
const text = arguments[0];
const urlbar = typeof gURLBar !== "undefined" ? gURLBar : null;
if (!urlbar) {
  return false;
}
urlbar.focus();
if (typeof urlbar.select === "function") {
  urlbar.select();
}
if (typeof urlbar._setValue === "function") {
  urlbar._setValue(text);
} else {
  urlbar.value = text;
}
const input = urlbar.inputField || urlbar.querySelector("#urlbar-input");
if (input) {
  input.setSelectionRange(text.length, text.length);
  input.dispatchEvent(new Event("input", { bubbles: true }));
}
return true;
"""


def _focus_urlbar_via_applescript(app_name: str, text: str) -> bool:
    """Fallback: real Cmd+L + keystrokes via macOS Accessibility."""
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    proc_list = _applescript_list(_firefox_process_names(app_name))
    script = f"""
    tell application "{app_name}" to activate
    delay 0.5
    tell application "System Events"
        repeat with procName in {proc_list}
            if exists process procName then
                tell process procName
                    set frontmost to true
                    keystroke "l" using command down
                    delay 0.4
                    keystroke "{escaped}"
                end tell
                return "ok"
            end if
        end repeat
    end tell
    """
    try:
        result = _run_applescript(script, required=False)
        return result == "ok"
    except Exception:
        return False


def _focus_urlbar_and_type(marionette: Any, text: str, *, app_name: str) -> bool:
    """Focus the browser urlbar in chrome scope and type a query (no Enter)."""
    from marionette_driver.by import By

    _activate_firefox(app_name)
    try:
        marionette.set_context("chrome")
        ok = bool(
            marionette.execute_script(
                _URLBAR_TYPE_SCRIPT,
                script_args=(text,),
                script_timeout=SCRIPT_TIMEOUT_MS,
            )
        )
        if not ok:
            selectors = ["#urlbar-input", "input#urlbar-input", "#urlbar textarea"]
            for selector in selectors:
                try:
                    el = marionette.find_element(By.CSS_SELECTOR, selector)
                    el.click()
                    el.clear()
                    el.send_keys(text)
                    ok = True
                    break
                except Exception:
                    continue
        marionette.set_context("content")
        if ok:
            time.sleep(1.2)
            return True
    except Exception as exc:
        print(f"  ! urlbar chrome focus/type failed: {exc}")
        try:
            marionette.set_context("content")
        except Exception:
            pass

    if _focus_urlbar_via_applescript(app_name, text):
        time.sleep(1.2)
        return True
    return False


def _wait_for_page_ready(marionette: Any, shot: ShotSpec) -> None:
    """Wait for navigation and heavy about: pages to settle before capture."""
    if shot.url in {"about:newtab", "about:home"}:
        _wait_for_nova_newtab_ready(marionette, timeout_s=max(shot.wait_ms / 1000, 10))
        return

    timeout_s = max(shot.wait_ms / 1000, 6)
    deadline = time.time() + timeout_s
    about_extra = shot.url.startswith("about:") and shot.url not in {"about:blank"}

    while time.time() < deadline:
        try:
            ready = marionette.execute_script("return document.readyState")
            if ready in {"interactive", "complete"}:
                break
        except Exception:
            pass
        time.sleep(0.25)

    if about_extra:
        time.sleep(2.0)
    else:
        time.sleep(0.8)

    try:
        marionette.execute_script("window.focus()")
    except Exception:
        pass


_NTP_ENABLE_PREFS: dict[str, bool] = {
    "browser.newtabpage.enabled": True,
    "browser.newtabpage.activity-stream.nova.enabled": True,
}

_NTP_READY_SCRIPT = """
const search = document.querySelector(
  '#newtab-search-text, input[type="search"], [data-l10n-id="newtab-search-box"], .search-wrapper input'
);
if (search && search.offsetParent !== null) {
  return true;
}
const topsites = document.querySelector(
  '.top-sites-list, [data-testid="top-sites"], .top-sites, .topsites-wrapper'
);
if (topsites && topsites.children.length > 0) {
  return true;
}
const wordmark = document.querySelector('.wordmark, .logo-and-wordmark, [class*="wordmark"]');
if (wordmark && wordmark.offsetParent !== null) {
  return true;
}
return false;
"""


def _ensure_nova_newtab(marionette: Any, shot: ShotSpec) -> None:
    """Re-enable Activity Stream NTP after Marionette session prefs, then reload."""
    if shot.url not in _NEW_TAB_URLS:
        return
    marionette.set_prefs(
        {
            **_NTP_ENABLE_PREFS,
            "browser.newtabpage.activity-stream.testing.shouldInitializeFeeds": True,
        }
    )
    marionette.navigate(shot.url)


def _wait_for_nova_newtab_ready(marionette: Any, *, timeout_s: float = 12) -> None:
    """Wait for Nova NTP search UI or top sites to paint (not Marionette blank)."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            ready = marionette.execute_script(_NTP_READY_SCRIPT, script_timeout=SCRIPT_TIMEOUT_MS)
            if ready:
                time.sleep(2.0)
                try:
                    marionette.execute_script("window.focus()")
                except Exception:
                    pass
                return
        except Exception:
            pass
        time.sleep(0.5)
    time.sleep(2.0)


def _firefox_process_names(app_name: str) -> list[str]:
    names = ["firefox", "Nightly", "Firefox Nightly"]
    if app_name not in names:
        names.insert(0, app_name)
    return names


def _capture_via_screen_region(dest: Path, app_name: str) -> bool:
    """Capture the frontmost Firefox window from screen pixels (includes web content)."""
    proc_list = _applescript_list(_firefox_process_names(app_name))
    bounds = _run_applescript(
        f"""
        tell application "System Events"
            repeat with procName in {proc_list}
                if exists process procName then
                    tell process procName
                        set frontmost to true
                        delay 0.4
                        if (count of windows) > 0 then
                            set winPos to position of window 1
                            set winSize to size of window 1
                            return (item 1 of winPos as text) & "," & (item 2 of winPos as text) & "," & (item 1 of winSize as text) & "," & (item 2 of winSize as text)
                        end if
                    end tell
                end if
            end repeat
        end tell
        return ""
        """,
        required=False,
    )
    if not bounds:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    cap = subprocess.run(
        ["screencapture", "-x", "-R", bounds, str(dest)],
        check=False,
        capture_output=True,
        text=True,
    )
    if cap.returncode != 0:
        err = (cap.stderr or cap.stdout or "").strip()
        raise RuntimeError(
            "screencapture failed"
            + (f": {err}" if err else "")
            + ". Grant Screen Recording to Terminal/Cursor in System Settings → Privacy & Security."
        )
    return dest.exists() and dest.stat().st_size > 0


SCRIPT_TIMEOUT_MS = 60_000


def _configure_marionette(marionette: Any) -> None:
    marionette.timeout.script = SCRIPT_TIMEOUT_MS / 1000
    marionette.timeout.page_load = 120


def _run_chrome_script(
    marionette: Any,
    script: str,
    *,
    async_script: bool = False,
    label: str = "chrome-script",
) -> bool:
    wrapped = script
    try:
        marionette.set_context("chrome")
        if async_script:
            marionette.execute_async_script(wrapped, script_timeout=SCRIPT_TIMEOUT_MS)
        else:
            marionette.execute_script(wrapped, script_timeout=SCRIPT_TIMEOUT_MS)
        marionette.set_context("content")
        return True
    except Exception as exc:
        print(f"  ! {label} failed: {exc}")
        try:
            marionette.set_context("content")
        except Exception:
            pass
        return False


def _chrome_has_attribute(marionette: Any, name: str) -> bool:
    try:
        marionette.set_context("chrome")
        return bool(
            marionette.execute_script(
                f'return document.documentElement.hasAttribute({json.dumps(name)});',
                script_timeout=SCRIPT_TIMEOUT_MS,
            )
        )
    except Exception:
        return False
    finally:
        try:
            marionette.set_context("content")
        except Exception:
            pass


def _click_sidebar_tool(marionette: Any, view_id: str, *, quiet: bool = False) -> bool:
    from marionette_driver.by import By

    selectors = [
        f'moz-button[view="{view_id}"]',
        f'[view="{view_id}"]',
        f'toolbarbutton[view="{view_id}"]',
    ]
    try:
        marionette.set_context("chrome")
        for selector in selectors:
            try:
                el = marionette.find_element(By.CSS_SELECTOR, selector)
                el.click()
                marionette.set_context("content")
                time.sleep(1.0)
                return True
            except Exception:
                continue
        raise RuntimeError(f"no selector matched for {view_id}")
    except Exception as exc:
        if not quiet:
            print(f"  ! click sidebar tool {view_id} failed: {exc}")
        try:
            marionette.set_context("content")
        except Exception:
            pass
        return False


def _history_uri_count(marionette: Any) -> int:
    try:
        marionette.set_context("chrome")
        count = marionette.execute_script(
            """
            const hs = Cc["@mozilla.org/browser/nav-history-service;1"]
              .getService(Ci.nsINavHistoryService);
            const options = hs.getNewQueryOptions();
            options.resultType = options.RESULTS_AS_URI;
            const root = hs.executeQuery(hs.getNewQuery(), options).root;
            root.containerOpen = true;
            const n = root.childCount;
            root.containerOpen = false;
            return n;
            """,
            script_timeout=SCRIPT_TIMEOUT_MS,
        )
        return int(count)
    except Exception:
        return -1
    finally:
        try:
            marionette.set_context("content")
        except Exception:
            pass


def _clear_browser_history(marionette: Any) -> None:
    _run_chrome_script(
        marionette,
        """
        const done = arguments[arguments.length - 1];
        (async () => {
          try {
            try {
              const { PlacesUtils } = await ChromeUtils.importESModule(
                "resource://gre/modules/PlacesUtils.sys.mjs"
              );
              await PlacesUtils.history.clear();
            } catch (e1) {
              const hs = Cc["@mozilla.org/browser/nav-history-service;1"]
                .getService(Ci.nsINavHistoryService);
              // TIME_FRAME_EVERYTHING === 0
              hs.removePagesByTimeframe(0, 0);
            }
          } catch (e) {}
          done();
        })();
        """,
        async_script=True,
        label="history-clear",
    )
    time.sleep(0.5)


def _show_history_sidebar(marionette: Any) -> bool:
    _run_chrome_script(
        marionette,
        """
        const done = arguments[arguments.length - 1];
        (async () => {
          try {
            const win = typeof BrowserWindowTracker !== "undefined"
              ? BrowserWindowTracker.getTopWindow()
              : window;
            const sc = win.SidebarController;
            await sc.promiseInitialized;
            if (sc.sidebarContainer?.hidden) {
              sc.handleToolbarButtonClick?.();
              await sc.sidebarMain?.updateComplete;
            }
            await sc.show("viewHistorySidebar");
            await sc.waitUntilStable();
            const browser = sc.browser;
            const component = browser?.contentDocument?.querySelector("sidebar-history");
            if (component?.updateComplete) await component.updateComplete;
          } catch (e) {}
          done();
        })();
        """,
        async_script=True,
        label="sidebar-history-show",
    )
    time.sleep(0.5)
    try:
        marionette.set_context("chrome")
        current = marionette.execute_script(
            "return window.SidebarController?.currentID || '';",
            script_timeout=SCRIPT_TIMEOUT_MS,
        )
        marionette.set_context("content")
        if current == "viewHistorySidebar":
            return True
    except Exception:
        try:
            marionette.set_context("content")
        except Exception:
            pass
    if _click_sidebar_tool(marionette, "viewHistorySidebar", quiet=True):
        return True
    return _click_sidebar_tool(marionette, "viewHistorySidebar")


def _try_tab_group(marionette: Any, *, collapse: bool = False) -> None:
    collapse_js = "true" if collapse else "false"
    _run_chrome_script(
        marionette,
        f"""
        const done = arguments[arguments.length - 1];
        (async () => {{
          try {{
            const win = typeof BrowserWindowTracker !== "undefined"
              ? BrowserWindowTracker.getTopWindow()
              : window;
            const gBrowser = win.gBrowser;
            for (let i = 0; i < 60; i++) {{
              if (gBrowser.tabs.length >= 3) {{
                break;
              }}
              await new Promise((resolve) => setTimeout(resolve, 250));
            }}
            const tabs = Array.from(gBrowser.tabs);
            if (tabs.length < 2 || !gBrowser.addTabGroup) {{
              done();
              return;
            }}
            let group;
            if ({collapse_js}) {{
              if (tabs.length < 3) {{
                done();
                return;
              }}
              const exampleTab = tabs.find((tab) =>
                tab.linkedBrowser?.currentURI?.spec?.includes("example.com")
              ) || tabs[0];
              group = gBrowser.addTabGroup([tabs[1], tabs[2]], {{ label: "QA" }});
              gBrowser.selectedTab = exampleTab;
              await new Promise((resolve) => setTimeout(resolve, 400));
              group.collapsed = true;
              await new Promise((resolve) => {{
                const finish = () => resolve();
                group.addEventListener(
                  "TabGroupAnimationComplete",
                  finish,
                  {{ once: true }}
                );
                setTimeout(finish, 1000);
              }});
              gBrowser.selectedTab = exampleTab;
            }} else {{
              group = gBrowser.addTabGroup(tabs.slice(0, 3), {{ label: "QA" }});
            }}
          }} catch (e) {{}}
          done();
        }})();
        """,
        async_script=True,
        label="tab-group",
    )


def _chrome_tab_count(marionette: Any) -> int:
    try:
        marionette.set_context("chrome")
        count = marionette.execute_script(
            """
            const win = typeof BrowserWindowTracker !== "undefined"
              ? BrowserWindowTracker.getTopWindow()
              : window;
            return win.gBrowser?.tabs?.length || 0;
            """,
            script_timeout=SCRIPT_TIMEOUT_MS,
        )
        return int(count)
    except Exception:
        return 0
    finally:
        try:
            marionette.set_context("content")
        except Exception:
            pass


def _focus_tab_by_url_part(marionette: Any, needle: str) -> bool:
    needle = needle.lower()
    try:
        for handle in marionette.window_handles:
            marionette.switch_to_window(handle)
            url = (marionette.get_url() or "").lower()
            if needle in url:
                return True
        opened = marionette.open(type="tab", focus=True)
        if opened and opened.get("handle"):
            marionette.switch_to_window(opened["handle"])
        target = needle if needle.startswith("http") else f"https://{needle}"
        marionette.navigate(target)
        time.sleep(1.5)
        return True
    except Exception as exc:
        print(f"  ! focus tab containing {needle!r} failed: {exc}")
        return False


def _shot_focus_url(shot: ShotSpec) -> str:
    if shot.open_tabs:
        return shot.open_tabs[0]
    return shot.url


def _shot_focus_needle(shot: ShotSpec) -> str:
    from urllib.parse import urlparse

    raw = _shot_focus_url(shot)
    if raw.startswith("http"):
        host = urlparse(raw).netloc
        return host or raw
    return raw


def _ensure_open_tabs(marionette: Any, shot: ShotSpec) -> None:
    if len(shot.open_tabs) <= 1:
        return
    wanted = len(shot.open_tabs)
    urls_json = json.dumps(shot.open_tabs)
    for attempt in range(3):
        _run_chrome_script(
            marionette,
            f"""
            const done = arguments[arguments.length - 1];
            (async () => {{
              try {{
                const urls = {urls_json};
                const win = typeof BrowserWindowTracker !== "undefined"
                  ? BrowserWindowTracker.getTopWindow()
                  : window;
                const gBrowser = win.gBrowser;
                for (let i = gBrowser.tabs.length; i < urls.length; i++) {{
                  const inBackground = i !== 0;
                  if (gBrowser.addTrustedTab) {{
                    gBrowser.addTrustedTab(urls[i], {{ inBackground }});
                  }} else {{
                    gBrowser.addTab(urls[i], {{ inBackground }});
                  }}
                  await new Promise((resolve) => setTimeout(resolve, 800));
                }}
                const exampleTab = [...gBrowser.tabs].find((tab) =>
                  tab.linkedBrowser?.currentURI?.spec?.includes("example.com")
                );
                if (exampleTab) {{
                  gBrowser.selectedTab = exampleTab;
                }} else if (gBrowser.tabs.length > 0) {{
                  gBrowser.selectedTab = gBrowser.tabs[0];
                }}
              }} catch (e) {{}}
              done();
            }})();
            """,
            async_script=True,
            label=f"ensure-open-tabs-{attempt + 1}",
        )
        time.sleep(1.5)
        count = _chrome_tab_count(marionette)
        if count >= wanted:
            _focus_tab_by_url_part(marionette, _shot_focus_needle(shot))
            return
        print(f"  ! ensure-open-tabs attempt {attempt + 1}: {count}/{wanted} tabs")
    print(f"  ! ensure-open-tabs: only {_chrome_tab_count(marionette)}/{wanted} tabs after retries")


def _try_activate_dark_theme_via_addons(marionette: Any, return_url: str) -> None:
    theme_ids = ["firefox-compact-dark@mozilla.org", "dark@mozilla.org"]
    try:
        marionette.navigate("about:addons")
        time.sleep(3.0)
        marionette.set_context("content")
        from marionette_driver.by import By

        activated = False
        for theme_id in theme_ids:
            try:
                card = marionette.find_element(
                    By.CSS_SELECTOR, f'addon-list-item[addon-id="{theme_id}"]'
                )
                card.click()
                time.sleep(0.5)
                for selector in (
                    "button.enable-button",
                    'moz-button[action="enable"]',
                    "button[data-action='enable']",
                ):
                    try:
                        marionette.find_element(By.CSS_SELECTOR, selector).click()
                        break
                    except Exception:
                        continue
                activated = True
                break
            except Exception:
                continue
        if not activated:
            marionette.execute_script(
                """
                for (const item of document.querySelectorAll("addon-list-item, addon-card")) {
                  const id = item.getAttribute("addon-id") || "";
                  if (!id.includes("dark")) continue;
                  item.click();
                  break;
                }
                """,
                script_timeout=SCRIPT_TIMEOUT_MS,
            )
        time.sleep(1.5)
    except Exception as exc:
        print(f"  ! dark theme via about:addons failed: {exc}")
    finally:
        try:
            marionette.set_context("content")
        except Exception:
            pass
    if return_url:
        marionette.navigate(return_url)
        time.sleep(2.0)


def _try_apply_builtin_theme(
    marionette: Any,
    theme_ids: list[str] | None = None,
) -> None:
    ids = theme_ids or [
        "firefox-compact-dark@mozilla.org",
        "dark@mozilla.org",
    ]
    ids_json = json.dumps(ids)
    _run_chrome_script(
        marionette,
        f"""
        const done = arguments[arguments.length - 1];
        (async () => {{
          try {{
            const themeIDs = {ids_json};
            const {{ Services }} = await ChromeUtils.importESModule(
              "resource://gre/modules/Services.sys.mjs"
            );
            const {{ BuiltInThemes }} = await ChromeUtils.importESModule(
              "resource:///modules/BuiltInThemes.sys.mjs"
            );
            const {{ AddonManager }} = await ChromeUtils.importESModule(
              "resource://gre/modules/AddonManager.sys.mjs"
            );
            await BuiltInThemes.ensureBuiltInThemes();
            for (const themeID of themeIDs) {{
              try {{
                Services.prefs.setStringPref("extensions.activeThemeID", themeID);
                BuiltInThemes.maybeInstallActiveBuiltInTheme();
                const theme = await AddonManager.getAddonByID(themeID);
                if (theme) {{
                  theme.userDisabled = false;
                  if (theme.enable) {{
                    await theme.enable();
                  }}
                  Services.obs.notifyObservers(null, "lightweight-theme-styling-update");
                  break;
                }}
              }} catch (e) {{}}
            }}
          }} catch (e) {{}}
          done();
        }})();
        """,
        async_script=True,
        label="apply-theme",
    )
    time.sleep(1.5)


def _close_sidebar_if_unwanted(marionette: Any, shot: ShotSpec) -> None:
    if shot.sidebar_panel:
        return
    visibility = shot.prefs.get("sidebar.visibility")
    if visibility in {"always", "always-show"}:
        return
    _run_chrome_script(
        marionette,
        """
        const done = arguments[arguments.length - 1];
        (async () => {
          try {
            const win = typeof BrowserWindowTracker !== "undefined"
              ? BrowserWindowTracker.getTopWindow()
              : window;
            const sc = win.SidebarController;
            await sc.promiseInitialized;
            if (!sc.isOpen) {
              done();
              return;
            }
            await sc.hide();
            await sc.waitUntilStable();
          } catch (e) {}
          done();
        })();
        """,
        async_script=True,
        label="sidebar-close",
    )
    time.sleep(0.5)


def _try_customize_toolbar(marionette: Any) -> None:
    _run_chrome_script(
        marionette,
        """
        if (window.gCustomizeMode?.enter) {
          window.gCustomizeMode.enter();
        } else {
          window.goDoCommand("cmd_customizeToolbars");
        }
        """,
        label="customize-enter",
    )
    time.sleep(1.5)
    if not _chrome_has_attribute(marionette, "customizing"):
        _run_chrome_script(
            marionette,
            """
            const done = arguments[arguments.length - 1];
            (async () => {
              try {
                await new Promise((resolve, reject) => {
                  const timeout = setTimeout(() => reject(new Error("customizationready timeout")), 15000);
                  const onReady = () => {
                    clearTimeout(timeout);
                    window.gNavToolbox.removeEventListener("customizationready", onReady);
                    setTimeout(resolve, 800);
                  };
                  window.gNavToolbox.addEventListener("customizationready", onReady);
                  window.goDoCommand("cmd_customizeToolbars");
                });
              } catch (e) {}
              done();
            })();
            """,
            async_script=True,
            label="customize-async",
        )
        time.sleep(1.0)
    if not _chrome_has_attribute(marionette, "customizing"):
        print("  ! customize toolbar: not in customize mode before capture")


def _try_sidebar_panel(marionette: Any, panel: str) -> None:
    if panel == "history":
        _try_history_sidebar_empty(marionette)
        return
    panel_map = {
        "bookmarks": "viewBookmarksSidebar",
    }
    view_id = panel_map.get(panel, panel)
    _run_chrome_script(
        marionette,
        f"""
        const done = arguments[arguments.length - 1];
        (async () => {{
          try {{
            const sc = window.SidebarController;
            await sc.promiseInitialized;
            await sc.show("{view_id}");
            await sc.waitUntilStable();
          }} catch (e) {{}}
          done();
        }})();
        """,
        async_script=True,
        label=f"sidebar-{panel}",
    )


def _try_history_sidebar_empty(marionette: Any) -> None:
    _clear_browser_history(marionette)
    if not _show_history_sidebar(marionette):
        print("  ! sidebar-history: could not open history panel")
        return
    # example.com loads at launch; clear again after sidebar is ready, then refresh.
    _clear_browser_history(marionette)
    _run_chrome_script(
        marionette,
        """
        const done = arguments[arguments.length - 1];
        (async () => {
          try {
            const win = typeof BrowserWindowTracker !== "undefined"
              ? BrowserWindowTracker.getTopWindow()
              : window;
            const sc = win.SidebarController;
            const browser = sc.browser;
            const component = browser?.contentDocument?.querySelector("sidebar-history");
            if (component?.refresh) component.refresh();
            else if (component?.updateComplete) await component.updateComplete;
          } catch (e) {}
          done();
        })();
        """,
        async_script=True,
        label="sidebar-history-refresh",
    )
    time.sleep(1.5)


def _try_background_tab(marionette: Any, url: str) -> None:
    safe_url = json.dumps(url)
    _run_chrome_script(
        marionette,
        f"""
        try {{
          const gBrowser = window.gBrowser;
          const foreground = gBrowser.selectedTab;
          if (gBrowser.addTrustedTab) {{
            gBrowser.addTrustedTab({safe_url}, {{ inBackground: true }});
          }} else {{
            gBrowser.addTab({safe_url}, {{ inBackground: true }});
          }}
          gBrowser.selectedTab = foreground;
        }} catch (e) {{}}
        """,
        label="background-tab",
    )


def _try_scroll_vertical_tabs(marionette: Any) -> None:
    _run_chrome_script(
        marionette,
        """
        try {
          const el =
            window.document.getElementById("vertical-tabs") ||
            window.document.querySelector(".vertical-tabs-container");
          if (el) el.scrollTop = el.scrollHeight;
        } catch (e) {}
        """,
        label="scroll-vertical-tabs",
    )


def _shot_uses_dark_theme(shot: ShotSpec) -> bool:
    theme_id = str(shot.prefs.get("extensions.activeThemeID", ""))
    return shot.id == "chrome-dark" or "dark" in theme_id.lower()


def _warn_if_setup_incomplete(marionette: Any, shot: ShotSpec) -> list[str]:
    warnings: list[str] = []

    def warn(message: str) -> None:
        warnings.append(message)
        print(f"  ! {message}")

    if shot.url in _NEW_TAB_URLS:
        try:
            ready = marionette.execute_script(_NTP_READY_SCRIPT, script_timeout=SCRIPT_TIMEOUT_MS)
            if not ready:
                warn(f"{shot.id}: Nova NTP content not visible — capture may be blank")
        except Exception as exc:
            warn(f"{shot.id}: could not verify NTP content: {exc}")

    if shot.customize_toolbar and not _chrome_has_attribute(marionette, "customizing"):
        warn(f"{shot.id}: expected customize mode — capture may be wrong")
    if _shot_uses_dark_theme(shot):
        try:
            marionette.set_context("chrome")
            theme_info = marionette.execute_script(
                """
                let id = "";
                try {
                  id = Services.prefs.getStringPref("extensions.activeThemeID", "");
                } catch (e) {}
                const root = document.documentElement;
                return {
                  id,
                  lwtheme: root.hasAttribute("lwtheme"),
                  mozlightdark: root.hasAttribute("lwtheme-mozlightdark"),
                };
                """,
                script_timeout=SCRIPT_TIMEOUT_MS,
            )
            marionette.set_context("content")
            if not theme_info or "dark" not in str(theme_info.get("id", "")).lower():
                warn(
                    f"{shot.id}: dark theme not active "
                    f"(theme={theme_info!r}) — capture may be wrong"
                )
        except Exception as exc:
            warn(f"{shot.id}: could not verify dark theme: {exc}")
            try:
                marionette.set_context("content")
            except Exception:
                pass
    if shot.tab_group:
        try:
            marionette.set_context("chrome")
            tab_count = marionette.execute_script(
                """
                const win = typeof BrowserWindowTracker !== "undefined"
                  ? BrowserWindowTracker.getTopWindow()
                  : window;
                return win.gBrowser?.tabs?.length || 0;
                """,
                script_timeout=SCRIPT_TIMEOUT_MS,
            )
            group_count = marionette.execute_script(
                """
                const win = typeof BrowserWindowTracker !== "undefined"
                  ? BrowserWindowTracker.getTopWindow()
                  : window;
                const groups = win.gBrowser?.getAllTabGroups?.() || [];
                return groups.length;
                """,
                script_timeout=SCRIPT_TIMEOUT_MS,
            )
            collapsed = marionette.execute_script(
                """
                const win = typeof BrowserWindowTracker !== "undefined"
                  ? BrowserWindowTracker.getTopWindow()
                  : window;
                const groups = win.gBrowser?.getAllTabGroups?.() || [];
                return groups.some((group) => group.collapsed);
                """,
                script_timeout=SCRIPT_TIMEOUT_MS,
            )
            foreground = ""
            if shot.tab_group_collapsed:
                foreground = marionette.execute_script(
                    """
                    const win = typeof BrowserWindowTracker !== "undefined"
                      ? BrowserWindowTracker.getTopWindow()
                      : window;
                    return win.gBrowser?.selectedTab?.linkedBrowser?.currentURI?.spec || "";
                    """,
                    script_timeout=SCRIPT_TIMEOUT_MS,
                )
            marionette.set_context("content")
            expected_tabs = len(shot.open_tabs) if shot.open_tabs else 1
            if tab_count < expected_tabs:
                warn(
                    f"{shot.id}: expected {expected_tabs} tabs, got {tab_count} — "
                    "capture may be wrong"
                )
            if not group_count:
                warn(f"{shot.id}: no tab groups created — capture may be wrong")
            elif shot.tab_group_collapsed and not collapsed:
                warn(f"{shot.id}: tab group not collapsed — capture may be wrong")
            elif shot.tab_group_collapsed and "example.com" not in str(foreground):
                warn(
                    f"{shot.id}: foreground is {foreground!r}, expected example.com — "
                    "capture may be wrong"
                )
        except Exception as exc:
            warn(f"{shot.id}: could not verify tab groups: {exc}")
            try:
                marionette.set_context("content")
            except Exception:
                pass
    if shot.sidebar_panel == "history":
        try:
            marionette.set_context("chrome")
            current = marionette.execute_script(
                "return window.SidebarController?.currentID || '';",
                script_timeout=SCRIPT_TIMEOUT_MS,
            )
            marionette.set_context("content")
            if current != "viewHistorySidebar":
                warn(
                    f"{shot.id}: history sidebar not open (current={current!r}) — "
                    "capture may be wrong"
                )
            else:
                count = _history_uri_count(marionette)
                if count > 0:
                    warn(
                        f"{shot.id}: history not empty ({count} entries) — "
                        "capture may be wrong"
                    )
        except Exception as exc:
            warn(f"{shot.id}: could not verify history sidebar: {exc}")
            try:
                marionette.set_context("content")
            except Exception:
                pass
    return warnings


def _apply_shot_setup(marionette: Any, shot: ShotSpec) -> None:
    if shot.tab_group:
        _try_tab_group(marionette, collapse=shot.tab_group_collapsed)
        time.sleep(0.8)
    if shot.customize_toolbar:
        _try_customize_toolbar(marionette)
        time.sleep(1.0)
    if shot.sidebar_panel:
        _try_sidebar_panel(marionette, shot.sidebar_panel)
        time.sleep(1.0)
    if shot.background_tab_url:
        _try_background_tab(marionette, shot.background_tab_url)
        time.sleep(1.5)
    if shot.scroll_vertical_tabs:
        _try_scroll_vertical_tabs(marionette)
        time.sleep(0.5)


def _capture_via_window_id(dest: Path) -> bool:
    """Capture Firefox window by CGWindow ID via bundled Swift helper."""
    script = repo_root_from_here() / "setup" / "bin" / "get-firefox-window-id.swift"
    if not script.exists():
        return False
    result = subprocess.run(
        ["swift", str(script)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False
    window_id = result.stdout.strip()
    if not window_id.isdigit():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    cap = subprocess.run(
        ["screencapture", "-x", "-l", window_id, str(dest)],
        check=False,
        capture_output=True,
        text=True,
    )
    if cap.returncode != 0:
        err = (cap.stderr or cap.stdout or "").strip()
        raise RuntimeError(
            "screencapture failed"
            + (f": {err}" if err else "")
            + ". Grant Screen Recording to Terminal/Cursor in System Settings → Privacy & Security."
        )
    return dest.exists() and dest.stat().st_size > 0


def _capture_via_quartz(dest: Path) -> bool:
    """Capture Firefox window by CGWindow ID (PyObjC path)."""
    try:
        import Quartz  # type: ignore[import-untyped]
    except ImportError:
        return False

    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements,
        Quartz.kCGNullWindowID,
    )
    candidates: list[tuple[float, Any]] = []
    for window in windows:
        owner = str(window.get("kCGWindowOwnerName", ""))
        if owner.lower() not in {"firefox", "firefox nightly"}:
            continue
        bounds = window.get("kCGWindowBounds") or {}
        width = float(bounds.get("Width", 0))
        height = float(bounds.get("Height", 0))
        if width < 400 or height < 300:
            continue
        if int(window.get("kCGWindowLayer", 0)) != 0:
            continue
        area = width * height
        candidates.append((area, window))

    if not candidates:
        return False

    _, best = max(candidates, key=lambda item: item[0])
    window_id = best["kCGWindowNumber"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["screencapture", "-x", "-l", str(window_id), str(dest)],
        check=True,
    )
    return dest.exists() and dest.stat().st_size > 0


def capture_firefox_window(dest: Path, app_name: str, width: int, height: int) -> None:
    """Capture the frontmost Firefox window including browser chrome."""
    _activate_firefox(app_name)
    time.sleep(0.5)
    # Prefer screen-region capture: screencapture -l often misses Firefox web content on macOS.
    if _capture_via_screen_region(dest, app_name):
        return
    if _capture_via_window_id(dest) or _capture_via_quartz(dest):
        return

    raise RuntimeError(
        "Could not find a Firefox window to capture. "
        "Grant Accessibility to Terminal/Cursor in System Settings → Privacy & Security."
    )


def _dismiss_crash_reporter() -> None:
    script = """
    tell application "System Events"
        repeat with procName in {"crashreporter", "Nightly Crash Reporter"}
            if exists process procName then
                tell process procName
                    repeat with w in windows
                        try
                            if exists (button "Quit Nightly" of w) then
                                click button "Quit Nightly" of w
                                return
                            end if
                        end try
                    end repeat
                end tell
            end if
        end repeat
    end tell
    """
    try:
        _run_applescript(script, required=False)
    except subprocess.CalledProcessError:
        pass


def _kill_firefox(app_name: str = DEFAULT_FIREFOX_APP) -> None:
    _dismiss_crash_reporter()
    subprocess.run(
        ["osascript", "-e", f'tell application "{app_name}" to quit'],
        check=False,
        capture_output=True,
    )
    time.sleep(1.5)
    subprocess.run(["pkill", "-x", "firefox"], check=False, capture_output=True)
    subprocess.run(["pkill", "-f", "plugin-container"], check=False, capture_output=True)
    subprocess.run(["pkill", "-f", "crashreporter"], check=False, capture_output=True)
    time.sleep(1)


def capture_shot(
    shot: ShotSpec,
    *,
    firefox_binary: Path,
    firefox_app: str,
    profile_dir: Path,
    output_path: Path,
    window: tuple[int, int],
) -> list[str]:
    _kill_firefox(firefox_app)
    proc, launch_mode = _launch_firefox_process(firefox_binary, profile_dir, window, shot)
    marionette = None
    warnings: list[str] = []
    try:
        # Hybrid path: no Marionette so Activity Stream / about:newtab can render.
        # Prefs (incl. browser.nova.* and Smart Window) are baked into the
        # profile via user.js, so we can just wait + capture.
        # Cold-start Nightly takes ~4-6s to paint chrome; Activity Stream React
        # mount + widgets need another ~3-4s. Floor at 10s to be safe.
        if shot.requires_no_marionette:
            wait_s = max(shot.wait_ms / 1000.0, 10.0)
            time.sleep(wait_s)
            _activate_firefox(firefox_app)
            time.sleep(1.5)  # let focus settle + any post-focus repaint
            capture_firefox_window(output_path, firefox_app, window[0], window[1])
            return warnings

        Marionette = _import_marionette()
        if not _wait_for_port(MARIONETTE_PORT, timeout=90):
            raise RuntimeError(
                _launch_failure_message(
                    firefox_binary,
                    used_direct_binary=launch_mode == "binary",
                )
            )

        marionette = Marionette(host="localhost", port=MARIONETTE_PORT)
        marionette.start_session()
        _configure_marionette(marionette)
        _ensure_nova_newtab(marionette, shot)
        time.sleep(2.0)

        if _shot_uses_dark_theme(shot):
            _try_apply_builtin_theme(marionette)

        _wait_for_page_ready(marionette, shot)
        _ensure_open_tabs(marionette, shot)
        _apply_shot_setup(marionette, shot)
        if shot.open_tabs or shot.tab_group:
            _focus_tab_by_url_part(marionette, _shot_focus_needle(shot))
        if _shot_uses_dark_theme(shot):
            _try_apply_builtin_theme(marionette)
            _try_activate_dark_theme_via_addons(marionette, _shot_focus_url(shot))
            _wait_for_page_ready(marionette, shot)
        _close_sidebar_if_unwanted(marionette, shot)
        warnings = _warn_if_setup_incomplete(marionette, shot)
        if shot.type_text:
            if not _focus_urlbar_and_type(marionette, shot.type_text, app_name=firefox_app):
                if shot.keys:
                    send_key_chords(marionette, shot.keys)
                _key_action_sequence(marionette).send_keys(shot.type_text).perform()
                time.sleep(0.8)
                warnings.append("urlbar focus/type used fallback keyboard path")
        elif shot.keys:
            _activate_firefox(firefox_app)
            send_key_chords(marionette, shot.keys)
        if shot.background_tab_url:
            time.sleep(2.5)

        capture_firefox_window(output_path, firefox_app, window[0], window[1])
        return warnings
    finally:
        if marionette is not None:
            try:
                marionette.delete_session()
            except Exception:
                pass
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        _kill_firefox(firefox_app)


def run_capture(
    *,
    root: Path | None = None,
    project_slug: str = DEFAULT_PROJECT_SLUG,
    dry_run: bool = False,
    only: list[str] | None = None,
    reset_profiles: bool = False,
    include_manual: bool = False,
    include_best_effort: bool = False,
) -> Path:
    root = root or repo_root_from_here()
    config = load_config(root, project_slug)
    all_shots = parse_shots(config)
    shots, skipped = filter_shots_for_run(
        all_shots,
        only=only,
        include_manual=include_manual,
        include_best_effort=include_best_effort,
    )

    firefox_binary = resolve_firefox_binary(config)
    version = fetch_nightly_version(firefox_binary)
    today = date.today().isoformat()
    out_dir = captures_dir(root, project_slug) / f"{today}__{version}"
    manifest_path = out_dir / "manifest.json"

    if dry_run:
        print(f"[dry-run] Nightly {version}")
        print(f"[dry-run] Output: {out_dir}")
        for shot in shots:
            print(f"  - {shot.filename} ({shot.id}, {shot.automation})")
        if skipped:
            print(f"[dry-run] Skipped ({len(skipped)}):")
            for shot in skipped:
                print(f"  - {shot.filename} ({shot.id}, {shot.automation})")
        return out_dir

    if skipped:
        skipped_ids = ", ".join(s.id for s in skipped)
        print(
            f"Skipping {len(skipped)} shot(s) — use --include-best-effort or "
            f"--include-manual: {skipped_ids}"
        )

    firefox_app = resolve_firefox_app(config, firefox_binary)
    bundle = resolve_firefox_bundle(firefox_binary)
    health = bundle_health_error(bundle)
    if health:
        print(f"Warning: {health}")
        print("  Launching firefox binary directly (may show 'Open existing' once).")
    window_cfg = config.get("window", {})
    window = (
        int(window_cfg.get("width", DEFAULT_WINDOW[0])),
        int(window_cfg.get("height", DEFAULT_WINDOW[1])),
    )
    base_prefs = {**BASE_PREFS, **config.get("base_prefs", {})}

    out_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []

    for shot in shots:
        print(f"Capturing {shot.id} → {shot.filename}")
        profile_dir = ensure_profile(
            root,
            project_slug,
            shot.profile,
            shot.prefs,
            base_prefs,
            reset=reset_profiles or shot.profile in {"first-run", "continuous"},
        )
        dest = out_dir / shot.filename
        warnings: list[str] = []
        try:
            warnings = capture_shot(
                shot,
                firefox_binary=firefox_binary,
                firefox_app=firefox_app,
                profile_dir=profile_dir,
                output_path=dest,
                window=window,
            )
            status = "warning" if warnings else "ok"
            error = None
        except Exception as exc:
            status = "error"
            error = str(exc)
            print(f"  ! {shot.id} failed: {exc}")

        results.append(
            {
                "id": shot.id,
                "filename": shot.filename,
                "automation": shot.automation,
                "status": status,
                "warnings": warnings,
                "error": error,
                "notes": shot.notes,
            }
        )

    skipped_results = [
        {
            "id": shot.id,
            "filename": shot.filename,
            "automation": shot.automation,
            "status": "skipped",
            "warnings": [],
            "error": None,
            "notes": shot.notes,
        }
        for shot in skipped
    ]

    manifest = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "nightly_version": version,
        "firefox_binary": str(firefox_binary),
        "firefox_app": firefox_app,
        "window": {"width": window[0], "height": window[1]},
        "base_prefs": base_prefs,
        "shots": results + skipped_results,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    state_path(root, project_slug).parent.mkdir(parents=True, exist_ok=True)
    state_path(root, project_slug).write_text(
        json.dumps(
            {
                "last_run": manifest["captured_at"],
                "last_version": version,
                "last_output": str(out_dir.relative_to(root)),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    ok = sum(1 for r in results if r["status"] == "ok")
    warn = sum(1 for r in results if r["status"] == "warning")
    err = sum(1 for r in results if r["status"] == "error")
    print(f"Done: {ok} ok, {warn} warning, {err} error → {out_dir}")
    if skipped:
        print(f"Skipped: {len(skipped)} (see manual-checklist.md)")
    return out_dir
