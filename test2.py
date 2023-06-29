from tkinter import *
from tkinter import messagebox

def selectionner_solvant(solvant):
    messagebox.showinfo("Choix de solvant", f"Vous avez sélectionné le solvant : {solvant}")

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Boîte de dialogue")

# Fonction appelée lorsque Solvant1 est sélectionné
def selectionner_solvant1():
    selectionner_solvant("Solvant1")

# Fonction appelée lorsque Solvant2 est sélectionné
def selectionner_solvant2():
    selectionner_solvant("Solvant2")

# Fonction appelée lorsque Solvant3 est sélectionné
def selectionner_solvant3():
    selectionner_solvant("Solvant3")

# Fonction appelée lorsque Solvant4 est sélectionné
def selectionner_solvant4():
    selectionner_solvant("Solvant4")

# Création des boutons pour les solvants
bouton_solvant1 = Button(fenetre, text="Solvant1", command=selectionner_solvant1)
bouton_solvant1.pack()

bouton_solvant2 = Button(fenetre, text="Solvant2", command=selectionner_solvant2)
bouton_solvant2.pack()

bouton_solvant3 = Button(fenetre, text="Solvant3", command=selectionner_solvant3)
bouton_solvant3.pack()

bouton_solvant4 = Button(fenetre, text="Solvant4", command=selectionner_solvant4)
bouton_solvant4.pack()

# Lancement de la boucle principale
fenetre.mainloop()
