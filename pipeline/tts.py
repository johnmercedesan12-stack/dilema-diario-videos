import os, sys, json, subprocess, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
lines = json.load(open(sys.argv[1]))
out = []
for i, t in enumerate(lines):
    s, sr = k.create(t, voice=os.environ.get("VOZ","ef_dora"), speed=float(os.environ.get("VEL","1.0")), lang="es")
    p = f"work/l{i:02d}.wav"; sf.write("work/_raw.wav", s, sr)
    # tono mas agudo y alegre sin cambiar la duracion
    T = float(os.environ.get("TONO", "1.07"))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i","work/_raw.wav","-af",f"asetrate={int(sr*T)},aresample={sr},atempo={1/T:.5f},treble=g=3","work/_p.wav"],check=True)
    s, sr = sf.read("work/_p.wav", dtype="float32"); sf.write(p, s, sr)
    out.append({"text": t, "file": p, "dur": round(len(s)/sr, 3)})
json.dump(out, open("work/tts.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False))
