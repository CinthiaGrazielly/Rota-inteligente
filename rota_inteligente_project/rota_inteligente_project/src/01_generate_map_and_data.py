
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import random

out = Path("../outputs")
out.mkdir(parents=True, exist_ok=True)

# Parameters
GRID_N = 12  # grid size (12x12)
random.seed(42)
np.random.seed(42)

# Build grid graph with weights simulating travel time (distance * random factor)
G = nx.grid_2d_graph(GRID_N, GRID_N)
G = nx.convert_node_labels_to_integers(G, first_label=0)
pos = {n: (n % GRID_N, n // GRID_N) for n in G.nodes()}

for u,v in G.edges():
    # base euclidean distance
    x1,y1 = pos[u]; x2,y2 = pos[v]
    dist = ((x1-x2)**2 + (y1-y2)**2)**0.5
    # add small random factor to simulate varying street lengths/traffic
    weight = dist * (1 + 0.2 * random.random())
    G[u][v]['weight'] = weight

# Save graph edges to CSV
edges = []
for u,v,data in G.edges(data=True):
    edges.append({'u':u,'v':v,'weight':data['weight']})
pd.DataFrame(edges).to_csv(out / "graph_edges.csv", index=False)

# Generate delivery points (random sample of nodes)
NUM_DELIVERIES = 40
delivery_nodes = np.random.choice(list(G.nodes()), size=NUM_DELIVERIES, replace=False)
pd.DataFrame({'node': delivery_nodes}).to_csv(out / "delivery_nodes.csv", index=False)

# Draw graph and delivery points
plt.figure(figsize=(10,10))
nx.draw(G, pos=pos, node_size=20, linewidths=0.2, node_color='gray', edge_color='lightgray')
# highlight delivery nodes
xs = [pos[n][0] for n in delivery_nodes]
ys = [pos[n][1] for n in delivery_nodes]
plt.scatter(xs, ys, c='red', s=40, label='deliveries')
plt.title('Mapa (grafo) simplificado da cidade com pontos de entrega')
plt.axis('off')
plt.legend()
plt.savefig(out / "graph_map.png", bbox_inches='tight', dpi=150)
print('Graph and data generated: outputs/graph_map.png, graph_edges.csv, delivery_nodes.csv')
