
import networkx as nx
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from heapq import heappush, heappop
from math import sqrt

out = Path("../outputs")
out.mkdir(parents=True, exist_ok=True)

# Utility: A* on the grid graph
def heuristic(a, b, pos):
    (x1,y1) = pos[a]; (x2,y2) = pos[b]
    return sqrt((x1-x2)**2 + (y1-y2)**2)

def astar_path(G, start, goal, pos):
    frontier = []
    heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    while frontier:
        _, current = heappop(frontier)
        if current == goal:
            break
        for nb in G.neighbors(current):
            new_cost = cost_so_far[current] + G[current][nb].get('weight', 1.0)
            if nb not in cost_so_far or new_cost < cost_so_far[nb]:
                cost_so_far[nb] = new_cost
                priority = new_cost + heuristic(nb, goal, pos)
                heappush(frontier, (priority, nb))
                came_from[nb] = current
    if goal not in came_from:
        return None, float('inf')
    # reconstruct path
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path, cost_so_far[goal]

# Load data
edges = pd.read_csv(out / "graph_edges.csv")
G = nx.Graph()
for _,r in edges.iterrows():
    G.add_edge(int(r.u), int(r.v), weight=float(r.weight))
pos = {n: (n % 12, n // 12) for n in G.nodes()}

delivery = pd.read_csv(out / "delivery_clusters.csv")

routes = {}
total_distance = 0.0

# For each cluster, build simple route: start at cluster centroid (approx), then NN heuristic to visit nodes
clusters = delivery.groupby('cluster')
for k,group in clusters:
    nodes = group['node'].tolist()
    # Start at the cluster center node (choose node nearest to centroid)
    centroid = group[['x','y']].mean().values
    start_node = min(nodes, key=lambda n: ((pos[n][0]-centroid[0])**2 + (pos[n][1]-centroid[1])**2))
    sequence = [start_node]
    remaining = set(nodes) - {start_node}
    current = start_node
    while remaining:
        # choose nearest in euclidean space (heuristic)
        next_node = min(remaining, key=lambda n: ((pos[n][0]-pos[current][0])**2 + (pos[n][1]-pos[current][1])**2))
        sequence.append(next_node)
        remaining.remove(next_node)
        current = next_node
    # build full path using A* between sequence nodes
    path_full = []
    dist_cluster = 0.0
    for i in range(len(sequence)-1):
        p, d = astar_path(G, sequence[i], sequence[i+1], pos)
        if p is None:
            continue
        if i>0:
            # avoid duplicating intermediate node
            path_full.extend(p[1:])
        else:
            path_full.extend(p)
        dist_cluster += d
    routes[k] = {'sequence': sequence, 'path': path_full, 'distance': dist_cluster}
    total_distance += dist_cluster

# Save routes summary
rows = []
for k,v in routes.items():
    rows.append({'cluster': k, 'sequence': v['sequence'], 'distance': v['distance']})
pd.DataFrame(rows).to_csv(out / "routes_summary.csv", index=False)

# Plot full map with routes (each cluster a different color)
plt.figure(figsize=(10,10))
nx.draw(G, pos=pos, node_size=10, node_color='lightgray', edge_color='lightgray')
colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown']
for k,v in routes.items():
    path = v['path']
    xs = [pos[n][0] for n in path]; ys = [pos[n][1] for n in path]
    plt.plot(xs, ys, '-', linewidth=2, label=f'cluster {k} (d={v["distance"]:.2f})')
    # mark sequence nodes
    seq = v['sequence']
    sx = [pos[n][0] for n in seq]; sy=[pos[n][1] for n in seq]
    plt.scatter(sx, sy, s=50)
plt.legend()
plt.title('Rotas por cluster (heurística NN + A*)')
plt.axis('off')
plt.savefig(out / "routes_by_cluster.png", bbox_inches='tight', dpi=150)

# Save total distance metric
with open(out / "metrics.txt", "w") as f:
    f.write(f"total_distance={total_distance}\n")
print('Routes computed and visualized. Check outputs/routes_by_cluster.png and outputs/routes_summary.csv')
