# Instruções de Uso do Extrator de Microrregiões e Geolocalização

Este documento fornece instruções sobre como usar o sistema de extração e geolocalização de dados, que foi refatorado para seguir princípios de Programação Orientada a Objetos (POO) e inclui um sistema de logging para maior verbosidade.

## Estrutura do Projeto

```
coordenadas_microrregiao/
├── assets/
│   └── template.csv
├── data/
│   ├── processed/
│   │   ├── geolocalizacao_poligonos.kmz
│   │   ├── geolocalizacao.kmz
│   │   ├── prepared_data.pkl
│   │   └── processed_data.pkl
│   └── raw/
│       └── coordenadas.csv
├── docs/
│   ├── microrregioes_agregado.csv
│   ├── relatorio_estatisticas.txt
│   ├── relatorio_geolocalizacao_atualizado.pdf
│   ├── relatorio_geolocalizacao.md
│   └── relatorio_geolocalizacao.pdf
├── src/
│   ├── generate_kmz_polygons.py
│   ├── generate_kmz.py
│   ├── generate_microrregiao_csv.py
│   ├── generate_pdf_content.py
│   ├── generate_stats_report.py
│   ├── prepare_data.py
│   ├── process_data.py
│   └── utils/
│       └── logger.py
├── .gitignore
├── main.py
└── requirements.txt
```

## Pré-requisitos

Certifique-se de ter o Python 3 instalado. As dependências do projeto estão listadas no arquivo `requirements.txt`. Para instalá-las, execute:

```bash
pip install -r requirements.txt
```

## Preparação dos Dados

O sistema espera um arquivo CSV com os dados brutos na pasta `data/raw/coordenadas.csv`. Um template para este arquivo pode ser encontrado em `assets/template.csv`.

### `assets/template.csv`

Este arquivo define a estrutura esperada para os dados de entrada. As colunas são:

- `fazenda`: Nome da fazenda/aviário.
- `proprietario`: Nome do proprietário.
- `cidade`: Cidade onde o aviário está localizado.
- `nome_tecnico`: Nome do técnico responsável.
- `nucleo`: Número do núcleo.
- `microrregiao`: Microrregião a qual pertence.
- `area`: Área em m².
- `capacidade`: Capacidade de alojamento.
- `dist_fab_1`: Distância para a fábrica 1.
- `dist_fab_2`: Distância para a fábrica 2.
- `global_gap`: Indica se é uma granja global (Verdadeiro/Falso).
- `bp_associado`: BP Associado.
- `coordenadas`: Coordenadas geográficas (latitude,longitude).

Certifique-se de que seu arquivo `coordenadas.csv` siga este formato.

## Executando o Pipeline

Para executar todo o pipeline de processamento de dados e geração de relatórios, execute o script `main.py` a partir da raiz do projeto:

```bash
python main.py
```

O script `main.py` orquestra as seguintes etapas:

1.  **`DataPreparer` (src/prepare_data.py):** Carrega o `coordenadas.csv`, limpa e renomeia colunas, trata valores ausentes, converte tipos de dados e salva o DataFrame processado em `data/processed/prepared_data.pkl`.
2.  **`DataProcessor` (src/process_data.py):** Carrega os dados preparados, agrupa-os por número de núcleo e salva o DataFrame agrupado em `data/processed/processed_data.pkl`.
3.  **`KMLGenerator` (src/generate_kmz.py):** Gera um arquivo KMZ (`data/processed/geolocalizacao.kmz`) com pontos para núcleos, organizados por município, extensionista e microrregião.
4.  **`KMLPolygonGenerator` (src/generate_kmz_polygons.py):** Gera um arquivo KMZ (`data/processed/geolocalizacao_poligonos.kmz`) com polígonos representando as áreas de atuação de extensionistas, municípios, microrregiões e círculos de 500m ao redor dos núcleos.
5.  **`MicrorregiaoCSVGenerator` (src/generate_microrregiao_csv.py):** Gera um arquivo CSV (`docs/microrregioes_agregado.csv`) com dados agregados por microrregião.
6.  **`PDFContentGenerator` (src/generate_pdf_content.py):** Gera o conteúdo Markdown para o relatório de geolocalização (`docs/relatorio_geolocalizacao.md`). Este arquivo pode ser convertido para PDF usando ferramentas externas.
7.  **`StatsReportGenerator` (src/generate_stats_report.py):** Gera um relatório de estatísticas em formato de texto (`docs/relatorio_estatisticas.txt`).

## Saídas Geradas

Após a execução do `main.py`, os seguintes arquivos serão gerados ou atualizados:

-   **`data/processed/geolocalizacao.kmz`**: Arquivo KMZ com pontos de geolocalização.
-   **`data/processed/geolocalizacao_poligonos.kmz`**: Arquivo KMZ com polígonos e círculos de geolocalização.
-   **`docs/microrregioes_agregado.csv`**: CSV com dados agregados por microrregião.
-   **`docs/relatorio_geolocalizacao.md`**: Conteúdo Markdown para o relatório de geolocalização.
-   **`docs/relatorio_estatisticas.txt`**: Relatório de estatísticas em texto.

## Logging

O módulo `src/utils/logger.py` configura um logger que exibe mensagens informativas durante a execução do pipeline, ajudando a acompanhar o progresso e identificar possíveis problemas.

## Contribuição

Para contribuir com o projeto, siga as boas práticas de Git, criando branches para novas funcionalidades ou correções e enviando Pull Requests para a branch `main`.
