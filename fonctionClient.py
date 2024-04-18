from saisie import *
from connexion import *
import threading
import time

def lecture(requette_valide):
    code_value = ""
    reception = "Erreur"
    if not requette_valide:
        #Récupération d'une requette valide
        requette_valide = demander_requete_format()
    #Récupération des champs de la requette 

    [protocol, ip_address, port, rsrc_id] = extraire_arguments_requete(requette_valide)
    #Connexion au serveur 
    socket = connecter_socket(ip_address, port)
    #Création du json a envoyer pour la lecture 
    if socket : 
        message = creer_json_lecture(protocol, rsrc_id)
        #Envoie du message 
        envoyer_message(socket, message)
        #Reception message
        reception = recevoir_reponse(socket)
        
        code_match = re.search(r'"code"\s*:\s*"(\d+)"', reception)

        if code_match:
            code_value = code_match.group(1)

        if (protocol == "wrdo" and code_value != "404"):
            while(1):
                #Reception message 
                reception = recevoir_reponse(socket)

        #Fermeture de la connexion 
        fermer_connexion(socket) 

    return reception

def ecriture():
    #Récupération d'une requette valide
    requette_valide = demander_requete_format()
    #Récupération des champs de la requette 
    [protocol, ip_address, port, rsrc_id] = extraire_arguments_requete(requette_valide)
    #Demande un json valide
    json = demander_json2()
    #Connexion au serveur
    socket = connecter_socket(ip_address, port)
    if socket : 
        #Création du json a envoyer pour l'écriture
        message = creer_json_ecriture(protocol,rsrc_id,json)
        print (message)
        #Envoie du message 
        envoyer_message(socket, message)
        #Reception message
        reception = recevoir_reponse(socket)
        #Fermeture de la connexion 
        fermer_connexion(socket)


def lectureIHM(requette_valide, fonctionAffichage):
    reception = "Problème de connexion"
    try :
        [protocol, ip_address, port, rsrc_id] = extraire_arguments_requete(requette_valide)
        # Connexion au serveur 
        socket = connecter_socket(ip_address, port)
    except Exception as e:
        return ["Requette non valide", None]

    # Création du json à envoyer pour la lecture 
    if socket : 
        message = creer_json_lecture(protocol, rsrc_id)
        # Envoie du message 
        envoyer_message(socket, message)
        # Réception message
        reception = recevoir_reponse(socket)

        if (protocol == "wrdo"):
            # Lancement d'un thread pour écouter en continu les réponses du serveur
            listener_thread = threading.Thread(target=receive_continuously, args=(socket,fonctionAffichage))
            listener_thread.start()
        else:
            # Fermer la connexion si le protocole est "rdo"
            fermer_connexion(socket)
            
    return [reception,socket]


def receive_continuously(socket, fonctionAffichage):
    while(1):
        message = recevoir_reponse(socket)
        if message:
                fonctionAffichage(message)
        else:
            # La connexion avec le serveur est fermée
            break

def ecritureIHM(requette_valide, donnee):
    reception = "Problème de connexion"
    try :
        [protocol, ip_address, port, rsrc_id] = extraire_arguments_requete(requette_valide)
        # Connexion au serveur 
        socket = connecter_socket(ip_address, port)
    except Exception as e:
        return "Requette non valide"

    if socket : 
        #Création du json a envoyer pour l'écriture
        message = creer_json_ecriture(protocol,rsrc_id,donnee)
        #Envoie du message 
        envoyer_message(socket, message)
        #Reception message
        reception = recevoir_reponse(socket)
        #Fermeture de la connexion 
        fermer_connexion(socket)
        
    return reception

