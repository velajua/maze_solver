# Maze Solver FastAPI

This FastAPI app creates and solves mazes using various algorithms.

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
6. Upload a maze file and select a pathing algorithm to see the solution in `/uploud_maze`.

### containerized

1. Clone this repository.
2. Build the container using the following command: `docker build -t maze_solver .`.
3. Run the container using the following command: `docker run -it -p 8000:8000 maze_solver`.
4. Navigate to `http://localhost:8000` in your web browser.
5. Generate maze files usign the form provided in `/maze_generator`.
6. Upload a maze file and select a pathing algorithm to see the solution in `/uploud_maze`.

## Usage

`http://localhost:8000/maze_generator` to generate the maze files.

The maze generator can make various mazes, taking parameters for how strict the pathing is, and the probability of having weighted cells.

![50x50 Weightless Maze](example/0796e10d-f39e-47b7-9a5e-691593417269.png "50x50 Weightless Maze")

`http://localhost:8000/upload_maze` to solve the maze file using a pathing algorithm.

Using Djikstra, the following solution can be obtained.

![50x50 Weightless Maze Solution](example/f9774cde-b79e-489c-a1b5-4c427c35cc65_maze_0_solution.png "50x50 Weightless Maze Solution")

Heavily weighted maze:

![100x100 Heavily Weighted Maze](example/a5a0fc42-5561-4098-8942-24b18db77596.png "100x100 Heavily Weighted Maze")


## Supported Algorithms

The app currently supports the following maze solving algorithms (Which can be found in [`here`](path_finding.py):

* Dijkstra's Algorithm
* A* Algorithm
* Breadth-First Search
* Depth-First Search
* Bellman-Ford Algorithm
* Bidirectional Search
* Beam Search
