#!/usr/bin/env bash
# Воспроизведение расшифровки. Медиа скачиваются в ../media (в git не попадают).
# Требуется: yt-dlp, ffmpeg, python3 + pip install faster-whisper
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p media && cd media
URL='https://vkvideo.ru/video-160329499_456285376'   # полная запись пленарной сессии
yt-dlp -f 'bestaudio[ext=m4a]' -o 'plenary_audio.%(ext)s' "$URL"
# фрагмент с ответом Ю. Максимова: 56:55–62:05 (3415–3725 с)
ffmpeg -y -loglevel error -ss 3415 -to 3725 -i plenary_audio.m4a -ac 1 -ar 16000 -c:a pcm_s16le maksimov_segment16k.wav
# видео фрагмента (необязательно)
yt-dlp -f 'best[height<=720]' --download-sections '*56:55-62:05' -o 'maksimov_segment_720p.%(ext)s' "$URL" || true
cd .. && python3 scripts/transcribe.py media/maksimov_segment16k.wav transcript/raw_whisper_large-v3.json
python3 scripts/make_timestamps.py
