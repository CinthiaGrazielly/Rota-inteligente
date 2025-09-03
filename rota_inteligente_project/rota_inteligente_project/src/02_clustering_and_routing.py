
import networkx as nx
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from pathlib import Path
import matplotlib.pyplot as plt
from math import sqrt

out = Path("../outputs")
out.mkdir(parents=True, exist_ok=True)

# Load data
edges = pd.read_csv(out / "graph_edges.csv")
delivery = pd.read_csv(out / "delivery_nodes.csv")['node'].values

# Reconstruct graph
G = nx.Graph()
for _,r in edges.iterrows():
    G.add_edge(int(r.u), int(r.v), weight=float(r.weight))
pos = {n: (n % 12, n // 12) for n in G.nodes()}

# Prepare points for clustering (use coordinates)
coords = np.array([pos[n] for n in delivery])

# Choose K using simple rule: one deliverer per ~8 deliveries, min 2, max 6
K = max(2, min(6, len(delivery)//8 + 1))
kmeans = KMeans(n_clusters=K, random_state=42).fit(coords)
labels = kmeans.labels_

# Save clusters to CSV
df = pd.DataFrame({'node': delivery, 'x': coords[:,0], 'y': coords[:,1], 'cluster': labels})
df.to_csv(out / "delivery_clusters.csv", index=False)

# Plot clusters
plt.figure(figsize=(8,8))
for k in range(K):
    c = df[df.cluster==k]
    plt.scatter(c.x, c.y, label=f'cluster {k}', s=50)
centers = kmeans.cluster_centers_
plt.scatter(centers[:,0], centers[:,1], marker='X', s=150, label='centers')
plt.title(f'Clusters de entregas (K={K})')
plt.legend()
plt.savefig(out / f"clusters_k{K}.png", bbox_inches='tight', dpi=150)
print('Clusters saved to outputs/delivery_clusters.csv and clusters image.')
