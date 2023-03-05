import math
import heapq

from collections import deque
from queue import PriorityQueue

from typing import List, Dict, Union, Tuple, Callable, Any


def floyd_warshall(graph: List[List[Union[int, float]]],
                   type: str = 'matrix') -> Union[
                       List[List[Union[int, float]]],
                       Dict[str, Dict[str, Union[int, float]]]]:
    """
    Computes the shortest path between all pairs of nodes in a graph
    using the Floyd-Warshall algorithm.

    Args:
        graph (List[List[Union[int, float]]]): A square matrix representing
            the graph where the value at index (i, j) represents the weight of
            the edge from node i to node j. A value of float('inf') represents
            that there is no edge between the nodes.
        type (str, optional): The format to return the shortest path in.
            Valid options are 'matrix', 'letters', and 'coords'.
            Defaults to 'matrix'.

    Returns:
        Union[List[List[Union[int, float]]],
            Dict[str, Dict[str, Union[int, float]]]]:
        A matrix of the shortest path between all pairs of nodes
            if type is 'matrix'.
        A dictionary representation of the graph where each key
            is a node and the value is a dictionary of its neighbors
            and their weights if type is 'letters' or 'coords'.
    """
    if type not in ['matrix', 'letters', 'coords']:
        return f'type not allowed: {type}; matrix, letters, coords'

    def floyd_warshall_to_dict(matrix: List[List[Union[int, float]]],
                               type: str = 'letters') -> Dict[
                                   str, Dict[str, Union[int, float]]]:
        """
        Converts a matrix to a dictionary representation of a graph.

        Args:
            matrix (List[List[Union[int, float]]]): A square matrix
                representing the graph where the value at index (i, j)
                represents the weight of the edge from node i to node j.
                A value of float('inf') represents that there is no
                edge between the nodes.
            type (str, optional): The format to return the graph in.
                Valid options are 'letters' and 'coords'.
                Defaults to 'letters'.

        Returns:
            Dict[str, Dict[str, Union[int, float]]]: A dictionary
            representation of the graph where each key is a node
            and the value is a dictionary of its neighbors and
            their weights.
        """
        if type == 'letters':
            nodes = [chr(i) for i in range(ord('A'), ord('A') + len(matrix))]
            graph = {}
            for i in range(len(nodes)):
                node = nodes[i]
                graph[node] = {}
                for j in range(len(nodes)):
                    if matrix[i][j] != float('inf'):
                        neighbor = nodes[j]
                        weight = matrix[i][j]
                        graph[node][neighbor] = weight
            return graph
        elif type == 'coords':
            graph = {}
            for i in range(len(matrix)):
                row = matrix[i]
                for j in range(len(row)):
                    if row[j] != float('inf'):
                        graph[(i, j)] = {}
                        for k in range(len(row)):
                            if k != j and matrix[j][k] != float('inf'):
                                graph[(i, j)][
                                    (j, k)] = matrix[i][j] + matrix[j][k]
            return graph
        else:
            return 'Invalid type'

    n = len(graph)
    dist = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0
            elif graph[i][j] != 0:
                dist[i][j] = graph[i][j]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist if type == 'matrix' else floyd_warshall_to_dict(
        dist, 'letters') if type == 'letters' else floyd_warshall_to_dict(
            dist, 'coords')


def djikstra(graph: Dict[str, Dict[str, float]], start: str,
             goal: str) -> Union[None, Dict[str, Union[List[str], float]]]:
    """
    Finds the shortest path between two nodes in a graph
    using Dijkstra's algorithm.

    Args:
        graph: A dictionary representing the graph with nodes as keys
            and their neighbors and weights as values.
        start: A string representing the starting node.
        goal: A string representing the goal node.

    Returns:
        A dictionary containing the shortest path as a list of nodes
        and the total cost as a float, or None if no path exists.
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start, [])]
    while pq:
        curr_distance, curr_node, path = heapq.heappop(pq)
        if curr_distance > distances[curr_node]:
            continue
        if curr_node == goal:
            return {'path': path + [curr_node], 'cost': curr_distance}
        for neighbor, weight in graph[curr_node].items():
            distance = curr_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor, path + [curr_node]))
    return None


def a_star(graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]],
           start: Tuple[int, int],
           goal: Tuple[int, int],
           heuristic: Callable[[Tuple[int, int], Tuple[int, int]], int]
           = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
           ) -> Dict[str, Union[List[Tuple[int, int]], int]]:
    """
    A* algorithm implementation for finding the shortest path between
    two nodes in a graph.

    Args:
        graph: A dictionary containing the graph in the form of
            an adjacency list. Each node is a tuple of two integers
            representing its (x, y) coordinates and each edge is a
            dictionary containing the neighbor node as key and the
            cost of the edge as value.
        start: A tuple of two integers representing the starting
            node's (x, y) coordinates. goal: A tuple of two integers
            representing the goal node's (x, y) coordinates.
        heuristic: A heuristic function that takes two nodes as input
            and returns an estimate of the distance between them.
            The default heuristic is Manhattan distance.

    Returns:
        A dictionary containing the shortest path and its cost
        from the starting node to the goal node. The 'path' key
        contains a list of tuples representing the nodes along the path
        in the order they were visited, and the 'cost' key contains
        the total cost of the path.
    """
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    while not frontier.empty():
        _, current = frontier.get()
        if current == goal:
            break
        for neighbor, cost in graph[current].items():
            new_cost = cost_so_far[current] + cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(goal, neighbor)
                frontier.put((priority, neighbor))
                came_from[neighbor] = current
    current, path = goal,  []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    cost = 0
    for i in range(len(path)-1):
        cost += graph[path[i]][path[i+1]]
    return {'path': path, 'cost': cost}


def bfs(graph: Dict[str, Dict[str, int]], start: str, goal: str) -> Dict[
        str, Union[List[str], None]]:
    """
    Perform a breadth-first search on a graph.

    Args:
    - graph: A dictionary representing the graph where the keys are nodes
        and the values are dictionaries representing edges and weights
        between the nodes.
    - start: The starting node for the search.
    - goal: The goal node for the search.

    Returns:
    - A dictionary containing the shortest path from the start node to the
        goal node and the cost of the path.
    """
    frontier = deque([(start, 0)])
    came_from = {start: None}
    cost_so_far = {start: 0}
    while frontier:
        current, current_cost = frontier.popleft()
        if current == goal:
            break
        for neighbor in graph[current]:
            new_cost = current_cost + graph[current][neighbor]
            if neighbor not in came_from or new_cost < cost_so_far[neighbor]:
                frontier.append((neighbor, new_cost))
                came_from[neighbor] = current
                cost_so_far[neighbor] = new_cost
    if goal not in came_from:
        return {'path': [], 'cost': None}
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return {'path': path, 'cost': cost_so_far[goal]}


def dfs(graph: Dict[Tuple, Dict[Tuple, int]], start: Tuple,
        goal: Tuple) -> Dict[str, Union[List[Tuple], int]]:
    """
    Implements depth-first search algorithm to find path from start
    node to goal node in given graph.

    Args:
        graph: The graph to search, represented as a dictionary where
            ach key is a node and the corresponding value is a dictionary
            of its neighbors and edge costs.
        start: The starting node for the search.
        goal: The goal node to reach.

    Returns:
        A dictionary containing the path from start to goal, represented as
        a list of nodes in the order they were visited, and the cost of
        the path as an integer.
    """
    stack = [(start, 0)]
    came_from = {start: None}
    while stack:
        current, cost = stack.pop()
        if current == goal:
            break
        for neighbor, edge_cost in graph[current].items():
            if neighbor not in came_from:
                stack.append((neighbor, cost + edge_cost))
                came_from[neighbor] = (current, edge_cost)
    current, path, total_cost = goal, [], 0
    while current != start:
        path.append(current)
        edge_cost = came_from[current][1]
        total_cost += edge_cost
        current = came_from[current][0]
    path.append(start)
    path.reverse()
    return {'path': path, 'cost': total_cost}


def bellman_ford(graph: Dict[Any, Dict[Any, Union[int, float]]], start: Any,
                 goal: Any) -> Dict[str, Union[List[Any], Union[int, float]]]:
    """
    Finds the shortest path from a given starting node to a goal node in a
    weighted directed graph using the Bellman-Ford algorithm.

    Parameters:
    - `graph` (Dict): A dictionary representation of the graph where the keys
        represent the nodes and the values represent the outgoing
        edges from each node with their weights.
    - `start` (Any): The starting node from which to find the shortest path.
    - `goal` (Any): The goal node to which the shortest path needs to be found.

    Returns:
    - A dictionary with the following keys:
        - `'path'` (List): A list of nodes representing the shortest path from
            the starting node to the goal node.
        - `'cost'` (int or float): The total cost of the shortest path.
    """
    distance = {node: float('inf') for node in graph}
    distance[start] = 0
    predecessor = {node: None for node in graph}
    for i in range(len(graph) - 1):
        for u in graph:
            for v, weight in graph[u].items():
                if distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    predecessor[v] = u
    for u in graph:
        for v, weight in graph[u].items():
            if distance[u] + weight < distance[v]:
                raise ValueError("Graph contains a negative-weight cycle")
    current, path, cost = goal, [], 0
    while current != start:
        path.append(temp := current)
        current = predecessor[current]
        cost += graph[current][temp]
    path.append(start)
    path.reverse()
    return {'path': path, 'cost': cost}


def bidirectional_search(graph: Dict[Any, Dict[Any, float]],
                         start: Any, goal: Any) -> Dict[str, Any]:
    """
    Finds the shortest path between `start` and `goal` nodes in an
    undirected graph `graph` using bidirectional search algorithm.

    Args:
    - graph: A dictionary representing the undirected graph, where
        the keys are the nodes and the values are dictionaries
        representing the neighbors and edge weights of each node.
    - start: The node to start the search from.
    - goal: The node to find the shortest path to.

    Returns:
    - A dictionary containing the shortest path and its cost,
        with keys 'path' and 'cost'.
    """
    def get_path(forward_came_from: Dict[Any, Any],
                 backward_came_from: Dict[Any, Any],
                 intersection: Any) -> List:
        """
        Given the dictionaries of visited nodes and their parent
        nodes from both directions, and the intersection node that was found,
        constructs the shortest path between `start` and `goal`.

        Args:
        - forward_came_from: A dictionary representing the visited
            nodes and their parent nodes during the forward search.
        - backward_came_from: A dictionary representing the visited
            nodes and their parent nodes during the backward search.
        - intersection: The node that was found in both searches.

        Returns:
        - A list of nodes representing the shortest path
            between `start` and `goal`.
        """
        path = []
        node = intersection
        while node is not None:
            path.append(node)
            node = forward_came_from[node]
        path = path[::-1]
        node = backward_came_from[intersection]
        while node is not None:
            path.append(node)
            node = backward_came_from[node]
        return path

    forward_queue = [start]
    forward_came_from = {start: None}
    backward_queue = [goal]
    backward_came_from = {goal: None}
    intersection = None
    while forward_queue and backward_queue:
        if intersection:
            path = get_path(forward_came_from, backward_came_from,
                            intersection)
            cost = sum(graph[node1][node2] for node1, node2 in zip(
                path[:-1], path[1:]))
            return {'path': path, 'cost': cost}
        current = forward_queue.pop(0)
        for neighbor in graph[current]:
            if neighbor not in forward_came_from:
                forward_came_from[neighbor] = current
                forward_queue.append(neighbor)
            if neighbor in backward_came_from:
                intersection = neighbor
                break
        if intersection:
            path = get_path(forward_came_from, backward_came_from,
                            intersection)
            cost = sum(graph[node1][node2] for node1, node2 in zip(
                path[:-1], path[1:]))
            return {'path': path, 'cost': cost}
        current = backward_queue.pop(0)
        for neighbor in graph[current]:
            if neighbor not in backward_came_from:
                backward_came_from[neighbor] = current
                backward_queue.append(neighbor)
            if neighbor in forward_came_from:
                intersection = neighbor
                break
    return None


def beam_search(graph: Dict[str, Dict[str, int]], start: str, end: str,
                beam_width: int = 500) -> Dict[
                    str, Union[None, List[str], int]]:
    """
    Given a weighted graph, a start node, an end node and a beam width,
    returns the shortest path between the start and end node as well
    as the cost of the path using beam search algorithm.

    Args:
        graph (Dict[str, Dict[str, int]]): A weighted graph represented
            as a dictionary where keys are the node names and values are
            dictionaries representing the neighbors and their
            corresponding edge weights.
        start (str): The starting node name.
        end (str): The ending node name.
        beam_width (int, optional): The width of the beam. Defaults to 2.

    Returns:
        Dict[str, Union[None, List[str], int]]: A dictionary with the shortest
            path as a list of node names under the key 'path',
            the cost of the path under the key 'cost', and None for
            both if no path exists.
    """
    visited = set()
    queue = [(0, [start])]
    while queue:
        (cost, path) = queue.pop(0)
        node = path[-1]
        if node == end:
            return {'path': path, 'cost': cost}
        if node not in visited:
            visited.add(node)
            neighbors = graph[node]
            for neighbor, neighbor_cost in neighbors.items():
                if neighbor not in visited:
                    new_cost = cost + neighbor_cost
                    new_path = path + [neighbor]
                    queue.append((new_cost, new_path))
            queue = sorted(queue, key=lambda x: x[0])[:int(beam_width)]
    return {'path': None, 'cost': None}
