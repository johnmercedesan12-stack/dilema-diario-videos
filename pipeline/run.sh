#!/usr/bin/env bash
# Uso: ./run.sh episode.json ../videos/dilema-00N.mp4
set -e
VOZ=${VOZ:-ef_dora} VEL=${VEL:-1.1} TONO=${TONO:-1.07} python3 build.py "$1"
node render.mjs "$2"
ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$2"
