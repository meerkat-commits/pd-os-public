# /meeting-ingest

Goal: quickly turn a Zoom transcript into updated `data/people/*.md` files.

## Usage (local)

```bash
python3 -m pd_os.cli ingest-latest --meeting-title "<Title>" --move-processed
```

## Notes

- Best results if transcript lines include speaker names like `Jane Doe: ...`
- If your Zoom export omits speakers, you’ll need a different extraction approach

