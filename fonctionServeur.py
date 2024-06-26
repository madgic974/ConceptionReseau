import socket
import sys
import json
from gestionjson import *
import os
import threading
import time
from fonctionClient import lecture
import re

def extract_strings_with_dollar(data):
    matches = []  # Liste pour stocker les correspondances à remplacer
    
    # Fonction récursive pour parcourir les données
    def recurse_extract(obj):
        nonlocal matches  # Déclaration pour accéder à la variable matches de l'enclosing scope
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = recurse_extract(value)
        elif isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = recurse_extract(obj[i])
        elif isinstance(obj, str):
            new_matches = re.findall(r'\$(\w+://[^"]+)', obj)
            matches.extend(new_matches)  # Ajouter les nouvelles correspondances à la liste
        return obj
    
    # Appeler la fonction récursive pour collecter les correspondances
    recurse_extract(data)

    
    # Remplacer toutes les correspondances dans les données
    for match in matches:
        try:
            change = lecture(match)
            print('--------------')
            print(change)
            print(match)
            data = data.replace(f"${match}", change,1)
            print('---------------')
        except:
            print("Impossible de récupérer les informations sur", match)
    return data

def is_valid_json(my_json):
    try:
        json_object = json.loads(my_json)
    except ValueError as e:  
        return False
    return True

def handle_client(client_socket, client_address, lock,stockage,HOST,PORT):
    while True:
        try:
            data = client_socket.recv(4096)

            if not data:
                break

            json_data = json.loads(data.decode())
            print("JSON reçu du client:", json_data)

            operation = json_data.get("operation")

            if operation == "GET":
                key = json_data.get("rsrcId")
                protocol = json_data.get("protocol")

                if (protocol == "wrdo" or protocol == "rdo"):

                    # Récupérer la valeur actuelle de la ressource
                    value = stockage.get(key)
                    print("ressource: ",value)
                    # Réponse initiale au client
                    if value is not None:
                        value2 = extract_strings_with_dollar(value)
                        reponse = {
                            "server": HOST,
                            "code": "200",
                            "rsrcId": key,
                            "data": value2
                        }
                    else:
                        reponse = {
                            "server": HOST,
                            "code": "404",
                            "message": f"La ressource avec l'identifiant '{key}' est inconnu."
                        }


                    if(protocol == "wrdo" and (value is not None) ):
                        # Envoyer la réponse au client
                        json_data = json.dumps(reponse)
                        donnees = json_data.replace("\\", "")
                        client_socket.sendall(donnees.encode())
                        # Le client reste en attente de modification de la ressource
                        while True:
                            # Attente d'une éventuelle modification de la ressource
                            new_value = stockage.get(key)
                            if new_value != value:
                                new_value2 = extract_strings_with_dollar(new_value)
                                print("ressource: ",new_value)
                                # Si la ressource a été modifiée, envoyer la nouvelle valeur au client
                                reponse = {
                                    "server": HOST,
                                    "code": "210",
                                    "rsrcId": key,
                                    "data": new_value2
                                }
                                json_data = json.dumps(reponse)
                                donnees = json_data.replace("\\", "")
                                try:
                                    client_socket.sendall(donnees.encode())
                                except Exception as e : 
                                    client_socket.close()

                                # Mettre à jour la valeur pour la prochaine comparaison
                                value = new_value

                else:
                    # Autre protocole non pris en charge
                    reponse = {
                        "server": HOST,
                        "code": "400",
                        "message": "Protocol non pris en charge."
                    }


            elif operation == "POST":
                data = json_data.get("data")
                id = json_data.get("rsrcId")
                if (is_valid_json(data) and (id != "")):
                    key = id
                    print("Ressource stockée à l'identifiant:",key)
                    value = data
                    #value = extract_strings_with_dollar(data)
                    print("valeur ", value)
                    with lock:
                        if key not in stockage:
                            stockage[key] = value
                            reponse = {
                                "server": HOST,
                                "code": "201",
                                "rsrcId": key,
                                "message": "Ressource creee"
                            }
                        else:
                            stockage[key] = value
                            reponse = {
                                "server": HOST,
                                "code": "211",
                                "rsrcId": key,
                                "message": "Ressource modifiee"
                            }
                else:
                    reponse = {
                        "server": HOST,
                        "code": "400",
                        "message": "Requete erronee : le corps de la requete est incorrect."
                    }
            else:
                print("Opération non supportée:", operation)

            ecraser_fichier_json(HOST.replace('.', '-') + '-' + str(PORT) + '.json', stockage)
            print("reponse : ",reponse)
            json_data = json.dumps(reponse)
            donnees = json_data.replace("\\" , "")
            client_socket.sendall(donnees.encode())

        except json.JSONDecodeError as e:
            print("Erreur lors du décodage du JSON:", e)
            response = "Erreur lors du décodage du JSON."
            client_socket.sendall(response.encode())
            break
    
    print("test")
    try : 
        client_socket.close()
        print(f"Connexion avec le client {client_address} fermée")
    except Exception as e :
        print("erreur",e)