# PD-OS — Brooke Katalinich

Public snapshot of a **Product Design Operating System**.

## What's here

| Path | Contents |
|------|----------|
| [`context-library/`](context-library/) | Stable product and process context |
| [`data/projects/`](data/projects/) | Example initiatives (Nova, velocity mandate) |
| [`pd_os/`](pd_os/) | Python CLI — digests, critique prep, dashboard |
| [`setup/`](setup/) | Agents, launchd templates, export scripts |

## Quick start (PD-OS)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m pd_os.cli dashboard --open
```

## Public vs private

This repo is a **redacted export**. Excluded: `data/people/`, meeting transcripts, calibration, internal metrics, manager 1:1 docs, full decision registries with colleague names.

Regenerate locally:

```bash
./setup/bin/export-public-github.sh
```

## Links

- AI Native Knowledge Hub: https://github.com/FirefoxUX/ai-native-knowledge-hub
- Maven (AI-Driven Design): https://maven.com/bkatalinich/ai-driven-design/preview/354376
- Substack: https://brookekatalinich.substack.com/
