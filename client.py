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

def GestionRequetteLecture(requette):

    if(requette=="") :
        requette = input("Saisie de la requette : ")

    # Utilisation d'une expression régulière pour extraire les parties de l'entrée
    match = re.match(r"(\w+)://(\d+\.\d+\.\d+\.\d+):(\d+)/(\w+)", requette)


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

        print("Json a envoyer au serveur : ", data)

        return [data, ip_address, port, protocol]
    else:
        print("L'entrée n'est pas au format attendu.")

def GestionRequetteEcriture(requette, donnee):

    if(requette=="") : 
        # Entrée
        requette = input("Saisie de la requette")

    # Utilisation d'une expression régulière pour extraire les parties de l'entrée
    match = re.match(r"(\w+)://(\d+\.\d+\.\d+\.\d+):(\d+)/(\w+)", requette)

    if match:
        # Extraction des parties de l'entrée
        protocol = match.group(1)
        ip_address = match.group(2)
        port = int(match.group(3))
        rsrc_id = match.group(4)
        
        if (donnee=="") : 
            donnee = input("Donner le json a stocker : ")


        # Création du JSON
        data = {
            "protocol": protocol,
            "operation": "POST",
            "rsrcId": rsrc_id,
            "data" : donnee
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
        print("Réponse du serveur: ", response.decode())

        return response.decode()


def lecture(requette):

    [data, ip_address, port] = GestionRequetteLecture(requette)

    #Création du socket 
    s = CreationSocket()

    # Connexion au serveur
    s.connect((ip_address, port))

    print(f"Connecté au serveur")

    message = EnvoieJson(s, data)

    # Fermeture de la connexion
    s.close()

    return message

def ecriture(requette, donnee) :

    [data, ip_address, port] = GestionRequetteEcriture(requette, donnee)

    #Création du socket 
    s = CreationSocket()

    # Connexion au serveur
    s.connect((ip_address, port))
    print(f"Connecté au serveur")

    message =EnvoieJson(s, data)

    # Fermeture de la connexion
    s.close()

    return message 



#----------------------------------------------------------------------------------
#                         Début du programme Client 
#----------------------------------------------------------------------------------


while True:

    choix = ChoixAction()

    if (choix=='1') : 
        
        [data, ip_address, port, protocol] = GestionRequetteLecture("")

        #Création du socket 
        s = CreationSocket()

        # Connexion au serveur
        s.connect((ip_address, port))

        print(f"Connecté au serveur")

        reponse1 = EnvoieJson(s, data)

        if (protocol == "wrdo"):

            while(1):
                
                # Attente de la réponse du serveur
                response = s.recv(4096) 
                print(reponse) 
        
        else : 
            # Fermeture de la connexion
            s.close()

    elif (choix=='2'):

        [data, ip_address, port] = GestionRequetteEcriture("","")

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


 
