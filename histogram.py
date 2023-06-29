import cv2
import numpy as np
from tkinter import Tk, simpledialog
from tkinter.filedialog import askopenfilenames

import matplotlib.pyplot as plt
import pandas as pd
import pyperclip 
from tkinter import messagebox

from sklearn.neighbors import KNeighborsClassifier


def CCMclassification():
    global knn
# Charger les données depuis la DataFrame
    df = pd.DataFrame({
        'R': [96, 76, 82, 112, 109, 145, 99, 126, 40, 1, 50, 84, 160, 119, 31, 68, 71, 12, 68, 6, 1, 7, 20, 16, 12, 113],
        'G': [148, 135, 9, 21, 118, 39, 64, 30., 136, 226, 127, 174, 51, 174, 127., 128, 149, 227, 120, 203, 226, 219, 118, 217, 118, 160],
        'B': [147, 133, 48, 19, 117, 44, 97, 14, 175, 1, 161, 181, 19, 175, 185, 145, 155, 2, 201, 4, 1, 1, 169, 1, 204, 162],
        'Classes': ['MM', 'MM', '365', '365', 'MM', '365', '365', '365', 'DRAGG', '254', 'DRAGG', 'MM', '365', 'MM', 'DRAGG', 'DRAGG', 'MM', '254', 'DRAGG', '254', '254', '254', 'DRAGG', '254', 'DRAGG', 'MM']
    })

    # Séparer les données en caractéristiques (X) et étiquettes (y)
    X = df[['R', 'G', 'B']]
    y = df['Classes']

    # Créer un classifieur KNN avec k=3
    knn = KNeighborsClassifier(n_neighbors=3)

    # Entraîner le modèle
    knn.fit(X, y)

# Définir la fonction de prédiction
def predict_class(R, G, B):

    # Créer une nouvelle DataFrame avec les valeurs R, G et B
    data = pd.DataFrame({'R': [R], 'G': [G], 'B': [B]})

    # Prédire la classe avec le modèle entraîné
    prediction = knn.predict(data)

    # Renvoyer la prédiction
    return str(prediction[0])


def clipboard2df():
    """ Transforme le presse papier en dataframe

    returns:
        df (Pandas object): Dataframe
      """
    # Récupérer le contenu du presse-papiers
    texte_pressepapier = pyperclip.paste() 

    # Diviser le texte en lignes
    lignes = texte_pressepapier.split('\n')

    # Extraire le premier mot de chaque ligne
    echantillon = [ligne.split()[0] for ligne in lignes]

    # Créer un DataFrame à partir des premiers mots
    df = pd.DataFrame(echantillon, columns=['Echantillon'])

    return df


def transform_array_proportions(arr, SETTING_NEWLENGHT):   
    """ normalise la série en série de 1000 px
    Args: 
        arr (array): série de valeurs à transformer 
        SETTING_NEWLENGHT (array): longueur de la nouvelle série
    returns:
        array (array).
    """
    old_length = len(arr) # type : array (longueur de la série brut) 
    indices = np.linspace(0, old_length - 1, num=SETTING_NEWLENGHT) # type : array (longueur de la nouvelle série)
    new_arr = np.interp(indices, np.arange(old_length), arr) # type : array (données de la nouvelle série)
    return new_arr


SETTING_REDUCTION = 3 # type : int
""" Facteur de réduction de l'image de la plaque CCM """

SETTING_NEWLENGHT = 1000 # type: int
""" Longueur finale de la série de données """
CCMclassification()

def main():
    global Revelateur
    root = Tk().withdraw() # Classe fenête 

    # Créer une fenêtre Tkinter pour la boîte de dialogue de sélection de fichier
    while root is not None: # Boucle cassée par cv2.waitkeys

        # Afficher la boîte de dialogue pour sélectionner une image
        file_names = askopenfilenames(
        title="Sélectionnez des photos", # nom de la fenêtre
        filetypes=(("Fichiers image", "*.jpg;*.jpeg;*.png"), ("Tous les fichiers", "*.*")) # type du ficher
        )
        
        dialog1 = simpledialog.askstring("Entrée", "Nombre de spot:") # type : Boite de dialogue
        print(dialog1) #
        if dialog1 !="":
            dialog2 = simpledialog.askstring("Entrée", "Nombre de canaux") # type : Boite de dialogue
        # Convertir l'input en entier
        try:
            user_input = int(dialog1) # type : int
            print("Input fourni :", user_input)
        except ValueError:
            print("Erreur : la valeur entrée n'est pas un entier.")

        # Enregistre la série de positions de la souris sur la vue de la plaque CCM
        global mouse_loc # type : list
        mouse_loc = []


        # Déclaration d'une instance de graph intensité/distance de migration
        global fig, ax # type : objet matplotlib 
        fig, ax = plt.subplots()
        
        # Traiter tous les fichiers sélectionnées pour transformer les tâches en série de données
        for file_name in file_names: # Pour chaque fichier dans la liste des ficher 
            # Vérifier si une image a été sélectionnée
            if file_name:
                # Charger l'image avec OpenCV
                image = cv2.imread(file_name)

                # Vérifier si l'image a été chargée avec succès
                if image is not None:
                    # Réduire la taille de l'image pour un affichage plus petit
                    resized_image = cv2.resize(image, (0, 0), fx=1/SETTING_REDUCTION, fy=1/SETTING_REDUCTION)

                    # Afficher l'image réduite
                    cv2.imshow('Image', resized_image)

                    # Variables pour stocker les coordonnées de la souris
                    mouse_x = -1
                    mouse_y = -1
                    

                    def mouse_callback(event, x, y, flags, param):
                        """ Fonction de rappel pour la détection du mouvement de la souris 
                            Args:
                                x (int): Position de la souris.
                                y (int) : Position de la souris.
                        """
                        global mouse_x, mouse_y, mouse_loc

                        # lorsque la souris bouge
                        if event == cv2.EVENT_MOUSEMOVE: 
                            mouse_x = x
                            mouse_y = y

                        # lors d'un clic gauche
                        if event == cv2.EVENT_LBUTTONDOWN:
                            
                            # les deux premier clic detectent la longueur de migration (ligne de front, ligne de dépot)
                            if len(mouse_loc) < 2:
                                mouse_loc.append((x*SETTING_REDUCTION, y*SETTING_REDUCTION))
                                print(mouse_loc)
                            
                            # les autres clic détecte le canal de migration observé
                            else:
                                print(x)
                                mouse_loc.append((x*SETTING_REDUCTION, y*SETTING_REDUCTION))
                                print(mouse_loc)
                        
                        if ((event == cv2.EVENT_RBUTTONDOWN) & (len(mouse_loc) > 2)):
                            # déclarer un canal vide
                            mouse_loc.append((x*SETTING_REDUCTION, -1))
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

                        # Attendre l'appui sur la touche 'enter' pour quitter la boucle ou la touche échap pour quitter le programmee
                        if cv2.waitKey(0) & 0xFF == ord('\r'): 
                            break
                        if cv2.waitKey(0) & 0xFF == 27:
                            exit()    
                            
                    cv2.destroyAllWindows()

                    # Extraire les canaux de couleur de l'image
                    red_channelBG = image[:, :, 2][mouse_loc[0][1]:mouse_loc[1][1]]
                    green_channelBG = image[:, :, 1][mouse_loc[0][1]:mouse_loc[1][1]]
                    blue_channelBG = image[:, :, 0][mouse_loc[0][1]:mouse_loc[1][1]]

                    print('Révélateur', np.mean(red_channelBG))
                    print('Révélateur', np.mean(green_channelBG))
                    print('Révélateur', np.mean(red_channelBG))

                    Revelateur = predict_class(np.mean(red_channelBG), np.mean(green_channelBG),np.mean(blue_channelBG))
                    print(Revelateur)

                    # Enregistre les informations de positon des spot sous forme de dataframe exportable.
                    global rf # type : DataFrame
                    rf = pd.DataFrame(columns=["Echantillon",Revelateur,"produit"])

                    width = 10

                    # red_channel=red_channelBG[:,mouse_loc[2]-width:mouse_loc[2]+width]
                    # green_channel=green_channelBG[:,mouse_loc[2]-width:mouse_loc[2]+width]
                    # blue_channel=blue_channelBG[:,mouse_loc[2]-width:mouse_loc[2]+width]

                    # Tronquer un canal de l'image

                    for i in mouse_loc[2:]:
                        red_channel=red_channelBG[:,i[0]-width:i[0]+width]
                        green_channel=green_channelBG[:,i[0]-width:i[0]+width]
                        blue_channel=blue_channelBG[:,i[0]-width:i[0]+width]
                        

                        # Moyenne des valeurs 
                        red_channel = np.mean(red_channel, axis=1)
                        green_channel = np.mean(green_channel, axis=1)
                        blue_channel = np.mean(blue_channel, axis=1)

                        # Exemple d'utilisation
                        red_channel = transform_array_proportions(red_channel[::-1], 1000)
                        green_channel = transform_array_proportions(green_channel[::-1], 1000)
                        blue_channel = transform_array_proportions(blue_channel[::-1], 1000)

                    
                        x = np.arange(len(green_channel))/1000
                        plt.plot(x, green_channel**2)
                        plt.plot(x, blue_channel**2)
                        plt.plot(x, red_channel**2)




            else:
                print('Erreur lors du chargement de l\'image.')

        else:
            print('Aucune image sélectionnée.')
            
        # Enregistrer les canaux de couleur dans des fichiers Excel

        df = clipboard2df()
        truncated_data = pd.qcut(range(image.shape[1]), q=len(df['Echantillon']), labels=False)
        elution = (mouse_loc[1][1]-mouse_loc[0][1])

        for i in mouse_loc[2:]:
            if i[1] == -1:
                value = "Nan"
            else:
                value = np.round(1-(i[1]-(image.shape[0]-mouse_loc[1][1]))/elution,2)
            rf = pd.concat([rf,pd.DataFrame([[df['Echantillon'][truncated_data[i[0]]],value,""]],columns=['Echantillon',Revelateur,"produit"])],join="inner")
            rf.to_clipboard(index=False)
        print(rf)

        rf = pd.DataFrame(columns=['Echantillon',Revelateur,"produit"])
        def onclick(event):
            global Revelateur
            global rf
            if event.button == 1:  # Clic gauche de la souris
                rf = pd.concat([rf,pd.DataFrame([["",np.round(event.xdata,2),""]],columns=['Echantillon',Revelateur,"produit"])],join="inner")
                rf.to_clipboard(index=False)
                
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.xlabel('Distance')
        plt.ylabel('Intensité')
        plt.title('Migration')
        plt.show()
        # Fermeture de la fenêtre
        
    
if __name__ == '__main__':

    main()

""" 
arbre de décisions:
    est ce qu'on analyse une seule plaque avec plusieurs canaux ? 
    est ce qu'on analyse plusieurs plaque avec 1 seul canal



 """