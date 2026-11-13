# Scènes des photomontages. Coordonnées en pixels de l'image d'origine (dossier « PHOTO CAS USAGE »).
# scene(nom, image, recadrage (x, y, largeur, hauteur), calques)

scene("photo-enseigne", "Enseigne YVRIS sur façade moderne-1.png", (0, 0, 1536, 1024), [
    art(enseigne_panel(600, 200), [[98, 373], [1394, 14], [1396, 596], [93, 742]], LIGHT),
])

scene("photo-roll-up", "Kakemono YVRIS dans un lobby moderne.png", (0, 0, 1024, 1536), [
    art(rollup(), [[221, 70], [794, 83], [796, 1366], [220, 1388]], LIGHT),
])

scene("photo-carte-de-visite", "Cartes de visite YVRIS modernes.png", (0, 0, 1536, 1024), [
    art(carte_recto(), [[398, 157], [1186, -6], [1383, 350], [612, 535]], LIGHT),
    art(carte_verso("Prénom NOM", "Responsable commercial"), [[225, 348], [1095, 492], [1012, 992], [88, 850]]),
])

scene("photo-badge", "Badges YVRIS aux accents tricolores.png", (525, 205, 485, 819), [
    art(badge(), [[590, 443], [933, 443], [933, 965], [590, 965]], "", "border-radius:4mm;overflow:hidden"),
])

scene("photo-papeterie", "Set de papeterie YVRIS sur bureau en bois.png", (0, 0, 1536, 1024), [
    art(cahier(), [[70, 232], [548, 120], [838, 688], [268, 880]], LIGHT, "border-radius:7mm;overflow:hidden"),
    art(blocnotes(), [[677, 130], [1106, 50], [1479, 563], [935, 712]]),
    patch([[1102, 756], [1237, 717], [1254, 775], [1119, 813]], "#27325a", 5),
    art(logo_px("blanc", 44), [[1124, 758], [1220, 730], [1232, 772], [1137, 800]]),
])

scene("photo-brochure", "Brochure corporative YVRIS moderne.png", (0, 0, 640, 1024), [
    art(brochure_couv(), [[28, 62], [594, 15], [594, 1000], [25, 985]], LIGHT),
])

scene("photo-polo", "Présentation professionnelle des polos YVRIS-2 (1).png", (0, 0, 1030, 684), [
    patch(box(326, 182, 108, 50), "#16224c", 5),
    art(logo_px("blanc", 38), box(336, 188, 86, 38)),
    patch(box(814, 191, 105, 49), "#edeff9", 5),
    art(logo_px("marine", 38), box(822, 197, 86, 38)),
    # étiquettes de col
    patch(box(266, 64, 40, 18), "#12172a", 1.5), art(logo_px("blanc", 11), box(273, 68, 25, 11)),
    patch(box(750, 66, 40, 18), "#f4f5fa", 1.5), art(logo_px("marine", 11), box(757, 70, 25, 11)),
])

scene("photo-polo-2", "Polos YVRIS _ Élégance corporate moderne.png", (0, 0, 1035, 700), [
    patch(box(382, 215, 96, 48), "#151b36", 5),
    art(logo_px("blanc", 36), box(389, 221, 81, 36)),
    patch(box(841, 210, 104, 50), "#e6e4f4", 5),
    art(logo_px("marine", 36), box(848, 217, 81, 36)),
])

# Enseigne sur fond clair : logo marine (version autorisée sur fond blanc).
scene("photo-enseigne-claire", "Façade moderne avec enseigne YVRIS-2.png", (0, 0, 1672, 941), [
    patch(box(585, 245, 600, 330), "#cbcbcd", 9),
    art(logo_px("marine", 250), box(600, 283, 563, 250)),
])

def badge_large(nom, role):
    """Le badge de la charte, élargi sans déformation pour un porte-badge plus large (60 mm)."""
    inner = badge(nom, role).replace(f"linear-gradient(135deg,{M} 40%,{P})", M)
    return (f'<div style="width:60.4mm;height:86mm;position:relative;background:#fff;overflow:hidden;border-radius:2.5mm">'
            f'<div class="abs" style="left:0;right:0;top:0;height:24mm;background:{M}"></div>'
            f'<div class="abs" style="left:0;right:0;bottom:0;height:9mm;background:{A}"></div>'
            f'<div class="abs" style="left:3.2mm;top:0">{inner}</div></div>')

scene("photo-badges", "Badges YVRIS aux couleurs corporatives.png", (180, 140, 1180, 550), [
    art(badge_large("Prénom NOM", "Responsable commercial"), box(270, 282, 251, 358)),
    art(badge_large("Prénom NOM", "Fonction"), box(641, 280, 250, 360)),
    art(badge_large("Prénom NOM", "Consultant"), box(1013, 282, 258, 358)),
])
