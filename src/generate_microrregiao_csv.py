import pandas as pd
from src.utils.logger import get_logger

class MicrorregiaoCSVGenerator:
    """
    Generates a CSV file with aggregated data by microrregion.
    """
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.logger = get_logger(__name__)

    def generate(self):
        """
        Generates the CSV file.
        """
        self.logger.info(f"Loading data from {self.input_path}")
        df = pd.read_pickle(self.input_path)

        self.logger.info("Grouping data by microrregiao.")
        microrregiao_grouped = df.groupby("microrregiao").agg(
            distancia_media_fabrica_1=('distancia_fabrica_1', 'mean'),
            distancia_media_fabrica_2=('distancia_fabrica_2', 'mean'),
            capacidade_alojamento_total=('capacidade_alojamento', 'sum'),
            associados_unicos=('bp_associado', lambda x: x.nunique())
        ).reset_index()

        self.logger.info(f"Saving CSV file to {self.output_path}")
        microrregiao_grouped.to_csv(self.output_path, index=False, encoding="utf-8")
        self.logger.info("CSV file by microrregiao generated successfully.")