# Python Maze Solver

This project is a Python application that generates a maze and solves it using either Value Iteration or Policy Iteration algorithms. The maze is visualized using the tkinter library.

## Files

- `maze.py`: This file contains the `MazeGenerator` and `MazeGUI` classes. `MazeGenerator` is responsible for generating the maze based on the specified size and obstacle density. `MazeGUI` is responsible for visualizing the maze and the solution path.

- `solver.py`: This file contains the `Solver` class which implements the Value Iteration and Policy Iteration algorithms to solve the maze. The `Solver` class also includes methods for policy evaluation and improvement.

## Requirements

- Python 3.6 or higher
- tkinter

## Usage

1. Clone the repository.
2. Run `maze.py` to generate and visualize a maze, and solve it using either Value Iteration or Policy Iteration algorithms.

## Settings

You can adjust the following settings in `maze.py`:

- `MAZE_SIZE`: The number of rows in the maze. This also determines the number of columns as the maze is a square.
- `OBSTACLE_DENSITY`: The possibility of every cell being an obstacle. This is a value between 0 and 1, where 1 means every cell will be an obstacle and 0 means there will be no obstacles.
- `USE_VALUE_ITERATION`: If set to `True`, Value Iteration will be used to solve the maze. If `False`, Policy Iteration will be used.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.
