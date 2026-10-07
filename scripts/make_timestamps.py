#!/usr/bin/env python3
"""Генерирует transcript_timestamps.md и .srt из сырого вывода faster-whisper (large-v3).
Тексты сегментов НЕ редактируются: это сырая машинная расшифровка."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(root / "transcript/raw_whisper_large-v3.json", encoding="utf-8"))
OFF = d["offset_in_plenary_s"]

def hms(t, ms=False):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    if ms:
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s-int(s))*1000))%1000:03d}"
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}" if h else f"{int(m):02d}:{int(s):02d}"

def speaker(start):
    if start < 11.9: return "Предыдущий спикер (конец реплики)"
    if start < 30.0: return "Ведущая (вопрос)"
    if start >= 296.0: return "Ведущая"
    return "Ю. Максимов"

md = ["# Сырая расшифровка с таймкодами (faster-whisper large-v3, без правок)", "",
      "Колонка «фрагмент» — время от начала вырезанного фрагмента (56:55 записи пленарной сессии).",
      "Колонка «запись» — время в полной записи VK Video (video-160329499_456285376).", "",
      "| фрагмент | запись | говорит | текст |", "|---|---|---|---|"]
srt = []
for i, s in enumerate(d["segments"], 1):
    md.append(f"| {hms(s['start'])}–{hms(s['end'])} | {hms(s['start']+OFF)} | {speaker(s['start'])} | {s['text']} |")
    srt += [str(i), f"{hms(s['start'], True)} --> {hms(s['end'], True)}", s["text"], ""]
(root / "transcript/transcript_timestamps.md").write_text("\n".join(md) + "\n", encoding="utf-8")
(root / "transcript/transcript.srt").write_text("\n".join(srt), encoding="utf-8")
print("ok", len(d["segments"]))
