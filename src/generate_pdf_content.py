import pandas as pd
from src.utils.logger import get_logger

class PDFContentGenerator:
    """
    Generates the Markdown content for the PDF report.
    """
    def __init__(self, grouped_data_path, full_data_path, output_path):
        self.grouped_data_path = grouped_data_path
        self.full_data_path = full_data_path
        self.output_path = output_path
        self.logger = get_logger(__name__)

    def generate(self):
        """
        Generates the Markdown content.
        """
        self.logger.info(f"Loading grouped data from {self.grouped_data_path}")
        df_grouped = pd.read_pickle(self.grouped_data_path)
        self.logger.info(f"Loading full data from {self.full_data_path}")
        df_full = pd.read_pickle(self.full_data_path)

        self.logger.info("Merging dataframes.")
        df_merged = pd.merge(df_grouped, df_full[["numero_nucleo", "granja_global"]].drop_duplicates(), on="numero_nucleo", how="left")

        self.logger.info("Generating Markdown content.")
        markdown_content = "# Relatório de Geolocalização de Núcleos e Aviários\n\n"
        markdown_content += "Este documento apresenta uma tabela detalhada dos núcleos, seus aviários associados, proprietários, coordenadas geográficas, links diretos para o Google Maps e indicação se a granja é global.\n\n"
        markdown_content += "## Tabela de Núcleos e Aviários\n\n"
        markdown_content += "| Número do Núcleo | Aviários (Fazendas) | Nome do Proprietário | Coordenadas | Link Google Maps | Granja Global |\n"
        markdown_content += "|------------------|---------------------|----------------------|-------------|------------------|---------------|\n"

        for index, row in df_merged.iterrows():
            nucleo = row["numero_nucleo"]
            aviarios = ", ".join(map(str, row["aviario"]))
            proprietario = row["nome_proprietario"]
            coordenadas = row["coordenadas"]
            google_maps_link = row["google_maps_link"]
            granja_global = "Sim" if row["granja_global"] else "Não"
            
            granja_global_formatted = granja_global

            markdown_content += f"| {nucleo} | {aviarios} | {proprietario} | {coordenadas} | [Ver no Mapa]({google_maps_link}) | {granja_global_formatted} |\n"

        self.logger.info(f"Saving Markdown content to {self.output_path}")
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        self.logger.info("Markdown content for PDF generated successfully.")