# Local Dictation

Push-to-talk speech-to-text that runs fully on your PC and learns your corrections.

- Speech recognition runs locally with `faster-whisper` (English). Nothing is sent to a cloud service.
- Hold **F9** to speak, release to transcribe.
- After each line, type a correction (or press Enter to keep it). The app learns the swapped words and uses your corrected words as hints next time.
- Learned data is stored in `%USERPROFILE%\.local-dictation\learned.json`. Delete that file to reset.

## Setup (Windows, Python 3.10+)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python dictate.py
```

The first run downloads the Whisper model once. The `keyboard` library may need to run as Administrator on some Windows setups.

## Tests

```powershell
pytest
```

## Limits

- It learns corrections and vocabulary. It does not retrain the speech model on your voice.
- Corrections are whole-word matches only.
