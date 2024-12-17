import data_dictionary as d_d
import distance as dist
import estimation_cov as ec
import numpy as np
import cProfile
import pstats


# Fonction principale pour profiler
def main():
    # Instanciez et préparez votre DataDictionary
    data_dict = d_d.DataDictionary()
    data_dict.runData_dict()

    # Instanciez Distance et exécutez
    distance = dist.Distance(data_dict)
    distance.runDist()

    # Calcul des covariances empiriques
    estimation = ec.EstimationCov(distance)
    estimation.runEstimCov()

# Profilage avec cProfile
if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()

    # Générer un rapport de profilage
    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats("cumulative")  # Trier par temps cumulé
    stats.print_stats(20)  # Afficher les 20 entrées les plus coûteuses

# data/geopot_ptloc_gravi_RD6p5km_noised
# data/data_EMC_dg
# data/data_EMC_T33

#     # Chargement des fichiers avec NumPy
# for i, file_name in enumerate(data_dict.files):
#     print(f"\nChargement du fichier {file_name} avec NumPy...")
#     # Définir les paramètres
#     delimiter = data_dict.delimiters[i] if data_dict.delimiters else " "
#     has_header = data_dict.headers[i] if data_dict.headers else None
#     skip_rows = 1 if has_header else 0  # Ignorer le header si présent
#     # Charger le fichier
#     data = np.genfromtxt(file_name, delimiter=delimiter, skip_header=skip_rows)
#     print(f"Contenu du fichier {file_name} :\n", data[:5])  # Affiche les 5 premières lignes