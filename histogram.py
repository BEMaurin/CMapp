import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import xlsxwriter
import matplotlib.pyplot as plt
import pandas as pd


# transforme la longueur de migration en série de 1000 px
def transform_array_proportions(arr, new_length):
    old_length = len(arr)
    indices = np.linspace(0, old_length - 1, num=new_length)
    new_arr = np.interp(indices, np.arange(old_length), arr)
    return new_arr

# Facteur de réduction de l'image de la plaque CCM
reduction = 3

# Enregistre la position des spots/ligne de front/ligne de dépot sur la plaque CCM
global mouse_loc
mouse_loc = []

# Enregistre les information de positon des spot 
global rf
rf = pd.DataFrame(columns=["rf","produit"])

# Déclaration du graph intensité/distance de migration
global fig, ax
fig, ax = plt.subplots()


def main():
    # Créer une fenêtre Tkinter pour la boîte de dialogue de sélection de fichier
    Tk().withdraw()

    for i in range(2):
        # Afficher la boîte de dialogue pour sélectionner une image
        image_path = askopenfilename()

        # Vérifier si une image a été sélectionnée
        if image_path:
            # Charger l'image avec OpenCV
            image = cv2.imread(image_path)

            # Vérifier si l'image a été chargée avec succès
            if image is not None:
                # Réduire la taille de l'image pour un affichage plus petit
                resized_image = cv2.resize(image, (0, 0), fx=1/reduction, fy=1/reduction)

                # Afficher l'image réduite
                cv2.imshow('Image', resized_image)

                # Variables pour stocker les coordonnées de la souris
                mouse_x = -1
                mouse_y = -1

                # Fonction de rappel pour la détection du mouvement de la souris
                def mouse_callback(event, x, y, flags, param):
                    global mouse_x, mouse_y, mouse_loc

                    if event == cv2.EVENT_MOUSEMOVE:
                        mouse_x = x
                        mouse_y = y

                    # facteur de grossissement de l'image réduite
                    if event == cv2.EVENT_LBUTTONDOWN:
                        print('clic', x)

                        if len(mouse_loc) < 2:
                            mouse_loc.append(y*reduction)
                            print(mouse_loc)
                        else:
                            mouse_loc.append(x*reduction)
                            print(mouse_loc)

                # Définir le rappel de la souris pour la fenêtre de l'image
                cv2.setMouseCallback('Image', mouse_callback)

                # Attendre la fermeture de la fenêtre
                while True:
                    cv2.imshow('Image', resized_image)

                    # Vérifier si les coordonnées de la souris ont été mises à jour
                    if mouse_x != -1 and mouse_y != -1:
                        # Tronquer les colonnes de la matrice de pixels
                        start_col = max(0, mouse_x - 10)
                        end_col = min(resized_image.shape[1], mouse_x + 11)
                        truncated_image = resized_image[:, start_col:end_col]

                        # Afficher la matrice tronquée
                        print('Matrice tronquée :')
                        print(truncated_image)

                        # Réinitialiser les coordonnées de la souris
                        mouse_x = -1
                        mouse_y = -1

                    # Attendre l'appui sur la touche 'q' pour quitter la boucle
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                cv2.destroyAllWindows()

                # Extraire les canaux de couleur de l'image
                red_channel = image[:, :, 2]
                green_channel = image[:, :, 1]
                blue_channel = image[:, :, 0]



                # Tronquer un canal de l'image
                print(mouse_loc)
                width = 10
                red_channel=red_channel[:,mouse_loc[2]-width:mouse_loc[2]+width]
                green_channel=green_channel[:,mouse_loc[2]-width:mouse_loc[2]+width]
                blue_channel=blue_channel[:,mouse_loc[2]-width:mouse_loc[2]+width]
                

            
                # Moyenne des valeurs 
                red_channel = np.mean(red_channel, axis=1)[mouse_loc[0]:mouse_loc[1]]
                green_channel = np.mean(green_channel, axis=1)[mouse_loc[0]:mouse_loc[1]]
                blue_channel = np.mean(blue_channel, axis=1)[mouse_loc[0]:mouse_loc[1]]



                # Exemple d'utilisation
                
                red_channel = transform_array_proportions(red_channel[::-1], 1000)
                green_channel = transform_array_proportions(green_channel[::-1], 1000)
                blue_channel = transform_array_proportions(blue_channel[::-1], 1000)


                
                def onclick(event):
                    global rf
                    if event.button == 1:  # Clic gauche de la souris
                        rf = pd.concat([rf,pd.DataFrame([[np.round(event.xdata/1000,2),""]],columns=["rf","produit"])],join="inner")
                        rf.to_clipboard(index=False)
                        

                # Enregistrer les canaux de couleur dans des fichiers Excel
                
                x = np.arange(len(green_channel))
                plt.plot(x, green_channel**2)
                plt.plot(x, blue_channel**2)
                plt.plot(x, red_channel**2)






        else:
            print('Erreur lors du chargement de l\'image.')
    else:
        print('Aucune image sélectionnée.')
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.xlabel('Distance')
    plt.ylabel('Intensité')
    plt.title('Courbe des moyennes des lignes')
    plt.show()

if __name__ == '__main__':
    main()
