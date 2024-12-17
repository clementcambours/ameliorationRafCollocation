import numpy as np
import pandas as pd

class Distance:
    def __init__(self, data_dictionary):
        self.data_dictionary = data_dictionary
        self.grouped_points = {}
        self.step_size = float(input("Donnez le pas de distance (en km) : ")) * 1000  # Convertir en mètres

    
    def matrix_distance(self):
        all_transformed_data = pd.concat(self.data_dictionary.transformed_data, ignore_index=True)
        print('all_transformed_data : ', all_transformed_data)
        # Extraction des coordonnées Lambert
        coords = all_transformed_data[["lambert_E", "lambert_N"]].values
        print('coord : ', type(coords))

        # Initialisation de la matrice des distances
        dist_matrix = np.zeros((coords.shape[0], coords.shape[0]))
        

        # Calcul des distances
        for l in range(coords.shape[0]):
            # Calcul des distances pour les indices supérieurs à l
            distE = coords[l, 0] - coords[l+1:, 0]
            # print('shape distE : ', distE.shape)
            distN = coords[l, 1] - coords[l+1:, 1]
            # print('shape distN : ', distN.shape)
            dist = np.sqrt(distE**2 + distN**2)
            # print('shape dist : ', dist.shape)

            # Remplissage de la matrice triangulaire supérieure
            dist_matrix[l, l+1:] = dist

        print("dist_matrix :\n", dist_matrix.shape)
        self.dist_matrix = dist_matrix
        self.all_transformed_data = all_transformed_data

    def getDistmatrix(self):
        if self.dist_matrix is None :
            self.matrix_distance()
        return self.dist_matrix
    
    def getAllDataTrans(self):
        return self.all_transformed_data

  
    def runDist(self):
        self.matrix_distance()
        print(f"\nDistances groupées par classe de {self.step_size / 1000} km : {self.grouped_points}")
