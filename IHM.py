import tkinter as tk
from tkinter import ttk
import client
import json 

# Définition globale de children_count
children_count = 0
count = 0
liste_id = []

def update_ip_port_proto():
    global ip_address, port, protocol
    ip_address = ip_entry.get()
    port = port_entry.get()
    protocol = protocol_combobox.get()
    print("Adresse IP mise à jour :", ip_address)
    print("Port mis à jour :", port)
    print("Protocol mis à jour :", protocol)


def generation_url():
    global protocol, id, resultat_lecture
    protocol = protocol_combobox.get()
    id = id_entry.get()
    resource_url = f"{protocol}://{ip_address}:{port}/{id}"

    print("Protocole sélectionné :", protocol)
    print("Id mis à jour :", id)
    print("URL de la ressource :", resource_url)
    print("resultat de la lecture :", resultat_lecture)

    message = client.lecture(resource_url)

    # Afficher le JSON formaté dans le widget de texte
    resultat_text.delete("1.0", tk.END)  # Effacer le contenu précédent
    resultat_text.insert(tk.END, message)


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

def buildJson():

    print(liste_id)
    print(json_entries)
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

    print(json.dumps(json_data, indent=4))  # Pour afficher le JSON formaté
    resource_url = f"{protocol}://{ip_address}:{port}/{id_write}"
    message = client.ecriture(resource_url, json.dumps(json_data))
    print(message)

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

    group_var = tk.StringVar()
    group_combobox = ttk.Combobox(entry_frame, values=["Groupe 1", "Groupe 2", "Groupe 3"], textvariable=group_var, width=10)
    group_combobox.pack(side="left", padx=2, pady=2)

    add_button = ttk.Button(entry_frame, text="Ajouter", command=lambda: add_nested_json_entry(entry_frame, liste_enfant))
    add_button.pack(side="left", padx=2, pady=2)

    delete_button = ttk.Button(entry_frame, text="Supprimer", command=lambda frame=entry_frame: delete_json_entry(id))
    delete_button.pack(side="left", padx=2, pady=2)

    json_entries.append((entry_frame, key_entry, value_entry, id, liste_enfant, group_var))

    liste_id.append(id)


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

    group_var = tk.StringVar()
    group_combobox = ttk.Combobox(entry_frame, values=["Groupe 1", "Groupe 2", "Groupe 3"], textvariable=group_var, width=10)
    group_combobox.pack(side="left", padx=2, pady=2)

    add_button = ttk.Button(entry_frame, text="Ajouter", command=lambda: add_nested_json_entry(entry_frame, liste_enfant2))
    add_button.pack(side="left", padx=2, pady=2)

    delete_button = ttk.Button(entry_frame, text="Supprimer", command=lambda frame=entry_frame: delete_json_entry(id))
    delete_button.pack(side="left", padx=2, pady=2)

    liste_enfant.append(id)

    liste_id.append(id)

    # Ajouter le dictionnaire JSON unique à la liste json_entries
    json_entries.append((entry_frame, key_entry, value_entry, id, liste_enfant2, group_var))

    # Masquer le value_entry du parent
    for entry_tuple in json_entries:
        if entry_tuple[0] == parent_frame:
            entry_tuple[2].pack_forget()  # value_entry
            break


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
            print(id)
            if id in entry_tuple[4] :
                entry_tuple[4].remove(id)


couleur="#20494A"

# Créer une instance de la fenêtre principale
root = tk.Tk()
root.title("Client")

# Changer la couleur de l'arrière-plan
root.configure(bg=couleur)

# Utilisation d'un thème stylisé
style = ttk.Style()

style.configure("Custom.TLabelframe", background=couleur, bordercolor="black")
style.configure("Custom.TLabelframe.Label", borderwidth=1, relief="solid", padding=5, foreground="black", background=couleur)

# Variables pour stocker l'adresse IP, le port et le protocole
ip_address = ""
port = ""
protocol = ""
id = ""
resultat_lecture = ""

# Liste pour stocker les champs de saisie JSON
json_entries = []

# Cadre pour les widgets IP, Port et bouton de mise à jour
ip_frame = ttk.LabelFrame(root, text="Configuration IP/Port/Protocole", style="Custom.TLabelframe")
ip_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Créer les champs de saisie pour l'adresse IP, le port et le protocole
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

# Bouton pour mettre à jour les variables
update_button = ttk.Button(ip_frame, text="Mettre à jour", command=update_ip_port_proto, style="Custom.TButton")
update_button.grid(row=1, column=2, columnspan=2, pady=10)

# Cadre pour les widgets de consultation
consultation_frame = ttk.LabelFrame(root, text="Consultation d’une ressource", style="Custom.TLabelframe")
consultation_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

id_label = ttk.Label(consultation_frame, text="Identifiant de la donnée:", style="RoundedLabel.TLabel")
id_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
id_entry = ttk.Entry(consultation_frame)
id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Bouton pour mettre à jour les variables
send_button = ttk.Button(consultation_frame, text="Consulter", command=generation_url, style="Custom.TButton")
send_button.grid(row=1, column=0, columnspan=2, pady=10)

# Créer un widget Text pour afficher le JSON
resultat_text = tk.Text(consultation_frame, wrap="word", height=4, width=50)
resultat_text.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

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
data_write_entry = tk.Text(ecriture_frame, wrap="word", height=4, width=50)
data_write_entry.grid(row=1, column=1, padx=10, pady=5)
data_write_entry.pack_forget()

# Bouton pour envoyer les données
send_data_button = ttk.Button(ecriture_frame, text="Envoyer", command=buildJson, style="Custom.TButton")
send_data_button.grid(row=2, column=0, columnspan=2, pady=10)

# Bouton pour ajouter un nouveau champ JSON
add_json_button = ttk.Button(ecriture_frame, text="Ajouter un nouveau champ JSON", command=lambda: add_json_entry(), style="Custom.TButton")
add_json_button.grid(row=3, column=0, columnspan=2, pady=10)

# Ajouter une entrée JSON par défaut au démarrage de l'application
add_json_entry()

# Créer un style pour les labels avec des bords arrondis
style.configure("RoundedLabel.TLabel", background=couleur)

# Exécuter la boucle principale de l'application
root.mainloop()