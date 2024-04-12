import socket

def connecter_socket(ip_address, port):
    try:
        # Création du socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connexion au serveur
        s.connect((ip_address, port))

        # Si la connexion réussit, renvoyer le socket
        print("Connexion au serveur réussi")
        return s
    except Exception as e:
        # En cas d'échec de la connexion, renvoyer None
        print(f"Erreur lors de la connexion au serveur : {e}")
        return None

def envoyer_message(s, message):
    try:
        # Envoi du message au serveur
        s.sendall(message.encode())
        print("Message envoyé au serveur.")
    except socket.error as e:
        print(f"Échec de l'envoi du message au serveur : {e}")

def recevoir_reponse(s):
    try:
        # Attente de la réponse du serveur
        response = s.recv(4096)  # Taille du buffer à adapter en fonction de vos besoins
        print("Réponse du serveur : ", response.decode())
        return response.decode()
    except socket.error as e:
        print(f"Échec lors de la réception de la réponse du serveur : {e}")
        return None

def fermer_connexion(s):
    try:
        s.close()
        print("Connexion fermée.")
    except socket.error as e:
        print(f"Échec lors de la fermeture de la connexion : {e}")

