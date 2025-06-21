import re
import requests

def lire_fichier_html(nom_fichier):
    """
    Lit le contenu HTML depuis un fichier local.
    """
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("❗ Fichier introuvable.")
        return ""

def lire_html_depuis_url(url):
    """
    Télécharge le contenu HTML à partir d'une URL.
    """
    try:
        reponse = requests.get(url)
        if reponse.status_code == 200:
            return reponse.text
        else:
            print(f"❗ Erreur HTTP {reponse.status_code} lors de l'accès à l'URL.")
            return ""
    except Exception as e:
        print("❗ Exception lors du téléchargement :", e)
        return ""

def extraire_balises(html):
    """
    Extrait toutes les balises HTML du contenu.
    """
    pattern = r'<[^>]+>'
    return re.findall(pattern, html)

def construire_arborescence(html):
    """
    Construit une arborescence simple des balises HTML (indentation).
    """
    balises = extraire_balises(html)
    indentation = 0
    arborescence = []

    for balise in balises:
        if re.match(r'</', balise):  # balise fermante
            indentation -= 1
        arborescence.append("  " * indentation + balise)
        if re.match(r'<[^/!][^>]*[^/]>$', balise):  # balise ouvrante (non auto-fermante)
            indentation += 1

    return arborescence

def analyser_elements(html):
    """
    Analyse les balises HTML et retourne une liste simple.
    """
    return extraire_balises(html)
