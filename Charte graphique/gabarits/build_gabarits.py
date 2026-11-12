"""Génère le pack de fichiers YVRIS : logos PNG/PDF, gabarits imprimables, visuels réseaux, Word, PowerPoint.
Usage : python build_gabarits.py"""
import sys, asyncio, pathlib, shutil
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "guide"))
from lib import *
from playwright.async_api import async_playwright

LOGO = ROOT / "logo"
TMP = HERE / "_tmp.html"
RESET = "@page{margin:0} html,body{margin:0;padding:0;background:transparent} body{font-size:10pt}"

def doc(inner, extra=""):
    return head("YVRIS", css_rel="../guide/charte.css", fonts_rel="../polices/polices.css", extra=RESET + extra) + inner + "</body></html>"

async def to_pdf(pg, inner, w, h, path, extra=""):
    # La feuille de style du guide impose un format paysage : on redéfinit ici le format exact de chaque gabarit.
    TMP.write_text(doc(inner, extra + f"@page{{size:{w}mm {h}mm;margin:0}}"), encoding="utf-8")
    await pg.goto(TMP.as_uri()); await pg.evaluate("document.fonts.ready")
    await pg.pdf(path=str(path), width=f"{w}mm", height=f"{h}mm", print_background=True, prefer_css_page_size=True)
    print("  pdf", path.relative_to(ROOT), f"{w}×{h} mm")

async def to_png(browser, inner, w, h, path, transparent=False):
    ctx = await browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
    pg = await ctx.new_page()
    TMP.write_text(doc(inner), encoding="utf-8")
    await pg.goto(TMP.as_uri()); await pg.evaluate("document.fonts.ready")
    await pg.screenshot(path=str(path), omit_background=transparent, clip={"x": 0, "y": 0, "width": w, "height": h})
    await ctx.close()
    print("  png", path.relative_to(ROOT), f"{w}×{h} px")

def bleed(card_html, bg, extra_html=""):
    """Carte 85×55 centrée dans une page 91×61 (3 mm de fond perdu)."""
    return (f'<div style="width:91mm;height:61mm;position:relative;overflow:hidden;background:{bg}">{extra_html}'
            f'<div style="position:absolute;left:3mm;top:3mm">{card_html.replace("border-radius:1mm", "border-radius:0")}</div></div>')

async def main():
    for d in ("png", "pdf"): (LOGO / d).mkdir(exist_ok=True)
    for d in ("icones", "reseaux-sociaux"): (HERE / d).mkdir(exist_ok=True)

    async with async_playwright() as p:
        try: b = await p.chromium.launch(channel="chrome")
        except Exception: b = await p.chromium.launch(channel="msedge")
        pg = await b.new_page()

        print("Logos")
        for variant in ("marine", "blanc", "noir"):
            for mono, name, wpx, hpx, wmm, hmm in ((False, "logo", 2000, 887, 200, 88.75), (True, "monogramme", 1024, 1024, 100, 100)):
                svg = logo(variant, 100, mono=mono, unit="%", style="width:100%")
                await to_png(b, f'<div style="width:{wpx}px;height:{hpx}px">{svg}</div>', wpx, hpx, LOGO / "png" / f"yvris-{name}-{variant}.png", transparent=True)
                await to_pdf(pg, f'<div style="width:{wmm}mm;height:{hmm}mm">{svg}</div>', wmm, hmm, LOGO / "pdf" / f"yvris-{name}-{variant}.pdf")

        print("Papeterie")
        grad = f"linear-gradient(135deg,{M} 40%,{P})"
        recto = bleed(carte_recto(), grad, f'<div style="position:absolute;left:0;right:0;bottom:0;height:4.4mm;background:{A};z-index:2"></div>')
        verso = bleed(carte_verso(), "#fff", f'<div style="position:absolute;left:0;top:0;bottom:0;width:4.4mm;background:{A};z-index:2"></div>')
        await to_pdf(pg, f'<div style="page-break-after:always">{recto}</div>{verso}', 91, 61, HERE / "carte-de-visite.pdf")
        await to_pdf(pg, entete(body=False), 210, 297, HERE / "papier-en-tete.pdf")
        await to_pdf(pg, enveloppe(), 220, 110, HERE / "enveloppe-DL.pdf")
        await to_pdf(pg, cahier().replace("border-radius:1.5mm", "border-radius:0"), 148, 210, HERE / "cahier-A5-couverture.pdf", ".a5p{border-radius:0}")
        await to_pdf(pg, blocnotes(), 148, 210, HERE / "bloc-notes-A5.pdf", ".a5p{border-radius:0}")
        await to_pdf(pg, badge(), 54, 86, HERE / "badge.pdf", ".badge{border-radius:0}")

        print("Grand format")
        await to_pdf(pg, rollup(), 850, 2000, HERE / "roll-up-85x200.pdf")
        await to_pdf(pg, f'<div style="zoom:.1">{enseigne_panel()}</div>', 300, 80, HERE / "enseigne-3000x800-echelle-1-10.pdf")

        print("Réseaux sociaux")
        RS = HERE / "reseaux-sociaux"
        await to_png(b, social_avatar(), 640, 640, RS / "avatar-640.png")
        await to_png(b, social_banner(), 1584, 396, RS / "banniere-linkedin-1584x396.png")
        await to_png(b, social_post(), 1080, 1080, RS / "publication-1080.png")
        await to_png(b, social_story(), 1080, 1920, RS / "story-1080x1920.png")

        print("Présentation : fond de la diapositive de titre")
        bg = (f'<div style="width:1920px;height:1080px;position:relative;overflow:hidden;background:{grad}">'
              f'{motif("#fff", .13, "position:absolute;right:-230px;bottom:-170px;width:1290px")}<div style="position:absolute;left:136px;top:113px">{logo("blanc", 91, unit="px")}</div></div>')
        await to_png(b, bg, 1920, 1080, HERE / "_fond-titre.png")
        await b.close()
    TMP.unlink(missing_ok=True)

    print("Icônes")
    for k in ICONS:
        (HERE / "icones" / f"yvris-icone-{k}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="96" height="96" fill="none" stroke="{M}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>', encoding="utf-8")
    print("  svg", len(ICONS), "icônes")

    print("Couleurs")
    css = "/* Couleurs et polices YVRIS — généré depuis tokens.json */\n:root {\n" + "".join(f"  --yvris-{k.replace('_', '-')}: {v};\n" for k, v in COLORS.items())
    css += f"  --yvris-degrade: linear-gradient(135deg, {M} 40%, {P});\n  --yvris-police-titres: 'Outfit', Arial, sans-serif;\n  --yvris-police-texte: 'Figtree', Arial, sans-serif;\n}}\n"
    (ROOT / "couleurs" / "yvris-couleurs.css").write_text(css, encoding="utf-8")
    import pymupdf
    g = pymupdf.open(GUIDE / "YVRIS-charte-graphique.pdf"); n = pymupdf.open()
    n.insert_pdf(g, from_page=8, to_page=10); n.save(ROOT / "couleurs" / "yvris-nuancier.pdf")
    print("  css + nuancier.pdf (3 pages)")

    print("Signature e-mail")
    shutil.copy(LOGO / "png" / "yvris-monogramme-marine.png", HERE / "yvris-monogramme-marine.png")
    (HERE / "signature-email.html").write_text(
        '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Signature e-mail YVRIS</title></head><body style="margin:24px;font-family:Arial,sans-serif">'
        '<p style="color:#4A4A5E;font-size:13px">Remplacez « Prénom NOM » et « Fonction », puis sélectionnez le bloc ci-dessous, copiez-le et collez-le dans les réglages de signature de Gmail ou Outlook.</p><hr style="border:0;border-top:1px solid #E7E7EA;margin:16px 0">'
        + email_signature() + "</body></html>", encoding="utf-8")

    word(); powerpoint()
    (HERE / "_fond-titre.png").unlink(missing_ok=True)
    print("Terminé.")

def word():
    from docx import Document
    from docx.shared import Mm, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    d = Document(); s = d.sections[0]
    s.page_width, s.page_height = Mm(210), Mm(297)
    s.left_margin = s.right_margin = Mm(20); s.top_margin = Mm(50); s.bottom_margin = Mm(28)
    s.header_distance, s.footer_distance = Mm(14), Mm(10)
    st = d.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(10); st.font.color.rgb = RGBColor(*rgb(COLORS["encre"]))
    st.paragraph_format.space_after = Pt(8); st.paragraph_format.line_spacing = 1.3
    def border(par, color, sz, side="bottom"):
        pPr = par._p.get_or_add_pPr(); bd = OxmlElement("w:pBdr"); e = OxmlElement(f"w:{side}")
        for k, v in (("val", "single"), ("sz", str(sz)), ("space", "6"), ("color", color.lstrip("#"))): e.set(qn(f"w:{k}"), v)
        bd.append(e); pPr.append(bd)
    t = s.header.add_table(1, 2, Mm(170)); t.autofit = False
    c1, c2 = t.rows[0].cells
    c1.paragraphs[0].add_run().add_picture(str(LOGO / "png" / "yvris-logo-marine.png"), height=Mm(15))
    pr = c2.paragraphs[0]; pr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = pr.add_run("YVRIS Business Cloud\n"); r.bold = True; r.font.size = Pt(8); r.font.color.rgb = RGBColor(*rgb(M))
    r = pr.add_run(f'{C["ville"]}\n{C["telephone"]}'); r.font.size = Pt(8); r.font.color.rgb = RGBColor(*rgb(COLORS["gris_texte"]))
    hp = s.header.paragraphs[0]; hp.paragraph_format.space_after = Pt(0)
    line = s.header.add_paragraph(); border(line, M, 6); line.paragraph_format.space_after = Pt(0)
    fp = s.footer.paragraphs[0]; border(fp, COLORS["gris_clair"], 4, "top")
    r = fp.add_run(C["site"]); r.bold = True; r.font.size = Pt(7.5); r.font.color.rgb = RGBColor(*rgb(M))
    r = fp.add_run(f'  ·  {C["email"]}  ·  {C["telephone"]}        '); r.font.size = Pt(7.5); r.font.color.rgb = RGBColor(*rgb(COLORS["gris_texte"]))
    r = fp.add_run(SIGN); r.bold = True; r.font.size = Pt(7.5); r.font.color.rgb = RGBColor(*rgb(A))
    for txt in ("Cotonou, le …", "", "Objet : …", "", "Madame, Monsieur,", "Saisissez ici le corps de votre courrier. L'en-tête et le pied de page se répètent automatiquement sur chaque page.", "Cordialement,", "", "Prénom NOM\nFonction"):
        d.add_paragraph(txt)
    d.save(HERE / "papier-en-tete.docx"); print("Word\n  docx gabarits/papier-en-tete.docx")

def powerpoint():
    from pptx import Presentation
    from pptx.util import Mm, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    pr = Presentation(); pr.slide_width, pr.slide_height = Mm(338.67), Mm(190.5)
    blank = pr.slide_layouts[6]
    import pymupdf
    def icon_png(k):
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="240" height="240" fill="none" stroke="#FFFFFF" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'
        f = HERE / f"_ico-{k}.png"; pymupdf.open(stream=svg.encode(), filetype="svg")[0].get_pixmap(alpha=True, dpi=288).save(f); return f
    col = lambda h: RGBColor(*rgb(h))
    def text(sl, x, y, w, h, runs, size, bold=False, color=M, font="Outfit", spacing=None):
        tb = sl.shapes.add_textbox(Mm(x), Mm(y), Mm(w), Mm(h)); tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        par = tf.paragraphs[0]
        if spacing: par.line_spacing = spacing
        for t, c in (runs if isinstance(runs, list) else [(runs, color)]):
            parts = t.split("\n")
            for i, part in enumerate(parts):
                if part:
                    r = par.add_run(); r.text = part; r.font.size = Pt(size); r.font.bold = bold; r.font.name = font; r.font.color.rgb = col(c)
                if i < len(parts) - 1: par.add_line_break()
        return tb
    def rect(sl, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
        sh = sl.shapes.add_shape(shape, Mm(x), Mm(y), Mm(w), Mm(h)); sh.fill.solid(); sh.fill.fore_color.rgb = col(fill); sh.shadow.inherit = False
        if line: sh.line.color.rgb = col(line); sh.line.width = Pt(.75)
        else: sh.line.fill.background()
        return sh
    def footer(sl, n):
        rect(sl, 24, 172, 290.67, .3, COLORS["gris_clair"])
        sl.shapes.add_picture(str(LOGO / "png" / "yvris-logo-marine.png"), Mm(24), Mm(176), height=Mm(8))
        text(sl, 290, 177, 24.67, 6, str(n), 10, color=COLORS["gris_texte"], font="Figtree")

    # 1. Titre
    s1 = pr.slides.add_slide(blank); s1.shapes.add_picture(str(HERE / "_fond-titre.png"), 0, 0, width=pr.slide_width, height=pr.slide_height)
    text(s1, 24, 66, 250, 60, [("Titre de la\n", "#FFFFFF"), ("présentation.", A)], 54, True, spacing=.92)
    text(s1, 24, 132, 250, 12, "Sous-titre · date · intervenant", 20, color="#FFFFFF", font="Figtree")
    text(s1, 24, 171, 120, 8, C["site"], 12, color="#FFFFFF", font="Figtree")
    # 2. Contenu en trois cartes
    s2 = pr.slides.add_slide(blank)
    text(s2, 24, 16, 200, 6, "SECTION", 11, True, A, "Figtree")
    text(s2, 24, 24, 290, 18, "Titre de la diapositive", 34, True)
    for i, lab in enumerate(MODULES[:3]):
        x = 24 + i * 100.2
        c = rect(s2, x, 56, 90.3, 100, COLORS["blanc_casse"], COLORS["gris_clair"], MSO_SHAPE.ROUNDED_RECTANGLE); c.adjustments[0] = .04
        b = rect(s2, x + 8, 64, 16, 16, M, shape=MSO_SHAPE.ROUNDED_RECTANGLE); b.adjustments[0] = .2
        f = icon_png(ICON_LABELS[i][0]); s2.shapes.add_picture(str(f), Mm(x + 11.5), Mm(67.5), height=Mm(9)); f.unlink()
        text(s2, x + 8, 86, 75, 10, lab, 18, True)
        text(s2, x + 8, 98, 75, 50, "Une phrase courte qui explique le bénéfice pour le client.", 13, color=COLORS["encre"], font="Figtree")
    footer(s2, 2)
    # 3. Texte + visuel
    s3 = pr.slides.add_slide(blank)
    text(s3, 24, 16, 200, 6, "SECTION", 11, True, A, "Figtree")
    text(s3, 24, 24, 150, 40, [("Une idée par\n", M), ("diapositive.", A)], 34, True, spacing=.95)
    text(s3, 24, 70, 135, 80, "Six lignes de texte au maximum. Le texte est en Figtree, aligné à gauche, couleur encre.", 16, color=COLORS["encre"], font="Figtree")
    ph = rect(s3, 176, 24, 138.67, 132, COLORS["gris_clair"], shape=MSO_SHAPE.ROUNDED_RECTANGLE); ph.adjustments[0] = .03
    text(s3, 186, 84, 118, 12, "Capture du logiciel ou photo", 13, color=COLORS["gris_texte"], font="Figtree")
    footer(s3, 3)
    # 4. Conclusion
    s4 = pr.slides.add_slide(blank); s4.shapes.add_picture(str(HERE / "_fond-titre.png"), 0, 0, width=pr.slide_width, height=pr.slide_height)
    text(s4, 24, 66, 290, 40, [("Parlons de votre\n", "#FFFFFF"), ("activité.", A)], 54, True, spacing=.92)
    text(s4, 24, 132, 290, 24, f'{C["telephone"]}  ·  {C["email"]}  ·  {C["site"]}', 18, color="#FFFFFF", font="Figtree")
    pr.save(HERE / "YVRIS-presentation.pptx"); print("PowerPoint\n  pptx gabarits/YVRIS-presentation.pptx (4 diapositives)")

asyncio.run(main())
