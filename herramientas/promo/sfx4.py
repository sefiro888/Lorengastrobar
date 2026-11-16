"""Efectos de sonido del reel 4 (barridos en cada corte, golpes, siseo y destello del queso). Uso: python sfx4.py salida.wav"""
import sys, wave
import numpy as np
SR = 44100; DUR = 35.0; N = int(SR * DUR)
rng = np.random.default_rng(3)
P = 0.3483 * 8
T = [0, 2.4, 2.4 + P, 2.4 + 2 * P, 2.4 + 3 * P, 2.4 + 4 * P, 2.4 + 5 * P, 2.4 + 6 * P, 2.4 + 7 * P, 2.4 + 7 * P + 5.57, 35.0]
out = np.zeros(N)
def poner(t, s, g=1.0):
    i = int(t * SR)
    if i < 0: s = s[-i:]; i = 0
    s = s[: max(0, N - i)]; out[i:i + len(s)] += s * g
def filtro_paso_banda(x, f0, f1):
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR); X[(fr < f0) | (fr > f1)] = 0; return np.fft.irfft(X, len(x))
def barrido(dur=0.55, f0=300, f1=7000):          # "whoosh": ruido que sube de agudos y se apaga
    n = int(SR * dur); r = rng.standard_normal(n); tt = np.linspace(0, 1, n)
    y = np.zeros(n)
    for k in range(6):
        a, b = int(n * k / 6), int(n * (k + 1) / 6)
        c = f0 * (f1 / f0) ** ((k + 0.5) / 6); y[a:b] = filtro_paso_banda(r[a:b], c * .7, c * 1.4)
    env = np.sin(np.pi * tt) ** 1.6; return y * env / (np.abs(y).max() + 1e-9)
def golpe(f=70, dur=0.5):                         # bombo grave
    n = int(SR * dur); tt = np.arange(n) / SR; fr = f * (1 + 4 * np.exp(-tt * 18)); ph = 2 * np.pi * np.cumsum(fr) / SR
    return np.sin(ph) * np.exp(-tt * 7)
def pluck(f, dur=0.5):                            # nota de arpa corta
    n = int(SR * dur); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + .4 * np.sin(2 * np.pi * 2 * f * tt) + .2 * np.sin(2 * np.pi * 3 * f * tt)) * np.exp(-tt * 6)
def destello(dur=1.4):                            # campanitas agudas
    n = int(SR * dur); tt = np.arange(n) / SR; y = np.zeros(n)
    for k, f in enumerate((2093, 2637, 3136, 4186)): y += np.sin(2 * np.pi * f * tt) * np.exp(-(tt - k * .07).clip(0) * 4) * (tt >= k * .07)
    return y / 3
def siseo(dur=2.2):
    n = int(SR * dur); r = filtro_paso_banda(rng.standard_normal(n), 3000, 9000); tt = np.linspace(0, 1, n)
    return r / np.abs(r).max() * np.minimum(1, tt * 5) * np.minimum(1, (1 - tt) * 4) * (0.7 + 0.3 * rng.random(n))
for k in range(1, 10):                            # un barrido en cada corte
    poner(T[k] - 0.3, barrido(), 0.5)
poner(0.1, golpe(), 0.9); poner(0.1, destello(), 0.35)
for k in range(2, 8):                             # un toque de arpa por paso, subiendo la nota
    poner(T[k] + 0.12, pluck([392, 440, 494, 523, 587, 659][k - 2]), 0.28)
poner(T[8] - 0.05, golpe(60, .7), 1.0); poner(T[8] + 0.1, destello(1.6), 0.5)   # el queso
poner(T[7] - 0.1, siseo(), 0.25)
poner(T[9] + 0.15, golpe(70, .6), .8); poner(T[9] + 0.4, pluck(523, .9), .3)
out /= max(1e-9, np.abs(out).max()) * 1.1
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok")
