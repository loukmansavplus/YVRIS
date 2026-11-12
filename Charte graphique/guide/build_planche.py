"""Construit la planche de validation (2 pages A4 paysage) : HTML + PDF.
Usage : python build_planche.py   (depuis n'importe où)
Les couleurs viennent de ../couleurs/tokens.json, les logos de ../logo/, les polices de ../polices/."""
import os, json, asyncio, pathlib
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
T = json.loads((ROOT / "couleurs" / "tokens.json").read_text(encoding="utf-8"))

def hexof(group, name): return T[group][name]["hex"]
MARINE, PRUNE, ACCENT = hexof("marque", "marine"), hexof("marque", "prune"), hexof("marque", "accent")
ENCRE, GRIS_T, GRIS_C, CASSE = (hexof("neutres", k) for k in ("encre", "gris_texte", "gris_clair", "blanc_casse"))

def svg(name, height_mm):
    s = (ROOT / "logo" / name).read_text(encoding="utf-8")
    return s.replace("<svg ", f'<svg style="height:{height_mm}mm;width:auto;display:block" ', 1)

# --- Contraste WCAG ---
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
PAIRS = [("Texte encre sur blanc", ENCRE, "#FFFFFF"), ("Texte gris sur blanc cassé", GRIS_T, CASSE),
         ("Blanc sur marine", "#FFFFFF", MARINE), ("Blanc sur accent (bouton)", "#FFFFFF", ACCENT),
         ("Accent sur marine (mot-clé)", ACCENT, MARINE), ("Accent sur blanc (mot-clé)", ACCENT, "#FFFFFF")]
def verdict(r): return "Tout texte" if r >= 4.5 else ("Grands titres et boutons seulement" if r >= 3 else "À éviter pour du texte")
contrast_rows = "".join(
    f'<tr><td><span class="ech" style="background:{bg};color:{fg}">Aa</span></td><td>{lab}</td>'
    f'<td class="num">{ratio(fg, bg):.1f} : 1</td><td>{verdict(ratio(fg, bg))}</td></tr>' for lab, fg, bg in PAIRS)

def rgb(h): return " ".join(str(int(h[i:i + 2], 16)) for i in (1, 3, 5))
def swatch(group, name, label, big=False):
    t = T[group][name]; h = t["hex"]
    dark = lum(h) < 0.4
    return (f'<div class="sw {"big" if big else ""}" style="background:{h};color:{"#fff" if dark else ENCRE};'
            f'{"" if dark else "border:0.3mm solid " + GRIS_C}"><b>{label}</b><span>{h}</span><span>RVB {rgb(h)}</span>'
            f'{"<em>" + t["role"] + "</em>" if big else ""}</div>')

def choice(title, why, options):
    opts = "".join(f'<div class="opt"><i class="box"></i><span class="chip" style="background:{c}"></span>'
                   f'<div><b>{lab}</b><small>{note}</small></div></div>' if c else
                   f'<div class="opt"><i class="box"></i><div><b>{lab}</b><small>{note}</small></div></div>'
                   for lab, c, note in options)
    return f'<div class="dec"><h3>{title}</h3><p>{why}</p>{opts}</div>'

HTML = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>YVRIS — Planche de validation</title>
<link rel="stylesheet" href="../polices/polices.css">
<style>
@page {{ size: 297mm 210mm; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: Figtree, Arial, sans-serif; color: {ENCRE}; font-size: 10pt; line-height: 1.4; -webkit-print-color-adjust: exact; print-color-adjust: exact }}
.page {{ width: 297mm; height: 210mm; padding: 12mm 15mm 10mm; display: flex; flex-direction: column; gap: 4.5mm; page-break-after: always; overflow: hidden; background: #fff }}
header {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 0.4mm solid {MARINE}; padding-bottom: 3mm }}
header .k {{ font-size: 8.5pt; letter-spacing: .12em; text-transform: uppercase; color: {ACCENT}; font-weight: 600 }}
h1 {{ font-family: Outfit, Arial, sans-serif; font-weight: 800; font-size: 25pt; line-height: 1.05; color: {MARINE} }}
h2 {{ font-family: Outfit, Arial, sans-serif; font-weight: 600; font-size: 12pt; color: {MARINE}; margin-bottom: 2mm }}
h3 {{ font-family: Outfit, Arial, sans-serif; font-weight: 600; font-size: 11pt; color: {MARINE} }}
header .r {{ font-size: 8.5pt; color: {GRIS_T}; text-align: right }}
footer {{ margin-top: auto; font-size: 8pt; color: {GRIS_T}; display: flex; justify-content: space-between }}
small {{ display: block; font-size: 8.5pt; color: {GRIS_T} }}

.tiles {{ display: grid; grid-template-columns: 1.25fr 1.25fr 1.25fr 1fr; gap: 4mm }}
.tile {{ height: 44mm; border-radius: 2.5mm; display: flex; align-items: center; justify-content: center; gap: 6mm; position: relative }}
.tile span {{ position: absolute; left: 3.5mm; bottom: 2.5mm; font-size: 8pt }}
.cols3 {{ display: grid; grid-template-columns: 1.15fr 1fr 1.1fr; gap: 7mm; flex: 1 }}
.zone {{ background: {CASSE}; border-radius: 2.5mm; height: 50mm; display: flex; align-items: center; justify-content: center }}
.zone .prot {{ border: 0.3mm dashed {ACCENT}; padding: 6mm; position: relative }}
.zone .prot::after {{ content: "x"; position: absolute; left: 50%; top: 1mm; font-size: 8pt; color: {ACCENT}; font-weight: 600 }}
.zone .prot::before {{ content: "x"; position: absolute; left: 2.2mm; top: 50%; transform: translateY(-50%); font-size: 8pt; color: {ACCENT}; font-weight: 600 }}
.mins {{ display: flex; align-items: flex-end; gap: 9mm; height: 26mm; padding: 0 2mm }}
.mins div {{ display: flex; flex-direction: column; gap: 1.5mm; align-items: flex-start; font-size: 8.5pt; color: {GRIS_T} }}
ul {{ list-style: none }}
ul.no li, ul.ok li {{ padding: 1.1mm 0 1.1mm 6mm; position: relative; border-bottom: 0.2mm solid {GRIS_C} }}
ul.no li::before {{ content: "✕"; position: absolute; left: 0; color: {ACCENT}; font-weight: 700 }}
ul.ok li::before {{ content: "✓"; position: absolute; left: 0; color: {T['etats']['succes']['hex']}; font-weight: 700 }}
p.note {{ margin-top: 2.5mm; font-size: 9pt; color: {GRIS_T} }}

.cols2 {{ display: grid; grid-template-columns: 1.08fr 1fr; gap: 9mm; flex: 1 }}
.sws {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.5mm; margin-bottom: 2.5mm }}
.sw {{ border-radius: 2mm; padding: 2mm 2.5mm; display: flex; flex-direction: column; font-size: 7.2pt; line-height: 1.3; min-height: 13mm }}
.sw.big {{ min-height: 25mm; font-size: 8.2pt; padding: 2.5mm 3mm }}
.sw b {{ font-family: Outfit, Arial, sans-serif; font-weight: 600; font-size: 8.6pt; white-space: nowrap }}
.sw.big b {{ font-size: 10pt }}
.sw em {{ font-style: normal; margin-top: auto; opacity: .85; font-size: 7.8pt; line-height: 1.25 }}
.sws.s5 {{ grid-template-columns: repeat(5, 1fr) }}
table {{ width: 100%; border-collapse: collapse; font-size: 8.8pt }}
td {{ padding: 0.75mm 1.5mm; border-bottom: 0.2mm solid {GRIS_C}; vertical-align: middle }}
td.num {{ font-variant-numeric: tabular-nums; white-space: nowrap; font-weight: 600 }}
.ech {{ display: inline-block; width: 9mm; text-align: center; border-radius: 1mm; font-weight: 600; padding: .4mm 0; border: 0.2mm solid {GRIS_C} }}
.typo {{ background: {CASSE}; border-radius: 2.5mm; padding: 3.5mm 5mm; margin-bottom: 3mm }}
.typo .t1 {{ font-family: Outfit; font-weight: 800; font-size: 20pt; line-height: 1.05; color: {MARINE} }}
.typo .t1 i {{ font-style: normal; color: {ACCENT} }}
.typo .t2 {{ font-family: Outfit; font-weight: 600; font-size: 12.5pt; color: {MARINE}; margin-top: 2mm }}
.typo .t3 {{ font-size: 10pt; margin-top: 1.5mm; max-width: 105mm }}
.typo .meta {{ font-size: 8pt; color: {GRIS_T}; margin-top: 2.5mm }}
.decs {{ display: grid; grid-template-columns: 1fr; gap: 2mm }}
.dec {{ border: 0.3mm solid {GRIS_C}; border-left: 1mm solid {ACCENT}; border-radius: 2mm; padding: 1.8mm 4mm; display: grid; grid-template-columns: 1fr 1fr; column-gap: 5mm; row-gap: 1mm }}
.dec h3, .dec p {{ grid-column: 1 / -1 }}
.dec p {{ font-size: 8.5pt; color: {GRIS_T} }}
.opt {{ display: flex; align-items: center; gap: 2mm; font-size: 9pt }}
.box {{ width: 3.6mm; height: 3.6mm; border: 0.35mm solid {MARINE}; border-radius: .6mm; flex: none }}
.chip {{ width: 7mm; height: 7mm; border-radius: 1.2mm; flex: none }}
</style></head><body>

<section class="page">
  <header><div><div class="k">Charte graphique YVRIS · Planche de validation 1/2</div><h1>Le logo</h1></div>
    <div class="r">Proposition à valider avant la rédaction du guide complet<br>Le logo existant est conservé, redessiné en vectoriel</div></header>

  <div class="tiles">
    <div class="tile" style="background:#fff;border:0.3mm solid {GRIS_C}">{svg("yvris-logo-marine.svg", 24)}<span style="color:{GRIS_T}">Version principale, sur fond clair</span></div>
    <div class="tile" style="background:{MARINE}">{svg("yvris-logo-blanc.svg", 24)}<span style="color:#fff">Version blanche, sur marine</span></div>
    <div class="tile" style="background:{ACCENT}">{svg("yvris-logo-blanc.svg", 24)}<span style="color:#fff">Version blanche, sur accent</span></div>
    <div class="tile" style="background:{CASSE};border:0.3mm solid {GRIS_C}">{svg("yvris-monogramme-marine.svg", 24)}{svg("yvris-monogramme-noir.svg", 24)}<span style="color:{GRIS_T}">Monogramme : avatar, favicon, tampon</span></div>
  </div>

  <div class="cols3">
    <div><h2>Zone de protection</h2>
      <div class="zone"><div class="prot">{svg("yvris-logo-marine.svg", 22)}</div></div>
      <p class="note">Aucun texte ni image à moins de <b>x</b> du logo. <b>x</b> = un quart de la hauteur de la pastille ronde.</p></div>
    <div><h2>Tailles minimales</h2>
      <div class="mins">
        <div>{svg("yvris-logo-marine.svg", 11.6)}<span>Logo : 25 mm de large<br>(120 px à l'écran)</span></div>
        <div>{svg("yvris-monogramme-marine.svg", 8)}<span>Monogramme : 8 mm<br>(16 px à l'écran)</span></div>
      </div>
      <p class="note">En dessous de ces tailles, les lettres « VRIS » se bouchent : utiliser le monogramme seul.</p>
      <h2 style="margin-top:4mm">Fichiers fournis</h2>
      <ul class="ok"><li>SVG vectoriel : marine, blanc, noir</li><li>Monogramme : marine, blanc, noir</li><li>PNG et PDF (livrés avec le guide)</li></ul></div>
    <div><h2>À ne pas faire</h2>
      <ul class="no"><li>Déformer, incliner ou recadrer le logo</li><li>Changer sa couleur hors marine, blanc ou noir</li>
        <li>Ajouter une ombre, un contour ou un dégradé</li><li>Le poser sur une photo chargée sans aplat</li>
        <li>Utiliser le « Y » hexagonal des maquettes IA</li><li>Réécrire « YVRIS » dans une autre police</li></ul>
      <p class="note">Tracé obtenu à partir du PNG d'origine (721 px). Si le fichier source du logo existe (AI, SVG, PDF), merci de le transmettre : il remplacera ce tracé.</p></div>
  </div>
  <footer><span>YVRIS Business Cloud · Charte graphique · Proposition</span><span>1 / 2</span></footer>
</section>

<section class="page">
  <header><div><div class="k">Charte graphique YVRIS · Planche de validation 2/2</div><h1>Couleurs, typographie, décisions</h1></div>
    <div class="r">Trois choix à cocher en bas à droite<br>Le reste du guide en découle</div></header>

  <div class="cols2">
    <div>
      <h2>Couleurs de marque</h2>
      <div class="sws">{swatch("marque", "marine", "Marine YVRIS", True)}{swatch("marque", "accent", "Rouge accent", True)}{swatch("marque", "prune", "Prune", True)}</div>
      <div class="sws s5">{swatch("neutres", "blanc", "Blanc")}{swatch("neutres", "blanc_casse", "Blanc cassé")}{swatch("neutres", "gris_clair", "Gris clair")}{swatch("neutres", "gris_texte", "Gris texte")}{swatch("neutres", "encre", "Encre")}</div>
      <div class="sws s5">{swatch("etats", "succes", "Succès")}{swatch("etats", "alerte", "Alerte")}{swatch("etats", "erreur", "Erreur")}{swatch("dataviz", "bleu", "Graph. 1")}{swatch("dataviz", "mauve", "Graph. 2")}</div>
      <p class="note" style="margin:0 0 3mm">Répartition visée : 60 % blanc et neutres, 30 % marine, 10 % accent au plus. Le rouge « erreur » est plus sombre que l'accent pour ne pas les confondre.</p>
      <h2>Lisibilité (contraste)</h2>
      <table>{contrast_rows}</table>
    </div>
    <div>
      <h2>Typographie (celle du site yvris.net, conservée)</h2>
      <div class="typo">
        <div class="t1">Gérez votre activité<br>avec <i>efficacité.</i></div>
        <div class="t2">Une seule plateforme pour toute votre gestion</div>
        <div class="t3">CRM, ventes, comptabilité, paie, stock et production réunis dans un même environnement, pensé pour les TPE et PME.</div>
        <div class="meta"><b>Outfit</b> ExtraBold et SemiBold pour les titres · <b>Figtree</b> Regular et SemiBold pour le texte · Gratuites (licence libre) · Repli Word/PowerPoint : Arial</div>
      </div>
      <h2>Trois décisions à valider</h2>
      <div class="decs">
        {choice("1. Bleu marine de référence", "Cinq marines différents circulent aujourd'hui. Il en faut un seul.",
                [("Marine du logo " + MARINE, MARINE, "Recommandé : c'est la couleur du logo"), ("Marine du site #00254A", "#00254A", "Plus bleu, moins profond")])}
        {choice("2. Couleur d'accent", "Le site et la brochure sont déjà en rouge ; des maquettes utilisaient un bleu.",
                [("Rouge " + ACCENT, ACCENT, "Recommandé : continuité avec l'existant"), ("Bleu électrique #2B42F5", "#2B42F5", "Change le site et la brochure")])}
        {choice("3. Signature de marque", "Une seule phrase accompagne le logo partout.",
                [("« Une agilité sans limites. »", None, "Déjà en tête du site"), ("« Votre entreprise. Notre solution. Votre succès. »", None, "Plus explicite, plus longue")])}
      </div>
    </div>
  </div>
  <footer><span>YVRIS Business Cloud · Charte graphique · Proposition</span><span>2 / 2</span></footer>
</section>
</body></html>"""

async def main():
    html_path = HERE / "planche-validation.html"
    html_path.write_text(HTML, encoding="utf-8")
    pdf_path = HERE / "YVRIS-planche-validation.pdf"
    async with async_playwright() as p:
        try: b = await p.chromium.launch(channel="chrome")
        except Exception: b = await p.chromium.launch(channel="msedge")
        pg = await b.new_page()
        await pg.goto(html_path.as_uri())
        await pg.evaluate("document.fonts.ready")
        await pg.pdf(path=str(pdf_path), width="297mm", height="210mm", print_background=True, prefer_css_page_size=True)
        await b.close()
    print("ok", pdf_path, os.path.getsize(pdf_path), "octets")
asyncio.run(main())
