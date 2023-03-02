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
5. Generate maze files usign the form provided.
6. Upload a maze file and select a pathing algorithm to see the solution.

## Usage

`http://localhost:8000/maze_generator` to generate the maze files.
`http://localhost:8000/upload_maze` to solve the maze file using a pathong algorithm.


## Supported Algorithms

The app currently supports the following maze solving algorithms:

* Dijkstra's Algorithm
* A* Algorithm
* Breadth-First Search
* Depth-First Search
* Bellman-Ford Algorithm
* Bidirectional Search
* Beam Search
