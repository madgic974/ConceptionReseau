import os
import json

DOSSIER_JSON = "DONNEES_SERVEUR"  # Nom du dossier pour stocker les fichiers JSON

# Vérifier si le dossier existe, sinon le créer
if not os.path.exists(DOSSIER_JSON):
    os.makedirs(DOSSIER_JSON)

# Fonction pour créer un fichier JSON
def creer_fichier_json(nom_fichier, donnees):
    chemin_fichier = os.path.join(DOSSIER_JSON, nom_fichier)
    with open(chemin_fichier, 'w') as f:
        json.dump(donnees, f, ensure_ascii=False)

# Fonction pour lire un fichier JSON
def lire_fichier_json(nom_fichier):
    chemin_fichier = os.path.join(DOSSIER_JSON, nom_fichier)
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as f:
            donnees = json.load(f)
        return donnees
    else:
        print(f"Le fichier {nom_fichier} n'existe pas. Création du fichier avec des données vides.")
        creer_fichier_json(nom_fichier, {})  # Créer le fichier avec un dictionnaire vide
        return {}

# Fonction pour modifier un fichier JSON
def modifier_fichier_json(nom_fichier, nouvelle_donnee):
    chemin_fichier = os.path.join(DOSSIER_JSON, nom_fichier)
    donnees = lire_fichier_json(chemin_fichier)
    donnees.update(nouvelle_donnee)
    with open(chemin_fichier, 'w') as f:
        json.dump(donnees, f, ensure_ascii=False)

# Fonction pour écraser entièrement un fichier JSON avec de nouvelles données
def ecraser_fichier_json(nom_fichier, nouvelles_donnees):
    chemin_fichier = os.path.join(DOSSIER_JSON, nom_fichier)
    with open(chemin_fichier, 'w') as f:
        json.dump(nouvelles_donnees, f, ensure_ascii=False)
