import re
import json
import socket
import sys

def CreationSocket():
    # Création du socket TCP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s
    except (socket.error, msg):
        print('Erreur de création su socket. Error Code : ' + str(msg[0]) + 'Message ' + msg[1])
        sys.exit()

def ChoixAction():
    print("Choisir l'action a éffectuer :")
    print("Saisir 1 pour lire une valeur  :")
    print("Saisir 2 pour ajouter une valeur :")
    return(input("Saisie : "))

def GestionRequetteLecture():

    entry = input("Saisie de la requette")

    # Utilisation d'une expression régulière pour extraire les parties de l'entrée
    match = re.match(r"(\w+)://(\d+\.\d+\.\d+\.\d+):(\d+)/(\w+)", entry)

    if match:
        # Extraction des parties de l'entrée
        protocol = match.group(1)
        ip_address = match.group(2)
        port = int(match.group(3))
        rsrc_id = match.group(4)

        # Création du JSON
        data = {
            "protocol": protocol,
            "operation": "GET",
            "rsrcId": rsrc_id
        }
        return [data, ip_address, port]
    else:
        print("L'entrée n'est pas au format attendu.")

def GestionRequetteEcriture():
    # Entrée
    entry = input("Saisie de la requette")

    # Utilisation d'une expression régulière pour extraire les parties de l'entrée
    match = re.match(r"(\w+)://(\d+\.\d+\.\d+\.\d+):(\d+)/(\w+)", entry)

    if match:
        # Extraction des parties de l'entrée
        protocol = match.group(1)
        ip_address = match.group(2)
        port = int(match.group(3))
        rsrc_id = match.group(4)
        
        donnees = input("Donner le json a stocker : ")

        # Création du JSON
        data = {
            "protocol": protocol,
            "operation": "POST",
            "data" : { 
                "identifiant" : rsrc_id,
                "donnees" : donnees 
            }
        }
        return [data, ip_address, port]
    else:
        print("L'entrée n'est pas au format attendu.")

def EnvoieJson(s, data): 
    # Encodage du JSON en chaîne de caractères JSON
        json_data = json.dumps(data)

        # Envoi du JSON encodé au serveur
        try:
            s.sendall(json_data.encode())
            print("JSON envoyé au serveur.")
        except socket.error:
            print("Échec de l'envoi du JSON au serveur.")

        # Attente de la réponse du serveur
        response = s.recv(4096)  # Taille du buffer à adapter en fonction de vos besoins
        print("Réponse du serveur:", response.decode())



#----------------------------------------------------------------------------------
#                         Début du programme Client 
#----------------------------------------------------------------------------------

while True:

    choix = ChoixAction()

    if (choix=='1') : 
        
        [data, ip_address, port] = GestionRequetteLecture()

        #Création du socket 
        s = CreationSocket()

        # Connexion au serveur
        s.connect((ip_address, port))

        print(f"Connecté au serveur")

        EnvoieJson(s, data)

        # Fermeture de la connexion
        s.close()

    elif (choix=='2'):

        [data, ip_address, port] = GestionRequetteEcriture()

        #Création du socket 
        s = CreationSocket()

        # Connexion au serveur
        s.connect((ip_address, port))
        print(f"Connecté au serveur")

        EnvoieJson(s, data)

        # Fermeture de la connexion
        s.close()

    else :
        print("Erreur de saisie")
 
