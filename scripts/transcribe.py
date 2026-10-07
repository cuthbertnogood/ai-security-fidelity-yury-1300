#!/usr/bin/env python3
"""Расшифровка фрагмента faster-whisper large-v3 (CPU).
Примечание: на тестовой машине compute_type=int8 давал пустой вывод, а float32 не помещался в память,
поэтому используется int16."""
import sys, json, wave
import numpy as np
from faster_whisper import WhisperModel

src = sys.argv[1] if len(sys.argv) > 1 else "media/maksimov_segment16k.wav"
dst = sys.argv[2] if len(sys.argv) > 2 else "transcript/raw_whisper_large-v3.json"
OFF = 3415.0  # смещение фрагмента в полной записи, сек

w = wave.open(src)
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
m = WhisperModel("large-v3", device="cpu", compute_type="int16", cpu_threads=8)
segs, _ = m.transcribe(a, language="ru", beam_size=5, word_timestamps=True,
                       condition_on_previous_text=False, vad_filter=False,
                       initial_prompt="Юрий Максимов, Positive Technologies. ИИ, ИИ-агент, агентная схема, инференс, промпт, кибербез, полигон, open source.")
out = []
for s in segs:
    out.append({"start": s.start, "end": s.end, "text": s.text.strip(), "avg_logprob": s.avg_logprob,
                "no_speech_prob": s.no_speech_prob,
                "words": [{"w": x.word, "s": x.start, "e": x.end, "p": x.probability} for x in (s.words or [])]})
    print(f"[{s.start:7.2f}] {s.text.strip()}", flush=True)
json.dump({"offset_in_plenary_s": OFF, "segments": out}, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
