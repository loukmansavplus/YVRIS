"""Bibliothèque commune au guide et aux gabarits YVRIS : couleurs, logos, icônes, objets à taille réelle."""
import json, pathlib, re

GUIDE = pathlib.Path(__file__).resolve().parent
ROOT = GUIDE.parent
T = json.loads((ROOT / "couleurs" / "tokens.json").read_text(encoding="utf-8"))
COLORS = {k: v["hex"] for g in ("marque", "neutres", "etats", "dataviz") for k, v in T[g].items()}
M, A, P = COLORS["marine"], COLORS["accent"], COLORS["prune"]
SIGN = T["marque_texte"]["signature"]
C = T["contact"]
MODULES = T["marque_texte"]["modules"]

def css_vars():
    return ":root{" + "".join(f"--{k}:{v};" for k, v in COLORS.items()) + "}"

def head(title, css_rel="charte.css", fonts_rel="../polices/polices.css", extra=""):
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{title}</title>'
            f'<link rel="stylesheet" href="{fonts_rel}"><link rel="stylesheet" href="{css_rel}">'
            f'<style>{css_vars()}{extra}</style></head><body>')

# ---------- Couleurs ----------
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def cmyk(h):
    r, g, b = (v / 255 for v in rgb(h)); k = 1 - max(r, g, b)
    if k >= 1: return (0, 0, 0, 100)
    return tuple(round(100 * v) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))

# ---------- Logo ----------
_TIGHT = {"logo": "12 12 697.5 309.5", "monogramme": "12 12 309.2 309.2"}
def logo(variant="marine", h=20, mono=False, unit="mm", style=""):
    kind = "monogramme" if mono else "logo"
    s = (ROOT / "logo" / f"yvris-{kind}-{variant}.svg").read_text(encoding="utf-8")
    s = re.sub(r'viewBox="[^"]+"', f'viewBox="{_TIGHT[kind]}"', s, 1)
    s = re.sub(r' width="[^"]+" height="[^"]+"', "", s, 1)
    return s.replace("<svg ", f'<svg style="height:{h}{unit};width:auto;display:block;flex:none;{style}" ', 1)

def motif(color="#fff", opacity=.16, style=""):
    """Motif « entreprise connectée » : un centre relié à six points."""
    import math
    pts = [(100 + 78 * math.cos(math.radians(a)), 60 + 44 * math.sin(math.radians(a))) for a in (200, 255, 320, 20, 80, 140)]
    lines = "".join(f'<line x1="100" y1="60" x2="{x:.1f}" y2="{y:.1f}"/>' for x, y in pts)
    ring = "".join(f'<line x1="{pts[i][0]:.1f}" y1="{pts[i][1]:.1f}" x2="{pts[(i+1)%6][0]:.1f}" y2="{pts[(i+1)%6][1]:.1f}" stroke-dasharray="1.5 3"/>' for i in range(6))
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2"/>' for x, y in pts)
    return (f'<svg viewBox="0 0 200 120" style="opacity:{opacity};{style}"><g stroke="{color}" stroke-width=".8" fill="none">{lines}{ring}</g>'
            f'<g fill="{color}">{dots}<circle cx="100" cy="60" r="7"/></g></svg>')

# ---------- Icônes (trait 1.75, bouts ronds, grille 24) ----------
ICONS = {
 "crm": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 5.2a3.2 3.2 0 0 1 0 5.6M21 20c0-2.6-1.5-4.8-3.7-5.6"/>',
 "ventes": '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h7"/>',
 "compta": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8.5 12h.01M12 12h.01M15.5 12h.01M8.5 16h.01M12 16h.01M15.5 16h.01"/>',
 "rh": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M6 16c.5-1.6 1.6-2.4 3-2.4s2.5.8 3 2.4M15 10h3M15 13.5h3"/>',
 "stock": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
 "production": '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>',
 "instance": '<rect x="4" y="4" width="16" height="6" rx="1.5"/><rect x="4" y="14" width="16" height="6" rx="1.5"/><path d="M7.5 7h.01M7.5 17h.01"/>',
 "cloud": '<path d="M7 18a4 4 0 0 1-.6-7.95A5.5 5.5 0 0 1 17 9.5a4.25 4.25 0 0 1 .5 8.5z"/><path d="M9.5 13.5l2 2 3.5-3.5"/>',
 "dgi": '<path d="M12 3l7 3v5.5c0 4.2-2.9 7.6-7 9.5-4.1-1.9-7-5.3-7-9.5V6z"/><path d="M9 12l2.2 2.2L15.2 10"/>',
 "aide": '<path d="M5 13v-1a7 7 0 0 1 14 0v1"/><rect x="3.5" y="13" width="3.5" height="5.5" rx="1.2"/><rect x="17" y="13" width="3.5" height="5.5" rx="1.2"/><path d="M19 18.5c0 1.6-1.6 2.5-4 2.5h-1.5"/>',
 "tel": '<path d="M6 3h3l1.5 4-2 1.5a12 12 0 0 0 7 7l1.5-2 4 1.5v3a2 2 0 0 1-2 2A16 16 0 0 1 4 5a2 2 0 0 1 2-2z"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/>',
 "web": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>',
 "lieu": '<path d="M12 21s7-6.2 7-11.5a7 7 0 0 0-14 0C5 14.800 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
}
ICON_LABELS = [("crm", "CRM"), ("ventes", "Ventes & Facturation"), ("compta", "Comptabilité"), ("rh", "RH & Paie"), ("stock", "Stock"), ("production", "Production")]
BADGE_LABELS = [("instance", "Instance dédiée"), ("cloud", "Hébergé & sauvegardé"), ("dgi", "Conforme DGI"), ("aide", "Accompagnement")]

def icon_svg(name, size="1em", color="currentColor", sw=1.75):
    return (f'<svg viewBox="0 0 24 24" style="width:{size};height:{size};flex:none" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')
def ico(name, cls=""): return f'<span class="ico {cls}">{icon_svg(name, "7mm")}</span>'

def contact_lines(color, size="7pt", gap="1.1mm", icon_color=None, keys=("tel", "mail", "web", "lieu")):
    vals = {"tel": C["telephone"], "mail": C["email"], "web": C["site"], "lieu": C["ville"]}
    return "".join(f'<div style="display:flex;align-items:center;gap:1.6mm;font-size:{size};color:{color};margin-bottom:{gap};white-space:nowrap">'
                   f'{icon_svg(k, "1.25em", icon_color or A)}{vals[k]}</div>' for k in keys)

# ---------- Objets à taille réelle ----------
def carte_recto():
    return (f'<div class="carte" style="background:linear-gradient(135deg,{M} 40%,{P});display:flex;flex-direction:column;align-items:center;justify-content:center">'
            f'{motif("#fff", .13, "position:absolute;right:-16mm;bottom:-9mm;width:62mm")}'
            f'{logo("blanc", 14.5)}<div class="outfit" style="color:#fff;font-size:6.6pt;letter-spacing:.14em;text-transform:uppercase;margin-top:4mm;opacity:.9">{SIGN}</div>'
            f'<div class="abs" style="left:0;right:0;bottom:0;height:1.4mm;background:{A}"></div></div>')

def carte_verso(nom="Prénom NOM", role="Fonction"):
    return (f'<div class="carte"><div class="abs" style="left:7mm;top:7mm">{logo("marine", 9.5, mono=True)}</div>'
            f'<div class="abs outfit" style="right:7mm;top:8.2mm;font-size:6.2pt;letter-spacing:.14em;color:{A};font-weight:600;text-transform:uppercase">Business Cloud</div>'
            f'<div class="abs" style="left:7mm;top:21.5mm"><div class="outfit" style="font-weight:600;font-size:11.5pt;color:{M};line-height:1.1">{nom}</div>'
            f'<div style="font-size:7.4pt;color:{COLORS["gris_texte"]};margin-top:.8mm">{role}</div></div>'
            f'<div class="abs" style="left:7mm;bottom:5.2mm">{contact_lines(COLORS["encre"], "6.9pt", ".9mm")}</div>'
            f'<div class="abs" style="left:0;top:0;bottom:0;width:1.4mm;background:{A}"></div></div>')

def entete(body=True):
    lines = "".join(f'<i style="width:{w}%"></i>' for w in (38, 0, 100, 96, 100, 91, 100, 62, 0, 100, 97, 100, 88, 100, 100, 45, 0, 100, 94, 70))
    return (f'<div class="a4p"><div class="abs" style="left:20mm;top:16mm">{logo("marine", 15)}</div>'
            f'<div class="abs" style="right:20mm;top:17mm;text-align:right;font-size:8pt;color:{COLORS["gris_texte"]};line-height:1.5">'
            f'<b style="color:{M}">YVRIS Business Cloud</b><br>{C["ville"]}<br>{C["telephone"]}</div>'
            f'<div class="abs" style="left:20mm;right:20mm;top:38mm;height:.35mm;background:{M}"></div>'
            f'<div class="abs" style="left:20mm;top:38mm;width:26mm;height:1.1mm;background:{A}"></div>'
            + (f'<div class="abs lines" style="left:20mm;right:20mm;top:62mm">{lines}</div>' if body else "") +
            f'<div class="abs" style="left:20mm;right:20mm;bottom:12mm;border-top:.25mm solid {COLORS["gris_clair"]};padding-top:3mm;display:flex;justify-content:space-between;font-size:7.6pt;color:{COLORS["gris_texte"]}">'
            f'<span><b style="color:{M}">{C["site"]}</b> · {C["email"]} · {C["telephone"]}</span><span class="outfit" style="color:{A};font-weight:600;letter-spacing:.06em">{SIGN}</span></div></div>')

def enveloppe():
    return (f'<div class="dl"><div class="abs" style="left:12mm;top:11mm">{logo("marine", 11)}</div>'
            f'<div class="abs" style="left:12mm;top:25.5mm;font-size:7.4pt;color:{COLORS["gris_texte"]}">{C["ville"]} · {C["site"]}</div>'
            f'<div class="abs" style="right:14mm;top:11mm;width:19mm;height:23mm;border:.3mm dashed {COLORS["gris_clair"]};border-radius:1mm"></div>'
            f'<div class="abs lines" style="left:118mm;top:58mm;width:70mm"><i style="width:80%"></i><i style="width:100%"></i><i style="width:60%"></i></div>'
            f'<div class="abs" style="left:0;right:0;bottom:0;height:2.2mm;background:{M}"></div><div class="abs" style="left:0;bottom:0;width:40mm;height:2.2mm;background:{A}"></div></div>')

def cahier():
    return (f'<div class="a5p" style="background:linear-gradient(150deg,{M} 35%,{P})">'
            f'<div class="abs" style="right:-38mm;bottom:-30mm;opacity:.10">{logo("blanc", 150, mono=True)}</div>'
            f'<div class="abs" style="left:14mm;top:16mm">{logo("blanc", 17)}</div>'
            f'<div class="abs outfit" style="left:14mm;bottom:30mm;color:#fff;font-weight:800;font-size:25pt;line-height:1.05">Une agilité<br>sans <span style="color:{A}">limites.</span></div>'
            f'<div class="abs" style="left:14mm;bottom:17mm;color:#fff;opacity:.75;font-size:8.5pt">{C["site"]}</div>'
            f'<div class="abs" style="left:0;top:0;bottom:0;width:5mm;background:rgba(0,0,0,.28)"></div></div>')

def blocnotes():
    return (f'<div class="a5p" style="border-radius:.6mm"><div class="abs" style="left:0;right:0;top:0;height:7mm;background:{M}"></div>'
            f'<div class="abs" style="left:12mm;top:14mm">{logo("marine", 10)}</div>'
            f'<div class="abs" style="right:12mm;top:15.5mm;font-size:7.6pt;color:{COLORS["gris_texte"]}">Date : ____ / ____ / ________</div>'
            f'<div class="abs" style="left:12mm;right:12mm;top:32mm;bottom:20mm;background-image:radial-gradient({COLORS["gris_clair"]} .45mm,transparent .5mm);background-size:5mm 5mm"></div>'
            f'<div class="abs" style="left:12mm;right:12mm;bottom:9mm;display:flex;justify-content:space-between;font-size:7.2pt;color:{COLORS["gris_texte"]}">'
            f'<span>{C["site"]} · {C["telephone"]}</span><span style="color:{A};font-weight:600">{SIGN}</span></div></div>')

def stylo():
    return (f'<div style="width:138mm;height:9mm;position:relative"><div class="abs" style="left:0;top:0;width:118mm;height:9mm;border-radius:4.5mm 1mm 1mm 4.5mm;background:{M}"></div>'
            f'<div class="abs" style="left:118mm;top:.8mm;width:12mm;height:7.4mm;background:{A}"></div>'
            f'<div class="abs" style="left:130mm;top:2.2mm;border-left:8mm solid #B9BCC6;border-top:2.3mm solid transparent;border-bottom:2.3mm solid transparent"></div>'
            f'<div class="abs" style="left:34mm;top:2.5mm">{logo("blanc", 4)}</div></div>')

def badge(nom="Prénom NOM", role="Fonction"):
    return (f'<div class="badge"><div class="abs center" style="left:0;right:0;top:0;height:24mm;background:linear-gradient(135deg,{M} 40%,{P})">{logo("blanc", 9.5)}</div>'
            f'<div class="abs center" style="left:16mm;top:15mm;width:22mm;height:22mm;border-radius:50%;background:{COLORS["gris_clair"]};border:1mm solid #fff;color:#A9ABB8">{icon_svg("crm", "11mm", "#A9ABB8", 1.4)}</div>'
            f'<div class="abs" style="left:0;right:0;top:41mm;text-align:center"><div class="outfit" style="font-weight:600;font-size:11pt;color:{M}">{nom}</div>'
            f'<div style="font-size:7.6pt;color:{COLORS["gris_texte"]};margin-top:.6mm">{role}</div></div>'
            f'<div class="abs" style="left:8mm;right:8mm;top:57mm;border-top:.25mm solid {COLORS["gris_clair"]};padding-top:3mm;text-align:center;font-size:7pt;color:{COLORS["gris_texte"]}">YVRIS Business Cloud<br>{C["site"]}</div>'
            f'<div class="abs center outfit" style="left:0;right:0;bottom:0;height:9mm;background:{A};color:#fff;font-weight:600;font-size:7.6pt;letter-spacing:.14em">ÉQUIPE</div></div>')

def polo(color=None, mark="blanc"):
    color = color or M
    return (f'<div style="width:120mm;height:118mm;position:relative"><svg viewBox="0 0 240 236" style="width:120mm;height:118mm;display:block">'
            f'<path d="M84 8 L44 22 L4 62 L30 96 L52 78 L52 228 L188 228 L188 78 L210 96 L236 62 L196 22 L156 8 L120 44 Z" fill="{color}"/>'
            f'<path d="M84 8 L120 44 L156 8 L142 4 L120 26 L98 4 Z" fill="{"#fff" if mark == "blanc" else M}" opacity=".9"/>'
            f'<path d="M120 44 L120 84" stroke="{"#fff" if mark == "blanc" else M}" stroke-width="1.2" opacity=".55"/>'
            f'<path d="M4 62 L30 96 L36 91 L10 57 Z M236 62 L210 96 L204 91 L230 57 Z" fill="{A}"/></svg>'
            f'<div class="abs" style="left:74mm;top:36mm">{logo(mark, 7)}</div></div>')

def rollup():
    mods = "".join(f'<div style="display:flex;align-items:center;gap:22mm;margin-bottom:26mm"><span class="center" style="width:92mm;height:92mm;border-radius:22mm;background:{M};color:#fff">{icon_svg(k, "50mm", "#fff", 1.6)}</span>'
                   f'<span class="outfit" style="font-weight:600;font-size:46mm;color:{M}">{lab}</span></div>' for k, lab in ICON_LABELS)
    return (f'<div class="rollup"><div class="abs" style="left:0;right:0;top:0;height:800mm;background:linear-gradient(150deg,{M} 40%,{P})"></div>'
            f'{motif("#fff", .14, "position:absolute;right:-180mm;top:330mm;width:820mm")}'
            f'<div class="abs" style="left:80mm;top:95mm">{logo("blanc", 118)}</div>'
            f'<div class="abs outfit" style="left:80mm;top:330mm;color:#fff;font-weight:800;font-size:112mm;line-height:1.02">Gérez votre<br>activité avec<br><span style="color:{A}">efficacité.</span></div>'
            f'<div class="abs" style="left:80mm;top:700mm;color:#fff;font-size:34mm;opacity:.88">Une seule plateforme pour toute votre gestion.</div>'
            f'<div class="abs" style="left:80mm;top:895mm">{mods}</div>'
            f'<div class="abs" style="left:0;right:0;top:1640mm;height:360mm;background:{M}"></div><div class="abs" style="left:0;top:1640mm;width:260mm;height:12mm;background:{A}"></div>'
            f'<div class="abs outfit" style="left:80mm;top:1690mm;color:#fff;font-weight:600;font-size:52mm">Demandez une démonstration</div>'
            f'<div class="abs" style="left:80mm;top:1775mm;color:#fff;font-size:36mm;line-height:1.5">{C["telephone"]}<br>{C["site"]}</div></div>')

def enseigne_panel(w=3000, h=800):
    return (f'<div style="width:{w}mm;height:{h}mm;background:{M};display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden">'
            f'{logo("blanc", h * .5)}<div class="abs" style="left:0;right:0;bottom:0;height:{h * .045}mm;background:{A}"></div></div>')

def slide_titre():
    return (f'<div class="slide" style="background:linear-gradient(135deg,{M} 45%,{P})">{motif("#fff", .13, "position:absolute;right:-30mm;bottom:-22mm;width:170mm")}'
            f'<div class="abs" style="left:18mm;top:15mm">{logo("blanc", 12)}</div>'
            f'<div class="abs outfit" style="left:18mm;top:52mm;color:#fff;font-weight:800;font-size:38pt;line-height:1.05">Titre de la<br><span style="color:{A}">présentation.</span></div>'
            f'<div class="abs" style="left:18mm;top:99mm;color:#fff;opacity:.85;font-size:14pt">Sous-titre · date · intervenant</div>'
            f'<div class="abs" style="left:18mm;bottom:12mm;color:#fff;opacity:.7;font-size:9pt">{C["site"]}</div></div>')

def slide_contenu():
    cards = "".join(f'<div style="flex:1;border:.3mm solid {COLORS["gris_clair"]};border-radius:3mm;padding:6mm;background:{COLORS["blanc_casse"]}"><span class="center" style="width:13mm;height:13mm;border-radius:3mm;background:{M}">{icon_svg(k, "7mm", "#fff")}</span>'
                    f'<div class="outfit" style="font-weight:600;font-size:13pt;color:{M};margin:4mm 0 2mm">{lab}</div><div class="lines"><i></i><i style="width:80%"></i><i style="width:55%"></i></div></div>' for k, lab in ICON_LABELS[:3])
    return (f'<div class="slide"><div class="abs" style="left:18mm;top:13mm;font-size:8pt;letter-spacing:.13em;color:{A};font-weight:600">SECTION</div>'
            f'<div class="abs outfit" style="left:18mm;top:19mm;font-weight:800;font-size:25pt;color:{M}">Titre de la diapositive</div>'
            f'<div class="abs" style="left:18mm;right:18mm;top:43mm;display:flex;gap:7mm">{cards}</div>'
            f'<div class="abs" style="left:18mm;right:18mm;bottom:8mm;display:flex;justify-content:space-between;align-items:center;border-top:.3mm solid {COLORS["gris_clair"]};padding-top:3mm">{logo("marine", 6)}<span style="font-size:8pt;color:{COLORS["gris_texte"]}">2</span></div></div>')

# Réseaux sociaux (dimensions en pixels)
def social_avatar(s=640):
    return f'<div class="px center" style="width:{s}px;height:{s}px;background:{M}">{logo("blanc", s * .56, mono=True, unit="px")}</div>'

def social_banner(w=1584, h=396):
    return (f'<div class="px" style="width:{w}px;height:{h}px;background:linear-gradient(120deg,{M} 45%,{P})">{motif("#fff", .14, "position:absolute;right:-60px;top:-40px;width:760px")}'
            f'<div class="abs" style="left:420px;top:112px">{logo("blanc", 76, unit="px")}</div>'
            f'<div class="abs outfit" style="left:420px;top:216px;color:#fff;font-weight:600;font-size:34px">Une seule plateforme pour toute votre gestion.</div>'
            f'<div class="abs" style="left:420px;top:272px;color:#fff;opacity:.8;font-size:22px">CRM · Ventes · Comptabilité · RH & Paie · Stock · Production</div>'
            f'<div class="abs" style="left:0;right:0;bottom:0;height:10px;background:{A}"></div></div>')

def social_post(s=1080):
    return (f'<div class="px" style="width:{s}px;height:{s}px;background:#fff"><div class="abs" style="left:0;right:0;top:0;height:640px;background:linear-gradient(135deg,{M} 45%,{P})"></div>'
            f'{motif("#fff", .13, "position:absolute;right:-120px;top:230px;width:760px")}'
            f'<div class="abs" style="left:80px;top:76px">{logo("blanc", 64, unit="px")}</div>'
            f'<div class="abs outfit" style="left:80px;top:230px;color:#fff;font-weight:800;font-size:96px;line-height:1.03">Du devis<br>à la <span style="color:{A}">facture.</span></div>'
            f'<div class="abs" style="left:80px;top:700px;right:80px;font-size:38px;line-height:1.35;color:{COLORS["encre"]}">Créez vos devis, transformez-les en factures normalisées et suivez vos règlements au même endroit.</div>'
            f'<div class="abs outfit" style="left:80px;bottom:76px;background:{A};color:#fff;font-weight:600;font-size:30px;letter-spacing:.04em;padding:22px 40px;border-radius:12px">DEMANDER UNE DÉMO</div>'
            f'<div class="abs" style="right:80px;bottom:96px;font-size:30px;color:{M};font-weight:600">{C["site"]}</div></div>')

def social_story(w=1080, h=1920):
    return (f'<div class="px" style="width:{w}px;height:{h}px;background:linear-gradient(160deg,{M} 40%,{P})">{motif("#fff", .13, "position:absolute;left:-200px;bottom:300px;width:1500px")}'
            f'<div class="abs" style="left:90px;top:250px">{logo("blanc", 84, unit="px")}</div>'
            f'<div class="abs outfit" style="left:90px;top:560px;color:#fff;font-weight:800;font-size:128px;line-height:1.02">Gérez votre<br>activité avec<br><span style="color:{A}">efficacité.</span></div>'
            f'<div class="abs" style="left:90px;right:90px;top:1040px;color:#fff;opacity:.88;font-size:46px;line-height:1.35">CRM, ventes, comptabilité, paie, stock et production dans un seul environnement.</div>'
            f'<div class="abs outfit" style="left:90px;bottom:330px;background:{A};color:#fff;font-weight:600;font-size:40px;letter-spacing:.04em;padding:30px 54px;border-radius:16px">DEMANDER UNE DÉMO</div></div>')

def brochure_couv():
    return (f'<div class="a4p" style="background:linear-gradient(150deg,{M} 40%,{P})">{motif("#fff", .13, "position:absolute;right:-60mm;top:150mm;width:260mm")}'
            f'<div class="abs" style="left:20mm;top:20mm">{logo("blanc", 17)}</div>'
            f'<div class="abs outfit" style="right:20mm;top:24mm;color:{A};font-weight:600;font-size:9pt;letter-spacing:.16em">BUSINESS CLOUD</div>'
            f'<div class="abs outfit" style="left:20mm;top:86mm;color:#fff;font-weight:800;font-size:44pt;line-height:1.03">Gérez votre<br>activité avec<br><span style="color:{A}">efficacité.</span></div>'
            f'<div class="abs" style="left:20mm;top:156mm;width:120mm;color:#fff;opacity:.88;font-size:13pt;line-height:1.4">La plateforme ERP qui centralise vos opérations dans un seul environnement.</div>'
            f'<div class="abs" style="left:20mm;top:196mm;display:flex;gap:3mm;flex-wrap:wrap;width:165mm">' + "".join(f'<span style="border:.3mm solid rgba(255,255,255,.5);color:#fff;border-radius:10mm;padding:1.6mm 4.5mm;font-size:9.5pt;font-weight:600">{m}</span>' for m in MODULES) + '</div>'
            f'<div class="abs" style="left:20mm;bottom:20mm;color:#fff;opacity:.75;font-size:9.5pt">{C["site"]} · {C["telephone"]}</div><div class="abs" style="left:0;right:0;bottom:0;height:3mm;background:{A}"></div></div>')

def brochure_int():
    cards = "".join(f'<div style="border:.3mm solid {COLORS["gris_clair"]};border-radius:3mm;padding:5mm;background:{COLORS["blanc_casse"]}"><span class="center" style="width:12mm;height:12mm;border-radius:3mm;background:{M}">{icon_svg(k, "6.5mm", "#fff")}</span>'
                    f'<div class="outfit" style="font-weight:600;font-size:12pt;color:{M};margin:3mm 0 2mm">{lab}</div><div class="lines"><i></i><i style="width:70%"></i></div></div>' for k, lab in ICON_LABELS)
    return (f'<div class="a4p"><div class="abs" style="left:20mm;top:20mm;font-size:8.5pt;letter-spacing:.14em;color:{A};font-weight:600">NOTRE SOLUTION</div>'
            f'<div class="abs outfit" style="left:20mm;top:27mm;font-weight:800;font-size:27pt;line-height:1.08;color:{M}">Une seule plateforme<br>pour toute votre gestion.</div>'
            f'<div class="abs lines" style="left:20mm;top:60mm;width:150mm"><i></i><i style="width:92%"></i><i style="width:60%"></i></div>'
            f'<div class="abs" style="left:20mm;right:20mm;top:82mm;display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm">{cards}</div>'
            f'<div class="abs" style="left:20mm;right:20mm;top:178mm;height:84mm;border-radius:3mm;background:{M};overflow:hidden"><img src="img/ui-compta.jpg" style="position:absolute;left:10mm;top:10mm;width:150mm;border-radius:2mm"></div>'
            f'<div class="abs" style="left:20mm;right:20mm;bottom:12mm;display:flex;justify-content:space-between;align-items:center">{logo("marine", 6.5)}<span style="font-size:8pt;color:{COLORS["gris_texte"]}">2</span></div></div>')

def email_signature(nom="Prénom NOM", role="Fonction", logo_src="yvris-monogramme-marine.png"):
    """Signature e-mail en tableau HTML (compatible Outlook / Gmail). Police de repli : Arial."""
    return (f'<table cellpadding="0" cellspacing="0" style="font-family:Arial,Helvetica,sans-serif;color:{COLORS["encre"]};font-size:13px;line-height:1.45"><tr>'
            f'<td style="padding-right:14px;border-right:3px solid {A};vertical-align:middle"><img src="{logo_src}" width="64" height="64" alt="YVRIS" style="display:block"></td>'
            f'<td style="padding-left:14px;vertical-align:middle"><div style="font-size:16px;font-weight:bold;color:{M}">{nom}</div>'
            f'<div style="color:{COLORS["gris_texte"]};white-space:nowrap">{role} · YVRIS Business Cloud</div>'
            f'<div style="margin-top:6px;white-space:nowrap">{C["telephone"]} · <a href="mailto:{C["email"]}" style="color:{M};text-decoration:none">{C["email"]}</a></div>'
            f'<div style="white-space:nowrap"><a href="https://{C["site"]}" style="color:{A};text-decoration:none;font-weight:bold">{C["site"]}</a> · {C["ville"]}</div></td></tr></table>')

def z(html, zoom, cls="z"):
    """Met un objet à l'échelle."""
    return f'<div class="{cls}" style="zoom:{zoom}">{html}</div>'
def obj(html, left, top, zoom, rot=0, flat=False):
    return f'<div class="obj {"flat" if flat else ""}" style="left:{left}mm;top:{top}mm;transform:rotate({rot}deg)">{z(html, zoom)}</div>'
