from html_parser import analyser_elements

# Liste simple de balises HTML valides (à compléter selon ton besoin)
BALISES_VALIDES = [
    'html', 'head', 'body', 'div', 'p', 'a', 'span', 'b', 'i', 'u', 'h1', 'h2',
    'input', 'br', 'hr', 'img', 'title', 'script', 'style', 'ul', 'li'
]

def valider_balises(html):
    erreurs = []
    pile = []
    elements = analyser_elements(html)

    for index, elem in enumerate(elements):
        if elem['type'] == 'ouvre':
            nom = elem['nom']
            if nom not in BALISES_VALIDES:
                erreurs.append(f"Balise inconnue ou mal orthographiée : <{nom}>")
            pile.append((nom, index))
        elif elem['type'] == 'ferme':
            nom = elem['nom']
            if not pile:
                erreurs.append(f"Balise fermante sans ouverture : </{nom}>")
            else:
                dernier_nom, pos = pile[-1]
                if nom == dernier_nom:
                    pile.pop()
                else:
                    erreurs.append(f"Balise mal fermée ou chevauchée : attendait </{dernier_nom}> mais a trouvé </{nom}>")
                    pile.pop()
        elif elem['type'] == 'auto':
            nom = elem['nom']
            if nom not in BALISES_VALIDES:
                erreurs.append(f"Balise auto-fermante inconnue : <{nom}/>")

    # Vérifier les balises encore ouvertes
    for nom_ouvert, i in pile:
        erreurs.append(f"Balise non fermée : <{nom_ouvert}>")

    return erreurs