from enum import Enum

import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 800
CELL_WIDTH = 20
CELL_HEIGHT = 20
GRID_WIDTH = WIDTH // CELL_WIDTH
GRID_HEIGHT = HEIGHT // CELL_HEIGHT
FPS = 60
UPDATE_FREQ = 10


class Color(Enum):
    BLACK = (0, 0, 0)
    DARK_GREY = (32, 32, 32)
    DEEP_RED = (64, 32, 32)
    YELLOW = (255, 255, 0)


class Cell:
    
    def __init__(self, row, col, width, height):
        # Position in the grid
        self.row = row
        self.col = col
        
        # Dimensions of the cell
        self.width = width
        self.height = height
        
        # Position on the screen
        self.x = row * width
        self.y = col * height
        
        # Color of the cell
        self.color = Color.DARK_GREY
        
        self.is_alive = False
    
    def get_position(self):
        return self.row, self.col
    
    def get_position_on_screen(self):
        return self.x, self.y
    
    def is_alive(self):
        return self.is_alive
    
    def is_dead(self):
        return not self.is_alive
    
    def make_alive(self):
        self.is_alive = True
        self.color = Color.YELLOW
    
    def make_dead(self):
        self.is_alive = False
        self.color = Color.DEEP_RED
    
    def clear(self):
        self.is_alive = False
        self.color = Color.DARK_GREY
        
    def draw(self, win):
        pygame.draw.rect(win, self.color.value, (self.x, self.y, self.width, self.height))
    

class Grid:
    
    def __init__(self, width, height, cell_width, cell_height):
        self.width = width
        self.height = height
        
        self.cell_width = cell_width
        self.cell_height = cell_height
        
        self.rows = width // cell_width
        self.cols = height // cell_height
        
        self.grid = Grid.create_new_grid(self.rows, self.cols, cell_width, cell_height)

    @staticmethod
    def create_new_grid(rows, cols, cell_width, cell_height):
        return [
            [Cell(row, col, cell_width, cell_height) for col in range(cols)]
            for row in range(rows)
        ]

    def get_cell(self, row, col):
        return self.grid[row][col]
    
    def get_neighbors(self, cell):
        x, y = cell.get_position()
        neighbors = []
        for dx in [-1, 0, 1]:
            if x + dx < 0 or x + dx >= self.rows:
                continue
            for dy in [-1, 0, 1]:
                if y + dy < 0 or y + dy >= self.cols:
                    continue
                if dx == 0 and dy == 0:
                    continue

                neighbors.append(self.get_cell(x + dx, y + dy))

        return neighbors
    
    def generate_random_cells(self):
        num = int((4 / 9) * self.cols)
        for _ in range(num):
            row = random.randrange(0, self.rows)
            col = random.randrange(0, self.cols)
            cell = self.get_cell(row, col)
            cell.make_alive()
        
    def clear(self):
        for row in self.grid:
            for cell in row:
                cell.clear()
    
    def draw(self, win):
        for row in self.grid:
            for cell in row:
                cell.draw(win)

        for row in range(self.rows):
            pygame.draw.line(
                win, 
                Color.BLACK.value, 
                (0, row * self.cell_width), 
                (self.width, row * self.cell_width)
            )

        for col in range(self.cols):
            pygame.draw.line(
                win, 
                Color.BLACK.value, 
                (col * self.cell_height, 0), 
                (col * self.cell_height, self.height)
            ) 
        
    def update(self):
        new_grid = Grid.create_new_grid(self.rows, self.cols, self.cell_width, self.cell_height)

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.get_cell(row, col)
                neighbors = self.get_neighbors(cell)
                alive_neighbors = len([n for n in neighbors if n.is_alive])

                if cell.is_alive and (alive_neighbors < 2 or alive_neighbors > 3):
                    new_grid[row][col].make_dead()
                elif cell.is_alive or alive_neighbors == 3:
                    new_grid[row][col].make_alive()

        self.grid = new_grid


def _mouse_position_in_grid(grid):
    mouse_focus = pygame.mouse.get_focused()

    if not mouse_focus:
        return -1, -1

    x, y = pygame.mouse.get_pos()
    row = x // grid.cell_width
    col = y // grid.cell_height
    return row, col


def _process_left_click(grid):
    row, col = _mouse_position_in_grid(grid)

    if row < 0 or col < 0:
        return

    if row >= grid.rows or col >= grid.cols:
        return

    cell = grid.get_cell(row, col)
    cell.make_alive()


def _process_right_click(grid):
    row, col = _mouse_position_in_grid(grid)

    if row < 0 or col < 0:
        return

    if row >= grid.rows or col >= grid.cols:
        return

    cell = grid.get_cell(row, col)
    cell.clear()


def run_simulation(screen, clock, grid):
    simulation_running, playing = True, False
    count, update_freq = 0, UPDATE_FREQ

    while simulation_running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            grid.update()

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulation_running = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                _process_left_click(grid)

            if pygame.mouse.get_pressed()[2]:  # RIGHT
                _process_right_click(grid)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_RETURN:
                    playing = True

                if event.key == pygame.K_p:
                    playing = False

                if event.key == pygame.K_c:
                    grid.clear()
                    playing = False
                    count = 0

                if event.key == pygame.K_g:
                    grid.generate_random_cells()

        screen.fill(Color.DEEP_RED.value)
        grid.draw(screen)
        pygame.display.update()


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Game of Life")

    grid = Grid(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT)

    run_simulation(screen, clock, grid)

    pygame.quit()


if __name__ == "__main__":
    main()
