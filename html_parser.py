import re

# Classe représentant un noeud HTML
class NoeudHTML:
    def __init__(self, nom, attributs=None, enfants=None, texte=''):
        self.nom = nom
        self.attributs = attributs or {}
        self.enfants = enfants or []
        self.texte = texte

    def afficher(self, niveau=0):
        indent = "  " * niveau
        attr_str = " ".join(f'{k}="{v}"' for k, v in self.attributs.items())
        print(f"{indent}<{self.nom} {attr_str}>".strip())
        for enfant in self.enfants:
            enfant.afficher(niveau + 1)

# Lire le contenu d'un fichier HTML
def lire_fichier_html(nom_fichier):
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        return fichier.read()

# Fonction pour extraire les attributs d'une balise HTML
def extraire_attributs(chaine):
    attributs = {}
    pattern = r'(\w+)(?:\s*=\s*"([^"]*)")?'
    for match in re.finditer(pattern, chaine):
        nom, valeur = match.groups()
        if valeur is None:
            valeur = nom  # Attribut booléen (ex: disabled)
        attributs[nom] = valeur
    return attributs

# Analyser les balises et leur type
def analyser_elements(html):
    pattern = r'(<!--.*?-->|<[^>]+>|[^<>]+)'
    morceaux = re.findall(pattern, html, re.DOTALL)

    elements = []
    for m in morceaux:
        m = m.strip()
        if not m:
            continue
        if m.startswith("<!--"):
            continue

        if m.startswith("</"):
            nom = m[2:-1].strip()
            elements.append({'type': 'ferme', 'nom': nom})
        elif m.startswith("<") and m.endswith("/>"):
            contenu = m[1:-2].strip()
            nom = contenu.split()[0]
            attr_texte = contenu[len(nom):].strip()
            attributs = extraire_attributs(attr_texte)
            elements.append({'type': 'auto', 'nom': nom, 'attributs': attributs})
        elif m.startswith("<"):
            contenu = m[1:-1].strip()
            nom = contenu.split()[0]
            attr_texte = contenu[len(nom):].strip()
            attributs = extraire_attributs(attr_texte)
            elements.append({'type': 'ouvre', 'nom': nom, 'attributs': attributs})
        else:
            elements.append({'type': 'texte', 'texte': m})
    return elements

# Construire l'arbre HTML avec imbrication
def construire_arbre_complet(elements):
    def helper(index):
        noeuds = []
        while index < len(elements):
            elem = elements[index]
            if elem['type'] == 'ouvre':
                nom = elem['nom']
                attributs = elem.get('attributs', {})
                index, enfants = helper(index + 1)
                noeuds.append(NoeudHTML(nom, attributs, enfants))
            elif elem['type'] == 'auto':
                nom = elem['nom']
                attributs = elem.get('attributs', {})
                noeuds.append(NoeudHTML(nom, attributs))
                index += 1
            elif elem['type'] == 'ferme':
                return index + 1, noeuds
            elif elem['type'] == 'texte':
                noeuds.append(NoeudHTML("texte", texte=elem['texte']))
                index += 1
        return index, noeuds

    _, enfants = helper(0)
    return NoeudHTML("racine", enfants=enfants)

# Programme principal
if __name__ == "__main__":
    contenu = lire_fichier_html("exemple.html")
    elements = analyser_elements(contenu)
    arbre = construire_arbre_complet(elements)
    arbre.afficher()
