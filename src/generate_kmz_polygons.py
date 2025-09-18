import pandas as pd
import simplekml
from math import radians, sin, cos
from src.utils.logger import get_logger

class KMLPolygonGenerator:
    """
    Generates a KML file with polygons from the data.
    """
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.logger = get_logger(__name__)
        self.colors = {
            "EXTENSIONISTA": simplekml.Color.changealphaint(150, simplekml.Color.blue), 
            "MUNICIPIOS": simplekml.Color.changealphaint(150, simplekml.Color.green), 
            "MICRORREGIOES": simplekml.Color.changealphaint(150, simplekml.Color.red), 
            "NUCLEOS": simplekml.Color.changealphaint(150, simplekml.Color.yellow) 
        }

    def generate(self):
        """
        Generates the KML file with polygons.
        """
        self.logger.info(f"Loading data from {self.input_path}")
        df_original = pd.read_csv(self.input_path, sep=";")
        df_original.columns = df_original.columns.str.strip()

        self.logger.info("Renaming columns.")
        df_original = df_original.rename(columns={
            "fazenda": "aviario", 
            "proprietario": "nome_proprietario", 
            "cidade": "municipio", 
            "nome_tecnico": "tecnico_nome",
            "nucleo": "numero_nucleo",
            "microrregiao": "microrregiao"
        })

        self.logger.info("Adding Google Maps link.")
        df_original["google_maps_link"] = df_original["coordenadas"].apply(lambda x: f"https://www.google.com/maps/search/?api=1&query={str(x).replace(' ', '')}" if pd.notna(x) else "")

        kml = simplekml.Kml()

        self._create_polygons(kml, df_original, "tecnico_nome", "EXTENSIONISTA", "Área de atuação do técnico")
        self._create_polygons(kml, df_original, "municipio", "MUNICIPIOS", "Área do município")
        self._create_polygons(kml, df_original, "microrregiao", "MICRORREGIOES", "Área da microrregião")
        self._create_nucleo_circles(kml, df_original)

        self.logger.info(f"Saving KML file to {self.output_path}")
        kml.save(self.output_path)
        self.logger.info("KML file with polygons generated successfully.")

    def _generate_circle(self, lat, lon, radius_meters=500, num_points=32):
        points = []
        R = 6371000  # Earth radius in meters

        for i in range(num_points):
            angle = 2 * 3.141592653589793 * i / num_points
            dx = radius_meters * cos(angle)
            dy = radius_meters * sin(angle)

            new_latitude = lat + (dy / R) * (180 / 3.141592653589793)
            new_longitude = lon + (dx / R) * (180 / 3.141592653589793) / cos(radians(lat))
            points.append((new_longitude, new_latitude))
        return points

    def _create_polygons(self, kml, df, column_name, folder_name, description_prefix):
        self.logger.info(f"Creating {folder_name} polygons.")
        folder = kml.newfolder(name=folder_name)
        for item in df[column_name].dropna().unique():
            item_data = df[df[column_name] == item]
            
            coords = []
            for c in item_data["coordenadas"]:
                try:
                    lat, lon = map(float, c.split(','))
                    coords.append((lon, lat))
                except (ValueError, AttributeError):
                    continue 

                if coords:
                    min_lon = min(c[0] for c in coords)
                    max_lon = max(c[0] for c in coords)
                    min_lat = min(c[1] for c in coords)
                    max_lat = max(c[1] for c in coords)

                    pol = folder.newpolygon(name=str(item))
                    pol.outerboundaryis = [
                        (min_lon, min_lat),
                        (max_lon, min_lat),
                        (max_lon, max_lat),
                        (min_lon, max_lat),
                        (min_lon, min_lat)
                    ]
                    pol.style.polystyle.color = self.colors[folder_name]
                    pol.style.polystyle.fill = 1
                    pol.style.polystyle.outline = 1
                    pol.description = f"{description_prefix}: {item}"

    def _create_nucleo_circles(self, kml, df):
        self.logger.info("Creating NUCLEOS circles.")
        folder_nucleos = kml.newfolder(name="NUCLEOS")
        nucleos_unicos = df.drop_duplicates(subset=["numero_nucleo"])
        for index, row in nucleos_unicos.iterrows():
            nucleo_num = row["numero_nucleo"]
            coordenadas = row["coordenadas"]
            if pd.isna(coordenadas):
                continue
            try:
                lat, lon = map(float, coordenadas.split(','))
                circle_coords = self._generate_circle(lat, lon)
                
                pol = folder_nucleos.newpolygon(name=f"Núcleo {nucleo_num}")
                pol.outerboundaryis = circle_coords
                pol.style.polystyle.color = self.colors["NUCLEOS"]
                pol.style.polystyle.fill = 1
                pol.style.polystyle.outline = 1
                pol.description = f"Círculo de 500m ao redor do Núcleo: {nucleo_num}\nCoordenadas: {coordenadas}"
            except (ValueError, AttributeError):
                continue