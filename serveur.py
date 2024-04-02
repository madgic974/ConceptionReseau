import socket
import sys
import json
from gestionjson import *
import os 

HOST = sys.argv[1]
PORT = int(sys.argv[2])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Permet une seule connexion à la fois

stockage = {}

print(f"En attente de connexion sur le port {PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connexion établie avec le client {client_address}")

    while True:
        stockage = lire_fichier_json("DONNEES_SERVEUR.json")
        try:
            # Réception des données du client
            data = client_socket.recv(4096)  # Taille du buffer à adapter en fonction de vos besoins

            if not data:
                break

            # Décodage des données JSON reçues
            json_data = json.loads(data.decode())
            print("JSON reçu du client:", json_data)

            # Traitement de la requête en fonction de la valeur du champ "operation"
            operation = json_data.get("operation")
            if operation == "GET":
                key = json_data.get("rsrcId")
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
                        "message": f"La ressource avec l'identifiant '{key}' n'a pas été trouvée."
                    }

            elif operation == "POST":
                if 'data' in json_data and 'identifiant' in json_data['data'] and 'donnees' in json_data['data']:
                    key = json_data['data']['identifiant']
                    value = json_data['data']['donnees']
                    if key not in stockage:
                        stockage[key] = value
                        reponse = {
                            "server": HOST,
                            "code": "201",
                            "rsrcId": key,
                            "message": "Ressource créée"
                        }
                    else:
                        stockage[key] = value
                        reponse = {
                            "server": HOST,
                            "code": "211",
                            "rsrcId": key,
                            "message": "Ressource modifiée"
                        }
                else:
                    reponse = {
                        "server": HOST,
                        "code": "400",
                        "message": "Requête erronée : le corps de la requête est incorrect."
                    }
            else:
                print("Opération non supportée:", operation)

            ecraser_fichier_json("DONNEES_SERVEUR.json", stockage)

            # Envoyer la réponse au client
            json_data = json.dumps(reponse)
            client_socket.sendall(json_data.encode())

        except json.JSONDecodeError as e:
            print("Erreur lors du décodage du JSON:", e)
            response = "Erreur lors du décodage du JSON."

            # Envoyer une réponse d'erreur au client
            client_socket.sendall(response.encode())
            break  # Sortir de la boucle pour fermer la connexion avec le client

    # Fermeture de la connexion avec le client
    client_socket.close()
    print(f"Connexion avec le client {client_address} fermée")

server_socket.close()
