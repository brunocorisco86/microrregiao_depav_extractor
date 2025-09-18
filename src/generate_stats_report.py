import pandas as pd
from src.utils.logger import get_logger

class StatsReportGenerator:
    """
    Generates a text file with statistics about the data.
    """
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.logger = get_logger(__name__)

    def generate(self):
        """
        Generates the statistics report.
        """
        self.logger.info(f"Loading data from {self.input_path}")
        df = pd.read_pickle(self.input_path)

        self.logger.info("Generating statistics report.")
        report_content = "Relatório de Estatísticas de Geolocalização\n\n"
        report_content += "==================================================\n\n"

        report_content += self._get_area_by_municipio(df)
        report_content += self._get_aviarios_by_extensionista(df)
        report_content += self._get_area_by_extensionista_m2(df)
        report_content += self._get_area_by_extensionista_km2(df)
        report_content += self._get_capacidade_by_extensionista(df)

        self.logger.info(f"Saving statistics report to {self.output_path}")
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        self.logger.info("Statistics report generated successfully.")

    def _get_area_by_municipio(self, df):
        content = "1. Área Total por Município (m²):\n"
        area_municipio = df.groupby("municipio")["area_m2"].sum().reset_index()
        for index, row in area_municipio.iterrows():
            content += f"- {row['municipio']}: {row['area_m2']:,.2f} m²\n"
        content += "\n"
        return content

    def _get_aviarios_by_extensionista(self, df):
        content = "2. Quantidade de Aviários por Extensionista:\n"
        aviarios_extensionista = df.groupby("tecnico_nome")["aviario"].count().reset_index()
        for index, row in aviarios_extensionista.iterrows():
            content += f"- {row['tecnico_nome']}: {row['aviario']} aviários\n"
        content += "\n"
        return content

    def _get_area_by_extensionista_m2(self, df):
        content = "3. Área Total (m²) por Extensionista:\n"
        area_extensionista_m2 = df.groupby("tecnico_nome")["area_m2"].sum().reset_index()
        for index, row in area_extensionista_m2.iterrows():
            content += f"- {row['tecnico_nome']}: {row['area_m2']:,.2f} m²\n"
        content += "\n"
        return content

    def _get_area_by_extensionista_km2(self, df):
        content = "4. Área Total (km²) por Extensionista:\n"
        area_extensionista_m2 = df.groupby("tecnico_nome")["area_m2"].sum().reset_index()
        area_extensionista_km2 = area_extensionista_m2.copy()
        area_extensionista_km2["area_km2"] = area_extensionista_km2["area_m2"] / 1_000_000
        for index, row in area_extensionista_km2.iterrows():
            content += f"- {row['tecnico_nome']}: {row['area_km2']:,.2f} km²\n"
        content += "\n"
        return content

    def _get_capacidade_by_extensionista(self, df):
        content = "5. Capacidade Total de Alojamento por Extensionista:\n"
        capacidade_extensionista = df.groupby("tecnico_nome")["capacidade_alojamento"].sum().reset_index()
        for index, row in capacidade_extensionista.iterrows():
            content += f"- {row['tecnico_nome']}: {row['capacidade_alojamento']:,.0f}\n"
        content += "\n"
        return content