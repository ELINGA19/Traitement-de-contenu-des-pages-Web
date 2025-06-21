import os
from html_parser import lire_fichier_html, lire_html_depuis_url, extraire_balises, construire_arborescence
from tag_validator import valider_balises
from html_inspector import contenu_balise, afficher_arborescence
from content_editor import calculer_taux_erreur, corriger_automatiquement, supprimer_balise, modifier_balise, ajouter_balise

def afficher_menu():
    print("\n===== VALIDATEUR DE PAGE HTML =====")
    print("1. Afficher toutes les balises utilisées")
    print("2. Afficher l'arborescence HTML")
    print("3. Afficher le contenu d'une balise spécifique")
    print("4. Valider les balises HTML")
    print("5. Calculer le taux d’erreur des balises")
    print("6. Corriger automatiquement le HTML")
    print("7. Supprimer une balise")
    print("8. Modifier une balise")
    print("9. Ajouter une balise")
    print("10. Sauvegarder les modifications dans un nouveau fichier")
    print("0. Quitter")

def demander_source():
    choix = input("🔍 Lire depuis : [1] URL ou [2] fichier local ? ")
    if choix.strip() == "1":
        url = input("🌐 Entrez l'URL : ")
        return lire_html_depuis_url(url)
    else:
        fichier = input("📄 Entrez le nom du fichier HTML (ex: exemple.html) : ")
        return lire_fichier_html(fichier)

def main():
    html = demander_source()

    while True:
        afficher_menu()
        choix = input("👉 Choisissez une option : ")

        if choix == "1":
            print("📌 Balises utilisées :", extraire_balises(html))

        elif choix == "2":
            print("\n📂 Arborescence des balises :")
            arbre = construire_arborescence(html)
            for ligne in arbre:
                print(ligne)

        elif choix == "3":
            nom = input("🔎 Nom de la balise à inspecter : ")
            contenus = contenu_balise(html, nom)
            for i, c in enumerate(contenus):
                print(f"Contenu {i+1} : {c.strip()}")

        elif choix == "4":
            erreurs = valider_balises(html)
            if erreurs:
                print("🚫 Erreurs détectées :")
                for err in erreurs:
                    print(" -", err)
            else:
                print("✅ Aucune erreur détectée.")

        elif choix == "5":
            taux = calculer_taux_erreur(html)
            print(f"📊 Taux d’erreur des balises : {taux}%")

        elif choix == "6":
            html = corriger_automatiquement(html)
            print("✅ HTML corrigé automatiquement.")

        elif choix == "7":
            nom = input("🧽 Nom de la balise à supprimer : ")
            html = supprimer_balise(html, nom)
            print("✅ Balise supprimée.")

        elif choix == "8":
            ancien = input("🔁 Balise à remplacer : ")
            nouveau = input("👉 Remplacer par : ")
            html = modifier_balise(html, ancien, nouveau)
            print("✅ Modification effectuée.")

        elif choix == "9":
            try:
                pos = int(input("📍 Position d'insertion : "))
                code = input("🧩 Code HTML à insérer : ")
                html = ajouter_balise(html, pos, code)
                print("✅ Balise ajoutée.")
            except:
                print("❗ Position invalide.")

        elif choix == "10":
            nom_nouveau = input("💾 Nom du nouveau fichier (ex: corrige.html) : ")
            with open(nom_nouveau, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"✅ Modifications sauvegardées dans : {nom_nouveau}")

        elif choix == "0":
            print("👋 Fin du programme. Merci !")
            break

        else:
            print("❗ Choix invalide. Réessaie.")
main()
