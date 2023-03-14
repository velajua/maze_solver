import os
import random
import matplotlib.pyplot as plt

from uuid import uuid4
from math import pi, cos, sin


FILE_PREF = 'maze_data' if 'maze_solver' in os.getcwd() else '/tmp/'


def random_letter_weighted_dict(num_nodes, num_edges, min_weight,
                                max_weight, directional=False, name_=None):
    nodes = [chr(i) for i in range(ord('A'), ord('A') + num_nodes)]
    graph = {node: {} for node in nodes}
    edges = set()
    while len(edges) < num_edges:
        u, v = random.sample(nodes, 2)
        if u != v:
            edges.add((u, v))
    for u, v in edges:
        if directional:
            weight_u_to_v = random.randint(min_weight, max_weight)
            weight_v_to_u = random.randint(min_weight, max_weight)
        else:
            weight = random.randint(min_weight, max_weight)
            weight_u_to_v = weight
            weight_v_to_u = weight
        graph[u][v] = weight_u_to_v
        graph[v][u] = weight_v_to_u
    with open(os.path.join(FILE_PREF, name_ + '.json'), 'w') as f:
        f.write(str(graph))
    return graph


def random_letter_dict(num_nodes, num_edges, directional=False, name_=None):
    nodes = [chr(i) for i in range(ord('A'), ord('A') + num_nodes)]
    graph = {node: [] for node in nodes}
    edges = set()
    while len(edges) < num_edges:
        u, v = random.sample(nodes, 2)
        if u != v:
            edges.add((u, v))
    for u, v in edges:
        if directional:
            graph[u].append(v)
        else:
            graph[u].append(v)
            graph[v].append(u)
    with open(os.path.join(FILE_PREF, name_ + '.json'), 'w') as f:
        f.write(str(graph))
    return graph


def draw_letter_weighted_dict(graph, weighted=False, name_='lettered', tries=0):
    try:
        fig, ax = plt.subplots(figsize=(15, 15))
        nodes = list(graph.keys())
        num_nodes, temp_ = len(nodes), []
        angle = 2 * pi / num_nodes
        for i, node in enumerate(nodes):
            x = cos(i * angle)/2.5 + 0.5
            y = sin(i * angle)/2.5 + 0.5
            ax.add_artist(plt.Circle((x, y), 0.03, color='r'))
            ax.text(x*1.01, y*1.01, node, fontsize=15)
            neighbors = graph[node]
            for neighbor, weight in neighbors.items():
                j = nodes.index(neighbor)
                xx = cos(j * angle)/2.5 + 0.5
                yy = sin(j * angle)/2.5 + 0.5
                mx = (x+xx)/2
                my = (y+yy)/2
                ax.annotate("", xy=(x, y), xytext=(xx, yy),
                            arrowprops=dict(arrowstyle="<->"))
                if weight > 0:
                    ax.text(mx-0.01 if ((mx, my) not in temp_ and weighted)
                            else mx, my-0.03 if ((mx, my) not in temp_ and weighted)
                            else my, str(weight), fontsize=15, color='blue')
            temp_.append((mx, my))
        ax.set_aspect('equal')
        if name_ == 'lettered':
            name_ = str(uuid4()) + '_' + name_
        fig.canvas.draw()
        fig.savefig(f := os.path.join(FILE_PREF, f"{name_}.png"))
        return fig, f
    except Exception:
        return draw_letter_weighted_dict(
            graph, weighted, name_, tries+1) if tries < 2 else 'Error'
