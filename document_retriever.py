import re
from html_parser import analyser_elements

def calculer_taux_erreur(html):
    """
    Calcule le pourcentage d'erreurs dans les balises HTML.
    """
    elements = analyser_elements(html)
    pile = []
    erreurs = 0

    for elem in elements:
        nom = elem['nom']
        if elem['type'] == 'ouvre':
            pile.append(nom)
        elif elem['type'] == 'ferme':
            if pile and pile[-1] == nom:
                pile.pop()
            else:
                erreurs += 1

    erreurs += len(pile)
    total = len(elements)
    taux = (erreurs / total) * 100 if total > 0 else 0
    return round(taux, 2)

def corriger_automatiquement(html):
    """
    Corrige automatiquement les balises non fermées en ajoutant les balises manquantes à la fin.
    Ne corrige pas tout, mais propose une aide basique.
    """
    elements = analyser_elements(html)
    pile = []
    for elem in elements:
        if elem['type'] == 'ouvre':
            pile.append(elem['nom'])
        elif elem['type'] == 'ferme':
            if pile and pile[-1] == elem['nom']:
                pile.pop()
            else:
                pass  # ignore pour l’instant

    for nom in reversed(pile):
        html += f"</{nom}>"
    return html

def ajouter_balise(html, position, balise):
    """
    Ajoute une balise HTML à une position spécifique dans le texte.
    Ex: position=50, balise="<b>Texte</b>"
    """
    if position < 0 or position > len(html):
        return html
    return html[:position] + balise + html[position:]

def supprimer_balise(html, nom_balise):
    """
    Supprime toutes les occurrences d’une balise (ouvrante et fermante).
    """
    pattern = fr"</?{nom_balise}[^>]*?>"
    return re.sub(pattern, '', html)

def modifier_balise(html, ancien_nom, nouveau_nom):
    """
    Remplace une balise HTML par une autre.
    """
    html = re.sub(fr"<{ancien_nom}([^>]*)>", fr"<{nouveau_nom}\1>", html)
    html = re.sub(fr"</{ancien_nom}>", fr"</{nouveau_nom}>", html)
    return html
