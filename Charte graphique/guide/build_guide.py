"""Construit le guide complet (HTML + PDF) et exporte les mises en situation en PNG.
Usage : python build_guide.py"""
import asyncio, os, math
from playwright.async_api import async_playwright
from lib import *

G, GT, GC, BC, ENC = COLORS["gris_texte"], COLORS["gris_texte"], COLORS["gris_clair"], COLORS["blanc_casse"], COLORS["encre"]
VERSION = "Version 1.0 · Novembre 2026"
PAGES = []  # (kick, title, lead, body)
def add(kick, title, lead, body): PAGES.append((kick, title, lead, body))

def tile(inner, bg, label, color=G, cls="", h=38):
    return f'<div class="tile {cls}" style="background:{bg};min-height:{h}mm">{inner}<span class="l" style="color:{color}">{label}</span></div>'
def sw(key, label, big=True, extra=True, mh=None):
    h = COLORS[key]; dark = lum(h) < .4
    role = next(v[key]["role"] for v in (T["marque"], T["neutres"], T["etats"], T["dataviz"]) if key in v)
    c, m, y, k = cmyk(h); r, g, b = rgb(h)
    return (f'<div class="sw {"" if big else "s"}" style="background:{h};color:{"#fff" if dark else ENC};{"" if dark else "border:.25mm solid " + GC};min-height:{mh or (46 if big else 24)}mm">'
            f'<b>{label}</b><span>HEX {h}</span><span>RVB {r} · {g} · {b}</span>' + (f'<span>CMJN {c} · {m} · {y} · {k}</span>' if extra else "") +
            (f'<span class="role">{role}</span>' if big else "") + '</div>')
def recolor(svg, color): return svg.replace(f'fill="{M}"', f'fill="{color}"')

# ================= 1. MARQUE =================
add("1 · La marque", "Qui est YVRIS", "Avant les couleurs et les polices : ce que la marque doit faire ressentir.", f"""
<div class="g g3 fill">
  <div class="card"><h2>Positionnement</h2>
    <p><b>YVRIS Business Cloud</b> est une plateforme de gestion en ligne (ERP) pour les créateurs d'entreprise, les TPE et les PME.</p>
    <p style="margin-top:2.5mm">Elle réunit dans un même environnement les grandes fonctions de l'entreprise, activables selon les besoins :</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:2.4mm;margin-top:3.5mm">{"".join(f'<div class="icorow">{ico(k, "dark")}<b style="font-size:8.6pt">{l}</b></div>' for k, l in ICON_LABELS)}</div>
    <p class="note" style="margin-top:4mm">Arguments de confiance : instance dédiée, hébergement et sauvegarde, factures normalisées conformes DGI, accompagnement par des experts-comptables, abonnement sans engagement.</p></div>
  <div class="card"><h2>Personnalité</h2>
    <table><tr><td><b>Professionnelle</b></td><td>Sérieuse sans être froide. On parle de gestion, on reste précis.</td></tr>
    <tr><td><b>Claire</b></td><td>Une idée par phrase. Aucun jargon inutile.</td></tr>
    <tr><td><b>Accessible</b></td><td>Compréhensible par un dirigeant qui n'est pas informaticien.</td></tr>
    <tr><td><b>Moderne</b></td><td>Formes nettes, beaucoup d'air, peu de couleurs.</td></tr>
    <tr><td><b>Rassurante</b></td><td>On montre le vrai produit, on ne promet que ce qui existe.</td></tr></table>
    <h2 style="margin-top:5mm">L'idée centrale</h2>
    <p>YVRIS n'est pas une liste de modules. C'est <b>le centre de pilotage de l'entreprise</b> : chaque activité est un point, YVRIS les relie.</p></div>
  <div class="card"><h2>Le ton</h2>
    <table><tr><th>On écrit</th><th>On évite</th></tr>
    <tr><td>« Du devis à la facture. »</td><td>« Solution intégrée de gestion du cycle commercial »</td></tr>
    <tr><td>« Sachez ce que vous avez en stock. »</td><td>« Module de gestion des stocks »</td></tr>
    <tr><td>« Parlons de votre activité. »</td><td>« Nous contacter »</td></tr>
    <tr><td>Des verbes d'action, des phrases courtes</td><td>Les paragraphes longs, le ton institutionnel</td></tr>
    <tr><td>Des bénéfices pour le dirigeant</td><td>La description technique seule</td></tr></table>
    <p class="note" style="margin-top:4mm">On vouvoie toujours. Les chiffres cités sont réels et vérifiés, ou clairement présentés comme des exemples.</p></div>
</div>""")

def hub():
    pts = [(150 + 108 * math.cos(math.radians(a)), 105 + 78 * math.sin(math.radians(a))) for a in (210, 270, 330, 30, 90, 150)]
    s = "".join(f'<line x1="150" y1="105" x2="{x:.0f}" y2="{y:.0f}" stroke="{M}" stroke-width="1"/>' for x, y in pts)
    s += "".join(f'<line x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[(i+1)%6][0]:.0f}" y2="{pts[(i+1)%6][1]:.0f}" stroke="{GC}" stroke-width="1" stroke-dasharray="2 3"/>' for i in range(6))
    for (x, y), (k, lab) in zip(pts, ICON_LABELS):
        s += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="#fff" stroke="{M}" stroke-width="1"/><g transform="translate({x-8:.0f},{y-8:.0f}) scale(.667)" fill="none" stroke="{M}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</g>'
              f'<text x="{x:.0f}" y="{(y-18) if y < 105 else (y+23):.0f}" text-anchor="middle" font-family="Figtree" font-size="7.5" font-weight="600" fill="{M}">{lab}</text>')
    s += f'<circle cx="150" cy="105" r="27" fill="{M}"/><circle cx="150" cy="105" r="31" fill="none" stroke="{A}" stroke-width="1.5"/>'
    return f'<svg viewBox="0 0 300 215" style="width:100%;display:block">{s}</svg>'

add("1 · La marque", "Signature, nom et concept", "Trois repères qui ne changent jamais d'un support à l'autre.", f"""
<div class="g fill" style="grid-template-columns:1fr 1.05fr 1.1fr">
  <div style="display:flex;flex-direction:column;gap:4mm">
    <div class="card dark center" style="flex-direction:column;gap:5mm;min-height:52mm;background:linear-gradient(135deg,{M} 40%,{P})">{logo("blanc", 17)}
      <div class="outfit" style="font-size:9pt;letter-spacing:.16em;text-transform:uppercase">{SIGN}</div></div>
    <div><h2>La signature</h2><ul class="dot"><li>Une seule signature : <b>« {SIGN} »</b></li><li>Toujours avec son point final, jamais modifiée.</li>
      <li>Placée sous le logo ou en pied de page, en petites capitales espacées.</li>
      <li>Les autres phrases (« Gérez votre activité avec efficacité. ») sont des <b>titres de campagne</b>, pas des signatures.</li></ul></div></div>
  <div><h2>Le nom</h2>
    <table><tr><th>Écriture</th><th>Usage</th></tr>
    <tr><td><b>YVRIS</b></td><td>Nom de la marque. Toujours en capitales.</td></tr>
    <tr><td><b>YVRIS Business Cloud</b></td><td>Nom complet du produit. À la première mention d'un document.</td></tr>
    <tr><td><b>le module Comptabilité</b></td><td>Les modules prennent une majuscule et gardent leur nom : {", ".join(MODULES)}.</td></tr>
    <tr><td><b>YVRIS, l'ERP en ligne</b></td><td>« ERP » décrit le produit, il ne fait pas partie du nom.</td></tr></table>
    <h2 style="margin-top:5mm">À ne pas écrire</h2>
    <ul class="no"><li>Yvris, yvris, Y-VRIS</li><li>YVRIS ERP comme nom de produit</li><li>« YVRIS » retapé dans une police fantaisie à la place du logo</li></ul></div>
  <div><h2>Le concept visuel : une entreprise connectée</h2><div class="card" style="padding:2mm 4mm">{hub()}</div>
    <p class="note" style="margin-top:2.5mm">Chaque activité est un point, YVRIS est le centre qui les relie. Ce motif de points et de lignes sert de décor discret sur les fonds marine (couvertures, bannières, roll-up).</p></div>
</div>""")

# ================= 2. LOGO =================
add("2 · Le logo", "Les versions du logo", "Le logo officiel de yvris.net, redessiné en vectoriel. On ne le modifie jamais.", f"""
<div class="g g3">{tile(logo("marine", 22), "#fff", "Principal : marine sur fond clair", cls="line", h=47)}{tile(logo("blanc", 22), M, "Inversé : blanc sur marine", "#fff", h=47)}{tile(logo("noir", 22), "#fff", "Noir : impression une couleur, tampon, fax", cls="line", h=47)}</div>
<div class="g fill" style="grid-template-columns:1.25fr 1fr 1fr">
  <div class="tile line" style="background:{BC};gap:7mm">{logo("marine", 21, mono=True)}<div class="center" style="background:{M};border-radius:4mm;width:29mm;height:29mm">{logo("blanc", 21, mono=True)}</div>{logo("noir", 21, mono=True)}
    <span class="l" style="color:{G}">Monogramme : quand la place manque</span></div>
  <div><h2>Quelle version choisir ?</h2><ul class="dot"><li><b>Fond blanc ou clair</b> : version marine.</li><li><b>Fond marine, dégradé ou photo assombrie</b> : version blanche.</li>
    <li><b>Une seule encre disponible</b> : version noire.</li><li><b>Moins de 25 mm de large</b>, avatar, favicon, icône d'application : monogramme.</li></ul></div>
  <div><h2>Fichiers</h2><table><tr><td><b>SVG, PDF</b></td><td>Impression, enseigne, grand format. Agrandissables sans perte.</td></tr>
    <tr><td><b>PNG</b></td><td>Word, PowerPoint, réseaux sociaux, e-mail. Fond transparent.</td></tr></table>
    <p class="note" style="margin-top:3mm">Dossier <b>logo/</b>. Ne jamais reprendre le logo par capture d'écran.</p></div>
</div>""")

add("2 · Le logo", "Espace, taille et placement", "Le logo a besoin d'air pour rester lisible.", f"""
<div class="g g3 fill">
  <div><h2>Zone de protection</h2>
    <div class="card center" style="height:62mm"><div style="border:.3mm dashed {A};padding:7mm;position:relative">{logo("marine", 28)}
      <span class="cote" style="left:50%;top:1.6mm">x</span><span class="cote" style="left:2.6mm;top:45%">x</span><span class="cote" style="right:2.6mm;top:45%">x</span><span class="cote" style="left:50%;bottom:1.2mm">x</span></div></div>
    <p class="note" style="margin-top:3mm">Aucun texte, aucune image, aucun bord de page à moins de <b>x</b> du logo.<br><b>x = un quart de la hauteur de la pastille ronde.</b></p></div>
  <div><h2>Tailles minimales</h2>
    <div class="card" style="height:62mm;display:flex;align-items:flex-end;gap:10mm;padding:7mm">
      <div>{logo("marine", 11.1)}<div class="cap">Logo<br><b>25 mm</b> de large · 120 px</div></div>
      <div>{logo("marine", 8, mono=True)}<div class="cap">Monogramme<br><b>8 mm</b> · 16 px</div></div></div>
    <p class="note" style="margin-top:3mm">En dessous, les lettres « VRIS » se bouchent : passer au monogramme. Sur une enseigne ou un roll-up, pas de taille maximale.</p></div>
  <div><h2>Placement</h2>
    <div class="card" style="height:62mm;display:flex;gap:3.5mm;align-items:center;justify-content:center;padding:3mm">
      <div style="width:23mm;height:33mm;background:#fff;border:.25mm solid {GC};position:relative"><div class="abs" style="left:2.5mm;top:2.5mm">{logo("marine", 3.4)}</div><div class="abs lines" style="left:2.5mm;right:2.5mm;top:11mm"><i></i><i style="width:80%"></i><i style="width:60%"></i></div></div>
      <div class="center" style="width:23mm;height:33mm;background:{M};flex-direction:column">{logo("blanc", 4.6)}</div>
      <div style="width:23mm;height:33mm;background:#fff;border:.25mm solid {GC};position:relative"><div class="abs lines" style="left:3mm;right:3mm;top:6mm"><i></i><i style="width:80%"></i></div><div class="abs" style="left:3mm;bottom:3mm">{logo("marine", 3.4)}</div></div></div>
    <p class="note" style="margin-top:3mm"><b>Documents</b> : en haut à gauche. <b>Couvertures et écrans d'accueil</b> : centré ou en haut à gauche. <b>Pied de page</b> : petit, en bas à gauche. Un seul logo par page.</p></div>
</div>""")

ok, non = '<span class="tag oui">Oui</span>', '<span class="tag non">Non</span>'
def t2(inner, bg, tagh, cap, extra=""):
    return f'<div><div class="tile" style="background:{bg};min-height:54mm;{extra}">{inner}</div><div class="cap">{tagh} {cap}</div></div>'
add("2 · Le logo", "Fonds autorisés", "La règle : le logo doit toujours se détacher nettement du fond.", f"""
<div class="g g3">
  {t2(logo("marine", 19), "#fff", ok, "Blanc : le cas général.", f"border:.25mm solid {GC}")}
  {t2(logo("marine", 19), COLORS["gris_clair"], ok, "Gris clair et blanc cassé.")}
  {t2(logo("blanc", 19), M, ok, "Marine : version blanche.")}
  {t2(logo("blanc", 19), f"linear-gradient(135deg,{M} 40%,{P})", ok, "Dégradé marine vers prune : couvertures.")}
  {t2(logo("blanc", 19), A, ok, "Accent : ponctuel (bandeau, sticker), version blanche.")}
  {t2(logo("blanc", 19), f"linear-gradient(rgba(12,13,59,.78),rgba(12,13,59,.78)),url(img/photo-oui.jpg) center/cover", ok, "Photo : seulement sous un voile marine à 75 % ou plus.")}
</div>""")

def bad(inner, cap, bg="#fff", extra=""):
    return f'<div><div class="tile line" style="background:{bg};min-height:33mm;overflow:hidden;{extra}">{inner}</div><div class="cap">{non} {cap}</div></div>'
hexy = (f'<div style="display:flex;align-items:center;gap:2mm"><svg viewBox="0 0 40 44" style="height:15mm"><path d="M20 2l17 10v20L20 42 3 32V12z" fill="{M}"/>'
        f'<text x="20" y="30" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="22" fill="#fff">Y</text></svg><span class="outfit" style="font-weight:800;font-size:22pt;color:{M}">YVRIS</span></div>')
add("2 · Le logo", "À ne jamais faire", "Huit erreurs fréquentes. En cas de doute : reprendre le fichier d'origine, sans y toucher.", f"""
<div class="g g4">
  {bad(logo("marine", 13, style="transform:scaleX(1.55)"), "Étirer ou écraser.")}
  {bad(logo("marine", 15, style="transform:rotate(-14deg)"), "Incliner.")}
  {bad(recolor(logo("marine", 15), "#2B42F5"), "Changer la couleur.")}
  {bad(logo("marine", 15, style="filter:drop-shadow(1.2mm 1.4mm 1mm rgba(0,0,0,.55))"), "Ajouter ombre, contour ou effet.")}
  {bad(logo("marine", 15), "Poser sur une photo sans voile.", "url(img/photo-non.jpg) center/cover")}
  {bad(logo("marine", 15), "Fond trop proche : contraste insuffisant.", P)}
  {bad(hexy, "Utiliser le « Y » hexagonal ou tout logo recréé par IA.")}
  {bad(f'<span style="font-family:Georgia,serif;font-style:italic;font-size:26pt;color:{M}">Yvris</span>', "Réécrire le nom dans une autre police.")}
</div>
<p class="note">Le logo ne se recadre pas, ne se découpe pas (la pastille et les lettres restent ensemble, sauf monogramme), et ne sert pas de mot dans une phrase.</p>""")

# ================= 3. COULEURS =================
add("3 · Les couleurs", "Couleurs de marque", "Trois couleurs suffisent. Le marine porte la marque, le rouge attire l'œil.", f"""
<div class="g g3">{sw("marine", "Marine YVRIS", mh=64)}{sw("accent", "Rouge accent", mh=64)}{sw("prune", "Prune", mh=64)}</div>
<div class="g fill" style="grid-template-columns:1.3fr 1fr">
  <div><h2>Proportions</h2>
    <div style="display:flex;height:17mm;border-radius:2mm;overflow:hidden;border:.25mm solid {GC}">
      <div class="center" style="flex:60;background:#fff;font-weight:600">60 % blanc et neutres</div><div class="center" style="flex:30;background:{M};color:#fff;font-weight:600">30 % marine</div><div class="center" style="flex:10;background:{A};color:#fff;font-weight:600">10 %</div></div>
    <ul class="dot" style="margin-top:3mm"><li>Le <b>rouge</b> est réservé à ce qui doit être vu en premier : le bouton d'action, un mot-clé du titre, un filet. Jamais en grand aplat de fond, sauf bandeau ponctuel.</li>
      <li>Sur les couvertures, la proportion s'inverse : le marine domine.</li><li>Le <b>prune</b> n'existe qu'en fin de dégradé, jamais seul.</li></ul></div>
  <div><h2>Le dégradé</h2><div style="height:17mm;border-radius:2mm;background:linear-gradient(135deg,{M} 40%,{P})"></div>
    <p class="note" style="margin-top:3mm">Marine vers prune, à 135°, le marine occupant au moins 40 %. Réservé aux couvertures, bannières et fonds d'écran.</p>
    <p class="note" style="margin-top:2mm"><b>Impression</b> : les valeurs CMJN sont une conversion approchée. Faire valider une épreuve par l'imprimeur avant tout tirage important.</p></div>
</div>""")

bars = "".join(f'<div style="flex:1;display:flex;gap:.8mm;align-items:flex-end;height:100%"><i style="flex:1;height:{a}%;background:{COLORS["bleu"]};border-radius:.6mm .6mm 0 0"></i><i style="flex:1;height:{b}%;background:{COLORS["mauve"]};border-radius:.6mm .6mm 0 0"></i></div>' for a, b in ((45, 30), (62, 41), (55, 48), (80, 52), (72, 66), (95, 70)))
add("3 · Les couleurs", "Neutres, états et graphiques", "Les couleurs de service : elles accompagnent, elles ne signent pas.", f"""
<div><h2>Neutres</h2><div class="g" style="grid-template-columns:repeat(5,1fr);gap:3mm">{sw("blanc", "Blanc", False, mh=34)}{sw("blanc_casse", "Blanc cassé", False, mh=34)}{sw("gris_clair", "Gris clair", False, mh=34)}{sw("gris_texte", "Gris texte", False, mh=34)}{sw("encre", "Encre", False, mh=34)}</div></div>
<div class="g fill" style="grid-template-columns:1.25fr 1fr">
  <div><h2>États (logiciel, tableaux, messages)</h2><div class="g g3" style="gap:3mm">{sw("succes", "Succès", False, mh=30)}{sw("alerte", "Alerte", False, mh=30)}{sw("erreur", "Erreur", False, mh=30)}</div>
    <p class="note" style="margin-top:3mm">Le rouge <b>erreur</b> est plus sombre que le rouge accent, pour qu'un bouton d'action ne ressemble jamais à un message d'erreur. Dans le logiciel, une erreur s'accompagne toujours d'une icône ou d'un texte, jamais de la couleur seule.</p>
    <p class="note" style="margin-top:2mm"><b>Encre</b> pour le texte courant, <b>gris texte</b> pour les légendes, <b>gris clair</b> pour les filets et bordures.</p></div>
  <div><h2>Graphiques</h2><div class="g g2" style="gap:3mm">{sw("bleu", "Série 1", False, False)}{sw("mauve", "Série 2", False, False)}</div>
    <div class="card" style="margin-top:3mm;height:44mm;display:flex;gap:2.5mm;align-items:flex-end;padding:3mm 4mm">{bars}</div>
    <p class="note" style="margin-top:2mm">Bleu et mauve ne servent <b>qu'aux graphiques et tableaux de bord</b>. Ils ne colorent ni titres, ni boutons, ni fonds.</p></div>
</div>""")

PAIRS = [("Encre sur blanc", ENC, "#FFFFFF"), ("Gris texte sur blanc cassé", G, BC), ("Blanc sur marine", "#FFFFFF", M), ("Blanc sur prune", "#FFFFFF", P),
         ("Blanc sur rouge accent", "#FFFFFF", A), ("Rouge accent sur marine", A, M), ("Rouge accent sur blanc", A, "#FFFFFF"), ("Marine sur gris clair", M, GC), ("Gris texte sur marine", G, M)]
def verdict(r): return ("Tout texte", "oui") if r >= 4.5 else (("Titres, boutons, mots-clés (14 pt gras et plus)", "oui") if r >= 3 else ("À ne pas utiliser pour du texte", "non"))
rows = "".join(f'<tr><td><span class="ech" style="background:{bg};color:{fg}">Texte</span></td><td>{lab}</td><td class="num"><b>{ratio(fg, bg):.1f} : 1</b></td>'
               f'<td><span class="tag {verdict(ratio(fg, bg))[1]}">{verdict(ratio(fg, bg))[1]}</span> {verdict(ratio(fg, bg))[0]}</td></tr>' for lab, fg, bg in PAIRS)
add("3 · Les couleurs", "Lisibilité et associations", "Rapports de contraste calculés selon la norme d'accessibilité WCAG 2.", f"""
<div class="g fill" style="grid-template-columns:1.45fr 1fr">
  <div><table><tr><th>Aperçu</th><th>Association</th><th>Contraste</th><th>Usage</th></tr>{rows}</table>
    <p class="note" style="margin-top:3mm">Seuils : 4,5 : 1 pour le texte courant, 3 : 1 pour les grands titres et les boutons.</p></div>
  <div style="display:flex;flex-direction:column;gap:4mm"><h2 style="margin:0">En pratique</h2>
    <div class="card center" style="gap:5mm;padding:6mm"><span class="btn">Demander une démo</span><span class="btn ghost">Nos modules</span></div>
    <div class="card dark center" style="gap:5mm;padding:6mm"><span class="btn">Demander une démo</span><span class="btn ghost" style="color:#fff">Nos modules</span></div>
    <ul class="dot"><li>Le rouge porte des <b>mots courts et gras</b> : bouton, mot-clé d'un titre. Jamais un paragraphe.</li>
      <li>Pas de texte gris sur fond marine : utiliser le blanc.</li><li>Un seul bouton rouge par écran ou par page.</li></ul></div>
</div>""")

# ================= 4. TYPOGRAPHIE =================
add("4 · La typographie", "Deux polices", "Ce sont celles du site yvris.net. Elles sont gratuites et libres de droits.", f"""
<div class="g g2 fill">
  <div class="card" style="display:flex;flex-direction:column"><div class="kick">Titres</div>
    <div class="outfit" style="font-weight:800;font-size:60pt;line-height:1;color:{M}">Outfit</div>
    <div class="outfit" style="font-weight:800;font-size:15pt;color:{M};margin-top:3mm">ABCDEFGHIJKLMNOPQRSTUVWXYZ</div>
    <div class="outfit" style="font-weight:600;font-size:15pt;color:{M}">abcdefghijklmnopqrstuvwxyz 0123456789</div>
    <div class="outfit" style="font-weight:600;font-size:15pt;color:{M}">é è ê à ç ù œ € % & « » FCFA</div>
    <div class="outfit" style="font-weight:800;font-size:27pt;line-height:1.05;color:{M};margin-top:9mm">Gérez votre activité<br>avec <span style="color:{A}">efficacité.</span></div>
    <div class="outfit" style="font-weight:600;font-size:14pt;color:{M};margin-top:3mm">Une seule plateforme pour toute votre gestion</div>
    <p style="margin-top:auto"><b>ExtraBold (800)</b> pour les grands titres · <b>SemiBold (600)</b> pour les sous-titres, boutons et étiquettes.</p></div>
  <div class="card" style="display:flex;flex-direction:column"><div class="kick">Texte</div>
    <div style="font-weight:600;font-size:60pt;line-height:1;color:{M}">Figtree</div>
    <div style="font-weight:600;font-size:15pt;color:{M};margin-top:3mm">ABCDEFGHIJKLMNOPQRSTUVWXYZ</div>
    <div style="font-size:15pt;color:{M}">abcdefghijklmnopqrstuvwxyz 0123456789</div>
    <div style="font-size:15pt;color:{M}">é è ê à ç ù œ € % & « » FCFA</div>
    <p style="font-size:12pt;margin-top:9mm">Clients, ventes, comptabilité, ressources humaines, stock et production : vos activités sont centralisées dans un environnement unique, qui évolue avec votre entreprise.</p>
    <p style="font-size:9pt;color:{G};margin-top:3mm">Légende ou note : 17 factures en attente · données de démonstration.</p>
    <p style="margin-top:auto"><b>Regular (400)</b> pour le texte courant · <b>SemiBold (600)</b> pour les mots importants et les libellés.</p></div>
</div>
<div class="g g3"><p class="note"><b>Où les trouver</b> : dossier <b>polices/</b> et fonts.google.com (Outfit, Figtree). Licence libre SIL OFL : usage commercial, impression et web autorisés.</p>
  <p class="note"><b>Si la police n'est pas installée</b> (Word, PowerPoint, e-mail) : remplacer les deux par <b>Arial</b>. Aucune autre police.</p>
  <p class="note"><b>Le logo n'est pas une police</b> : le mot « VRIS » est un dessin. On ne le recompose jamais au clavier.</p></div>""")

SCALE = [("Surtitre", "Figtree 600, capitales espacées", "8 pt", "13 px", "couleur accent"), ("Titre 1", "Outfit 800", "26 à 44 pt", "40 à 64 px", "interligne 1,05"),
         ("Titre 2", "Outfit 600", "13 à 16 pt", "22 à 28 px", "interligne 1,2"), ("Titre 3", "Outfit 600", "10 à 11 pt", "17 à 18 px", ""),
         ("Texte courant", "Figtree 400", "10 pt", "16 px", "interligne 1,45"), ("Légende", "Figtree 400", "8 pt", "13 px", "gris texte"), ("Bouton", "Outfit 600, capitales", "9 pt", "14 px", "blanc sur accent")]
add("4 · La typographie", "Hiérarchie des textes", "Quatre niveaux, toujours dans le même ordre.", f"""
<div class="g fill" style="grid-template-columns:1.2fr 1fr">
  <div><table><tr><th>Niveau</th><th>Police</th><th>Imprimé A4</th><th>Écran</th><th>Remarque</th></tr>
    {"".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td class='num'>{c}</td><td class='num'>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in SCALE)}</table>
    <h2 style="margin-top:5mm">Règles</h2><ul class="dot"><li><b>Le mot-clé en rouge</b> : dans un grand titre, le dernier mot important passe en accent, suivi d'un point. Un seul par titre.</li>
      <li>Texte <b>aligné à gauche</b>, jamais justifié, jamais centré sur plus de trois lignes.</li><li><b>Capitales</b> réservées aux surtitres et aux boutons.</li>
      <li>Jamais de texte courant sous 8 pt à l'impression : un texte illisible n'apporte rien.</li><li>Pas d'italique décoratif, pas de souligné (sauf liens).</li></ul></div>
  <div class="card" style="padding:7mm"><div class="kick">Notre solution</div>
    <div class="outfit" style="font-weight:800;font-size:27pt;line-height:1.05;color:{M};margin-top:1.5mm">Une seule plateforme pour toute votre <span style="color:{A}">gestion.</span></div>
    <div class="outfit" style="font-weight:600;font-size:13pt;color:{M};margin-top:4mm">Activez les modules dont vous avez besoin</div>
    <p style="margin-top:2mm;font-size:10pt">Clients, ventes, comptabilité, ressources humaines, stock et production : vos activités sont centralisées dans un environnement unique, qui évolue avec votre entreprise.</p>
    <p class="cap" style="margin-top:2mm">Légende : tableau de bord du module Comptabilité, données de démonstration.</p>
    <div style="margin-top:5mm"><span class="btn">Demander une démo</span></div></div>
</div>""")

# ================= 5. ÉLÉMENTS GRAPHIQUES =================
add("5 · Les éléments graphiques", "Icônes", "Un seul style de pictogramme pour tous les supports.", f"""
<div class="g fill" style="grid-template-columns:1.5fr 1fr">
  <div><h2>Les six modules</h2><div class="g g3" style="gap:3.5mm">{"".join(f'<div class="card icorow" style="padding:3mm">{ico(k, "dark")}<b>{l}</b></div>' for k, l in ICON_LABELS)}</div>
    <h2 style="margin-top:5mm">Les quatre repères de confiance</h2><div class="g g4" style="gap:3.5mm">{"".join(f'<div class="card" style="padding:3mm;text-align:center"><div class="center" style="margin-bottom:2mm">{ico(k)}</div><b style="font-size:8.4pt">{l}</b></div>' for k, l in BADGE_LABELS)}</div>
    <h2 style="margin-top:5mm">Trois habillages</h2><div class="icorow" style="gap:6mm">{ico("stock")}<span class="note">Clair : sur fond blanc</span>{ico("stock", "dark")}<span class="note">Marine : cartes, listes</span>{ico("stock", "acc")}<span class="note">Accent : un seul, pour mettre en avant</span></div></div>
  <div><h2>Règles de dessin</h2><ul class="dot"><li>Dessin <b>au trait</b>, sans remplissage, sur une grille de 24 unités.</li><li>Épaisseur constante de <b>1,75 unité</b>, extrémités et angles arrondis.</li>
    <li>Une seule couleur par icône : marine, blanc ou accent.</li><li>Dans un carré aux coins arrondis (rayon 3 mm pour 13 mm de côté).</li></ul>
    <h2 style="margin-top:5mm">À éviter</h2><ul class="no"><li>Mélanger plusieurs familles d'icônes dans un même document.</li><li>Les icônes en couleur, en 3D ou avec dégradé.</li><li>Les émojis à la place des icônes.</li><li>Une icône sans libellé pour un module.</li></ul>
    <p class="note" style="margin-top:3mm">Fichiers SVG dans <b>gabarits/icones/</b>.</p></div>
</div>""")

add("5 · Les éléments graphiques", "Boutons, cartes et motif", "Les briques qui reviennent partout : site, brochure, présentation, logiciel.", f"""
<div class="g g3 fill">
  <div style="display:flex;flex-direction:column;gap:4mm"><div><h2>Boutons</h2><div class="card" style="display:flex;flex-direction:column;gap:3mm;align-items:flex-start">
      <div class="icorow"><span class="btn">Action principale</span><span class="note">Accent. Un seul par page.</span></div>
      <div class="icorow"><span class="btn navy">Action secondaire</span><span class="note">Marine.</span></div>
      <div class="icorow"><span class="btn ghost">Action discrète</span><span class="note">Contour.</span></div></div></div>
    <div><h2>Étiquettes</h2><div class="card" style="display:flex;flex-wrap:wrap;gap:2mm">{"".join(f'<span class="pill">{m}</span>' for m in MODULES)}</div></div>
    <p class="note">Angles : <b>1,6 mm</b> pour les boutons, <b>2,5 à 3 mm</b> pour les cartes et images, <b>arrondi complet</b> pour les étiquettes.</p></div>
  <div style="display:flex;flex-direction:column;gap:4mm"><div><h2>Carte</h2><div class="card">{ico("ventes", "dark")}<h3 style="margin:3mm 0 1mm">Ventes & Facturation</h3><p>Du devis au règlement, sans ressaisie.</p></div></div>
    <div><h2>Filet accent</h2><div class="card"><div style="height:.35mm;background:{M};position:relative"><div style="position:absolute;left:0;top:0;width:26mm;height:1.1mm;background:{A}"></div></div>
      <p class="note" style="margin-top:4mm">Un trait marine fin, démarré par un segment rouge épais : il souligne un en-tête ou sépare deux zones.</p></div></div>
    <p class="note">Fond des cartes : blanc cassé, bordure gris clair d'un quart de millimètre. Pas d'ombre portée à l'impression.</p></div>
  <div style="display:flex;flex-direction:column;gap:4mm"><h2 style="margin:0">Le motif « connexion »</h2>
    <div class="center" style="flex:1;min-height:55mm;border-radius:2.5mm;background:linear-gradient(135deg,{M} 40%,{P});overflow:hidden">{motif("#fff", .5, "width:92%")}</div>
    <ul class="dot"><li>Uniquement sur fond marine ou dégradé, en blanc à 10 ou 15 % d'opacité.</li><li>Débordant d'un coin, jamais centré derrière un texte.</li><li>Une seule fois par page.</li></ul></div>
</div>""")

# ================= 6. IMAGES =================
add("6 · Les images", "Photographies", "Des personnes réelles, au travail, dans un cadre sobre.", f"""
<div class="g fill" style="grid-template-columns:1.25fr 1fr 1fr">
  <div><div style="height:88mm;border-radius:2.5mm;background:url(img/photo-oui.jpg) center/cover"></div><div class="cap">{ok} Un professionnel concentré, lumière douce, tons marine et neutres.</div>
    <ul class="dot" style="margin-top:2mm"><li>Dirigeants, comptables, commerciaux, équipes : les métiers des clients, dans un contexte ouest-africain.</li><li>Tons froids et neutres, une touche de marine si possible.</li><li>Priorité aux <b>vraies photos</b> (équipe, clients, locaux à Cotonou).</li></ul></div>
  <div><div style="height:88mm;border-radius:2.5mm;background:linear-gradient(rgba(12,13,59,.78),rgba(12,13,59,.78)),url(img/photo-oui.jpg) center/cover;display:flex;align-items:flex-end;padding:6mm">
      <div class="outfit" style="color:#fff;font-weight:800;font-size:17pt;line-height:1.05">Pilotez votre entreprise<span style="color:{A}">.</span></div></div>
    <div class="cap">{ok} Voile marine à 75 % dès qu'un texte ou le logo passe sur la photo.</div>
    <ul class="dot" style="margin-top:2mm"><li>Coins arrondis de 2,5 à 3 mm.</li><li>Images générées par IA : tolérées en attendant de vraies photos, mêmes règles de style, jamais de logo ni de texte dessiné par l'IA.</li></ul></div>
  <div><div style="height:88mm;border-radius:2.5mm;background:url(img/photo-non.jpg) center/cover"></div><div class="cap">{non} L'écran montre le logiciel d'un autre éditeur.</div>
    <ul class="no" style="margin-top:2mm"><li>Toute image montrant une autre marque ou un autre logiciel.</li><li>Les clichés de banque d'images : poignées de main, sourires forcés.</li><li>Les filtres colorés, le noir et blanc, les photos floues ou pixelisées.</li><li>Les images dont les droits ne sont pas clairs.</li></ul></div>
</div>""")

add("6 · Les images", "Captures et écrans du logiciel", "Un logiciel se vend en le montrant. On montre le vrai.", f"""
<div class="g fill" style="grid-template-columns:1.35fr 1fr">
  <div class="scene center" data-name="01-ecran-logiciel" style="flex-direction:column;padding:8mm 0"><div class="laptop" style="width:140mm"><div class="scr"><img src="img/ui-compta.jpg"></div><div class="base"></div></div>
    <div class="cap" style="margin-top:4mm">Tableau de bord du module Comptabilité (capture réelle, données de démonstration)</div></div>
  <div><h2>Règles</h2><ul class="ok"><li><b>Captures réelles</b> du logiciel, à jour, en français.</li><li><b>Données de démonstration</b> : « Client Démo », montants en FCFA, aucun nom de vrai client.</li>
    <li>Présentées dans un <b>cadre d'ordinateur sobre</b>, de face, sur fond clair ou marine.</li><li>Une légende indique le module et précise « données de démonstration ».</li><li>Largeur minimale : 1 500 px pour l'impression.</li></ul>
    <h2 style="margin-top:4mm">À éviter</h2><ul class="no"><li>Les interfaces <b>inventées par IA</b> : elles montrent un produit qui n'existe pas.</li><li>Les chiffres de démonstration présentés comme des résultats réels.</li><li>Les captures inclinées, floues, ou recadrées au point d'être illisibles.</li></ul>
    <p class="note" style="margin-top:3mm"><b>À harmoniser</b> : la barre du logiciel utilise aujourd'hui un autre marine ({T["releves_existant"]["interface_barre_nav"]}). L'aligner sur le marine YVRIS fait partie de l'option « kit d'interface ». Version mobile : même règle, dès que des captures existent.</p></div>
</div>""")

# ================= 7. MISE EN PAGE =================
cols = "".join(f'<i style="flex:1;background:rgba(227,58,44,.10);border-left:.15mm solid rgba(227,58,44,.35);border-right:.15mm solid rgba(227,58,44,.35)"></i>' for _ in range(12))
add("7 · La mise en page", "Grille et composition", "Une page réussie se comprend en cinq secondes.", f"""
<div class="g fill" style="grid-template-columns:auto 1fr 1fr;gap:8mm">
  <div><h2>Grille A4</h2><div style="width:76mm;height:107.5mm;border:.25mm solid {GC};background:#fff;position:relative">
      <div class="abs" style="left:7.2mm;right:7.2mm;top:7.2mm;bottom:7.2mm;display:flex;gap:1.45mm">{cols}</div>
      <span class="cote" style="left:1mm;top:1mm">20</span><span class="cote" style="right:1mm;bottom:1mm">20</span></div>
    <p class="cap">12 colonnes, gouttière 4 mm, marges 20 mm.<br>A5 et cartes : marges 12 à 14 mm.</p></div>
  <div><h2>La formule d'une page</h2><table>
    <tr><td class="num"><b class="outfit" style="font-size:15pt;color:{A}">1</b></td><td><b>idée</b> principale, pas davantage.</td></tr>
    <tr><td class="num"><b class="outfit" style="font-size:15pt;color:{A}">1</b></td><td><b>accroche</b> lisible immédiatement (Titre 1).</td></tr>
    <tr><td class="num"><b class="outfit" style="font-size:15pt;color:{A}">1</b></td><td><b>visuel dominant</b> : capture, photo ou schéma.</td></tr>
    <tr><td class="num"><b class="outfit" style="font-size:15pt;color:{A}">3 à 6</b></td><td><b>informations secondaires</b>, en cartes ou en liste.</td></tr>
    <tr><td class="num"><b class="outfit" style="font-size:15pt;color:{A}">1</b></td><td><b>action</b> proposée : démonstration, contact, site.</td></tr></table>
    <h2 style="margin-top:5mm">Respiration</h2><ul class="dot"><li>Le vide est voulu : il met un élément en valeur. Un vide qui ne met rien en valeur est à remplir ou à supprimer.</li><li>Tout s'aligne sur la marge gauche.</li><li>Espacements par multiples de 4 mm.</li></ul></div>
  <div><h2>Exemple</h2><div class="center" style="background:{BC};border:.25mm solid {GC};border-radius:2.5mm;padding:5mm">{z(brochure_int(), .36)}</div>
    <p class="cap">Surtitre, accroche, six cartes, une capture, le logo en pied de page.</p></div>
</div>""")

# ================= 8. APPLICATIONS =================
def app(title, lead, name, scene_inner, specs):
    add("8 · Les applications", title, lead, f'<div class="g fill" style="grid-template-columns:1fr 80mm"><div class="scene" data-name="{name}">{scene_inner}</div><div>{specs}</div></div>')

app("Carte de visite", "Recto marine, verso blanc. Le rouge n'apparaît qu'en filet.", "02-carte-de-visite",
    obj(carte_recto(), 14, 14, 1, -7) + obj(carte_verso(), 88, 44, 1, 5) + obj(carte_verso("Prénom NOM", "Responsable commercial"), 16, 98, 1, -3),
    f"""<h2>Caractéristiques</h2><table><tr><td><b>Format</b></td><td>85 × 55 mm</td></tr><tr><td><b>Fond perdu</b></td><td>3 mm de chaque côté (fichier 91 × 61 mm)</td></tr>
    <tr><td><b>Marge de sécurité</b></td><td>5 mm : aucun texte au-delà</td></tr><tr><td><b>Papier conseillé</b></td><td>350 g, couché mat</td></tr><tr><td><b>Impression</b></td><td>Quadrichromie recto verso</td></tr></table>
    <h2 style="margin-top:4mm">Contenu</h2><ul class="dot"><li><b>Recto</b> : logo blanc centré, signature, filet rouge en pied.</li><li><b>Verso</b> : monogramme, prénom et nom (Outfit 600, 11,5 pt), fonction, quatre lignes de contact (Figtree 7 pt).</li><li>Pas de QR code ni de slogan supplémentaire au verso.</li></ul>
    <p class="note" style="margin-top:3mm">Fichier : <b>gabarits/carte-de-visite.pdf</b></p>""")

app("Papier à en-tête et enveloppe", "Courriers, devis, contrats : le logo en haut à gauche, les coordonnées en pied.", "03-papeterie",
    obj(entete(), 12, 8, .47, -3) + obj(enveloppe(), 70, 98, .47, 4) + obj(carte_recto(), 120, 14, .62, 9),
    f"""<h2>Papier à en-tête</h2><table><tr><td><b>Format</b></td><td>A4, 210 × 297 mm</td></tr><tr><td><b>Marges</b></td><td>20 mm ; texte à partir de 62 mm du haut</td></tr><tr><td><b>Logo</b></td><td>15 mm de haut, en haut à gauche</td></tr><tr><td><b>Texte</b></td><td>Figtree 10 pt (Arial si absente), encre</td></tr></table>
    <h2 style="margin-top:4mm">Enveloppe</h2><table><tr><td><b>Format</b></td><td>DL, 220 × 110 mm</td></tr><tr><td><b>Logo</b></td><td>11 mm de haut, en haut à gauche</td></tr></table>
    <ul class="dot" style="margin-top:3mm"><li>Le modèle Word reprend l'en-tête et le pied de page : on ne tape que le corps du courrier.</li><li>Les mentions légales (RCCM, IFU) s'ajoutent dans le pied de page.</li></ul>
    <p class="note" style="margin-top:3mm">Fichiers : <b>papier-en-tete.docx</b>, <b>papier-en-tete.pdf</b>, <b>enveloppe-DL.pdf</b></p>""")

app("Cahier, bloc-notes et stylo", "Les objets remis en formation, en démonstration ou en rendez-vous.", "04-cahier-bloc-notes",
    obj(cahier(), 12, 10, .62, -4) + obj(blocnotes(), 82, 18, .6, 3) + f'<div class="obj ns" style="left:36mm;top:144mm;transform:rotate(-3deg)">{z(stylo(), .8)}</div>',
    f"""<h2>Cahier</h2><table><tr><td><b>Format</b></td><td>A5, 148 × 210 mm</td></tr><tr><td><b>Couverture</b></td><td>Dégradé marine, logo blanc 17 mm, grand monogramme en filigrane (10 %)</td></tr><tr><td><b>Finition</b></td><td>Pelliculage mat, reliure spirale ou dos carré</td></tr></table>
    <h2 style="margin-top:4mm">Bloc-notes</h2><table><tr><td><b>Format</b></td><td>A5, 50 feuilles, 80 g</td></tr><tr><td><b>Page</b></td><td>Bandeau marine 7 mm, logo 10 mm, trame de points 5 mm</td></tr></table>
    <h2 style="margin-top:4mm">Stylo</h2><p>Corps marine, bague rouge, logo blanc en une couleur. Marquage par tampographie.</p>
    <p class="note" style="margin-top:3mm">Fichiers : <b>cahier-A5-couverture.pdf</b>, <b>bloc-notes-A5.pdf</b></p>""")

facade = (f'<div class="abs" style="left:0;right:0;top:0;height:74%;background:linear-gradient(#E9ECF2,#DDE1EA)"></div><div class="abs" style="left:0;right:0;bottom:0;height:26%;background:#C9CDD8"></div>'
          f'<div class="abs" style="left:12mm;right:12mm;top:50mm;bottom:17mm;background:#F6F7FA;border:.3mm solid #C4C8D3"></div>'
          f'<div class="abs" style="left:22mm;top:92mm;width:44mm;bottom:17mm;background:linear-gradient(160deg,#AEBBD0,#7F8FA9);border:1mm solid #2A2C3A"></div>'
          f'<div class="abs" style="left:74mm;top:92mm;width:26mm;bottom:17mm;background:linear-gradient(160deg,#B9C5D8,#8A99B2);border:1mm solid #2A2C3A"></div>'
          f'<div class="abs" style="left:108mm;top:92mm;width:44mm;bottom:17mm;background:linear-gradient(160deg,#AEBBD0,#7F8FA9);border:1mm solid #2A2C3A"></div>'
          f'<div class="obj" style="left:22mm;top:56mm">{z(enseigne_panel(), .0433)}</div>'
          f'<div class="abs center" style="left:83mm;top:108mm;width:9mm;height:9mm;border-radius:50%;background:#fff">{logo("marine", 7.4, mono=True)}</div>')
plan = (f'<div style="position:relative;height:46mm;margin:2mm 0 0 9mm">{z(enseigne_panel(), .022, "")}'
        f'<span class="cote h" style="left:0;top:20mm;width:66mm">3 000 mm</span><span class="cote v" style="left:-9mm;top:0;height:17.6mm;border-left:0;border-right:.25mm solid {A};padding:0 1.2mm 0 0">800</span>'
        f'<span class="cote" style="left:0;top:27mm;white-space:normal;width:66mm;color:{G};font-weight:400">Logo : 400 mm de haut (50 % du panneau), centré. Filet rouge : 36 mm en pied.</span></div>')
app("Enseigne", "Le logo blanc sur fond marine, centré, sans rien d'autre.", "05-enseigne", facade,
    f"""<h2>Plan coté (exemple 3 m × 0,8 m)</h2>{plan}
    <ul class="dot"><li>Les dimensions s'adaptent à la façade en gardant les <b>proportions</b> : logo à 50 % de la hauteur, marges latérales d'au moins une demi-hauteur de panneau.</li>
      <li>Aucun slogan, numéro ou adresse sur l'enseigne.</li><li>Support : panneau composite aluminium 3 mm, ou caisson lumineux à lettres blanches.</li><li>Teinte marine à faire valider sur échantillon par le fabricant.</li></ul>
    <p class="note" style="margin-top:3mm">Vitrophanie de porte : monogramme seul, 20 cm. Fichier : <b>enseigne-plan-cote.pdf</b> + logos vectoriels.</p>""")

app("Roll-up, badge et polo", "Salons, formations, démonstrations chez le client.", "06-evenementiel",
    obj(rollup(), 10, 5, .074, 0) + obj(badge(), 86, 8, .92, 4) + f'<div class="obj ns" style="left:92mm;top:86mm">{z(polo(), .58)}</div>',
    f"""<h2>Roll-up</h2><table><tr><td><b>Format</b></td><td>85 × 200 cm</td></tr><tr><td><b>Zone utile</b></td><td>Rien d'important dans les 20 cm du bas (enrouleur)</td></tr><tr><td><b>Lecture</b></td><td>Logo et accroche au-dessus de 1,20 m</td></tr></table>
    <h2 style="margin-top:4mm">Badge</h2><table><tr><td><b>Format</b></td><td>54 × 86 mm, portrait, PVC</td></tr><tr><td><b>Contenu</b></td><td>Logo, photo, nom, fonction, bandeau rouge</td></tr></table>
    <h2 style="margin-top:4mm">Polo</h2><ul class="dot"><li>Polo marine, logo blanc brodé côté cœur, 8 cm de large.</li><li>Variante : polo blanc, logo marine.</li><li>Liseré rouge discret (manches) en option. Rien dans le dos, ou le logo seul, 25 cm.</li></ul>
    <p class="note" style="margin-top:3mm">Fichiers : <b>roll-up-85x200.pdf</b>, <b>badge.pdf</b></p>""")

add("8 · Les applications", "Réseaux sociaux", "Le monogramme en avatar, le marine en fond, une seule idée par visuel.", f"""
<div class="scene fill" data-name="07-reseaux-sociaux" style="display:flex;gap:8mm;align-items:center;justify-content:center;padding:6mm">
  <div><div class="obj" style="position:static">{z(social_story(), .235)}</div></div>
  <div><div class="obj" style="position:static">{z(social_post(), .235)}</div></div>
  <div style="display:flex;flex-direction:column;gap:7mm"><div class="obj" style="position:static">{z(social_banner(), .235)}</div>
    <div style="display:flex;gap:6mm;align-items:center"><div class="obj" style="position:static"><div class="z" style="zoom:.19;border-radius:50%;overflow:hidden">{social_avatar()}</div></div>
      <div style="font-size:8.6pt;max-width:60mm"><b>YVRIS Business Cloud</b><br><span style="color:{G}">Logiciel de gestion en ligne · Cotonou</span></div></div></div>
</div>
<div class="g g4"><p class="note"><b>Story / statut</b> 1080 × 1920 px. Texte dans la zone centrale, loin des bords haut et bas.</p><p class="note"><b>Publication</b> 1080 × 1080 px. Une accroche, deux lignes de texte, un bouton.</p>
  <p class="note"><b>Bannière LinkedIn</b> 1584 × 396 px. Le tiers gauche reste vide (photo de profil).</p><p class="note"><b>Avatar</b> 640 × 640 px : monogramme blanc sur marine, pour LinkedIn, Facebook et WhatsApp Business.</p></div>""")

mail = (f'<div style="background:#fff;border:.25mm solid {GC};border-radius:2.5mm;overflow:hidden"><div style="background:{BC};border-bottom:.25mm solid {GC};padding:2.5mm 4mm;font-size:8pt;color:{G}">Nouveau message</div>'
        f'<div style="padding:5mm 6mm"><div class="lines"><i style="width:30%"></i><i></i><i style="width:85%"></i><i style="width:40%"></i></div><div style="margin-top:6mm">{email_signature(logo_src="../logo/yvris-monogramme-marine.svg")}</div></div></div>')
add("8 · Les applications", "Signature e-mail et présentation", "Les deux supports les plus utilisés au quotidien.", f"""
<div class="g fill" style="grid-template-columns:112mm 1fr">
  <div><h2>Signature e-mail</h2>{mail}
    <ul class="dot" style="margin-top:3mm"><li>Monogramme 64 px, filet rouge vertical, nom en marine.</li><li>Police Arial (les messageries n'affichent pas Outfit).</li><li>Pas d'image de bannière, pas de citation, pas de couleur supplémentaire.</li></ul>
    <p class="note" style="margin-top:2mm">Fichier : <b>signature-email.html</b> (à copier-coller dans Gmail ou Outlook).</p></div>
  <div><h2>Présentation PowerPoint (16:9)</h2>
    <div style="display:flex;gap:5mm"><div class="scene" data-name="08-presentation" style="padding:6mm;display:flex;flex-direction:column;gap:5mm;flex:none"><div class="obj" style="position:static">{z(slide_titre(), .36)}</div><div class="obj" style="position:static">{z(slide_contenu(), .36)}</div></div>
    <div><ul class="dot"><li><b>Diapositive de titre</b> : dégradé marine, logo blanc, mot-clé en rouge.</li><li><b>Diapositives de contenu</b> : fond blanc, surtitre rouge, titre marine, logo en pied.</li><li>Une idée par diapositive, six lignes de texte au maximum.</li></ul>
    <p class="note" style="margin-top:2mm">Fichier : <b>YVRIS-presentation.pptx</b></p></div></div></div>
</div>""")

add("8 · Les applications", "Brochure", "La charte appliquée à une plaquette A4.", f"""
<div class="g fill" style="grid-template-columns:1fr 78mm">
  <div class="scene" data-name="09-brochure">{obj(brochure_couv(), 14, 8, .47, -3)}{obj(brochure_int(), 86, 12, .47, 3)}</div>
  <div><h2>Principes</h2><ul class="dot"><li><b>Couverture</b> : dégradé marine, logo blanc, accroche avec mot-clé rouge, les six modules en étiquettes.</li><li><b>Pages intérieures</b> : fond blanc, surtitre rouge, cartes de modules avec icône, une vraie capture du logiciel.</li>
    <li><b>Dernière page</b> : un appel à l'action (« Demandez une démonstration »), coordonnées, QR code vers le site.</li></ul>
    <h2 style="margin-top:4mm">Fabrication</h2><table><tr><td><b>Format</b></td><td>A4 portrait, 4 ou 8 pages</td></tr><tr><td><b>Papier</b></td><td>170 g couché mat, couverture 250 g</td></tr><tr><td><b>Fichier d'envoi</b></td><td>PDF de moins de 10 Mo (WhatsApp)</td></tr></table>
    <p class="note" style="margin-top:3mm">La brochure actuelle est un PDF d'images, non modifiable. Sa refonte en version éditable suit ces deux pages modèles.</p></div>
</div>""")

# Photomontages : décors du dossier « PHOTO CAS USAGE », visuels posés par mises-en-situation/build_photos.py
def photo(name, cap, h=None):
    src = f"../mises-en-situation/photos/photo-{name}.jpg"
    img = (f'<img src="{src}" style="display:block;height:{h}mm;width:auto;border-radius:2.5mm">' if h else
           f'<img src="{src}" style="display:block;width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:2.5mm">')
    return f'<div>{img}<div class="cap">{cap}</div></div>'
add("8 · Les applications", "Aperçu en situation réelle", "Ce que donne la charte une fois imprimée, brodée ou posée.", f"""
<div class="g g3" style="gap:5mm">{photo("enseigne", "<b>Enseigne</b> : logo blanc sur panneau marine, filet rouge en pied.")}
  {photo("carte-de-visite", "<b>Carte de visite</b> : recto marine, verso blanc.")}{photo("papeterie", "<b>Cahier, bloc-notes et stylo</b>")}</div>
<div style="display:flex;gap:5mm;justify-content:space-between">{photo("polo", "<b>Polos</b> : marine ou blanc, logo côté cœur, liseré rouge discret.", 71)}
  {photo("roll-up", "<b>Roll-up</b> 85 × 200 cm", 71)}{photo("badge", "<b>Badge</b> 54 × 86 mm", 71)}{photo("brochure", "<b>Brochure</b> A4", 71)}</div>
<p class="note"><b>Photomontages indicatifs.</b> Les décors sont générés par IA ; le logo et les visuels viennent des fichiers de la charte et sont posés ensuite, comme le demande la page « Photographies ». Teintes et finitions restent à valider sur épreuve.</p>""")

add("8 · Les applications", "Aperçu en situation réelle (suite)", "Variantes et autres supports.", f"""
<div style="display:flex;gap:5mm">{photo("enseigne-claire", "<b>Enseigne sur façade claire</b> : logo marine en lettres découpées.", 72)}
  {photo("polo-2", "<b>Polos sur mannequin</b> : marine et blanc, logo côté cœur.", 72)}</div>
<div style="display:flex;gap:6mm;align-items:flex-start">{photo("badges", "<b>Badges</b> : le même gabarit pour toute l'équipe.", 56)}
  <div class="card" style="flex:1"><h2>À retenir</h2><ul class="dot"><li>L'enseigne de référence reste le <b>panneau marine à logo blanc</b>. Sur une façade claire, le logo marine est la version prévue pour les fonds blancs : variante à valider avant fabrication.</li>
    <li>Polo marine ou blanc uniquement. Le rouge reste un liseré, jamais la couleur du vêtement.</li><li>Un porte-badge plus large que 54 mm se remplit en élargissant les bandeaux, <b>sans étirer le logo</b>.</li></ul></div></div>""")

# ================= 9. RÉCAPITULATIF =================
add("9 · En pratique", "Avant de diffuser un support", "Dix vérifications, puis les fichiers à utiliser.", f"""
<div class="g fill" style="grid-template-columns:1.1fr 1fr 1fr">
  <div><h2>Liste de contrôle</h2><ul class="ok"><li>Le logo vient du dossier <b>logo/</b>, sans modification.</li><li>Sa zone de protection et sa taille minimale sont respectées.</li><li>Seules les couleurs de la charte sont utilisées.</li><li>Le rouge ne dépasse pas 10 % de la surface.</li><li>Titres en Outfit, texte en Figtree (ou Arial).</li>
    <li>Aucun texte sous 8 pt.</li><li>Les captures montrent le vrai logiciel, avec des données de démonstration.</li><li>Les photos sont libres de droits et sans autre marque.</li><li>Une seule idée et une seule action par page.</li><li>Coordonnées et orthographe vérifiées.</li></ul></div>
  <div><h2>Fichiers fournis</h2><table><tr><td><b>logo/</b></td><td>Logo et monogramme : marine, blanc, noir. SVG, PDF, PNG.</td></tr><tr><td><b>couleurs/</b></td><td>Valeurs de référence, variables pour le web, nuancier.</td></tr><tr><td><b>polices/</b></td><td>Outfit et Figtree, avec la licence.</td></tr>
    <tr><td><b>gabarits/</b></td><td>Carte, papier à en-tête, enveloppe, cahier, bloc-notes, badge, roll-up, enseigne, présentation, signature, réseaux sociaux, icônes.</td></tr><tr><td><b>mises-en-situation/</b></td><td>Les visuels de ce guide en images, et les photomontages (dossier photos/).</td></tr></table></div>
  <div style="display:flex;flex-direction:column;gap:4mm"><div><h2>Imprimeurs et prestataires</h2><ul class="dot"><li>Travailler à partir des fichiers <b>SVG ou PDF</b>.</li><li>Demander une épreuve couleur avant tirage.</li><li>En cas de doute, ce guide fait référence.</li></ul></div>
    <div class="card dark" style="margin-top:auto;background:linear-gradient(135deg,{M} 40%,{P})">{logo("blanc", 11)}<div style="margin-top:4mm">{contact_lines("#fff", "8.6pt", "1.3mm")}</div></div></div>
</div>""")

# ================= Assemblage =================
def render():
    toc, seen = [], set()
    for i, (kick, *_rest) in enumerate(PAGES):
        if kick not in seen:
            seen.add(kick); toc.append((kick, i + 3))
    toc_html = "".join(f'<tr><td class="num"><b class="outfit" style="font-size:13pt;color:{A}">{k.split(" · ")[0]}</b></td><td><b>{k.split(" · ")[1]}</b></td><td class="num" style="text-align:right;color:{G}">p. {p}</td></tr>' for k, p in toc)
    cover = (f'<section class="page cover">{motif("#fff", .14, "position:absolute;right:-40mm;bottom:-28mm;width:230mm")}{logo("blanc", 24)}'
             f'<div style="margin-top:auto"><div class="outfit" style="font-size:10pt;letter-spacing:.18em;text-transform:uppercase;opacity:.85;margin-bottom:5mm">YVRIS Business Cloud</div>'
             f'<h1>Charte<br>graphique<i>.</i></h1><div class="meta" style="margin-top:8mm">Guide d\'utilisation de l\'identité visuelle · {VERSION}</div></div></section>')
    sommaire = f"""<div class="g fill" style="grid-template-columns:1fr 1.25fr;gap:10mm">
      <div><h2>Sommaire</h2><table>{toc_html}</table></div>
      <div style="display:flex;flex-direction:column;gap:4mm"><div class="g g2" style="gap:4mm"><div class="card"><h2>À quoi sert ce guide</h2><p>À ce que YVRIS ait le même visage partout : site, brochure, carte de visite, enseigne, réseaux sociaux, logiciel. Il fixe les règles et fournit les fichiers.</p></div>
        <div class="card"><h2>Pour qui</h2><p>L'équipe YVRIS, les graphistes, imprimeurs, agences et développeurs qui produisent un support pour la marque.</p></div></div>
      <div class="card dark" style="flex:1"><h2>Les cinq règles d'or</h2><table style="color:#fff">
        <tr><td class="num"><b class="outfit" style="font-size:14pt;color:{A}">1</b></td><td>Le logo ne se modifie jamais : ni couleur, ni forme, ni effet.</td></tr>
        <tr><td class="num"><b class="outfit" style="font-size:14pt;color:{A}">2</b></td><td>Le marine et le blanc dominent. Le rouge reste rare : 10 % au plus.</td></tr>
        <tr><td class="num"><b class="outfit" style="font-size:14pt;color:{A}">3</b></td><td>Outfit pour les titres, Figtree pour le texte. Aucune autre police.</td></tr>
        <tr><td class="num"><b class="outfit" style="font-size:14pt;color:{A}">4</b></td><td>On montre le vrai logiciel, avec des données de démonstration.</td></tr>
        <tr><td class="num"><b class="outfit" style="font-size:14pt;color:{A}">5</b></td><td>Une idée, une accroche, une action par page.</td></tr></table></div></div></div>"""
    allp = [("Introduction", "Mode d'emploi", "Comment utiliser cette charte.", sommaire)] + PAGES
    out = [cover]
    for i, (kick, title, lead, body) in enumerate(allp):
        out.append(f'<section class="page"><header><div><div class="kick">{kick}</div><h1>{title}</h1></div><div class="lead">{lead}</div></header>'
                   f'<div class="body">{body}</div><footer><span>YVRIS · Charte graphique · {VERSION}</span><span>{i + 2}</span></footer></section>')
    extra = ".obj.ns>.z{box-shadow:none;filter:drop-shadow(0 1.5mm 2.5mm rgba(12,13,59,.28))} .card.dark td{border-color:rgba(255,255,255,.18)}"
    return head("YVRIS — Charte graphique", extra=extra) + "".join(out) + "</body></html>"

async def main():
    html_path = GUIDE / "charte-graphique.html"
    html_path.write_text(render(), encoding="utf-8")
    pdf_path = GUIDE / "YVRIS-charte-graphique.pdf"
    scenes_dir = ROOT / "mises-en-situation"
    async with async_playwright() as p:
        try: b = await p.chromium.launch(channel="chrome")
        except Exception: b = await p.chromium.launch(channel="msedge")
        ctx = await b.new_context(viewport={"width": 1123, "height": 794}, device_scale_factor=2.5)
        pg = await ctx.new_page()
        await pg.goto(html_path.as_uri()); await pg.evaluate("document.fonts.ready")
        over = await pg.evaluate("""() => [...document.querySelectorAll('.page')].map((p, i) => {
            const b = p.querySelector('.body'); const f = p.querySelector('footer');
            const pr = p.getBoundingClientRect();
            let worst = 0;
            if (b) for (const el of b.querySelectorAll('*')) { if (el.closest('.scene') || el.closest('.tile')) continue;
                const r = el.getBoundingClientRect(); if (r.height && r.bottom > (f ? f.getBoundingClientRect().top : pr.bottom) + 1) worst = Math.max(worst, r.bottom - f.getBoundingClientRect().top); }
            return [i + 1, Math.round(worst)]; }).filter(x => x[1] > 0)""")
        print("pages:", len(PAGES) + 2, "| débordements (page, px):", over or "aucun")
        await pg.pdf(path=str(pdf_path), width="297mm", height="210mm", print_background=True, prefer_css_page_size=True)
        for el in await pg.query_selector_all(".scene[data-name]"):
            name = await el.get_attribute("data-name")
            await el.screenshot(path=str(scenes_dir / f"{name}.png"))
        await b.close()
    print("ok", pdf_path.name, round(os.path.getsize(pdf_path) / 1e6, 2), "Mo | scènes:", sorted(f.name for f in scenes_dir.glob("*.png")))
asyncio.run(main())
