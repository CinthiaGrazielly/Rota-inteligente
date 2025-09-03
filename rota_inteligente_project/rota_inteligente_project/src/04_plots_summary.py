
# Este script apenas carrega resultados e plota um comparativo simples

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

out = Path("../outputs")
routes = pd.read_csv(out / "routes_summary.csv")
metrics = {}
with open(out / "metrics.txt") as f:
    for line in f:
        k,v = line.strip().split('=')
        metrics[k]=float(v)

# Plot bar chart of distance per cluster
plt.figure(figsize=(8,5))
plt.bar(routes['cluster'].astype(str), routes['distance'].astype(float))
plt.xlabel('cluster')
plt.ylabel('distance (simulated)')
plt.title('Distância por cluster (simulação)')
plt.savefig(out / "distance_per_cluster.png", bbox_inches='tight', dpi=150)
print('Plotted distance_per_cluster.png')
