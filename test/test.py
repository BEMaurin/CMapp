import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Données de la série
x = np.linspace(0, 2*np.pi, 100)
series_data = [
    {"label": "Série 1", "data": np.sin(x)},
    {"label": "Série 2", "data": np.cos(x)},
    {"label": "Série 3", "data": np.tan(x)}
]

# Fonction de mise à jour du graphique
def update_plot():
    # Récupérer les séries sélectionnées
    selected_series = []
    for i, checkbox in enumerate(checkboxes):
        if checkbox.get() == 1:
            selected_series.append(series_data[i])

    # Effacer le graphique existant
    ax.cla()

    # Afficher les séries sélectionnées sur le graphique
    for series in selected_series:
        ax.plot(x, series["data"], label=series["label"])

    ax.legend()
    canvas.draw()

# Création de la fenêtre
window = tk.Tk()
window.title("Choix des séries")

checkboxes = []

# Création des cases à cocher
for series in series_data:
    var = tk.IntVar()
    checkbox = ttk.Checkbutton(window, text=series["label"], variable=var, command=update_plot)
    checkbox.pack()
    checkboxes.append(var)

# Création de la figure et du graphique
fig = plt.Figure()
ax = fig.add_subplot(111)

# Création du canevas pour afficher le graphique
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()

# Affichage de la fenêtre
window.mainloop()
