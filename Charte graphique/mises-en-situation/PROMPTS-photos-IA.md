# Photos réalistes : trois scènes à générer

Les images de ce dossier (`01-…png` à `09-…png`) sont des mises en situation « à plat », produites à partir des vrais fichiers de la charte. Elles suffisent pour le guide.

Pour des photos **réalistes** (façade, bureau, stand), la méthode est en deux temps :

1. Vous générez la scène avec ChatGPT (ou un autre outil d'images), avec des objets **vierges**, sans texte ni logo.
2. Le vrai logo est posé ensuite sur l'image, à partir du fichier vectoriel.

**Ne demandez jamais à l'IA de dessiner le logo YVRIS.** Elle le déforme ou en invente une variante (c'est l'origine du « Y » hexagonal apparu dans une ancienne maquette).

## Consignes communes

- Format paysage 3:2, haute résolution.
- Les surfaces qui recevront le logo doivent être **planes, de face ou de trois quarts léger, bien éclairées, sans reflet ni pli**.
- Couleur des objets : bleu marine très sombre `#0C0D3B`, avec un détail rouge `#E33A2C`.
- Toujours terminer le prompt par : *no text, no logo, no letters, no watermark*.

## Scène 1 : façade avec enseigne

> Photo réaliste de la façade d'un bureau moderne en rez-de-chaussée dans une rue commerçante de Cotonou, Bénin, en journée, lumière douce. Au-dessus de la porte vitrée, un grand panneau d'enseigne rectangulaire horizontal, entièrement uni, bleu marine très sombre (#0C0D3B), totalement vierge, vu de face. Murs clairs, porte et vitrines en verre, trottoir propre. Style photographie d'architecture, netteté élevée. No text, no logo, no letters, no watermark.

Le logo blanc sera posé au centre du panneau, à 50 % de sa hauteur.

## Scène 2 : bureau avec papeterie

> Photo réaliste vue de dessus d'un bureau en bois clair, lumière naturelle douce venant de la gauche. Posés à plat : un cahier A5 à couverture unie bleu marine très sombre (#0C0D3B), deux cartes de visite (une bleu marine unie, une blanche unie), une feuille A4 blanche vierge, un stylo bleu marine avec une bague rouge, un ordinateur portable fermé gris. Tous les objets sont vierges, sans aucune inscription. Ombres douces, composition aérée. No text, no logo, no letters, no watermark.

Le logo sera posé sur le cahier, la carte marine et la feuille.

## Scène 3 : stand avec roll-up

> Photo réaliste d'un petit stand dans un salon professionnel en intérieur, éclairage homogène. À gauche, un kakémono roll-up vertical 85 × 200 cm, entièrement uni, bleu marine très sombre (#0C0D3B) en haut et blanc en bas, vierge, vu de face. À droite, une table haute blanche avec un ordinateur portable ouvert dont l'écran est éteint. Deux personnes en polo bleu marine uni discutent, vues de trois quarts dos. Arrière-plan flou. No text, no logo, no letters, no watermark.

Le visuel du roll-up (`gabarits/roll-up-85x200.pdf`) sera posé sur le kakémono, et une vraie capture du logiciel sur l'écran.

## Ensuite

Déposez les images générées dans ce dossier (`scene-1.png`, `scene-2.png`, `scene-3.png`). La pose du logo se fait par transformation de perspective sur les quatre coins de chaque surface. Elle fonctionne bien sur les surfaces planes, mal sur un tissu froissé : pour le polo, garder la mise en situation à plat.
