import pandas as pd
from src.utils.logger import get_logger
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch

class PDFContentGenerator:
    """
    Generates the Markdown and PDF content for the report.
    """
    def __init__(self, grouped_data_path, full_data_path, output_path):
        self.grouped_data_path = grouped_data_path
        self.full_data_path = full_data_path
        self.output_path = output_path
        self.logger = get_logger(__name__)
        self.styles = getSampleStyleSheet()

    def generate_markdown_report(self):
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

    def generate_pdf_report(self):
        """
        Generates a PDF report with a table of microrregioes, proprietarios-nucleos, and aviarios.
        """
        self.logger.info(f"Loading grouped data from {self.grouped_data_path}")
        df_grouped = pd.read_pickle(self.grouped_data_path)
        self.logger.info(f"Loading full data from {self.full_data_path}")
        df_full = pd.read_pickle(self.full_data_path)

        self.logger.info("Merging dataframes for PDF report.")
        # Ensure 'microrregiao' is in df_grouped or df_full, assuming it's in df_grouped for now
        # Also assuming 'numero_nucleo' is the common key
        df_merged = pd.merge(df_grouped, df_full, on="numero_nucleo", how="left", suffixes=('_grouped', '_full'))

        # Prepare 'proprietario-nucleo' column
        df_merged['proprietario-nucleo'] = df_merged['nome_proprietario_grouped'] + ' - ' + df_merged['numero_nucleo'].astype('Int64').astype(str)

        # Prepare 'Aviários do nucleo' (melt)
        # Assuming 'aviario' is a list of aviaries per nucleo in df_grouped
        df_merged['Aviários do nucleo'] = df_merged['aviario_grouped'].apply(lambda x: ", ".join(map(str, x)))

        # Group by microrregiao, proprietario-nucleo, and Aviários do nucleo to eliminate duplicates in columns 2 and 3
        # and aggregate coordinates and google maps links
        df_final_report = df_merged.groupby(['microrregiao_grouped', 'proprietario-nucleo', 'Aviários do nucleo']).agg(
            coordenadas_full=('coordenadas_full', lambda x: x.dropna().astype(str).iloc[0] if not x.dropna().empty else '&nbsp;'),
            google_maps_link_full=('google_maps_link_full', lambda x: x.dropna().astype(str).iloc[0] if not x.dropna().empty else '#')
        ).reset_index()

        # Sort data
        df_final_report = df_final_report.sort_values(by=['microrregiao_grouped', 'proprietario-nucleo']).reset_index(drop=True)

        # PDF generation setup
        doc = SimpleDocTemplate(self.output_path, pagesize=letter)
        elements = []

        # Title
        elements.append(Paragraph("Relatório Detalhado de Microrregiões e Aviários", self.styles['h1']))
        elements.append(Spacer(1, 0.2 * inch))

        # Prepare table data
        table_data = [['Micro', 'Prop - Núcleo', 'Aviarios', 'Coordenadas', 'Google Maps']]
        
        # Initialize table style commands
        table_style_commands = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('WORDWRAP', (1, 1), (4, -1)), # Apply word wrap to proprietario-nucleo, aviarios, coordenadas, and google maps link
            ('ALIGN', (1, 1), (4, -1), 'LEFT'), # Align content left for wrapped text
        ]

        last_microrregiao = None
        microrregiao_start_row = 1 # Start from 1 because of header row

        for index, row in df_final_report.iterrows():
            microrregiao = row['microrregiao_grouped'] if pd.notna(row['microrregiao_grouped']) else '&nbsp;'
            proprietario_nucleo_text = row['proprietario-nucleo'] if pd.notna(row['proprietario-nucleo']) else '&nbsp;'
            proprietario_nucleo = Paragraph(proprietario_nucleo_text, self.styles['Normal'])
            aviarios_do_nucleo_text = row['Aviários do nucleo'] if pd.notna(row['Aviários do nucleo']) else '&nbsp;'
            aviarios_do_nucleo = Paragraph(aviarios_do_nucleo_text, self.styles['Normal'])
            coordenadas_text = row['coordenadas_full'] if pd.notna(row['coordenadas_full']) else '&nbsp;'
            coordenadas = Paragraph(coordenadas_text.replace(',', '<br/>'), self.styles['Normal'])
            google_maps_link_text = row['google_maps_link_full'] if pd.notna(row['google_maps_link_full']) else '#'
            google_maps_link = Paragraph(f"<font color=\"blue\"><a href=\"{google_maps_link_text}\">Google Maps</a></font>", self.styles['Normal'])
            
            if last_microrregiao is not None and microrregiao != last_microrregiao:
                current_microrregiao_cell = microrregiao
            elif last_microrregiao is None:
                current_microrregiao_cell = microrregiao
            else:
                current_microrregiao_cell = '' # Empty string for visually merged cells

            table_data.append([current_microrregiao_cell, proprietario_nucleo, aviarios_do_nucleo, coordenadas, google_maps_link])

            last_microrregiao = microrregiao
        
        table = Table(table_data, colWidths=[doc.width/5.0]*5) # Distribute width evenly among 5 columns
        table.setStyle(TableStyle(table_style_commands))
        elements.append(table)

        self.logger.info(f"Saving PDF report to {self.output_path}")
        doc.build(elements)
        self.logger.info("PDF report generated successfully.")