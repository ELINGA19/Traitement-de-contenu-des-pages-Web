# main_cli.py
from storage import save_data, load_data

def afficher_menu():
    print("\n--- Menu ---")
    print("1. Afficher les éléments")
    print("2. Ajouter un élément")
    print("3. Supprimer un élément")
    print("4. Sauvegarder")
    print("5. Quitter")

def afficher_elements(data):
    if not data:
        print("Aucun élément.")
    else:
        for i, item in enumerate(data, 1):
            print(f"{i}. {item}")

def ajouter_element(data):
    item = input("Entrez un nouvel élément : ")
    data.append(item)
    print("Élément ajouté.")

def supprimer_element(data):
    afficher_elements(data)
    try:
        index = int(input("Numéro de l’élément à supprimer : ")) - 1
        if 0 <= index < len(data):
            supprimé = data.pop(index)
            print(f"Élément '{supprimé}' supprimé.")
        else:
            print("Indice invalide.")
    except ValueError:
        print("Entrée non valide.")

def main():
    data = load_data()
    while True:
        afficher_menu()
        choix = input("Choix : ").strip()
        if choix == "1":
            afficher_elements(data)
        elif choix == "2":
            ajouter_element(data)
        elif choix == "3":
            supprimer_element(data)
        elif choix == "4":
            save_data(data)
            print("Données sauvegardées.")
        elif choix == "5":
            save_data(data)
            print("Sauvegarde et fermeture.")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()









