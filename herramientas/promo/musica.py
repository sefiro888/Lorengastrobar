"""Pieza original en estilo polca paraguaya (compás de 6/8) con sonido de arpa, bajo, guitarra y maracas.
Sintetizada con numpy (cuerda pulsada Karplus-Strong). Es una composición propia: sin derechos de terceros.
Uso: python herramientas/promo/musica.py [salida.wav]"""
import sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(7)
CROMA = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def hz(nota, octava):  # nota "C", "F#"...
    n = CROMA[nota[0]] + (1 if "#" in nota else 0)
    return 440.0 * 2 ** ((n + 12 * (octava - 4) - 9) / 12)


def cuerda(f, dur, brillo=0.5, vida=0.996):
    """Karplus-Strong: cuerda pulsada."""
    n = int(SR * dur)
    p = max(2, int(SR / f))
    buf = (rng.random(p) * 2 - 1) * brillo + (rng.random(p) * 2 - 1) * (1 - brillo) * np.linspace(1, 0, p)
    out = np.empty(n)
    for i in range(n):
        j = i % p
        out[i] = buf[j]
        buf[j] = vida * 0.5 * (buf[j] + buf[(j + 1) % p])
    return out


_cache = {}


def nota(f, dur, **k):
    clave = (round(f, 2), round(dur, 3), tuple(sorted(k.items())))
    if clave not in _cache:
        _cache[clave] = cuerda(f, dur, **k)
    return _cache[clave]


def poner(pista, t, s, g=1.0):
    i = int(t * SR)
    if i < 0:
        s = s[-i:]
        i = 0
    if i >= len(pista) or len(s) == 0:
        return
    s = s[: len(pista) - i] * g
    pista[i : i + len(s)] += s


# 6/8: 6 corcheas por compás. Tempo vivo de polca: corchea = 0.17 s (~ 118 negras con puntillo/min)
C8 = 0.17
COMP = 6 * C8
DUR = 46.0
N = int(DUR * SR)
arpa, bajo, guit, maraca = (np.zeros(N) for _ in range(4))

# Progresión (Do mayor, aire de polca): C | G | C | F | C | G | C | C  (8 compases) y variación
ACORDES = [("C", ["C", "E", "G"]), ("G", ["B", "D", "G"]), ("C", ["C", "E", "G"]), ("F", ["C", "F", "A"]),
           ("C", ["C", "E", "G"]), ("G", ["B", "D", "G"]), ("C", ["C", "E", "G"]), ("C", ["C", "E", "G"])]
# motivo de la arpa en corcheas por compás (grados del acorde, 0/1/2 y octavas); None = silencio
MOTIVO_A = [2, None, 1, 2, None, 1]
MOTIVO_B = [2, 1, 0, 2, 1, 0]
MOTIVO_C = [0, 2, 1, 2, 0, 1]
compases = int(DUR / COMP) + 1
for c in range(compases):
    raiz, ac = ACORDES[c % len(ACORDES)]
    t0 = c * COMP
    seccion = (c // 8) % 3
    patron = [MOTIVO_A, MOTIVO_B, MOTIVO_C][seccion]
    # bajo: pulso en 1 y 4 (el "oom-pah" de la polca)
    fb = hz(raiz, 2)
    poner(bajo, t0, nota(fb, 0.5, brillo=0.2, vida=0.998), 0.9)
    poner(bajo, t0 + 3 * C8, nota(fb * (1.5 if raiz != "F" else 1.25), 0.4, brillo=0.2, vida=0.998), 0.6)
    # guitarra: rasgueo corto en 2, 3, 5, 6
    for k in (1, 2, 4, 5):
        for q, n_ in enumerate(ac):
            poner(guit, t0 + k * C8 + q * 0.012, nota(hz(n_, 3), 0.25, brillo=0.7, vida=0.992), 0.22)
    # arpa: melodía en la octava 5, con un adorno en el último tiempo
    for k, g in enumerate(patron):
        if g is None:
            continue
        n_ = ac[g]
        oc = 5 + (1 if (seccion == 2 and g == 2) else 0)
        poner(arpa, t0 + k * C8, nota(hz(n_, oc), 0.7, brillo=0.55, vida=0.9975), 0.55 if k % 3 == 0 else 0.4)
    # glissando de arpa al empezar cada 4 compases (típico del arpa paraguaya)
    if c % 4 == 0:
        for q, n_ in enumerate(["C", "E", "G", "C", "E", "G"]):
            poner(arpa, t0 - 0.3 + q * 0.04, nota(hz(n_, 4 + q // 3), 0.9, brillo=0.5, vida=0.998), 0.28)
    # maracas: ruido breve en cada corchea, más fuerte en 1 y 4
    for k in range(6):
        ruido = rng.random(int(0.05 * SR)) * 2 - 1
        ruido *= np.exp(-np.linspace(0, 9, len(ruido))) * (0.18 if k in (0, 3) else 0.09)
        poner(maraca, t0 + k * C8, np.diff(np.concatenate([[0], ruido])), 1.0)

mezcla = arpa * 1.0 + bajo * 0.9 + guit * 0.7 + maraca * 0.8
# eco suave (sala pequeña)
eco = np.zeros_like(mezcla)
for d, g in ((0.19, 0.28), (0.37, 0.16)):
    k = int(d * SR)
    eco[k:] += mezcla[:-k] * g
mezcla = mezcla + eco
mezcla /= np.max(np.abs(mezcla)) * 1.15
# entrada y salida suaves
f_in, f_out = int(1.2 * SR), int(3.0 * SR)
mezcla[:f_in] *= np.linspace(0, 1, f_in)
mezcla[-f_out:] *= np.linspace(1, 0, f_out)
sal = sys.argv[1] if len(sys.argv) > 1 else "polca-original.wav"
with wave.open(sal, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mezcla * 32767).astype(np.int16).tobytes())
print("ok", sal, round(len(mezcla) / SR, 1), "s")
