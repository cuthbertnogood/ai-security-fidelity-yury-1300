#!/usr/bin/env bash
# Перерендер всех схем Mermaid в PNG и SVG.
# Требуется: npm i -g @mermaid-js/mermaid-cli  (команда mmdc)
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p diagrams/rendered
for f in diagrams/*.mmd; do
  n=$(basename "$f" .mmd)
  mmdc -p scripts/puppeteer.json -i "$f" -o "diagrams/rendered/$n.svg" -b white
  mmdc -p scripts/puppeteer.json -i "$f" -o "diagrams/rendered/$n.png" -b white -s 2
  echo "rendered $n"
done
