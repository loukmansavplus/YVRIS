"""Photomontages réalistes : pose les vrais visuels de la charte sur les décors du dossier « PHOTO CAS USAGE ».
Usage : uv run --with playwright python build_photos.py [nom-de-scene ...]     (DEBUG=1 pour voir les calages)
Les décors sont générés par IA ; tout ce qui porte la marque vient de lib.py (logo vectoriel, gabarits)."""
import asyncio, json, os, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "guide"))
from lib import *
from playwright.async_api import async_playwright

SRC = ROOT.parent / "PHOTO CAS USAGE"
OUT = HERE / "photos"
DEBUG = os.environ.get("DEBUG") == "1"

def art(html, quad, shade="", clip=""):
    """Visuel posé en perspective sur les quatre coins (haut-gauche, haut-droit, bas-droit, bas-gauche)."""
    sh = f'<div style="position:absolute;inset:0;background:{shade};pointer-events:none"></div>' if shade else ""
    return f'<div class="art" data-quad="{json.dumps(quad)}" style="{clip}">{html}{sh}</div>'

def patch(points, color, blur=3):
    """Cache une zone de la photo par un aplat aux bords adoucis."""
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    x0, y0, w, h = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    poly = ",".join(f"{x - x0}px {y - y0}px" for x, y in points)
    return (f'<div class="patch" data-xy="[{x0},{y0}]" style="width:{w}px;height:{h}px;filter:blur({blur}px)">'
            f'<div style="width:100%;height:100%;background:{color};clip-path:polygon({poly})"></div></div>')

def box(x, y, w, h): return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
def logo_px(variant, h, mono=False): return logo(variant, h, mono=mono, unit="px")

LIGHT = "linear-gradient(100deg,rgba(255,255,255,.07),rgba(255,255,255,0) 45%,rgba(0,0,0,.10))"

SCENES = {}
def scene(name, src, crop, layers): SCENES[name] = (src, crop, layers)

# Les scènes sont déclarées plus bas (coordonnées en pixels de l'image d'origine).
exec((HERE / "photos_scenes.py").read_text(encoding="utf-8"))

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../polices/polices.css"><link rel="stylesheet" href="../guide/charte.css">
<style>%(vars)s html,body{margin:0;background:#000} .stage{position:relative;overflow:hidden;width:%(w)spx;height:%(h)spx}
.stage>img{position:absolute;left:-%(cx)spx;top:-%(cy)spx}
.art{position:absolute;left:0;top:0;transform-origin:0 0;display:inline-block;%(dbg)s}
.patch{position:absolute}</style></head><body><div class="stage"><img src="%(src)s">%(layers)s</div>
<script>
function solve(A,b){const n=b.length;for(let i=0;i<n;i++){let m=i;for(let r=i+1;r<n;r++)if(Math.abs(A[r][i])>Math.abs(A[m][i]))m=r;
 [A[i],A[m]]=[A[m],A[i]];[b[i],b[m]]=[b[m],b[i]];for(let r=i+1;r<n;r++){const f=A[r][i]/A[i][i];for(let c=i;c<n;c++)A[r][c]-=f*A[i][c];b[r]-=f*b[i];}}
 const x=Array(n).fill(0);for(let i=n-1;i>=0;i--){let s=b[i];for(let c=i+1;c<n;c++)s-=A[i][c]*x[c];x[i]=s/A[i][i];}return x;}
const CX=%(cx)s,CY=%(cy)s;
for(const el of document.querySelectorAll('.art')){const w=el.offsetWidth,h=el.offsetHeight,src=[[0,0],[w,0],[w,h],[0,h]];
 const dst=JSON.parse(el.dataset.quad).map(p=>[p[0]-CX,p[1]-CY]);const A=[],b=[];
 for(let i=0;i<4;i++){const [x,y]=src[i],[u,v]=dst[i];A.push([x,y,1,0,0,0,-u*x,-u*y]);b.push(u);A.push([0,0,0,x,y,1,-v*x,-v*y]);b.push(v);}
 const q=solve(A,b);el.style.transform=`matrix3d(${q[0]},${q[3]},0,${q[6]},${q[1]},${q[4]},0,${q[7]},0,0,1,0,${q[2]},${q[5]},0,1)`;}
for(const el of document.querySelectorAll('.patch')){const [x,y]=JSON.parse(el.dataset.xy);el.style.left=(x-CX)+'px';el.style.top=(y-CY)+'px';}
</script></body></html>"""

async def main():
    OUT.mkdir(exist_ok=True)
    names = sys.argv[1:] or list(SCENES)
    tmp = HERE / "_photo.html"
    async with async_playwright() as p:
        try: b = await p.chromium.launch(channel="chrome")
        except Exception: b = await p.chromium.launch(channel="msedge")
        for name in names:
            src, (cx, cy, w, h), layers = SCENES[name]
            tmp.write_text(PAGE % dict(vars=css_vars(), w=w, h=h, cx=cx, cy=cy, src=(SRC / src).as_uri(), layers="".join(layers),
                                       dbg="opacity:.55;outline:2px solid lime" if DEBUG else ""), encoding="utf-8")
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1 if DEBUG else 1.25)
            pg = await ctx.new_page()
            await pg.goto(tmp.as_uri()); await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(150)
            out = OUT / (("_debug-" if DEBUG else "") + name + ".jpg")
            await (await pg.query_selector(".stage")).screenshot(path=str(out), type="jpeg", quality=86)
            print("ok", out.name, round(out.stat().st_size / 1e3), "ko")
            await ctx.close()
        await b.close()
    tmp.unlink(missing_ok=True)
asyncio.run(main())
