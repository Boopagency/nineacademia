"""Gera assets/ a partir de material/ (rodar da raiz: python3 material/gerar-assets.py).
Quando chegarem originais em alta, troque os arquivos em material/ e rode de novo."""
import subprocess, os
from PIL import Image

G, V = "material/galeria", "material/videos"
OUT_IMG, OUT_VID = "assets/img/galeria", "assets/video"
os.makedirs(OUT_IMG, exist_ok=True); os.makedirs(OUT_VID, exist_ok=True); os.makedirs("assets/img/pilares", exist_ok=True)

def ff(*a): subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *a], check=True)
def vid(n): return next(f"{V}/{f}" for f in sorted(os.listdir(V)) if f.startswith(f"reel-{n}-"))

def webp(im, name):
    im = im.convert("RGB")
    im.thumbnail((1600, 1600)); im.save(f"{OUT_IMG}/{name}.webp", quality=80)
    t = im.copy(); t.thumbnail((600, 4000)); t.save(f"{OUT_IMG}/{name}-600.webp", quality=72)
    return im.size

# Fotos do acervo
sizes = {}
for f in sorted(os.listdir(G)):
    if f[:2].isdigit():
        sizes[f[:2]] = webp(Image.open(f"{G}/{f}"), f[:2])

# Quadros tirados dos vídeos: (reel, segundo)
for n, t in [("01", 21), ("02", 9), ("04", 3), ("04", 12), ("04", 40), ("05", 39), ("05", 55), ("07", 12), ("07", 43), ("06", 17)]:
    tmp = f"/tmp/_v{n}-{t}.png"; ff("-ss", str(t), "-i", vid(n), "-frames:v", "1", tmp)
    sizes[f"v{n}-{t}"] = webp(Image.open(tmp), f"v{n}-{t}")

# Colagens dos pilares (recorte provisório do print do site atual)
ref = Image.open("referencias/site-atual.png").convert("RGB")
for i, box in enumerate([(410, 2235, 848, 2955), (1011, 3245, 1462, 3995), (410, 4415, 860, 5160)], 1):
    ref.crop(box).save(f"assets/img/pilares/pilar-0{i}.webp", quality=88)

# Vídeos: (saída, reel, início, duração, com áudio?)
clips = [
    ("hero-1", "01", 15, 8, False), ("hero-2", "02", 6, 8, False), ("hero-3", "04", 38, 8, False),
    ("zoom", "03", 24, 12, False),
] + [(f"reel-{n}", n, s, 15, True) for n, s in [("01", 9), ("02", 0), ("03", 0), ("04", 0), ("05", 30), ("06", 5), ("07", 0)]]
for out, n, start, dur, audio in clips:
    a = ["-c:a", "aac", "-b:a", "64k", "-ac", "1"] if audio else ["-an"]
    ff("-ss", str(start), "-t", str(dur), "-i", vid(n), "-vf", "scale=720:-2", "-c:v", "libx264", "-preset", "slow",
       "-crf", "30", "-maxrate", "800k", "-bufsize", "1600k", "-pix_fmt", "yuv420p", *a, "-movflags", "+faststart", f"{OUT_VID}/{out}.mp4")
    ff("-ss", "0.5", "-i", f"{OUT_VID}/{out}.mp4", "-frames:v", "1", "-q:v", "75", f"{OUT_VID}/{out}.webp")

for k, v in sizes.items(): print(k, v)
