
from src.prepare_data import DataPreparer
from src.process_data import DataProcessor
from src.generate_kmz import KMLGenerator
from src.generate_kmz_polygons import KMLPolygonGenerator
from src.generate_microrregiao_csv import MicrorregiaoCSVGenerator
from src.generate_pdf_content import PDFContentGenerator
from src.generate_stats_report import StatsReportGenerator
from src.utils.logger import get_logger

def main():
    """
    Main function to run the entire data processing and report generation pipeline.
    """
    logger = get_logger(__name__)
    logger.info("Starting the data processing pipeline.")

    # Define file paths
    raw_data_path = "data/raw/coordenadas.csv"
    prepared_data_path = "data/processed/prepared_data.pkl"
    processed_data_path = "data/processed/processed_data.pkl"
    kml_output_path = "data/processed/geolocalizacao.kmz"
    kml_polygons_output_path = "data/processed/geolocalizacao_poligonos.kmz"
    microrregiao_csv_path = "docs/microrregioes_agregado.csv"
    pdf_content_path = "docs/relatorio_geolocalizacao.md"
    stats_report_path = "docs/relatorio_estatisticas.txt"

    # Prepare data
    data_preparer = DataPreparer(raw_data_path, prepared_data_path)
    data_preparer.prepare()

    # Process data
    data_processor = DataProcessor(prepared_data_path, processed_data_path)
    data_processor.process()

    # Generate KML file
    kml_generator = KMLGenerator(processed_data_path, raw_data_path, kml_output_path)
    kml_generator.generate()

    # Generate KML file with polygons
    kml_polygon_generator = KMLPolygonGenerator(raw_data_path, kml_polygons_output_path)
    kml_polygon_generator.generate()

    # Generate microrregiao CSV
    microrregiao_csv_generator = MicrorregiaoCSVGenerator(prepared_data_path, microrregiao_csv_path)
    microrregiao_csv_generator.generate()

    pdf_content_path = "docs/relatorio_geolocalizacao.pdf"

    # Generate PDF content
    pdf_content_generator = PDFContentGenerator(processed_data_path, prepared_data_path, pdf_content_path)
    pdf_content_generator.generate_pdf_report()

    # Generate stats report
    stats_report_generator = StatsReportGenerator(prepared_data_path, stats_report_path)
    stats_report_generator.generate()

    logger.info("Data processing pipeline finished successfully.")

if __name__ == "__main__":
    main()
