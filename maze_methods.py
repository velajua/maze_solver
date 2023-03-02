import os
import random

from uuid import uuid4
from PIL import Image, ImageDraw

from typing import Dict, Tuple, Optional, Union, List

FILE_PREF = 'maze_data' if 'maze_algorithms' in os.getcwd() else '/tmp/'


def generate_maze_(width: int, height: int, strict: float = 0.9, add_weights_prob: float = 0.2,
                   name_: str = None) -> Dict[Tuple[int, int], Dict[Tuple[int, int], int]]:
    """
    Generates a maze using a modified version of the Depth-First Search algorithm.

    Args:
        width (int): The width of the maze.
        height (int): The height of the maze.
        strict (float, optional): The strictness of the maze. A value between 0 and 1,
            where 1 generates a perfect maze. Defaults to 0.9.
        add_weights_prob (float, optional): The probability of adding weights to the edges.
            A value between 0 and 1. Defaults to 0.2.
        name_ (str, optional): The name of the file where the maze will be saved.
            Defaults to None.

    Returns:
        Dict[Tuple[int, int], Dict[Tuple[int, int], int]]: The maze represented as a
            dictionary of dictionaries. The keys of the outer dictionary are the coordinates
            of the cells, and the values are dictionaries containing the neighbors of the
            cells and the weights of the edges that connect them.
    """
    maze = {}
    for x in range(width):
        for y in range(height):
            maze[(x, y)] = {}
    for x in range(width):
        for y in range(height):
            if x > 0:
                maze[(x, y)][(x-1, y)] = 100
            if x < width - 1:
                maze[(x, y)][(x+1, y)] = 100
            if y > 0:
                maze[(x, y)][(x, y-1)] = 100
            if y < height - 1:
                maze[(x, y)][(x, y+1)] = 100
    visited = []
    stack = [(0, 0)]
    while stack:
        current = stack[-1]
        visited.append(current)
        unvisited_neighbors = []
        for neighbor in maze[current]:
            if neighbor not in visited:
                unvisited_neighbors.append(neighbor)
        if unvisited_neighbors:
            neighbor = random.choice(unvisited_neighbors)
            maze[current][neighbor] = 0
            maze[neighbor][current] = 0
            if random.random() <= add_weights_prob:
                weight = random.randint(1, 10)
                maze[current][neighbor] = weight
                maze[neighbor][current] = weight
            if random.randint(1, 10) <= 10*(1-strict):
                neighbor = random.choice(unvisited_neighbors)
                maze[current][neighbor] = 0
                maze[neighbor][current] = 0
                if random.random() <= add_weights_prob:
                    weight = random.randint(1, 10)
                    maze[current][neighbor] = weight
                    maze[neighbor][current] = weight
            stack.append(neighbor)
        else:
            stack.pop()
    with open(os.path.join(FILE_PREF, name_ + '.json'), 'w') as f:
        f.write(str(maze))
    return maze


def draw_maze(maze: Dict[Tuple[int, int], Dict[Tuple[int, int], int]],
              path: Optional[Dict[str, Union[int, List[Tuple[int, int]]]]
                             ] = None, name_: str = 'maze') -> Tuple[Image.Image, str]:
    """
    Draws a maze represented as a dictionary of coordinates and walls.

    Args:
        maze: A dictionary of coordinates and their connected walls.
        path: An optional dictionary containing the path taken through the maze and its cost.
        name_: An optional name for the saved image file.

    Returns:
        A tuple containing the drawn image and the file path.
    """
    max_x = max(coord[0] for coord in maze.keys())
    max_y = max(coord[1] for coord in maze.keys())
    cell_size = 20
    wall_size = 3
    image_width = max_x * cell_size + wall_size + cell_size
    image_height = max_y * cell_size + wall_size + cell_size
    img = Image.new("RGB", (image_width, image_height), "white")
    img_draw = ImageDraw.Draw(img)
    for coord, walls in maze.items():
        x, y = coord
        for neighbor, wall in walls.items():
            weight = 255 - wall * 25
            color = (255, weight, weight)
            if wall == 100:
                dx = neighbor[0] - x
                dy = neighbor[1] - y
                if dx == 1:
                    x1 = (x + 1) * cell_size + wall_size // 2
                    y1 = y * cell_size + wall_size // 2
                    x2 = x1
                    y2 = (y + 1) * cell_size - wall_size // 2
                elif dx == -1:
                    x1 = x * cell_size + wall_size // 2
                    y1 = y * cell_size + wall_size // 2
                    x2 = x1
                    y2 = (y + 1) * cell_size - wall_size // 2
                elif dy == 1:
                    x1 = x * cell_size + wall_size // 2
                    y1 = (y + 1) * cell_size + wall_size // 2
                    x2 = (x + 1) * cell_size - wall_size // 2
                    y2 = y1
                elif dy == -1:
                    x1 = x * cell_size + wall_size // 2
                    y1 = y * cell_size + wall_size // 2
                    x2 = (x + 1) * cell_size - wall_size // 2
                    y2 = y1
                img_draw.line((x1, y1, x2, y2), fill="black", width=wall_size)
            else:
                if wall != 0:
                    dx = neighbor[0] - x
                    dy = neighbor[1] - y
                    x1 = coord[0] * cell_size + wall_size
                    y1 = coord[1] * cell_size + wall_size
                    x2 = (coord[0] + 1) * cell_size - wall_size
                    y2 = (coord[1] + 1) * cell_size - wall_size
                    img_draw.rectangle((x1, y1, x2, y2), fill=color)
                    img_draw.text((x1, y1), text=str(wall), fill='black')
                    img_draw = ImageDraw.Draw(img)
                    if dx > 0:
                        img_draw.polygon([(x2-wall_size*2, y2-wall_size*2), (x2-wall_size*2, y2), (x2-wall_size, y2-wall_size)], fill="black")
                    elif dx < 0:
                        img_draw.polygon([(x2-wall_size, y2), (x2-wall_size, y2-wall_size*2), (x2-wall_size*2, y2-wall_size)], fill="black")
                    elif dy > 0:
                        img_draw.polygon([(x2-wall_size*2, y1+wall_size*3), (x2, y1+wall_size*3), (x2-wall_size, y1+wall_size*4)], fill="black")
                    elif dy < 0:
                        img_draw.polygon([(x2, y1+wall_size*4), (x2-wall_size*2, y1+wall_size*4), (x2-wall_size, y1+wall_size*3)], fill="black")
    img_draw.ellipse((cell_size//2-3, cell_size//2-3, cell_size//2+3, cell_size//2+3), fill="green", outline="green")
    img_draw.ellipse((image_width-cell_size//2-3, image_height-cell_size//2-3, image_width-cell_size//2+3, image_height-cell_size//2+3), fill="red", outline="red")
    if name_ == 'maze':
        name_ = str(uuid4()) + '_' + name_
    if path:
        path_coords = [(coord[0] * cell_size + cell_size // 2, coord[1] * cell_size + cell_size // 2) for coord in path['path']]
        img_draw.line(path_coords, fill="blue", width=4)
        img.save(f := os.path.join(FILE_PREF, f"{name_}_{path.get('cost', '')}_solution.png"))
    else:
        img.save(f := os.path.join(FILE_PREF, f"{name_}.png"))
    return img, f


def filter_maze_passages(maze: Dict[str, Dict[str, int]]
                         ) -> Dict[str, Dict[str, int]]:
    """
    Filters out any closed passages from the given maze.

    Args:
        maze (Dict[str, Dict[str, int]]): A dictionary
        representing the maze where each key represents a cell
        and each value represents a dictionary of adjacent cells
        and their weights.

    Returns:
        Dict[str, Dict[str, int]]: A filtered version of the
        maze dictionary containing only open passages where each key
        represents a cell and each value represents a dictionary
        of adjacent cells and their weights.
    """
    open_passages = {}
    for cell, adjacents in maze.items():
        open_adjacents = {}
        for adj, weight in adjacents.items():
            if weight != 100:
                open_adjacents[adj] = weight
        if open_adjacents:
            open_passages[cell] = open_adjacents
    return open_passages
