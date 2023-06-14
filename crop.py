import cv2
import numpy as np
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory


save_path = ""
# save_path = "C:/Users/Asus/Downloads/Pause Diabolo Temp/Photo - Analyses/"

SETTING_DELETE_RAW = False
SETTING_DEBUG = True
SETTING_SINGLE_FILE = False
SETTING_MULTI_FILE = True

def debug(param):
    """ 
    Afficher les informations de debuggage dans la console

    args:
        param (str): informations de debuggage
    """
    if SETTING_DEBUG == True:
        print(param)
        return


# DEBUG
debug(save_path)

def pythagore(a,b):
    """ calcul de longueur de côté par pythagore
    args:
        a (int): coordonnée 1
        b (int): coordonnée 2

    returns:
        longueur (in): longueur de côté
        """
    longueur = ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)
    return longueur

def proportions(list):
    """ 
    Calcul du ratio longueur/hauteur de la plaque CCM
    args:
        list(list): list des coordonées x,y des 4 points

    returns:
        ratio (float): ratio des longueurs
        """    
    a,b,c,d = list[0],list[1],list[2],list[3]

    gauche = (pythagore(a,b)+pythagore(c,d))/2
    droite = (pythagore(b,c)+pythagore(d,a))/2
    ratio = droite/gauche

    return ratio
# Fonction pour gérer les clics de souris
def mouse_callback(event, x, y, flags, param):
    global points, cropping
    
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        
        # Afficher un cercle sur le point cliqué
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Image", image)
        
        # Cropper l'image lorsqu'on a cliqué sur les 4 points
        if len(points) == 4:
            cropping = True
            cv2.destroyAllWindows()

# Ouvrir la boîte de dialogue pour sélectionner le dossier contenant les images
Tk().withdraw()  # Cacher la fenêtre principale Tkinter
folder_path = askdirectory(title="Sélectionner un dossier")

# Vérifier si le dossier existe
if not os.path.isdir(folder_path):
    print("Le dossier sélectionné n'existe pas.")
    exit()

# Liste pour stocker les chemins des images du dossier
image_paths = []

# Parcourir le dossier et récupérer les chemins des images
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
        image_paths.append(file_path)

# Vérifier si des images ont été trouvées dans le dossier
if not image_paths:
    print("Aucune image n'a été trouvée dans le dossier sélectionné.")
    exit()

debug(len(image_paths)) # affche le nombre d'objects sélectionnés 

# Parcourir les images et appliquer l'algorithme de sélection des points et de transformation
for image_path in image_paths:
    # Charger l'image
    image = cv2.imread(image_path)

    # Vérifier si l'image a été chargée correctement
    if image is None:
        print(f"Impossible de charger l'image : {image_path}")
        continue

    # Redimensionner l'image pour l'affichage (facultatif)
    scale_percent = 20  # Ajuster la valeur selon vos préférences
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    image = cv2.resize(image, (width, height))

    # Afficher l'image
    cv2.imshow("Image", image)

    # Attendre que l'utilisateur clique sur 4 points
    points = []
    cropping = False
    cv2.setMouseCallback("Image", mouse_callback)
    cv2.waitKey(0)

    # Vérifier si 4 points ont été cliqués
    if len(points) != 4:
        print(f"Veuillez sélectionner 4 points sur l'image : {image_path}")
        continue

    # Déclarer les dimensions du rectangle
    height = 2000
    width = int(height/ proportions(points))

    # Définir les coordonnées des 4 coins du rectangle de destination
    dst_points = [(0, 0), (width, 0), (width, height), (0, height)]

    # Calculer la transformation perspective
    matrix = cv2.getPerspectiveTransform(
        src=np.float32(points),
        dst=np.float32(dst_points)
    )

    # Appliquer la transformation perspective à l'image
    cropped_image = cv2.warpPerspective(image, matrix, (width, height))
    print(str(folder_path))
    print(str(filename))
    print(image_path)
    
    # Redimensionner et afficher l'image transformée 
    width = int(cropped_image.shape[1] * scale_percent / 100)
    height = int(cropped_image.shape[0] * scale_percent / 100)
    image = cv2.resize(cropped_image, (width, height))
    cv2.imshow("Cropped Image", image)

    # Afficher l'image transformée
    while True:
        if cv2.waitKey(1000) & 0xFF == ord('\r'):
            # Supprimmer les photos brut 
            if SETTING_DELETE_RAW == True:
                os.remove(image_path)
                print('deleted successfully')
            break
        if cv2.waitKey(1) & 0xFF == 27:
            break 
    print('saved: ',str(save_path)+os.path.basename(image_path))
    cv2.imwrite(str(save_path)+os.path.basename(image_path), cropped_image)
    cv2.destroyAllWindows()
        
    

# Fermer toutes les fenêtres affichant les images
cv2.destroyAllWindows()
