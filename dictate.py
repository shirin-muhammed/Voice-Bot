"""Push-to-talk local dictation: hold F9 to speak, release to transcribe, then optionally correct."""
import sys

import keyboard
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

import corrections

RATE = 16000
HOTKEY = "f9"
MODEL_SIZE = "small"  # shortcut: small model for CPU speed; use "medium" if you have the RAM


def record_while_held() -> np.ndarray:
    chunks = []
    stream = sd.InputStream(samplerate=RATE, channels=1, dtype="float32",
                            callback=lambda indata, *_: chunks.append(indata.copy()))
    with stream:
        keyboard.wait(HOTKEY, suppress=False, trigger_on_release=False)
        while keyboard.is_pressed(HOTKEY):
            sd.sleep(20)
    return np.concatenate(chunks).flatten() if chunks else np.zeros(0, dtype="float32")


def main() -> None:
    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    print(f"Hold {HOTKEY.upper()} to speak. Ctrl+C to quit.")
    while True:
        audio = record_while_held()
        if audio.size < RATE // 4:
            continue
        data = corrections.load()
        segments, _ = model.transcribe(audio, language="en",
                                       initial_prompt=corrections.initial_prompt(data))
        text = corrections.apply(" ".join(s.text.strip() for s in segments), data["corrections"])
        print(f"\n> {text}")
        fixed = input("Correction (Enter to keep): ").strip()
        if fixed and fixed != text:
            corrections.save(corrections.learn(text, fixed, data))
            print("Learned.")
        keyboard.write(fixed or text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
