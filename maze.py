import tkinter as tk
import random
from solver import Solver, STUCK_VALUE


MAZE_SIZE = 10
OBSTACLE_DENSITY = .2


class MazeGenerator:
    def __init__(self, size, obstacle_density):
        self.size = size
        self.obstacle_density = obstacle_density
        self.maze = [[0] * size for _ in range(size)]

    def generate_maze(self):
        self.maze = [[0] * self.size for _ in range(self.size)]
        # Place obstacles randomly based on obstacle density
        for row in range(self.size):
            for col in range(self.size):
                if random.random() < self.obstacle_density:
                    self.maze[row][col] = 1

        # Set start and end points
        self.maze[0][0] = 0
        self.maze[self.size - 1][self.size - 1] = 0

        print(self.maze)

    def get_maze(self):
        return self.maze


class MazeGUI:
    def __init__(self, root, maze_size, obstacle_density):
        self.root = root
        self.root.title("Maze Generator")
        self.canvas_size = 400
        self.cell_size = self.canvas_size // maze_size
        self.maze_generator = MazeGenerator(maze_size, obstacle_density)

        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()

        self.generate_button = tk.Button(root, text="Generate Maze", command=self.generate_maze)
        self.generate_button.pack()

        self.generate_maze()

    def generate_maze(self):
        self.maze_generator.generate_maze()
        maze = self.maze_generator.get_maze()
        self.draw_maze(maze)
        self.canvas.update()
        print("Maze: ", maze)
        self.solve_maze()

    def draw_maze(self, maze):
        self.canvas.delete("all")
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                x0, y0 = col * self.cell_size, row * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size

                if maze[row][col] == 1:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")

    def visualize_policy(self, policy):
        self.canvas.delete("all")
        maze = self.maze_generator.get_maze()
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                if row == col == 0:
                    continue

                x0, y0 = col * self.cell_size, row * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size

                ind = row*len(maze)+col

                if maze[row][col] == 1:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                else:
                    draw_arrow(self.canvas, (x0 + x1) / 2, (y0 + y1) / 2, policy[ind].lower(), self.cell_size)

    def solve_maze(self):
        print(self.maze_generator.get_maze())
        ai = Solver(self.maze_generator.get_maze())
        # print(ai.value_iteration())
        print(ai.policy_iteration())
        print(ai.policy_representation())
        self.visualize_policy(ai.policy_representation())


def draw_arrow(canvas, x, y, direction, cell_size):
    arrow_length = 20
    arrow_width = 1

    if direction == 'l':
        canvas.create_line(x, y, x - arrow_length, y, arrow=tk.LAST, width=arrow_width)
        canvas.create_polygon(x - arrow_length, y - arrow_width / 2, x - arrow_length, y + arrow_width / 2,
                              x - arrow_length - arrow_width, y, fill='black')
    elif direction == 'r':
        canvas.create_line(x, y, x + arrow_length, y, arrow=tk.LAST, width=arrow_width)
        canvas.create_polygon(x + arrow_length, y - arrow_width / 2, x + arrow_length, y + arrow_width / 2,
                              x + arrow_length + arrow_width, y, fill='black')
    elif direction == 'u':
        canvas.create_line(x, y, x, y - arrow_length, arrow=tk.LAST, width=arrow_width)
        canvas.create_polygon(x - arrow_width / 2, y - arrow_length, x + arrow_width / 2, y - arrow_length,
                              x, y - arrow_length - arrow_width, fill='black')
    elif direction == 'd':
        canvas.create_line(x, y, x, y + arrow_length, arrow=tk.LAST, width=arrow_width)
        canvas.create_polygon(x - arrow_width / 2, y + arrow_length, x + arrow_width / 2, y + arrow_length,
                              x, y + arrow_length + arrow_width, fill='black')

    elif direction == 's':
        # canvas.create_oval(x - arrow_length, y - arrow_length, x + arrow_length, y + arrow_length, fill='red')
        canvas.create_rectangle(x - cell_size/2, y - cell_size/2, x + cell_size/2, y + cell_size/2, fill='red')

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeGUI(root, MAZE_SIZE, OBSTACLE_DENSITY)
    root.mainloop()
