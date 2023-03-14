import os
import random
import matplotlib.pyplot as plt

from uuid import uuid4
from math import pi, cos, sin

from typing import Dict, List, Optional, Union, Tuple

FILE_PREF = 'maze_data' if 'maze_solver' in os.getcwd() else '/tmp/'


def random_letter_weighted_dict(num_nodes: int, num_edges: int,
                                min_weight: int, max_weight: int,
                                directional: bool = False,
                                name_: str = None
                                ) -> Dict[str, Dict[str, int]]:
    """
    Generates a random undirected or directed graph with
    weighted edges and returns it as a dictionary.

    Args:
        num_nodes (int): The number of nodes in the graph.
        num_edges (int): The number of edges in the graph.
        min_weight (int): The minimum weight of an edge.
        max_weight (int): The maximum weight of an edge.
        directional (bool, optional): If True, the graph is directed.
            If False, the graph is undirected. Defaults to False.
        name_ (str, optional): The name of the file to save the
            graph to as a JSON object. Defaults to None.

    Returns:
        Dict[str, Dict[str, int]]: A dictionary representing the graph.
            The keys are the node labels and the values are dictionaries of
        neighbor node labels and edge weights.
    """
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


def random_letter_dict(num_nodes: int, num_edges: int,
                       directional: bool = False, name_: Optional[str] = None
                       ) -> Dict[str, List[str]]:
    """
    Generates a random undirected or directed graph
    and returns it as a dictionary.

    Args:
        num_nodes (int): The number of nodes in the graph.
        num_edges (int): The number of edges in the graph.
        directional (bool, optional): If True, the graph is directed.
            If False, the graph is undirected. Defaults to False.
        name_ (str, optional): The name of the file to save the graph
            to as a JSON object. Defaults to None.

    Returns:
        Dict[str, List[str]]: A dictionary representing the graph.
            The keys are the node labels and the values are lists of neighbor
        node labels.
    """
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


def draw_letter_weighted_dict(
    graph: Dict[str, Dict[str, Union[int, float]]],
    weighted: bool = False,
    name_: str = 'lettered',
    tries: int = 0) -> Union[str, Tuple[plt.Figure, str]]:
    """
    Draws a graph visualization of a letter-labeled
    weighted dictionary graph.

    Parameters:
    graph (Dict[str, Dict[str, Union[int, float]]]):
        A dictionary representing the graph
        with nodes labeled with letters and weighted edges.
    weighted (bool): A flag indicating if the graph has weighted edges.
        Default is False.
    name_ (str): The name of the file to save the visualization image.
        Default is "lettered".
    tries (int): The number of attempts to draw the graph. Default is 0.

    Returns:
    Union[str, Tuple[plt.Figure, str]]: Returns a tuple of the
        matplotlib Figure object and the filename of the saved image.
        If an error occurs, returns "Error" string or retries
        the function up to 2 times.
    """
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
                            else mx, my-0.03
                            if ((mx, my) not in temp_ and weighted)
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


def random_coords_graph(num_nodes: int, num_edges: int, min_weight: int,
                        max_weight: int, directional: bool = False,
                        name_: str = None
                        ) -> Dict[Tuple[int, int], Dict[Tuple[int, int], int]]:
    """
    Generates a random graph with coordinates as nodes and random weights.

    Args:
        num_nodes (int): The number of nodes in the graph.
        num_edges (int): The number of edges in the graph.
        min_weight (int): The minimum weight for the edges.
        max_weight (int): The maximum weight for the edges.
        directional (bool): If True, the graph is directed.
            Otherwise, it is undirected. Default is False.
        name_ (str): The name of the file to save the generated graph.
            Default is None.

    Returns:
        dict: A dictionary representing the generated graph.
            The keys are tuples of coordinates and the values
        are dictionaries representing the adjacent nodes and their weights.
    """
    nodes = [(i, j) for i in range(num_nodes) for j in range(num_nodes)]
    graph = {node: {} for node in nodes}
    edges = set()
    while len(edges) < num_edges:
        u, v = random.sample(nodes, 2)
        if u != v and v not in graph[u]:
            edges.add((u, v))
    for u, v in edges:
        weight = random.randint(min_weight, max_weight)
        graph[u][v] = weight
        if not directional:
            graph[v][u] = weight
    with open(os.path.join(FILE_PREF, name_ + '.json'), 'w') as f:
        f.write(str(graph))
    return graph


def draw_random_coords_graph(
        graph: Dict[Tuple[float, float], Dict[Tuple[float, float], float]],
        name_: str = 'coords') -> Tuple[plt.Figure, str]:
    """
    Draws a graph represented as a dictionary with nodes as keys and
    their connections as values, as a random coordinates graph.

    Args:
    - graph: A dictionary with nodes as keys, and their connections
        represented as a nested dictionary with connection nodes as
        keys and their weights as values.
    - name_: Optional. The name to be given to the saved image file.
        Defaults to 'coords'.

    Returns:
    - fig: The matplotlib Figure object.
    - f: The path to the saved image file.
    """
    fig, ax = plt.subplots(figsize=(15, 15))
    for node, connections in graph.items():
        for connection, weight in connections.items():
            ax.plot([node[0], connection[0]], [node[1], connection[1]],
                    'k-')
            x = (node[0] + connection[0]) / 2
            y = (node[1] + connection[1]) / 2
            ax.text(x, y, str(weight), fontsize=15, ha='center',
                    va='center', color='blue')
            ax.text(node[0], node[1], str(node), fontsize=15, ha='center',
                    va='center', color='red')
            ax.text(connection[0], connection[1], str(connection),
                    fontsize=15, ha='center', va='center', color='red')
    if name_ == 'coords':
        name_ = str(uuid4()) + '_' + name_
    fig.canvas.draw()
    fig.savefig(f := os.path.join(FILE_PREF, f"{name_}.png"))
    return fig, f


def random_weighted_adjacency_matrix(num_nodes: int, num_edges: int,
                                     min_weight: int, max_weight: int,
                                     name_: str = None) -> List[List[int]]:
    """
    Generates a random weighted adjacency matrix for a graph with a
    given number of nodes and edges. The weights of the edges are
    randomly generated between the given minimum and maximum weights.

    Args:
    - num_nodes (int): The number of nodes in the graph.
    - num_edges (int): The number of edges in the graph.
    - min_weight (int): The minimum weight of an edge.
    - max_weight (int): The maximum weight of an edge.
    - name_ (str): The name of the file to write the adjacency matrix to.

    Returns:
    - List[List[int]]: The random weighted adjacency matrix for the graph.
    """
    adjacency_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    edges = set()
    while len(edges) < num_edges:
        u, v = random.sample(range(num_nodes), 2)
        if u != v and (u, v) not in edges:
            edges.add((u, v))
            edges.add((v, u))
            weight = random.randint(min_weight, max_weight)
            adjacency_matrix[u][v] = weight
            adjacency_matrix[v][u] = weight
    with open(os.path.join(FILE_PREF, name_ + '.json'), 'w') as f:
        f.write(str(adjacency_matrix))
    return adjacency_matrix


def draw_adjacency_matrix(matrix: List[List[int]],
                          name_: str = 'matrix') -> Tuple[plt.Figure, str]:
    """
    Draws a graph's adjacency matrix with weighted edges.

    Args:
    - matrix (List[List[int]]): The adjacency matrix for the graph.
    - name_ (str): The name to save the figure as.

    Returns:
    - Tuple[plt.Figure, str]: The figure object and the filename.
    """
    fig, ax = plt.subplots(figsize=(len(matrix)/2, len(matrix)/2))
    nodes = [chr(65+i) for i in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > 0:
                ax.plot([i, j], [j, i], 'bo-',
                        linewidth=matrix[i][j]/2, markersize=10)
                ax.annotate(str(matrix[i][j]), ((i+j)/2, (i+j)/2),
                            fontsize=15)
    for i, node in enumerate(nodes):
        ax.annotate(node, (i, -0.1), xycoords='data', ha='center',
                    va='center', color='black', fontsize=15)
        ax.annotate(node, (-0.1, i), xycoords='data', ha='center',
                    va='center', color='black', fontsize=15)
    ax.axis('off')
    if name_ == 'matrix':
        name_ = str(uuid4()) + '_' + name_
    fig.canvas.draw()
    fig.savefig(f := os.path.join(FILE_PREF, f"{name_}.png"))
    return fig, f
