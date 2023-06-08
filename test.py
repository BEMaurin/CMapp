import numpy as np

matrice = np.array([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]])

moyennes_lignes = np.mean(matrice, axis=1)
print(10-moyennes_lignes)