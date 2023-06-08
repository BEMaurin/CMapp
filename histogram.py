import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_histogram(image, x):
    # Extraire la ligne verticale de pixels de l'image
    line_pixels = image[:, x]

    # Calculer les histogrammes des canaux de couleurs
    red_hist = np.histogram(line_pixels[:, 0], bins=256, range=(0, 256))[0]
    green_hist = np.histogram(line_pixels[:, 1], bins=256, range=(0, 256))[0]
    blue_hist = np.histogram(line_pixels[:, 2], bins=256, range=(0, 256))[0]

    # Créer une figure pour afficher l'histogramme
    fig, ax = plt.subplots()
    ax.plot(np.arange(256), red_hist, color='red', label='Red')
    ax.plot(np.arange(256), green_hist, color='green', label='Green')
    ax.plot(np.arange(256), blue_hist, color='blue', label='Blue')
    ax.set_xlabel('Intensité de la couleur')
    ax.set_ylabel('Hauteur du pixel')
    ax.set_title('Histogramme RGB')
    ax.legend()
    plt.show()

def main():
    # Afficher la boîte de dialogue pour sélectionner une image
    image_path = cv2.imread(cv2.dialogueFileDialog(cv2.IMREAD_ANYCOLOR)[0])

    # Vérifier si une image a été sélectionnée
    if image_path is not None:
        # Afficher l'image
        cv2.imshow('Image', image_path)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Obtenir la position x de la ligne verticale depuis l'utilisateur
        x = int(input("Entrez la position x de la ligne verticale : "))

        # Afficher l'histogramme de la ligne verticale
        display_histogram(image_path, x)
    else:
        print('Aucune image sélectionnée.')

if __name__ == '__main__':
    main()
