#!/usr/bin/env python3
"""One-off debug: does Nova NTP load under Marionette with our profile prefs?"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from pd_os.nightly_screenshots import (  # noqa: E402
    _NTP_ENABLE_PREFS,
    _NTP_READY_SCRIPT,
    _kill_firefox,
    _wait_for_port,
    ensure_profile,
    load_config,
    parse_shots,
    repo_root_from_here,
)

MARIONETTE_PORT = 2828
FIREFOX = Path("/Applications/Firefox Nightly.app/Contents/MacOS/firefox")


def main() -> None:
    root = repo_root_from_here()
    config = load_config(root, "2026-06-nova-nightly-screenshots")
    shot = next(s for s in parse_shots(config) if s.id == "new-tab")
    profile = ensure_profile(
        root,
        "2026-06-nova-nightly-screenshots",
        shot.profile,
        shot.prefs,
        config.get("base_prefs", {}),
        reset=False,
    )
    _kill_firefox("Firefox Nightly")
    cmd = [
        str(FIREFOX),
        "-marionette",
        "-remote-allow-system-access",
        "-no-remote",
        "-profile",
        str(profile),
        "-width=1440",
        "-height=900",
        "about:blank",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not _wait_for_port(MARIONETTE_PORT, timeout=90):
            raise SystemExit("Marionette port not ready")
        from marionette_driver.marionette import Marionette

        m = Marionette(host="localhost", port=MARIONETTE_PORT)
        m.start_session()
        for key in (
            "browser.newtabpage.enabled",
            "browser.newtabpage.activity-stream.nova.enabled",
            "browser.nova.enabled",
        ):
            print(f"before set_prefs {key} =", m.get_pref(key))
        m.set_prefs(
            {
                **_NTP_ENABLE_PREFS,
                "browser.newtabpage.activity-stream.testing.shouldInitializeFeeds": True,
                "browser.topsites.contile.enabled": True,
            }
        )
        for key in (
            "browser.newtabpage.enabled",
            "browser.newtabpage.activity-stream.nova.enabled",
        ):
            print(f"after set_prefs {key} =", m.get_pref(key))
        m.navigate("about:newtab")
        for sec in (3, 6, 10, 15):
            time.sleep(3 if sec == 3 else 3)
            ready = m.execute_script(_NTP_READY_SCRIPT, script_timeout=30000)
            text_len = m.execute_script(
                "return (document.body && document.body.innerText) ? document.body.innerText.length : -1"
            )
            url = m.get_url()
            print(f"t={sec}s url={url} ready={ready} text_len={text_len}")
        m.delete_session()
    finally:
        proc.terminate()
        _kill_firefox("Firefox Nightly")


if __name__ == "__main__":
    main()
