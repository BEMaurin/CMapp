import tkinter as tk
from tkinter import ttk
from random import uniform

def select_molecule(event, entry_var, combo_box):
    selected_molecule = event.widget.get()
    if selected_molecule:
        entry_var.set(selected_molecule)

# Liste des molécules avec les nombres associés
molecules = [
    ("Molécule 1", uniform(0.05, 0.95)),
    ("Molécule 2", uniform(0.05, 0.95)),
    ("Molécule 3", uniform(0.05, 0.95)),
    ("Molécule 4", uniform(0.05, 0.95)),
    ("Molécule 5", uniform(0.05, 0.95)),
    ("Molécule 6", uniform(0.05, 0.95)),
    ("Molécule 7", uniform(0.05, 0.95)),
    ("Molécule 8", uniform(0.05, 0.95)),
    ("Molécule 9", uniform(0.05, 0.95)),
    ("Molécule 10", uniform(0.05, 0.95)),
    ("Molécule 11", uniform(0.05, 0.95)),
    ("Molécule 12", uniform(0.05, 0.95)),
    # Ajoutez plus de molécules ici         
]


# Création de la fenêtre principale
window = tk.Tk()
window.title("Boîte de dialogue avec champs de saisie")

# Création des champs de saisie, des étiquettes et des listes déroulantes associées
entry_vars = []
combo_boxes = []

for i, molecule in enumerate(molecules):
    entry_var = tk.StringVar()
    entry_vars.append(entry_var)

    # Calcul du numéro de canal, de la valeur et du numéro de champ
    canal_numero = i // 3 + 1
    valeur_numero = uniform(0.05, 0.95)
    champ_numero = i % 3 + 1

    # Création des étiquettes de canal, de valeur et de champ
    canal_label = ttk.Label(window, text=f"Canal {canal_numero}")
    canal_label.grid(row=i, column=0, padx=5)

    valeur_label = ttk.Label(window, text=f"Valeur {valeur_numero:.2f}")
    valeur_label.grid(row=i, column=1, padx=5)

    champ_label = ttk.Label(window, text=f"Champ {champ_numero}")
    champ_label.grid(row=i, column=2, padx=5)

    entry = ttk.Entry(window, textvariable=entry_var)
    entry.grid(row=i, column=3)

    combo_box = ttk.Combobox(window, state="readonly")
    combo_box.grid(row=i, column=4)
    combo_box.bind("<<ComboboxSelected>>", lambda event, entry_var=entry_var, combo_box=combo_box: select_molecule(event, entry_var, combo_box))
    combo_boxes.append(combo_box)

    # Filtrer les éléments des listes déroulantes en fonction du numéro de valeur avec une marge d'erreur de 10%
    filtered_molecules = [mol for mol in molecules if abs(mol[1] - valeur_numero) <= 0.1 * mol[1]]
    combo_box['values'] = [f"{mol[0]} ({mol[1]:.2f})" for mol in filtered_molecules]

# Démarrage de la boucle principale
window.mainloop()
