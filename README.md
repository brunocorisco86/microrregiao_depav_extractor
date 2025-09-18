# microrregiao_depav_extractor

Este repositório contém um sistema para processar dados de coordenadas, gerar arquivos KMZ para geolocalização de microrregiões e aviários, e produzir diversos relatórios. O projeto foi refatorado para seguir princípios de Programação Orientada a Objetos (POO) e inclui um sistema de logging robusto para maior verbosidade durante a execução.

## Funcionalidades Principais

-   **Processamento de Dados:** Carrega e prepara dados brutos de coordenadas.
-   **Geração de KMZ:** Cria arquivos KMZ com pontos e polígonos para visualização no Google Earth, organizados por município, extensionista e microrregião.
-   **Relatórios:** Gera relatórios estatísticos e um arquivo Markdown para posterior conversão em PDF, detalhando núcleos, aviários e outras informações relevantes.
-   **Estrutura Modular:** Código organizado em classes para facilitar a manutenção e escalabilidade.
-   **Logging:** Verbose logging para acompanhar o fluxo de execução e depuração.

## Como Usar

Para instruções detalhadas sobre como configurar o ambiente, preparar os dados de entrada, executar o pipeline e entender as saídas geradas, por favor, consulte o arquivo `docs/instructions.md`.

## Estrutura do Projeto

```
coordenadas_microrregiao/
├── assets/
│   └── template.csv             # Template para o arquivo CSV de entrada
├── data/
│   ├── processed/               # Dados processados e arquivos KMZ gerados
│   └── raw/                     # Dados brutos de entrada (coordenadas.csv)
├── docs/                        # Documentação e relatórios gerados
│   └── instructions.md          # Instruções detalhadas de uso
├── src/                         # Código fonte organizado em módulos e classes
│   └── utils/                   # Utilitários (ex: logger.py)
├── .gitignore                   # Arquivos e diretórios a serem ignorados pelo Git
├── main.py                      # Ponto de entrada principal para executar o pipeline
└── requirements.txt             # Dependências do projeto
```

## Contribuição

Sinta-se à vontade para contribuir com o projeto. Por favor, siga as boas práticas de Git, criando branches para novas funcionalidades ou correções e enviando Pull Requests para a branch `main`.