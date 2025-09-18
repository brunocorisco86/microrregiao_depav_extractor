import pandas as pd
from src.utils.logger import get_logger

class DataProcessor:
    """
    Processes the prepared data.
    """
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.logger = get_logger(__name__)

    def process(self):
        """
        Loads the prepared data, processes it, and saves the processed data.
        """
        self.logger.info(f"Loading prepared data from {self.input_path}")
        df = pd.read_pickle(self.input_path)
        self.logger.info("Grouping data by 'numero_nucleo'.")
        df_grouped = df.groupby("numero_nucleo").agg({
            "aviario": lambda x: list(x),
            "nome_proprietario": "first",
            "coordenadas": "first",
            "google_maps_link": "first",
            "municipio": "first",
            "tecnico": "first",
            "microrregiao": "first"
        }).reset_index()
        self.logger.info(f"Saving processed data to {self.output_path}")
        df_grouped.to_pickle(self.output_path)
        self.logger.info("Data processing complete.")