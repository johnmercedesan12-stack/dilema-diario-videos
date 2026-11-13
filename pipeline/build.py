# Uso: python3 build.py episode.json  -> work/timeline.json + work/audio.wav
import sys, json, subprocess, numpy as np, soundfile as sf
ep = json.load(open(sys.argv[1]))
lines = [ep["hook"]] + [d["say"] for d in ep["dilemmas"]] + [ep["outro"]]
json.dump(lines, open("work/lines.json","w"), ensure_ascii=False)
subprocess.run(["python3","tts.py","work/lines.json"], check=True, stdout=subprocess.DEVNULL)
tts = json.load(open("work/tts.json"))
SR = 44100; COUNT = 3.0
t = 0.25; segs = []; voice = []; ticks = []
voice.append((t, tts[0]["file"])); segs.append({"type":"hook","start":0,"end":t+tts[0]["dur"]+0.35}); t = segs[-1]["end"]
for i, d in enumerate(ep["dilemmas"]):
    s = t; voice.append((s+0.35, tts[i+1]["file"])); cs = s+0.35+tts[i+1]["dur"]+0.15
    for k in range(3): ticks.append(cs+k)
    segs.append({"type":"dilemma","i":i,"start":s,"count":cs,"end":cs+COUNT}); t = cs+COUNT
voice.append((t+0.3, tts[-1]["file"])); segs.append({"type":"outro","start":t,"end":t+0.3+tts[-1]["dur"]+1.0}); total = segs[-1]["end"]
json.dump({"total":total,"segs":segs,"ep":ep}, open("work/timeline.json","w"), ensure_ascii=False)
n = int(total*SR)+SR//2; mix = np.zeros(n, dtype=np.float32)
def add(sig, at, g=1.0):
    a = int(at*SR); b = min(n, a+len(sig)); mix[a:b] += sig[:b-a]*g
for at, f in voice:
    s, sr = sf.read(f, dtype="float32")
    idx = np.linspace(0, len(s)-1, int(len(s)*SR/sr)); add(np.interp(idx, np.arange(len(s)), s), at, 1.0)
def tone(f, d, dec=18):
    x = np.arange(int(d*SR))/SR; return (np.sin(2*np.pi*f*x)*np.exp(-dec*x)).astype(np.float32)
for at in ticks: add(tone(880,0.18), at, 0.22)
for sg in segs:
    if sg["type"]=="dilemma":
        add(tone(1320,0.5,7)+tone(1760,0.5,7), sg["end"]-0.02, 0.12)   # ding al cerrar
        x = np.arange(int(0.35*SR))/SR                                    # whoosh de entrada
        add((np.random.randn(len(x))*np.sin(np.pi*x/0.35)**2).astype(np.float32), sg["start"], 0.05)
# base musical: pulso grave + arpegio suave (La menor), 100 bpm
beat = 0.6; notes = [220.0, 261.63, 329.63, 261.63, 196.0, 246.94, 293.66, 246.94]
tt = 0.0; k = 0
while tt < total:
    add(tone(55 if (k//8)%2==0 else 49, 0.5, 6), tt, 0.20)
    add(tone(notes[k%8], 0.3, 9), tt, 0.045); add(tone(notes[(k+2)%8]*2, 0.25, 12), tt+beat/2, 0.025)
    tt += beat; k += 1
fade = int(0.8*SR); mix[-fade:] *= np.linspace(1,0,fade)
mix = np.tanh(mix*1.4)*0.9
sf.write("work/audio.wav", mix, SR); print("total", round(total,2))
