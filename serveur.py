import socket
import sys
import json
from gestionjson import *
import os
import threading
import time
from fonctionClient import lecture
import re
from fonctionServeur import *

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

    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, lock,stockage,HOST,PORT))
    client_handler.start()

server_socket.close()
