import cv2

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

# Sélectionner le fichier d'image
image_path = input("Entrez le chemin de l'image : ")

# Charger l'image
image = cv2.imread(image_path)

# Vérifier si l'image a été chargée correctement
if image is None:
    print("Impossible de charger l'image.")
    exit()

# Redimensionner l'image pour l'affichage (facultatif)
scale_percent = 50  # Ajuster la valeur selon vos préférences
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
    print("Veuillez sélectionner 4 points sur l'image.")
    exit()

# Calculer les dimensions du rectangle
width = 1000
height = 2000

# Définir les coordonnées des 4 coins du rectangle de destination
dst_points = [(0, 0), (width, 0), (width, height), (0, height)]

# Calculer la transformation perspective
matrix = cv2.getPerspectiveTransform(
    src=np.float32(points),
    dst=np.float32(dst_points)
)

# Appliquer la transformation perspective à l'image
cropped_image = cv2.warpPerspective(image, matrix, (width, height))

# Afficher l'image recadrée et redimensionnée
cv2.imshow("Cropped Image", cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
