import tkinter as tk
from tkinter import ttk
import json
import client


def send_data():
    global id_write, data_write
    id_write = id_write_entry.get()
    data_write = data_write_entry.get("1.0", tk.END)  # Récupérer le texte du widget Text
    print("Identifiant de la donnée :", id_write)
    print("Données à envoyer :", data_write)

    resource_url = f"{protocol}://{ip_address}:{port}/{id_write}"

    print(resource_url)

    message = client.ecriture(resource_url, data_write)

    # Afficher le JSON formaté dans le widget de texte
    data_write_entry.delete("1.0", tk.END)  # Effacer le contenu précédent
    data_write_entry.insert(tk.END, message)



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



couleur="#438485"

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
data_write_entry = tk.Text(ecriture_frame, wrap="word", height=4, width=50)
data_write_entry.grid(row=1, column=1, padx=10, pady=5)

# Bouton pour envoyer les données
send_data_button = ttk.Button(ecriture_frame, text="Envoyer", command=send_data, style="Custom.TButton")
send_data_button.grid(row=2, column=0, columnspan=2, pady=10)

# Créer un style pour les labels avec des bords arrondis
style.configure("RoundedLabel.TLabel", background=couleur)



# Exécuter la boucle principale de l'application
root.mainloop()
