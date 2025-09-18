import pandas as pd
from src.utils.logger import get_logger

class DataPreparer:
    """
    Prepares the raw data for processing.
    """
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.logger = get_logger(__name__)

    def prepare(self):
        """
        Loads the raw data, cleans it, and saves the prepared data.
        """
        self.logger.info(f"Loading data from {self.input_path}")
        df = pd.read_csv(self.input_path, sep=";")
        self.logger.info("Cleaning column names.")
        df.columns = df.columns.str.strip()
        self.logger.info("Renaming columns.")
        df = df.rename(columns={
            "fazenda": "aviario", 
            "proprietario": "nome_proprietario", 
            "cidade": "municipio", 
            "nome_tecnico": "tecnico_nome",
            "nucleo": "numero_nucleo",
            "microrregiao": "microrregiao",
            "area": "area_m2",
            "capacidade": "capacidade_alojamento",
            "dist_fab_1": "distancia_fabrica_1",
            "dist_fab_2": "distancia_fabrica_2",
            "global_gap": "granja_global",
            "bp_associado": "bp_associado"
        })
        self.logger.info("Handling missing values and creating Google Maps link.")
        df["coordenadas"] = df["coordenadas"].fillna("")
        df["google_maps_link"] = df["coordenadas"].apply(lambda x: "https://www.google.com/maps/search/?api=1&query=" + x.replace(" ", "") if x else "")
        self.logger.info("Converting 'granja_global' to boolean.")
        df["granja_global"] = df["granja_global"].astype(str).str.lower().str.strip() == "verdadeiro"
        self.logger.info("Converting columns to numeric.")
        df["distancia_fabrica_1"] = pd.to_numeric(df["distancia_fabrica_1"], errors='coerce')
        df["distancia_fabrica_2"] = pd.to_numeric(df["distancia_fabrica_2"], errors='coerce')
        df["capacidade_alojamento"] = pd.to_numeric(df["capacidade_alojamento"], errors='coerce')
        df["area_m2"] = pd.to_numeric(df["area_m2"], errors='coerce')
        self.logger.info("Ensuring 'bp_associado' is string.")
        df["bp_associado"] = df["bp_associado"].astype(str)
        self.logger.info(f"Saving prepared data to {self.output_path}")
        df.to_pickle(self.output_path)
        self.logger.info("Data preparation complete.")