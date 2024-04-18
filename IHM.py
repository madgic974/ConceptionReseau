import tkinter as tk
from tkinter import ttk
from fonctionClient import * 
from connexion import *
import socket
import json 

#--------------------------------------------------Variables-----------------------------------------------------

#------------------Variable config-------------------------
ip_address = ""
port = ""
protocol = ""

#------------------Variable lecture-------------------------

socket_wrdo = None

#------------------Variable ecriture-------------------------

count = 0
liste_id = []

# Liste pour stocker les champs de saisie JSON
json_entries = []
etat_wrdo = False

#-----------------Variable console--------------------------

etat_console = False

#--------------------------------------------------Fonctions------------------------------------------------------

#-----------------------Fonction gestion configuration--------------------------------------

def is_valid_ip(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        return False

def is_valid_port(port):
    try:
        port = int(port)
        return 0 <= port <= 65535
    except ValueError:
        return False

# Fonction pour mettre à jour l'affichage de la configuration actuelle
def update_current_configuration():
    current_ip_value.config(text=ip_address)
    current_port_value.config(text=port)
    current_protocol_value.config(text=protocol)


#Récupère les valeurs saisie de la configuration, regarde si ils sont valide et si oui les met a jour
def update_ip_port_proto():
    global ip_address, port, protocol

    # Récupérer les valeurs saisies par l'utilisateur
    ip_address_temp = ip_entry.get()
    port_temp = port_entry.get()
    protocol_temp = protocol_combobox.get()

    # Vérifier que l'adresse IP est valide
    if not is_valid_ip(ip_address_temp):
        log_message("Adresse IP invalide. Veuillez saisir une adresse IP valide.")
        return

    # Vérifier que le port est un entier compris entre 0 et 65535
    if not is_valid_port(port_temp):
        log_message("Port invalide. Veuillez saisir un port valide (compris entre 0 et 65535).")
        return

    # Vérifier que le protocole est soit "wrdo" soit "rdo"
    if protocol_temp not in ["wrdo", "rdo"]:
        log_message("Protocole invalide. Veuillez choisir entre 'wrdo' et 'rdo'.")
        return

    # Si toutes les vérifications sont passées, mettre à jour la configuration
    ip_address = ip_address_temp
    port = port_temp
    protocol = protocol_temp

    log_message("Adresse IP mise à jour : " + ip_address)
    log_message("Port mis à jour : " + port)
    log_message("Protocol mis à jour : " + protocol)
    update_current_configuration()  # Mettre à jour la configuration actuelle


#--------------------------------------Fonction gestion lecture----------------------------------

def CloseConnexion(socket, button):
    button.grid_forget()
    fermer_connexion(socket)
    log_message("Connexion fermée")

def envoie_lecture():
    id = id_entry.get()
    resource_url = f"{protocol}://{ip_address}:{port}/{id}"

    log_message("Requête envoyée au serveur : " + resource_url)

    [message,socket] = lectureIHM(resource_url, update_textbox)

    if(protocol == "wrdo"):
        socket_wrdo = socket
        button = ttk.Button(consultation_frame, text="Fermer connexion", command=lambda: CloseConnexion(socket_wrdo, button))
        button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

    log_message("Résultat de la lecture : " + message)

    # Afficher le JSON formaté dans le widget de texte
    resultat_text.delete("1.0", tk.END)  # Effacer le contenu précédent
    resultat_text.insert(tk.END, message)


def update_textbox(message):
    resultat_text.delete("1.0", tk.END)  # Effacer le contenu précédent
    resultat_text.insert(tk.END, "Mise à jour serveur : ")
    resultat_text.insert(tk.END, message)
    log_message(message)
    

#--------------------------------------Fonction gestion ecriture--------------------------------------

#Ajuste la taille de la fenêtre de saisie des json 
def adjust_data_write_height():
    if not json_entries:  # Si aucune frame de saisie JSON n'est présente
        data_write_entry.config(height=7)  # Augmenter la hauteur de data_write_entry
    else:
        data_write_entry.config(height=4)  # Réinitialiser la hauteur de data_write_entry

#Ajoute un champs de saisie json parent 
def add_json_entry():

    global count, liste_id
    # Ajouter un nouveau champ de saisie pour une paire clé-valeur JSON
    id = count 
    count=count+1
    liste_enfant = []

    entry_frame = ttk.Frame(data_write_entry)
    entry_frame.pack(fill="x", padx=5, pady=2)

    key_entry = ttk.Entry(entry_frame)
    key_entry.pack(side="left", padx=2, pady=2)

    value_entry = ttk.Entry(entry_frame)
    value_entry.pack(side="left", padx=2, pady=2)

    add_button = ttk.Button(entry_frame, text="Ajouter", command=lambda: add_nested_json_entry(entry_frame, liste_enfant))
    add_button.pack(side="left", padx=2, pady=2)

    delete_button = ttk.Button(entry_frame, text="Supprimer", command=lambda frame=entry_frame: delete_json_entry(id))
    delete_button.pack(side="left", padx=2, pady=2)

    json_entries.append((entry_frame, key_entry, value_entry, id, liste_enfant))

    liste_id.append(id)

#Ajoute un champs de saisie enfant 
def add_nested_json_entry(parent_frame, liste_enfant):

    global count, liste_id
    id = count 
    count=count+1
    liste_enfant2 = []

    # Ajouter un nouveau champ de saisie JSON dans le cadre parent
    entry_frame = ttk.Frame(parent_frame)
    entry_frame.pack(fill="x", padx=5, pady=2)

    key_entry = ttk.Entry(entry_frame)
    key_entry.pack(side="left", padx=2, pady=2)

    value_entry = ttk.Entry(entry_frame)
    value_entry.pack(side="left", padx=2, pady=2)

    add_button = ttk.Button(entry_frame, text="Ajouter", command=lambda: add_nested_json_entry(entry_frame, liste_enfant2))
    add_button.pack(side="left", padx=2, pady=2)

    delete_button = ttk.Button(entry_frame, text="Supprimer", command=lambda frame=entry_frame: delete_json_entry(id))
    delete_button.pack(side="left", padx=2, pady=2)

    liste_enfant.append(id)

    liste_id.append(id)

    # Ajouter le dictionnaire JSON unique à la liste json_entries
    json_entries.append((entry_frame, key_entry, value_entry, id, liste_enfant2))

#Supprime un champs de saisie et ses enfant de facon récursive
def delete_json_entry(id):
   
    global liste_id
    # Parcourir la liste des entrées JSON et supprimer celle qui correspond au frame donné
    for entry_tuple in json_entries[:]:
        if entry_tuple[3] == id:
            if entry_tuple[4]: 
                print(entry_tuple[4])
                for id_enfant in entry_tuple[4]:
                    print("id enfant : ",id_enfant)
                    delete_json_entry(id_enfant)
            
            entry_tuple[0].destroy()  # Supprimer le cadre parent
            json_entries.remove(entry_tuple)  # Retirer l'entrée de la liste
            liste_id.remove(id)
            if id in entry_tuple[4] :
                entry_tuple[4].remove(id)
    
    adjust_data_write_height()

#Crée le json a partir de la frame si on ne le rentre pas à la main
def buildJson():

    global protocol,ip_address,port, id_write_entry
    id_write = id_write_entry.get()
    json_data = {}
    processed_ids = []  # Liste pour suivre les identifiants déjà traités
    for entry_tuple in json_entries[:]:
        if entry_tuple[3] not in processed_ids:
            if entry_tuple[4]:
                nested_json = {}
                for nested_id in entry_tuple[4]:
                    json_temp = buildJson2(nested_id, processed_ids)
                    nested_json.update(json_temp)
                    processed_ids.append(nested_id)
                json_data[entry_tuple[1].get()] = nested_json
            else:
                json_data[entry_tuple[1].get()] = entry_tuple[2].get()
            processed_ids.append(entry_tuple[3])  # Ajouter l'identifiant traité à la liste

    return json.dumps(json_data)

def buildJson2(id, processed_ids):
    json_data = {}
    for entry_tuple in json_entries[:]:
        if entry_tuple[3] == id:
            if entry_tuple[4]:
                nested_json = {}
                for nested_id in entry_tuple[4]:
                    if nested_id not in processed_ids:
                        nested_json.update(buildJson2(nested_id, processed_ids))
                        processed_ids.append(nested_id)
                json_data[entry_tuple[1].get()] = nested_json
            else:
                json_data[entry_tuple[1].get()] = entry_tuple[2].get()
    return json_data

#Choisie la facon de constuire le json et envoie la requette 
def ConstruireJSON():
    global protocol,ip_address,port, id_write_entry,data_write_entry
    id_write = id_write_entry.get()
    if not json_entries : 
        json = data_write_entry.get("1.0", tk.END)
    else : 
        json = buildJson()

    resource_url = f"{protocol}://{ip_address}:{port}/{id_write}"

    log_message("Requette : "+ resource_url)
    log_message("Json envoyé : "+ json)

    message = ecritureIHM(resource_url, json)

    log_message("Réponse du serveur  : "+ message)

#---------------------Fonction console--------------------------------------

# Ajouter une fonction pour écrire dans la console
def log_message(message):
    console_text.insert(tk.END, message + "\n")
    console_text.see(tk.END)

def view_console():
    global etat_console
    if(etat_console):
        hide_console()
        clear_console_button.grid_forget()  # Masquer le bouton pour effacer la console
        etat_console = False
    else:
        show_console()
        clear_console_button.grid(row=4, column=0, pady=10)  # Afficher le bouton pour effacer la console
        etat_console = True

def show_console():
    global etat_console
    console_text.grid(row=0, column=1, columnspan=2, rowspan=4, padx=10, pady=10, sticky="nsew")

def hide_console():
    console_text.grid_forget()

def clear_console():
    console_text.delete('1.0', tk.END)


#------------------------------------------------------------------------------------------------------------------

#Couleur de l'interface 
couleur="#2B4F60"

# Créer une instance de la fenêtre principale
root = tk.Tk()
root.title("Client")
root.configure(bg=couleur)

# Utilisation d'un thème stylisé
style = ttk.Style()
style.configure("Custom.TLabelframe", background=couleur, bordercolor="black")
style.configure("Custom.TLabelframe.Label", borderwidth=1, relief="solid", padding=5, foreground="black", background=couleur)
# Créer un style pour les labels avec des bords arrondis
style.configure("RoundedLabel.TLabel", background=couleur)

#-------------------------------------------Frame pour la configuration----------------------------------------

# Cadre pour les widgets IP, Port et bouton de mise à jour
ip_frame = ttk.LabelFrame(root, text="Configuration IP/Port/Protocole", style="Custom.TLabelframe")
ip_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Créer les champs de saisie pour l'adresse IP, le port et le protocol 
ip_label = ttk.Label(ip_frame, text="Adresse IP:", style="RoundedLabel.TLabel")
ip_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
ip_entry = ttk.Entry(ip_frame)
ip_entry.grid(row=0, column=1, padx=10, pady=5)

port_label = ttk.Label(ip_frame, text="Port:", style="RoundedLabel.TLabel")
port_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
port_entry = ttk.Entry(ip_frame)
port_entry.grid(row=0, column=3, padx=10, pady=5)

# Sélecteur pour le protocole
protocol_label = ttk.Label(ip_frame, text="Protocole:", style="RoundedLabel.TLabel")
protocol_label.grid(row=0, column=4, padx=10, pady=5, sticky="w")
protocol_combobox = ttk.Combobox(ip_frame, values=["rdo", "wrdo"], style="Custom.TCombobox")
protocol_combobox.grid(row=0, column=5, padx=10, pady=5, sticky="w")

# Cadre pour afficher la configuration actuelle
current_config_frame = ttk.LabelFrame(ip_frame, text="Configuration actuelle", style="Custom.TLabelframe")
current_config_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky="ew")

# Créer des étiquettes pour afficher la configuration actuelle dans le cadre
current_ip_label = ttk.Label(current_config_frame, text="Adresse IP actuelle:", style="RoundedLabel.TLabel")
current_ip_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

current_ip_value = ttk.Label(current_config_frame, text="", style="RoundedLabel.TLabel")
current_ip_value.grid(row=2, column=1, padx=10, pady=5, sticky="w")

current_port_label = ttk.Label(current_config_frame, text="Port actuel:", style="RoundedLabel.TLabel")
current_port_label.grid(row=2, column=2, padx=10, pady=5, sticky="e")

current_port_value = ttk.Label(current_config_frame, text="", style="RoundedLabel.TLabel")
current_port_value.grid(row=2, column=3, padx=10, pady=5, sticky="w")

current_protocol_label = ttk.Label(current_config_frame, text="Protocole actuel:", style="RoundedLabel.TLabel")
current_protocol_label.grid(row=2, column=4, padx=10, pady=5, sticky="e")

current_protocol_value = ttk.Label(current_config_frame, text="", style="RoundedLabel.TLabel")
current_protocol_value.grid(row=2, column=5, padx=10, pady=5, sticky="w")

# Bouton pour mettre à jour les variables
update_button = ttk.Button(ip_frame, text="Mettre à jour", command=update_ip_port_proto, style="Custom.TButton")
update_button.grid(row=1, column=2, columnspan=2, pady=10)

#----------------------------------------Frame pour la lecture-----------------------------------------------

# Cadre pour les widgets de consultation
consultation_frame = ttk.LabelFrame(root, text="Consultation d’une ressource", style="Custom.TLabelframe")
consultation_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

id_label = ttk.Label(consultation_frame, text="Identifiant de la donnée:", style="RoundedLabel.TLabel")
id_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
id_entry = ttk.Entry(consultation_frame)
id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Bouton pour mettre à jour les variables
send_button = ttk.Button(consultation_frame, text="Consulter", command=envoie_lecture, style="Custom.TButton")
send_button.grid(row=1, column=1, columnspan=2, pady=10)

# Créer un widget Text pour afficher le JSON
resultat_text = tk.Text(consultation_frame, wrap="word", height=8, width=50)
resultat_text.grid(row=0, column=2, columnspan=2, padx=10, pady=5)

#---------------------------------------Frame pour l'écriture------------------------------------------------

# Cadre pour les widgets d'écriture
ecriture_frame = ttk.LabelFrame(root, text="Ajout d’une ressource", style="Custom.TLabelframe")
ecriture_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

# Créer les champs de saisie pour l'identifiant de la donnée et le JSON à envoyer
id_write_label = ttk.Label(ecriture_frame, text="Identifiant de la donnée:", style="RoundedLabel.TLabel")
id_write_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
id_write_entry = ttk.Entry(ecriture_frame)
id_write_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

data_write_label = ttk.Label(ecriture_frame, text="Données à envoyer (JSON):", style="RoundedLabel.TLabel")
data_write_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

# Créer un widget Text pour les données JSON (initialement masqué)
data_write_entry = tk.Text(ecriture_frame, wrap="word", height=16, width=50)
data_write_entry.grid(row=1, column=1, padx=10, pady=5)
data_write_entry.pack_forget()

# Bouton pour ajouter un nouveau champ JSON
add_json_button = ttk.Button(ecriture_frame, text="Ajouter un nouveau champ JSON", command=lambda: add_json_entry(), style="Custom.TButton")
add_json_button.grid(row=2, column=0, columnspan=2, pady=10)

# Bouton pour envoyer les données
send_data_button = ttk.Button(ecriture_frame, text="Envoyer", command=ConstruireJSON, style="Custom.TButton")
send_data_button.grid(row=3, column=0, columnspan=2, pady=10)

#-------------------------------------------Console et bouton associé-------------------------------------------

# Créer un widget Text pour la console
console_text = tk.Text(root, wrap="word", height=15, width=50)
console_text.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")

# Bouton pour ouvrir/fermer la console
console_button = ttk.Button(root, text="Afficher/Masquer Console", command=view_console)
console_button.grid(row=3, column=0, pady=10)

clear_console_button = ttk.Button(root, text="Effacer Console", command=clear_console)

# Exécuter la boucle principale de l'application
add_json_entry()
hide_console()
root.mainloop()