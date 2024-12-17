  
import pandas as pd
from pyproj import Proj, Transformer

class DataDictionary:
    def __init__(self):
        self.files = []
        self.column_mappings = []
        self.transformed_data = []  # Données transformées en pandas DataFrame avec Lambert 93 inclus

    def collect_user_input(self):
        # Nombre de fichiers
        num_files = int(input("Entrez le nombre de fichiers de données : "))

        for i in range(num_files):
            print(f"\n--- Configuration du fichier {i + 1} ---")
            file_name = input(f"Entrez le chemin du fichier {i + 1} : ")
            self.files.append(file_name)

            # Présence de header
            has_header = input("Le fichier contient-il un header ? (oui/non) : ").strip().lower() == "oui"
            skip_header = int(input("Entez la première ligne de donnée "))-1

            delimiter = input("Entrez le délimiteur utilisé (par défaut ' ') : ").strip()
            delimiter = delimiter if delimiter else " "

            # Demander les noms des colonnes et leur correspondance
            print("Listez les colonnes dans l'ordre où elles apparaissent dans le fichier.")
            print("Par exemple : lat, lon, h, data, err")
            raw_columns = input("Colonnes (séparées par des virgules) : ").strip().split(",")
            raw_columns = [col.strip() for col in raw_columns]

            print("\nIndiquez le rôle de chaque colonne. Options disponibles :")
            print("lat, lon, h, data, err, ou autre nom personnalisé.")
            mappings = {}
            for col in raw_columns:
                role = input(f"À quoi correspond '{col}' ? : ").strip()
                mappings[col] = role

            self.column_mappings.append({
                "file_name": file_name,
                "delimiter": delimiter,
                "skip_header": skip_header,
                "mappings": mappings
            })

    def transform_to_lambert93(self, lat, lon):
        """
        Transforme des coordonnées géographiques en coordonnées Lambert 93.

        :param lat: Latitude en degrés
        :param lon: Longitude en degrés
        :return: Coordonnées (x, y) en Lambert 93
        """
        geo_proj = Proj(proj="latlong", ellps="WGS84")
        lambert93 = Proj(proj="lcc", lat_1=44, lat_2=49, lat_0=46.5, lon_0=3, x_0=700000, y_0=6600000, ellps="WGS84")
        transformer = Transformer.from_proj(geo_proj, lambert93)
        x, y = transformer.transform(lat, lon)
        return x, y

    def prepare_data(self):
        """
        Charge les fichiers, mappe les colonnes et ajoute les coordonnées Lambert 93.
        """
        for mapping in self.column_mappings:
            file_name = mapping["file_name"]
            delimiter = mapping["delimiter"]
            skip_header = mapping["skip_header"]
            column_roles = mapping["mappings"]

            # Charger les données en pandas
            data = pd.read_csv(file_name, delimiter=delimiter, skiprows=skip_header, header=None)
            data.columns = column_roles.keys()  # Assigner des noms temporaires

            # Renommer les colonnes selon les rôles définis
            data = data.rename(columns=column_roles)

            # Vérifier que les colonnes lat et lon sont présentes
            if "lat" not in data.columns or "lon" not in data.columns:
                print(f"Erreur : les colonnes 'lat' et 'lon' sont nécessaires dans le fichier {file_name}.")
                continue

            # Ajouter les colonnes Lambert 93
            data["lambert_E"], data["lambert_N"] = self.transform_to_lambert93(data["lat"], data["lon"])

            self.transformed_data.append(data)
            print("type self transformed data : ", self.transformed_data)

    def runData_dict(self):
        self.collect_user_input()
        self.prepare_data()
        print("\nDonnées transformées avec succès !")

        # Exemple d'affichage des données transformées
        for i, df in enumerate(self.transformed_data):
            print(f"\nFichier {i + 1} :")
            print(df.head())



