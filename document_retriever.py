import re
from html_parser import lire_fichier_html

def extraire_balises(html):
    """
    Retourne la liste de toutes les balises (ouvrantes et fermantes) utilisées dans le fichier HTML.
    """
    pattern = r"</?([a-zA-Z0-9]+)"
    return list(set(re.findall(pattern, html)))

def afficher_arborescence(html, niveau=0):
    """
    Affiche l’arborescence des balises HTML (parent d’abord, indentée).
    """
    pattern = r"<(/?)([a-zA-Z0-9]+)(.*?)>"
    indent = "  " * niveau
    for match in re.finditer(pattern, html):
        type_balise = "Fermante" if match.group(1) == "/" else "Ouvrante"
        print(f"{indent}<{match.group(2)}> → {type_balise}")
        if type_balise == "Ouvrante":
            afficher_arborescence("", niveau + 1)

def contenu_balise(html, nom_balise):
    """
    Affiche le contenu textuel de toutes les balises de nom donné.
    """
    pattern = fr"<{nom_balise}[^>]*>(.*?)</{nom_balise}>"
    resultats = re.findall(pattern, html, re.DOTALL)
    return resultats

def compter_balises(html):
    """
    Compte les balises correctes et incorrectes.
    """
    pattern = r"</?([a-zA-Z0-9]+)[^>]*>"
    toutes_balises = re.findall(pattern, html)
    pile = []
    erreurs = 0

    for tag in re.finditer(r"</?([a-zA-Z0-9]+)[^>]*>", html):
        nom = tag.group(1)
        if not tag.group(0).startswith("</"):
            pile.append(nom)
        else:
            if pile and pile[-1] == nom:
                pile.pop()
            else:
                erreurs += 1
    erreurs += len(pile)
    correctes = len(toutes_balises) - erreurs
    return correctes, erreurs

def ligne_colonne_premiere_erreur(html):
    """
    Retourne la ligne et la colonne approximative de la première erreur.
    """
    lignes = html.split('\n')
    pile = []
    for i, ligne in enumerate(lignes):
        for tag in re.finditer(r"</?([a-zA-Z0-9]+)[^>]*>", ligne):
            nom = tag.group(1)
            if not tag.group(0).startswith("</"):
                pile.append((nom, i, tag.start()))
            else:
                if pile and pile[-1][0] == nom:
                    pile.pop()
                else:
                    return i + 1, tag.start() + 1
    if pile:
        return pile[0][1] + 1, pile[0][2] + 1
    return None, None

def portions_mal_ecrites(html):
    """
    Affiche les balises qui semblent incorrectes ou mal formées.
    """
    erreurs = []
    pattern = r"<[^>]*[^/>]$|<[^<>\s]+[^<>]*[^>]?$"
    lignes = html.split('\n')
    for i, ligne in enumerate(lignes):
        if re.search(pattern, ligne):
            erreurs.append((i + 1, ligne.strip()))
    return erreurs
