import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import xlsxwriter

def save_to_excel(filename, data):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    for row, row_data in enumerate(data):
        for col, value in enumerate(row_data):
            worksheet.write(row, col, value)

    workbook.close()
    print(f"Les données ont été enregistrées dans le fichier {filename}")

reduction = 3
global mouse_loc
mouse_loc = []
def main():
    # Créer une fenêtre Tkinter pour la boîte de dialogue de sélection de fichier
    Tk().withdraw()

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

                if event == cv2.EVENT_LBUTTONDOWN:
                    print('clic', x)

                    # facteur de grossissement de l'image réduite
                    mouse_loc = x*reduction

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
            red_channel=red_channel[:,mouse_loc-10:mouse_loc+10]
            green_channel=green_channel[:,mouse_loc-10:mouse_loc+10]
            blue_channel=blue_channel[:,mouse_loc-10:mouse_loc+10]
            
            

            # Moyenne des valeurs 
            red_channel = np.mean(red_channel, axis=1)
            green_channel = np.mean(green_channel, axis=1)
            blue_channel = np.mean(blue_channel, axis=1)

            import matplotlib.pyplot as plt
            # Enregistrer les canaux de couleur dans des fichiers Excel
            x = np.arange(len(green_channel))
            plt.plot(x, green_channel**2)
            plt.plot(x, blue_channel**2)
            plt.plot(x, red_channel**2)
            plt.xlabel('Distance')
            plt.ylabel('Intensité')
            plt.title('Courbe des moyennes des lignes')
            plt.show()

        else:
            print('Erreur lors du chargement de l\'image.')
    else:
        print('Aucune image sélectionnée.')

if __name__ == '__main__':
    main()
