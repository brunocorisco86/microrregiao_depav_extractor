import pandas as pd
import simplekml
from src.utils.logger import get_logger

class KMLGenerator:
    """
    Generates a KML file from the processed data.
    """
    def __init__(self, grouped_data_path, original_data_path, output_path):
        self.grouped_data_path = grouped_data_path
        self.original_data_path = original_data_path
        self.output_path = output_path
        self.logger = get_logger(__name__)

    def generate(self):
        """
        Generates the KML file.
        """
        self.logger.info(f"Loading grouped data from {self.grouped_data_path}")
        df_grouped = pd.read_pickle(self.grouped_data_path)
        self.logger.info(f"Loading original data from {self.original_data_path}")
        df_original = pd.read_csv(self.original_data_path, sep=";")
        df_original.columns = df_original.columns.str.strip()

        self.logger.info("Renaming columns in original data.")
        df_original = df_original.rename(columns={
            "fazenda": "aviario",
            "proprietario": "nome_proprietario",
            "cidade": "municipio",
            "nucleo": "numero_nucleo"
        })

        self.logger.info("Adding Google Maps link to original data.")
        df_original["google_maps_link"] = df_original["coordenadas"].apply(lambda x: f"https://www.google.com/maps/search/?api=1&query={str(x).replace(' ', '')}" if pd.notna(x) else "")

        kml = simplekml.Kml()

        self._create_municipios_folder(kml, df_grouped)
        self._create_extensionista_folder(kml, df_original)
        self._create_microrregioes_folder(kml, df_grouped)

        self.logger.info(f"Saving KML file to {self.output_path}")
        kml.save(self.output_path)
        self.logger.info("KML file generated successfully.")

    def _create_municipios_folder(self, kml, df_grouped):
        self.logger.info("Creating MUNICIPIOS folder in KML.")
        folder_municipios = kml.newfolder(name="MUNICIPIOS")
        for municipio in df_grouped["municipio"].unique():
            if pd.isna(municipio):
                continue
            mun_folder = folder_municipios.newfolder(name=str(municipio))
            municipio_data = df_grouped[df_grouped["municipio"] == municipio]
            for index, row in municipio_data.iterrows():
                lat, lon = map(float, row["coordenadas"].split(','))
                pnt = mun_folder.newpoint(name=f"Núcleo {row['numero_nucleo']} - {row['nome_proprietario']}", coords=[(lon, lat)])
                pnt.style.iconstyle.scale = 0.9
                pnt.style.labelstyle.scale = 0.9
                aviarios_str = ", ".join(map(str, row['aviario']))
                pnt.description = (
                    f"Número do Núcleo: {row['numero_nucleo']}\n"
                    f"Aviários: {aviarios_str}\n"
                    f"Proprietário: {row['nome_proprietario']}\n"
                    f"Coordenadas: {row['coordenadas']}\n"
                    f"Link Google Maps: {row['google_maps_link']}"
                )

    def _create_extensionista_folder(self, kml, df_original):
        self.logger.info("Creating EXTENSIONISTA folder in KML.")
        folder_extensionista = kml.newfolder(name="EXTENSIONISTA")
        for tecnico in df_original["tecnico"].unique():
            if pd.isna(tecnico):
                continue
            tec_folder = folder_extensionista.newfolder(name=str(tecnico))
            tecnico_data = df_original[df_original["tecnico"] == tecnico]
            for proprietario in tecnico_data["nome_proprietario"].unique():
                if pd.isna(proprietario):
                    continue
                prop_folder = tec_folder.newfolder(name=str(proprietario))
                proprietario_data = tecnico_data[tecnico_data["nome_proprietario"] == proprietario]
                nucleos_unicos = proprietario_data.drop_duplicates(subset=["numero_nucleo"])
                for index, row in nucleos_unicos.iterrows():
                    lat, lon = map(float, row["coordenadas"].split(','))
                    pnt = prop_folder.newpoint(name=f"Núcleo {row['numero_nucleo']} - {row['nome_proprietario']}", coords=[(lon, lat)])
                    pnt.style.iconstyle.scale = 0.9
                    pnt.style.labelstyle.scale = 0.9
                    pnt.description = (
                        f"Número do Núcleo: {row['numero_nucleo']}\n"
                        f"Aviário: {row['aviario']}\n"
                        f"Proprietário: {row['nome_proprietario']}\n"
                        f"Coordenadas: {row['coordenadas']}\n"
                        f"Link Google Maps: {row['google_maps_link']}"
                    )

    def _create_microrregioes_folder(self, kml, df_grouped):
        self.logger.info("Creating MICRORREGIÕES folder in KML.")
        folder_microrregioes = kml.newfolder(name="MICRORREGIÕES")
        for microrregiao in df_grouped["microrregiao"].unique():
            if pd.isna(microrregiao):
                continue
            micro_folder = folder_microrregioes.newfolder(name=str(microrregiao))
            microrregiao_data = df_grouped[df_grouped["microrregiao"] == microrregiao]
            for index, row in microrregiao_data.iterrows():
                lat, lon = map(float, row["coordenadas"].split(','))
                pnt = micro_folder.newpoint(name=f"Núcleo {row['numero_nucleo']} - {row['nome_proprietario']}", coords=[(lon, lat)])
                pnt.style.iconstyle.scale = 0.9
                pnt.style.labelstyle.scale = 0.9
                aviarios_str = ", ".join(map(str, row['aviario']))
                pnt.description = (
                    f"Número do Núcleo: {row['numero_nucleo']}\n"
                    f"Aviários: {aviarios_str}\n"
                    f"Proprietário: {row['nome_proprietario']}\n"
                    f"Coordenadas: {row['coordenadas']}\n"
                    f"Link Google Maps: {row['google_maps_link']}"
                )