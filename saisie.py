import re
import json 

#Demande à l'utilisateur de saisir une requette
def saisie_requette():

    print("Saisir la requette à envoyer au serveur :")
    requette = input("Saisie de la requette : ")

    return requette

#Verifie si la requette est au bon format 
def verifier_format_requete(requete):
    # Expression régulière pour vérifier le format de la requête
    pattern = r"(\w+)://(\d+\.\d+\.\d+\.\d+):(\d+)/(\w+)"
    
    # Tentative de correspondance avec le pattern
    match = re.match(pattern, requete)
    
    # Si la correspondance est trouvée et les groupes sont extraits
    if match:
        return True
    else:
        return False

#Demande une requette tant qu'elle n'est pas au bon format
def demander_requete_format():
    while True:
        requete = saisie_requette()
        if verifier_format_requete(requete):
            return requete
        else:
            print("La requête n'est pas au bon format. Veuillez réessayer.")

#Extrait les données d'une requette au bon format 
def extraire_arguments_requete(requete):
    # Expression régulière pour extraire les parties de la requête
    pattern = r"(\w+)://(\d+\.\d+\.\d+\.\d+):(\d+)/(\w+)"
    
    # Tentative de correspondance avec le pattern
    match = re.match(pattern, requete)
    
    # Si la correspondance est trouvée et les groupes sont extraits
    if match:
        # Extraction des parties de l'entrée
        protocol = match.group(1)
        ip_address = match.group(2)
        port = int(match.group(3))
        rsrc_id = match.group(4)
        
        return protocol, ip_address, port, rsrc_id
    else:
        return None

#Création du json a envoyer pour la lecture 
def creer_json_lecture(protocol, rsrc_id):
    # Création du JSON avec les informations fournies
    data = {
        "protocol": protocol,
        "operation": "GET",
        "rsrcId": rsrc_id
    }
    return json.dumps(data)

def demander_json():
    while True:
        json_str = input("Veuillez saisir un JSON : ")
        try:
            # Essayer de charger la chaîne JSON en un objet Python
            json_obj = json.loads(json_str)
            
            # Vérifier si l'objet est au format attendu
            if isinstance(json_obj, dict):
                # Si le JSON est un objet (dictionnaire), on le retourne
                return json.dumps(json_obj)
            else:
                print("Le JSON saisi n'est pas au bon format. Veuillez saisir un JSON valide.")
        except json.JSONDecodeError:
            print("La chaîne saisie n'est pas au format JSON. Veuillez saisir un JSON valide.")

def creer_json_ecriture(protocol, rsrc_id, donnee):
    # Création du JSON avec les données fournies
    data = {
        "protocol": protocol,
        "operation": "POST",
        "rsrcId": rsrc_id,
        "data": donnee
    }
    return json.dumps(data)
