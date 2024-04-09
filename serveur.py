import socket
import sys
import json
from gestionjson import *
import os
import threading
import time

def is_valid_json(my_json):
    try:
        json_object = json.loads(my_json)
    except ValueError as e:
        return False
    return True

def handle_client(client_socket, client_address, lock):
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

                if protocol == "wrdo":
                    # Récupérer la valeur actuelle de la ressource
                    value = stockage.get(key)

                    # Réponse initiale au client
                    if value is not None:
                        reponse = {
                            "server": HOST,
                            "code": "200",
                            "rsrcId": key,
                            "data": value
                        }
                    else:
                        reponse = {
                            "server": HOST,
                            "code": "404",
                            "message": f"La ressource avec l'identifiant '{key}' est inconnu."
                        }

                    # Envoyer la réponse au client
                    json_data = json.dumps(reponse)
                    donnees = json_data.replace("\\", "")
                    client_socket.sendall(donnees.encode())

                    # Le client reste en attente de modification de la ressource
                    while True:
                        # Attente d'une éventuelle modification de la ressource
                        new_value = stockage.get(key)
                        if new_value != value:
                            # Si la ressource a été modifiée, envoyer la nouvelle valeur au client
                            reponse = {
                                "server": HOST,
                                "code": "210",
                                "rsrcId": key,
                                "data": new_value
                            }
                            json_data = json.dumps(reponse)
                            donnees = json_data.replace("\\", "")
                            client_socket.sendall(donnees.encode())

                            # Mettre à jour la valeur pour la prochaine comparaison
                            value = new_value

                elif protocol == "rdo":
                    # Logique actuelle pour récupérer la ressource
                    value = stockage.get(key)

                    if value is not None:
                        reponse = {
                            "server": HOST,
                            "code": "200",
                            "rsrcId": key,
                            "data": value
                        }
                    else:
                        reponse = {
                            "server": HOST,
                            "code": "404",
                            "message": f"La ressource avec l'identifiant '{key}' est inconnue."
                        }
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
                    print(key)
                    value = data
                    print("valeur ", value)
                    with lock:
                        print("Bloque")
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
                                "message": "Ressource modifiée"
                            }
                        print("Libre")
                else:
                    reponse = {
                        "server": HOST,
                        "code": "400",
                        "message": "Requête erronée : le corps de la requête est incorrect."
                    }
            else:
                print("Opération non supportée:", operation)

            ecraser_fichier_json(HOST.replace('.', '-') + '-' + str(PORT) + '.json', stockage)

            json_data = json.dumps(reponse)
            donnees = json_data.replace("\\" , "")
            client_socket.sendall(donnees.encode())

        except json.JSONDecodeError as e:
            print("Erreur lors du décodage du JSON:", e)
            response = "Erreur lors du décodage du JSON."
            client_socket.sendall(response.encode())
            break

    client_socket.close()
    print(f"Connexion avec le client {client_address} fermée")

HOST = sys.argv[1]
PORT = int(sys.argv[2])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
lock = threading.Lock()

print(f"En attente de connexion sur le port {PORT}...")
fichier = HOST.replace('.', '-') + '-' + str(PORT) + '.json'
stockage = lire_fichier_json(fichier)
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connexion établie avec le client {client_address}")

    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, lock))
    client_handler.start()

server_socket.close()
