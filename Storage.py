# storage.py
import json
import os

DATA_FILE = "data.json"

def save_data(data, filename=DATA_FILE):
    """Sauvegarde les données dans un fichier JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_data(filename=DATA_FILE):
    """Charge les données depuis un fichier JSON. Retourne une liste vide si le fichier n'existe pas."""
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
