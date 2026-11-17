"""«Palabra guaraní de la semana»: vídeo vertical de unos 15 s con la voz de Loren (audio/*.mp3 del diccionario).
Uso:  python herramientas/promo/palabra.py <clave> <numero_semana> <carpeta_trabajo> <salida_con_musica.mp4> [salida_solo_voz.mp4]
Claves: tuicha, rohayhu, pora, angiru, avati, mandio, pira, chyryry, vya, jaha, eju, tembiu, aguyje, mbaeichapa, nanduti
Necesita el servidor local en el puerto 8123 (python -m http.server 8123)."""
import os, sys, json, subprocess, shutil, glob, wave
import numpy as np
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
FF = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg-win-x86_64-v7.1.exe")
FPS = 30

# clave: (palabra, pronunciación, significado, frase de ejemplo, foto, frase que dice el audio)
PAL = {
    "tuicha": ("Tuicha", "tui-CHA", "Grande", "Como la chipa guazú", "img/platos/hl-chipa-guazu.webp", "Tuicha, grande, como la chipa guazú"),
    "rohayhu": ("Rohayhu", "ro-ha-YHU", "Te quiero", "La forma más común de decir «te amo»", "img/local/mesa-grupo.webp", "Rohayhu es te quiero o te amo"),
    "pora": ("Porã", "po-RÃ", "Bueno · Lindo", "Así de bonito se ve un plato de Loren", "img/platos/mila-caballo-pro.webp", "Porã, lindo"),
    "angiru": ("Angirũ", "an-gi-RŨ", "Amigo · Amiga", "Con quien compartes la mesa", "img/local/mesa-grupo.webp", "Angirũ, amigo o amiga"),
    "avati": ("Avati", "a-va-TÍ", "Maíz", "La base de la chipa guazú y la sopa paraguaya", "img/platos/sopa-paraguaya.webp", "Avati, maíz"),
    "mandio": ("Mandi'ó", "man-di-Ó", "Mandioca · Yuca", "El pan de cada día en Paraguay", "img/nuevo/yuca-brava.webp", "Mandi'o, mandioca o yuca"),
    "tembiu": ("Tembi'u", "tem-bi-Ú", "Comida", "Tembi'u paraguái: la comida paraguaya", "img/platos/mila-caballo-pro.webp", "Tembi'u es comida"),
    "jaha": ("Jaha", "ja-JÁ", "¡Vamos!", "¿Vamos a comer?", "img/local/sala-entrada.webp", "Jaha, vamos"),
    "eju": ("Eju", "e-JÚ", "¡Ven!", "La puerta está abierta", "img/local/sala-entrada.webp", "Eju es ven o vení"),
    "vya": ("Vy'a", "vi-YÁ", "Alegría", "Lo que se siente en la mesa de Loren", "img/local/mesa-grupo.webp", "Vy'a, alegría o felicidad"),
    "pira": ("Pira", "pi-RÁ", "Pez · Pescado", "Una palabra para tu próximo viaje", "img/platos/hl-chipa-guazu.webp", "Pira, pez o pescado"),
    "chyryry": ("Chyryry", "chi-ri-RÍ", "El chisporroteo", "El ruido de la sartén", "img/platos/hl-chyryry.webp", "Chyryry, cualquier fritura en sartén o en freidora"),
    "aguyje": ("Aguyje", "a-gui-YÉ", "Gracias", "La palabra que más decimos aquí", "img/local/mesa-grupo.webp", "Aguyje, gracias en guaraní"),
    "mbaeichapa": ("Mba'éichapa", "mba-é-i-CHA-pa", "¿Qué tal?", "El saludo de siempre de los paraguayos", "img/local/sala-pared-verde.webp", "Mba'éichapa, ¿qué tal? El saludo de siempre de los paraguayos"),
    "nanduti": ("Ñandutí", "ñan-du-TÍ", "Tela de araña", "El encaje paraguayo que decora esta web", "img/kv/flor-kv.webp", "Ñandutí es la tela de araña, el encaje paraguayo"),
}
clave, semana, TMP, SAL = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
SAL_VOZ = sys.argv[5] if len(sys.argv) > 5 else None
palabra, pron, signif, ejemplo, foto, frase = PAL[clave]
AUDIO = os.path.join(RAIZ, "audio", clave + ".mp3")
os.makedirs(TMP, exist_ok=True)

# 1) envolvente de la voz (para que las ondas bailen con ella)
wav = os.path.join(TMP, "voz.wav")
subprocess.run([FF, "-y", "-loglevel", "error", "-i", AUDIO, "-ac", "1", "-ar", "8000", wav], check=True)
w = wave.open(wav); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float); sr = w.getframerate()
DURA = len(x) / sr
n = int(DURA * FPS) + 2
env = [float(np.sqrt((x[int(i * sr / FPS):int((i + 1) * sr / FPS)] ** 2).mean() + 1e-9)) for i in range(n)]
m = max(env) or 1
env = [round(min(1.0, e / m) ** 0.7, 3) for e in env]
V0 = 2.7                                   # la voz entra en este segundo
T_SIG = V0 + DURA + 0.35                    # aparece el significado
T_FIN = T_SIG + 4.3                         # tarjeta final
DUR = round(T_FIN + 4.2, 1)

HTML = r'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Palabra guaraní</title>
<link rel="stylesheet" href="../../css/fuentes.css">
<style>
:root{--vino:#59011d;--vino9:#2a000e;--vino5:#7d0b2e;--crema:#f3eedc;--maiz:#e8b43a;--maiz2:#f4d27a;--carbon:#151012}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;overflow:hidden;background:#000}
#l{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Montserrat,sans-serif;color:var(--crema);background:var(--carbon) url("../../img/kv/textura-oscura.webp") center/cover}
#l::before{content:"";position:absolute;inset:0;background:linear-gradient(rgba(21,16,18,.58),rgba(21,16,18,.58)),radial-gradient(75% 55% at 50% 42%,rgba(125,11,46,.75),transparent 70%),radial-gradient(60% 40% at 50% 100%,rgba(234,106,38,.3),transparent 70%)}
#l>*{position:absolute}
.flor{left:50%;top:50%;width:1800px;height:1800px;margin:-900px 0 0 -900px;object-fit:contain;opacity:.15}
.c{left:0;right:0;text-align:center}.anton{font-family:Anton,sans-serif;text-transform:uppercase;line-height:1}
.kau{font-family:"Kaushan Script",cursive;color:var(--maiz);line-height:1.05}
.eye{font-weight:800;font-size:36px;letter-spacing:.3em;text-transform:uppercase;color:var(--maiz)}
.sh{text-shadow:0 6px 30px rgba(0,0,0,.85),0 2px 6px rgba(0,0,0,.65)}
.badge{width:170px;height:170px;border-radius:50%;background:var(--maiz);color:var(--vino9);display:grid;place-items:center;box-shadow:0 20px 40px -10px rgba(232,180,58,.6),0 0 0 10px rgba(21,16,18,.5);font-family:Anton;line-height:1}
.badge small{font-family:Montserrat;font-weight:800;font-size:22px;letter-spacing:.2em;display:block;text-align:center}.badge b{font-size:92px;display:block;text-align:center;margin-top:-6px}
.altavoz{left:50%;top:1100px;width:250px;height:250px;margin:-125px 0 0 -125px;border-radius:50%;background:var(--maiz);display:grid;place-items:center;box-shadow:0 30px 60px -10px rgba(232,180,58,.55)}
.barra{position:absolute;left:540px;top:1085px;width:16px;border-radius:8px;background:var(--maiz2);transform-origin:0 0;box-shadow:0 0 18px rgba(244,210,122,.8)}
.cap{left:60px;right:60px;top:1430px;background:rgba(42,0,14,.88);border:3px solid var(--maiz);border-radius:34px;padding:30px 36px;font-weight:700;font-size:44px;line-height:1.3;text-align:center;box-shadow:0 30px 60px -20px rgba(0,0,0,.9)}
.cap em{font-style:normal;color:var(--maiz)}
.disco{left:50%;width:560px;height:560px;margin-left:-280px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 12px rgba(243,238,220,.96),0 0 0 24px rgba(232,180,58,.95),0 50px 90px -20px rgba(0,0,0,.9)}
.disco img{width:100%;height:100%;object-fit:cover;display:block}
.enc{left:50%;width:900px;height:900px;margin-left:-450px;object-fit:contain;opacity:.55}
.chip{left:50%;background:var(--crema);color:var(--vino9);border-radius:70px;padding:24px 52px;font-weight:800;font-size:42px;white-space:nowrap;box-shadow:0 30px 60px -20px rgba(0,0,0,.9)}
.pill{display:inline-block;background:var(--maiz);color:var(--vino9);font-weight:800;font-size:46px;padding:24px 58px;border-radius:999px;box-shadow:0 20px 44px -10px rgba(232,180,58,.6)}
.chispa{width:12px;height:12px;border-radius:50%;background:var(--maiz2);box-shadow:0 0 20px 7px rgba(244,210,122,.85);opacity:0}
#flash{inset:0;background:#fff;opacity:0}#fin{inset:0;opacity:0;visibility:hidden}
#finfondo{inset:0;background:var(--carbon) url("../../img/kv/textura-oscura.webp") center/cover}
#finfondo::before{content:"";position:absolute;inset:0;background:linear-gradient(rgba(21,16,18,.62),rgba(21,16,18,.62)),radial-gradient(75% 55% at 50% 42%,rgba(125,11,46,.75),transparent 70%)}
#fin>*{position:absolute}
.brasas i{position:absolute;width:9px;height:9px;border-radius:50%;background:var(--maiz2);box-shadow:0 0 16px 5px rgba(244,210,122,.75);opacity:0}
</style></head><body><div id="l">
<img class="flor" id="flor" src="../../img/kv/flor-kv.webp" alt="">
<div class="brasas" id="brasas" style="inset:0"></div>

<div class="badge" id="badge" style="left:455px;top:150px"><div><small>SEMANA</small><b>@SEMANA@</b></div></div>
<div class="c eye sh" id="eye" style="top:360px">Palabra guaraní de la semana</div>

<div class="c anton sh" id="pal" style="top:470px;font-size:@TAM@px;color:var(--crema)">@PALABRA@</div>
<div class="c kau sh" id="pron" style="top:@PRONTOP@px;font-size:86px">@PRON@</div>

<div class="altavoz" id="alt"><svg viewBox="0 0 24 24" width="140" height="140" fill="none" stroke="#2a000e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg></div>
<div id="ondas"></div>
<div class="cap" id="cap">@FRASE@</div>

<div class="c eye sh" id="sig1" style="top:760px;opacity:0">Significa</div>
<div class="c anton sh" id="sig2" style="top:830px;font-size:@TAMSIG@px;color:var(--maiz);opacity:0">@SIGNIF@</div>
<img class="enc" id="enc" data-r="30" style="top:1015px;opacity:0" src="../../img/kv/flor-kv.webp" alt="">
<div class="disco" id="disco" style="top:1130px;opacity:0"><img src="../../@FOTO@"></div>
<div class="chip" id="chip" style="top:1730px;opacity:0">@EJEMPLO@</div>
<div id="chispas"></div>

<div id="fin"><div id="finfondo"></div>
  <img class="flor" id="florf" src="../../img/kv/flor-kv.webp" alt="" style="position:absolute">
  <img id="flogo" src="../../img/marca/logo-loren.webp" style="left:270px;top:250px;width:540px;filter:drop-shadow(0 24px 40px rgba(0,0,0,.6))">
  <div class="c kau sh" id="f1" style="top:620px;font-size:116px">¿La repites?</div>
  <div class="c anton" id="f2" style="top:790px;font-size:150px;line-height:.95">Dilo en<br>los comentarios</div>
  <div class="c" id="f3" style="top:1170px"><span class="pill">lorenrestobar.com</span></div>
  <div class="c" id="f4" style="top:1320px;font-size:40px;font-weight:600;line-height:1.4;left:40px;right:40px">Pruébala en Loren Restobar<br>Carrer de la Muntanya 115 · Barcelona</div>
  <div class="c kau" id="f5" style="top:1500px;font-size:110px">Aguyje!</div>
</div>
<div id="flash"></div></div>
<script>
const $=(s)=>document.querySelector(s),cl=(x)=>Math.max(0,Math.min(1,x));
const eo=(x)=>1-Math.pow(1-cl(x),3);
const eb=(x)=>{x=cl(x);const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const ENV=@ENV@,V0=@V0@,DURA=@DURA@,TS=@TSIG@,TF=@TFIN@,FPS=@FPS@;
const BR=$("#brasas");for(let i=0;i<30;i++){const e=document.createElement("i");e.dataset.x=(i*137.5)%1080;e.dataset.v=60+(i*53)%90;e.dataset.f=(i*0.41)%6;BR.appendChild(e)}
const ON=$("#ondas");const NB=56;for(let i=0;i<NB;i++){const b=document.createElement("div");b.className="barra";b.dataset.a=(i/NB)*Math.PI*2;ON.appendChild(b)}
const CH=$("#chispas");for(let i=0;i<22;i++){const e=document.createElement("div");e.className="chispa";e.style.cssText="position:absolute;left:540px;top:1410px";e.dataset.a=(i/22)*Math.PI*2;e.dataset.r=300+(i*71)%260;CH.appendChild(e)}
function render(t){
  $("#flor").style.transform=`rotate(${t*3}deg)`;$("#florf").style.transform=`rotate(${t*4}deg)`;
  document.querySelectorAll("#brasas i").forEach(e=>{const ph=((t+ +e.dataset.f)%6)/6;e.style.left=(+e.dataset.x+Math.sin(ph*9+ +e.dataset.f)*40)+"px";e.style.top=(1980-ph*(760+ +e.dataset.v*8))+"px";e.style.opacity=Math.sin(ph*Math.PI)*.85});
  // gancho
  $("#eye").style.opacity=cl((t-.2)/.4)*(1-cl((t-TS)/.3));$("#eye").style.transform=`translateY(${(1-eb((t-.2)/.7))*70}px)`;
  $("#badge").style.opacity=cl((t-.1)/.3);$("#badge").style.transform=`scale(${.3+.7*eb((t-.1)/.8)}) rotate(${(1-eb((t-.1)/.8))*-40}deg)`;
  // la palabra golpea la pantalla
  const pw=t-1.2;$("#pal").style.opacity=cl(pw/.15);$("#pal").style.transform=`scale(${1+(1-cl(pw/.3))*1.9})`;
  const pr=t-1.9;$("#pron").style.opacity=cl(pr/.4);$("#pron").style.transform=`translateY(${(1-eb(pr/.7))*60}px)`;
  let fl=0;if(pw>0&&pw<.25)fl=.5*(1-pw/.25);
  // la voz de Loren: altavoz y ondas
  const va=t-(V0-.4),dentro=t>=V0&&t<V0+DURA,idx=Math.max(0,Math.min(ENV.length-1,Math.floor((t-V0)*FPS))),amp=dentro?ENV[idx]:0;
  const sal=cl((t-TS)/.4);
  $("#alt").style.opacity=cl(va/.4)*(1-sal);$("#alt").style.transform=`scale(${(.4+.6*eb(va/.6))*(1+.1*amp)})`;
  document.querySelectorAll(".barra").forEach(b=>{const a=+b.dataset.a,h=14+amp*170*(.55+.45*Math.sin(a*5+t*18));b.style.opacity=cl(va/.4)*(1-sal);b.style.height=h+"px";b.style.transform=`rotate(${a*180/Math.PI-90}deg) translate(0,${-(135+0)}px) rotate(0deg)`;b.style.left=(540+Math.cos(a)*165)+"px";b.style.top=(1100+Math.sin(a)*165)+"px";b.style.transformOrigin="0 0";b.style.transform=`rotate(${a*180/Math.PI+90}deg)`;});
  $("#cap").style.opacity=cl((t-V0+.1)/.3)*(1-sal);$("#cap").style.transform=`translateY(${(1-eb((t-V0+.1)/.6))*80}px)`;
  // significado
  const ps=t-TS;
  $("#pal").style.top=(470-sal*120)+"px";$("#pal").style.fontSize=(@TAM@*(1-.35*sal))+"px";
  $("#pron").style.top=(@PRONTOP@-sal*210)+"px";$("#pron").style.fontSize=(86-26*sal)+"px";
  $("#sig1").style.opacity=cl(ps/.3);$("#sig1").style.transform=`translateY(${(1-eb(ps/.6))*60}px)`;
  $("#sig2").style.opacity=cl((ps-.1)/.2);$("#sig2").style.transform=`scale(${1+(1-cl((ps-.1)/.35))*1.8})`;
  if(ps>.1&&ps<.35)fl=Math.max(fl,.45*(1-(ps-.1)/.25));
  $("#enc").style.opacity=.55*cl((ps-.6)/.5);$("#enc").style.transform=`rotate(${t*30}deg) scale(${.6+.4*eo((ps-.6)/.8)})`;
  $("#disco").style.opacity=cl((ps-.6)/.3);$("#disco").style.transform=`scale(${.3+.7*eb((ps-.6)/.8)})`;
  $("#chip").style.opacity=cl((ps-1.4)/.3);$("#chip").style.transform=`translateX(-50%) translateY(${(1-eb((ps-1.4)/.6))*70}px)`;
  document.querySelectorAll(".chispa").forEach(e=>{const q=ps-.7-(+e.dataset.a%1)*.5,p=cl(q/1.4),r=+e.dataset.r*eo(p);e.style.opacity=p>0&&p<1?Math.sin(p*Math.PI):0;e.style.transform=`translate(${Math.cos(+e.dataset.a)*r}px,${Math.sin(+e.dataset.a)*r*.8}px) scale(${1.4-p})`});
  // tarjeta final
  const pf=t-TF,fin=$("#fin");fin.style.visibility=pf>-.3?"visible":"hidden";fin.style.opacity=cl((pf+.3)/.3);
  ["#flogo","#f1","#f2","#f3","#f4","#f5"].forEach((id,k)=>{const q=pf-.1-k*.22,e=eb(q/.7),el=$(id);el.style.opacity=cl(q/.4);el.style.transform=id==="#flogo"?`scale(${.5+.5*e})`:`translateY(${(1-e)*70}px)`});
  if(pf>-.3&&pf<0)fl=Math.max(fl,.5*(1+pf/.3));
  $("#flash").style.opacity=fl;
}
window.render=render;document.fonts.ready.then(()=>{window.LISTO=true;render(0)});
</script></body></html>'''
tam = 330 if len(palabra) <= 8 else (260 if len(palabra) <= 10 else 205)
tam_sig = 250 if len(signif) <= 9 else (190 if len(signif) <= 14 else 140)
pron_top = 470 + int(tam * 1.05)
rep = {"@SEMANA@": str(semana), "@PALABRA@": palabra, "@TAM@": str(tam), "@PRONTOP@": str(pron_top), "@PRON@": pron, "@TAMSIG@": str(tam_sig),
       "@SIGNIF@": signif, "@EJEMPLO@": ejemplo, "@FOTO@": foto, "@ENV@": json.dumps(env), "@V0@": str(V0), "@DURA@": str(round(DURA, 3)),
       "@TSIG@": str(round(T_SIG, 3)), "@TFIN@": str(round(T_FIN, 3)), "@FPS@": str(FPS)}
frase_html = frase
for pieza in (palabra,):
    frase_html = frase.replace(pieza, f"<em>{pieza}</em>", 1) if pieza in frase else frase
rep["@FRASE@"] = "«" + frase_html + "»"
out = HTML
for k, v in rep.items():
    out = out.replace(k, v)
html_ruta = os.path.join(AQUI, f"palabra_{clave}.html")
open(html_ruta, "w", encoding="utf-8").write(out)

# 2) fotogramas
fr = os.path.join(TMP, "frames")
N = int(DUR * FPS)
if not os.path.isdir(fr) or len(glob.glob(os.path.join(fr, "*.jpg"))) < N:
    shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
    with sync_playwright() as pw:
        nav = pw.chromium.launch(); pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.on("pageerror", lambda e: print("ERR", e))
        pg.goto(f"http://localhost:8123/herramientas/promo/palabra_{clave}.html", wait_until="load")
        pg.wait_for_function("window.LISTO === true"); pg.wait_for_timeout(1500)
        for i in range(N):
            pg.evaluate(f"render({i / FPS})")
            pg.screenshot(path=os.path.join(fr, f"{i:05d}.jpg"), type="jpeg", quality=93)
        nav.close()
print("fotogramas listos", N, "· duración", DUR, "s", flush=True)

# 3) audio: voz de Loren (+ sonidos) y, opcional, música original muy baja
voz = f"[1:a]loudnorm=I=-15:TP=-1.5:LRA=7,adelay={int(V0 * 1000)}|{int(V0 * 1000)},apad=whole_dur={DUR}[v]"
golpes = (f"anoisesrc=d=0.5:c=pink:r=44100,highpass=f=500,lowpass=f=6000,afade=t=in:st=0:d=0.4,afade=t=out:st=0.4:d=0.1,volume=0.3,adelay=1000|1000,apad=whole_dur={DUR}[w1];"
          f"anoisesrc=d=0.5:c=pink:r=44100,highpass=f=500,lowpass=f=6000,afade=t=in:st=0:d=0.4,afade=t=out:st=0.4:d=0.1,volume=0.3,adelay={int((T_SIG - 0.2) * 1000)}|{int((T_SIG - 0.2) * 1000)},apad=whole_dur={DUR}[w2];"
          f"anoisesrc=d=0.5:c=pink:r=44100,highpass=f=500,lowpass=f=6000,afade=t=in:st=0:d=0.4,afade=t=out:st=0.4:d=0.1,volume=0.3,adelay={int((T_FIN - 0.3) * 1000)}|{int((T_FIN - 0.3) * 1000)},apad=whole_dur={DUR}[w3]")
mus = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "para-loren", "promo", "polca-original.wav")
base_v = ["-framerate", str(FPS), "-i", os.path.join(fr, "%05d.jpg"), "-i", AUDIO]
subprocess.run([FF, "-y", "-loglevel", "error"] + base_v + ["-filter_complex", f"{voz};{golpes};[v][w1][w2][w3]amix=inputs=4:normalize=0,atrim=0:{DUR}[a]",
               "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(DUR), SAL_VOZ or SAL.replace(".mp4", "-solo-voz.mp4")], check=True)
if os.path.exists(mus):
    subprocess.run([FF, "-y", "-loglevel", "error"] + base_v + ["-i", mus, "-filter_complex",
                   f"{voz};{golpes};[2:a]volume=0.2,afade=t=in:st=0:d=1,afade=t=out:st={DUR - 2}:d=2,atrim=0:{DUR}[m];[v][w1][w2][w3][m]amix=inputs=5:normalize=0,atrim=0:{DUR}[a]",
                   "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(DUR), SAL], check=True)
print("hecho:", SAL)
