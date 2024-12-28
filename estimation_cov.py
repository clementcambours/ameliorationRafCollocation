import numpy as np
import pandas as pd

class EstimationCov:
    def __init__(self, distance_instance):
        self.distance_instance = distance_instance
        self.data_dictionary = distance_instance.data_dictionary  # Correction : ajouter l'assignation
        self.data_types = []  # Liste pour stocker 1 ou 2 types de données choisis par l'utilisateur
        self.covariances = []  # Moyennes des covariances empiriques pour chaque tranche de distance
        self.step_size = self.distance_instance.step_size

    def select_data_types(self):
        """
        Permet à l'utilisateur de choisir un ou deux types de données pour le calcul des covariances.
        """
        print("Quels types de données voulez-vous utiliser pour calculer les covariances ?")
        print("Options disponibles : 'T', 'dg', 'N'")
        first_type = input("Entrez le premier type de données : ").strip()
        second_type = input("Entrez un second type de données (ou appuyez sur Entrée pour n'en choisir qu'un) : ").strip()

        self.data_types = [first_type]
        if second_type:
            self.data_types.append(second_type)

        print(f"Types de données sélectionnés : {self.data_types}")

    # def calculate_covariances(self):
    #     """
    #     Calcule les covariances empiriques pour les types de données choisis.
    #     """
    #     all_transformed_data = self.distance_instance.getAllDataTrans()

    #     # Vérifier que les colonnes sélectionnées existent
    #     for data_type in self.data_types:
    #         if data_type not in all_transformed_data.columns:
    #             raise ValueError(f"Le type de données '{data_type}' n'est pas présent dans les colonnes des données.")

    #     # Extraire les valeurs pour les types de données choisis
    #     if len(self.data_types) == 1:
    #         values1 = all_transformed_data[self.data_types[0]].values
    #         values2 = values1  # Auto-covariance
    #     else:
    #         values1 = all_transformed_data[self.data_types[0]].values
    #         values2 = all_transformed_data[self.data_types[1]].values
    #         print('values 1 : ', values1)
    #         print('values 2 : ', values2)

    #     # Extraction de la matrice des distances
    #     dist_matrix = self.distance_instance.getDistmatrix()
    #     print("aaaaaaa : ", dist_matrix)
    #     # Initialisation des covariances par tranche de distance
    #     max_distance = np.nanmax(dist_matrix)
    #     print("max_distance : ", max_distance)
    #     num_bins = int(np.ceil(max_distance / self.step_size))
    #     self.covariances = [[] for _ in range(num_bins)]

    #     # Scanner la matrice de distance pour grouper les indices
    #     for i in range(dist_matrix.shape[0]):
    #         for j in range(i + 1, dist_matrix.shape[1]):
    #             distance = dist_matrix[i, j]

    #             # Ignorer les distances NaN
    #             if np.isnan(distance):
    #                 continue

    #             # Ignorer les paires si l'une des valeurs est NaN
    #             if np.isnan(values1[i]) or np.isnan(values2[j]):
    #                 continue
    #             bin_index = int(distance // self.step_size)

    #             # Calcul de la covariance empirique pour les paires (i, j)
    #             cov = (values1[i] - np.nanmean(values1)) * (values2[j] - np.nanmean(values2))
    #             self.covariances[bin_index].append(cov)

    #     # Moyenne des covariances pour chaque tranche
    #     self.covariances = [
    #         np.nanmean(cov_list) if cov_list else None
    #         for cov_list in self.covariances
    #     ]

    def calculate_covariances(self):
        all_transformed_data = self.distance_instance.getAllDataTrans()
        print('all_transformed_data : ', all_transformed_data)
        dist_matrix = self.distance_instance.getDistmatrix()
        print('dist_matrix : ', dist_matrix)

        # Vérification des colonnes
        values1 = all_transformed_data[self.data_types[0]].values
        print('values 1 : ', values1)
        values2 = all_transformed_data[self.data_types[1]].values if len(self.data_types) > 1 else values1
        print('values 2 : ', values2)

        # Masque pour éliminer les NaN
        valid_mask = ~np.isnan(values1) & ~np.isnan(values2)

        # Appliquer le masque aux distances et aux valeurs
        valid_dist_matrix = dist_matrix[valid_mask][:, valid_mask]
        print('valid_dist_matrix : ', valid_dist_matrix)
        valid_values1 = values1[valid_mask]
        valid_values2 = values2[valid_mask]

        # Grouper les distances par tranche
        max_valid_dist_matrix = np.nanmax(valid_dist_matrix)
        bins = np.arange(0,  max_valid_dist_matrix + self.step_size, self.step_size)
        print('max valid_dist_matrix : ', max_valid_dist_matrix)
        self.covariances = []

        for i in range(len(bins) - 1):
            # Trouver les paires de points dans la tranche de distance
            in_bin = (valid_dist_matrix >= bins[i]) & (valid_dist_matrix < bins[i + 1])

            if not np.any(in_bin):
                # Si aucune paire n'existe pour cette tranche, ajouter None
                self.covariances.append(None)
                continue

            # Extraire les indices des paires dans la tranche
            indices = np.where(in_bin)
            v1 = valid_values1[indices[0]]
            v2 = valid_values2[indices[1]]

            # Calcul de la covariance empirique pour cette tranche
            cov = np.nanmean((v1 - np.nanmean(valid_values1)) * (v2 - np.nanmean(valid_values2)))
            self.covariances.append(cov)

    def runEstimCov(self):
        """
        Exécute le processus complet de sélection des types de données et calcul des covariances.
        """
        self.select_data_types()
        self.calculate_covariances()
        print("\nMoyennes des covariances empiriques par tranche de distance :")
        for i, cov in enumerate(self.covariances):
            distance_range = f"[{i * self.step_size / 1000}, {(i + 1) * self.step_size / 1000}] km"
            print(f"{distance_range} : {cov}")