#!/bin/bash
python src/01_generate_map_and_data.py
python src/02_clustering_and_routing.py
python src/03_evaluate_and_plot.py
echo "Execução completa. Cheque a pasta outputs/ para imagens e dados."
