#!/usr/bin/env bash
# Prepara el entorno desde cero (ejecutar dentro de pipeline/)
set -e
pip install --break-system-packages -q kokoro-onnx soundfile numpy
mkdir -p models work out
[ -f models/kokoro-v1.0.onnx ] || curl -sSL -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f models/voices-v1.0.bin ] || curl -sSL -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
[ -d node_modules ] || npm i -s puppeteer-core gsap
echo listo
