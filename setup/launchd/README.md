# macOS automation (launchd)

Runs PD-OS on a schedule **without Cursor open**.

| Job | Schedule | What it runs |
|-----|----------|----------------|
| **Daily** | Every day **16:00** | `sync-granola` (24h) → daily digest → commitments tracker → project hygiene |
| **Weekly** | **Monday 07:30** | `sync-granola` (last week) → weekly rollup → commitments → project hygiene |
| **Nightly Nova** *(optional)* | Every day **06:30** | Firefox Nightly punch-QA screenshots → `data/projects/2026-06-nova-nightly-screenshots/captures/` |

Optional: `run-daily --stakeholder-drafts` / `run-weekly --stakeholder-drafts` for message context files.

**Nightly Nova screenshots** (separate installer):

```bash
./setup/launchd/install-nightly-nova.sh
```

Secrets live in **`~/.config/pd-os/env`** (not in the repo).

## Outputs

| Artifact | Path |
|----------|------|
| Daily digest | `data/digests/YYYY-MM-DD.md` |
| Commitments tracker | `data/digests/commitments-YYYY-MM-DD.md` |
| Project hygiene | `data/digests/project-hygiene-YYYY-MM-DD.md` |
| Weekly rollup | `data/rollups/weekly/...` |
| Stakeholder draft context | `data/drafts/stakeholder/YYYY-MM-DD__Person.md` |

## One-time install

```bash
cd ~/VibeCoding_BK/work/pd-os
chmod +x setup/launchd/install.sh setup/launchd/uninstall.sh setup/bin/*.sh
./setup/launchd/install.sh
```

1. Creates `.venv` and installs `requirements.txt` if needed.
2. Copies `setup/config/env.example` → `~/.config/pd-os/env` (if missing).
3. Installs plists into `~/Library/LaunchAgents/` and loads them.

**Edit your API key:**

```bash
nano ~/.config/pd-os/env   # set GRANOLA_API_KEY='grn_...'
chmod 600 ~/.config/pd-os/env
```

## Test manually

```bash
~/VibeCoding_BK/work/pd-os/setup/bin/run-daily.sh
~/VibeCoding_BK/work/pd-os/setup/bin/run-weekly.sh
```

Or via CLI:

```bash
python3 -m pd_os.cli run-daily
python3 -m pd_os.cli run-weekly
```

## Logs

```bash
tail -n 200 /tmp/pd-os.daily.log
tail -n 200 /tmp/pd-os.weekly.log
```

## Uninstall

```bash
./setup/launchd/uninstall.sh
```

## Change schedule

Edit the installed plist in `~/Library/LaunchAgents/`, then:

```bash
launchctl bootout gui/$(id -u)/com.pd-os.daily
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.pd-os.daily.plist
```

Or re-run `./setup/launchd/install.sh` after editing templates under `setup/launchd/`.

## Cursor agent prompts (optional)

If you want a **Cursor agent** to review outputs (not replace launchd), use the prompts in [`../agents/`](../agents/).
