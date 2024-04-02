import json

# Fonction pour créer un fichier JSON
def creer_fichier_json(nom_fichier, donnees):
    with open(nom_fichier, 'w') as f:
        json.dump(donnees, f)

# Fonction pour lire un fichier JSON
def lire_fichier_json(nom_fichier):
    with open(nom_fichier, 'r') as f:
        donnees = json.load(f)
    return donnees

# Fonction pour modifier un fichier JSON
def modifier_fichier_json(nom_fichier, nouvelle_donnee):
    donnees = lire_fichier_json(nom_fichier)
    donnees.update(nouvelle_donnee)
    with open(nom_fichier, 'w') as f:
        json.dump(donnees, f)

# Exemple d'utilisation
if __name__ == "__main__":
    # Créer un fichier JSON
    creer_fichier_json("donnees.json", {"nom": "John", "age": 30})

    # Lire un fichier JSON
    donnees_lues = lire_fichier_json("donnees.json")
    print("Données lues à partir du fichier JSON:", donnees_lues)

    # Modifier un fichier JSON
    modifier_fichier_json("donnees.json", {"ville": "Paris", "pays": "France"})

    # Lire à nouveau les données après la modification
    donnees_modifiees = lire_fichier_json("donnees.json")
    print("Données modifiées:", donnees_modifiees)
