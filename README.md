# Maze Solver FastAPI

This FastAPI app uses path finding algorithms to create and solve mazes while allowing for strict pathing and accounting for weighted cells.

This [`repository`](https://github.com/velajua/maze_solver) contains the necessary files to daploy a containerized app using Docker which is able to create mazes using a modified version of the Breadth-First-Search algorithm, as well as solutions to the generated mazes using various path-finding algorithms which can be found below.

## Requirements

* Python 3.6+
* FastAPI
* uvicorn

## How to Run

1. Clone this repository.
2. Install the requirements using `pip install -r requirements.txt`.
3. Run the app using the following command: `uvicorn maze_app:app --reload`.
4. Navigate to `http://localhost:8000` in your web browser.
5. Generate maze files usign the form provided in `/maze_generator`.
6. Upload a maze file and select a pathing algorithm to see the solution in `/upload_maze`.

### Docker

1. Clone this repository.
2. Build the container using the following command: `docker build -t maze_solver .`.
3. Run the container using the following command: `docker run -it -p 8000:8000 maze_solver`.
4. Navigate to `http://localhost:8000` in your web browser.
5. Generate maze files usign the form provided in `/maze_generator`.
6. Upload a maze file and select a pathing algorithm to see the solution in `/upload_maze`.

## Usage

`http://localhost:8000/maze_generator` to generate the maze files.

The maze generator can make various mazes, taking parameters for how strict the pathing is, and the probability of having weighted cells.
A Demo of the maze_generator can be found [`here`](https://maze-solver-4r64swfrtq-uc.a.run.app/maze_generator)

![50x50 Weightless Maze](example/0796e10d-f39e-47b7-9a5e-691593417269.png "50x50 Weightless Maze")

`http://localhost:8000/upload_maze` to solve the maze file using a pathing algorithm.
Using Djikstra, the following solution can be obtained.

A Demo of the maze_solver can be found [`here`](https://maze-solver-4r64swfrtq-uc.a.run.app/upload_maze)

![50x50 Weightless Maze Solution](example/f9774cde-b79e-489c-a1b5-4c427c35cc65_maze_0_solution.png "50x50 Weightless Maze Solution")

-------------------------------------------------------------------------------------------

This is an example of a heavily weighted 100x100 maze:
Its solution along with the cost fo the solution from coordinates (0, 0) to coordinates (99, 99) is as follows:
{'path': [(0, 0), (1, 0), (1, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (2, 12), (2, 13), (3, 13), (4, 13), (5, 13), (5, 14), (6, 14), (6, 15), (6, 16), (7, 16), (8, 16), (8, 17), (8, 18), (8, 19), (9, 19), (9, 20), (8, 20), (8, 21), (8, 22), (8, 23), (9, 23), (9, 24), (10, 24), (11, 24), (11, 25), (12, 25), (12, 24), (13, 24), (13, 25), (14, 25), (15, 25), (16, 25), (16, 26), (16, 27), (15, 27), (15, 28), (16, 28), (17, 28), (17, 29), (16, 29), (16, 30), (16, 31), (17, 31), (18, 31), (18, 30), (19, 30), (19, 31), (20, 31), (21, 31), (22, 31), (23, 31), (24, 31), (25, 31), (26, 31), (27, 31), (27, 32), (28, 32), (28, 33), (28, 34), (29, 34), (29, 33), (30, 33), (30, 32), (31, 32), (31, 31), (32, 31), (33, 31), (33, 32), (32, 32), (32, 33), (33, 33), (33, 34), (34, 34), (34, 33), (35, 33), (35, 34), (35, 35), (34, 35), (34, 36), (34, 37), (35, 37), (36, 37), (36, 38), (36, 39), (36, 40), (37, 40), (37, 41), (38, 41), (39, 41), (40, 41), (40, 42), (39, 42), (39, 43), (38, 43), (37, 43), (36, 43), (35, 43), (35, 42), (34, 42), (34, 43), (33, 43), (33, 44), (33, 45), (34, 45), (34, 44), (35, 44), (36, 44), (36, 45), (36, 46), (36, 47), (35, 47), (34, 47), (34, 48), (33, 48), (33, 47), (32, 47), (31, 47), (31, 48), (32, 48), (32, 49), (32, 50), (32, 51), (32, 52), (32, 53), (33, 53), (33, 54), (34, 54), (34, 55), (35, 55), (36, 55), (37, 55), (38, 55), (38, 56), (38, 57), (38, 58), (38, 59), (38, 60), (39, 60), (40, 60), (41, 60), (41, 61), (42, 61), (42, 62), (43, 62), (43, 63), (43, 64), (43, 65), (44, 65), (44, 66), (44, 67), (44, 68), (43, 68), (43, 69), (42, 69), (42, 70), (42, 71), (42, 72), (43, 72), (43, 73), (43, 74), (44, 74), (44, 75), (45, 75), (46, 75), (46, 76), (47, 76), (48, 76), (49, 76), (50, 76), (51, 76), (51, 77), (51, 78), (52, 78), (52, 79), (53, 79), (53, 78), (54, 78), (55, 78), (56, 78), (56, 79), (56, 80), (55, 80), (55, 81), (55, 82), (54, 82), (54, 83), (53, 83), (53, 84), (53, 85), (53, 86), (52, 86), (52, 87), (51, 87), (51, 88), (50, 88), (50, 89), (51, 89), (52, 89), (52, 90), (53, 90), (54, 90), (54, 91), (55, 91), (56, 91), (56, 92), (56, 93), (55, 93), (55, 94), (56, 94), (57, 94), (57, 95), (58, 95), (58, 96), (58, 97), (58, 98), (58, 99), (59, 99), (59, 98), (60, 98), (61, 98), (61, 97), (62, 97), (62, 98), (62, 99), (63, 99), (64, 99), (65, 99), (65, 98), (66, 98), (66, 99), (67, 99), (67, 98), (68, 98), (69, 98), (70, 98), (70, 97), (71, 97), (72, 97), (73, 97), (74, 97), (75, 97), (75, 96), (75, 95), (75, 94), (75, 93), (76, 93), (77, 93), (77, 94), (78, 94), (78, 93), (78, 92), (78, 91), (77, 91), (77, 90), (78, 90), (78, 89), (79, 89), (79, 90), (80, 90), (81, 90), (81, 89), (82, 89), (83, 89), (83, 88), (84, 88), (85, 88), (85, 87), (86, 87), (86, 88), (87, 88), (88, 88), (89, 88), (89, 87), (90, 87), (90, 88), (91, 88), (92, 88), (93, 88), (93, 89), (93, 90), (93, 91), (93, 92), (92, 92), (92, 93), (92, 94), (91, 94), (91, 95), (92, 95), (93, 95), (94, 95), (95, 95), (96, 95), (96, 96), (95, 96), (94, 96), (94, 97), (94, 98), (95, 98), (95, 99), (96, 99), (97, 99), (98, 99), (99, 99)], 'cost': 584}

![100x100 Heavily Weighted Maze](example/9e733760-75ec-4202-859c-ac0400e44668_maze_584_solution.png "100x100 Heavily Weighted Maze")


## Supported Algorithms

The maze_solver currently supports the following maze solving algorithms (Which can be found in [`here`](path_finding.py):

* Dijkstra's Algorithm
* A* Algorithm
* Breadth-First Search
* Depth-First Search
* Bellman-Ford Algorithm
* Bidirectional Search
* Beam Search
