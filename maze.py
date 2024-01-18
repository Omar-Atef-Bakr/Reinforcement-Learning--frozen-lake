import tkinter as tk
import random
from solver import Solver, STUCK_VALUE


'''
longest path for every size:
2: 2    4    2.666
3: 6    9   6
4: 11   16  10.666
5: 17   25  16.6666
6: 23   36  24
7: 34   49  32.66

longest path is always bound by (n**2) * 2/3 where n is the number of rows

therefore setting the maximum number of iterations to 2.5/3 * (n**2) garuntees we find the solution for any puzzle 
without too many useless iterations in the case of unsolvable cells 
'''

##############################
# Settings to adjust
MAZE_SIZE = 25                  # number of rows in the maze
OBSTACLE_DENSITY = 0.2          # possibility of every cell being an obstacle
USE_VALUE_ITERATION = True      # if True value iteration will be use. if False then policy iteration will be used
##############################


WINDOW_SIZE = 600


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

        # print(self.maze)

    def get_maze(self):
        return self.maze

class MazeGUI:
    def __init__(self, root, maze_size, obstacle_density, use_value_iteration):
        self.root = root
        self.root.title("Maze Generator")
        self.maze_size = maze_size
        self.obstacle_density = obstacle_density
        self.use_value_iteration = use_value_iteration
        self.value_visualize=[]
        

        self.maze_generator = MazeGenerator(self.maze_size, self.obstacle_density)

        self.cell_size = WINDOW_SIZE // self.maze_size
        self.canvas_size = self.cell_size * self.maze_size

        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()

        self.generate_button = tk.Button(root, text="Generate Maze", command=self.generate_maze)
        self.generate_button.pack()

        self.generate_button = tk.Button(root, text="Visualize value", command=self.visualize_value)
        self.generate_button.pack()

        self.maze_size_label = tk.Label(root, text="Maze Size:")
        self.maze_size_entry = tk.Entry(root)
        self.maze_size_entry.insert(0, str(self.maze_size))
        self.maze_size_label.pack()
        self.maze_size_entry.pack()

        self.obstacle_density_label = tk.Label(root, text="Obstacle Density:")
        self.obstacle_density_entry = tk.Entry(root)
        self.obstacle_density_entry.insert(0, str(self.obstacle_density))
        self.obstacle_density_label.pack()
        self.obstacle_density_entry.pack()

        self.use_value_iteration_button = tk.Button(root, text="Toggle Value Iteration",
                                                    command=self.toggle_value_iteration)
        self.use_value_iteration_button.pack()

        self.generate_maze()

    def generate_maze(self):
        self.maze_size = int(self.maze_size_entry.get())
        self.obstacle_density = float(self.obstacle_density_entry.get())

        self.maze_generator = MazeGenerator(self.maze_size, self.obstacle_density)
        self.maze_generator.generate_maze()

        self.cell_size = WINDOW_SIZE // self.maze_size
        self.canvas_size = self.cell_size * self.maze_size

        self.canvas.config(width=self.canvas_size, height=self.canvas_size)

        self.canvas.update()
        self.solve_maze()

    def toggle_value_iteration(self):
        self.use_value_iteration = not self.use_value_iteration
        self.use_value_iteration_button.config(text="Toggle Value Iteration (Currently {})".format(
            "On" if self.use_value_iteration else "Off"))
                    

    def visualize_value(self):
        self.canvas.delete("all")
        maze = self.maze_generator.get_maze()
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                if row == col == 0:
                    continue

                x0, y0 = col * self.cell_size, row * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size

                ind = row*len(maze)+col
            
                value = self.value_visualize[ind]
    
                self.canvas.create_rectangle(x0, y0, x1, y1, fill='white', outline="black")
                self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(round(value, 2)))
                

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
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                    draw_arrow(self.canvas, (x0 + x1) / 2, (y0 + y1) / 2, policy[ind].lower(), self.cell_size)

    def solve_maze(self):
        # print(self.maze_generator.get_maze())
        ai = Solver(self.maze_generator.get_maze())

        self.value_visualize = ai.value_iteration() if self.use_value_iteration else ai.policy_iteration()
        # print(solution)
        self.visualize_policy(ai.policy_representation())


def draw_arrow(canvas, x, y, direction, cell_size):
    arrow_length = cell_size // 3
    arrow_width = cell_size // 20

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
        canvas.create_rectangle(x - cell_size/2, y - cell_size/2, x + cell_size/2, y + cell_size/2, fill='red')


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeGUI(root, MAZE_SIZE, OBSTACLE_DENSITY, USE_VALUE_ITERATION)
    root.mainloop()
