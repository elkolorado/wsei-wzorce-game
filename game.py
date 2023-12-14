import pygame
import numpy as np
import pickle
import tkinter as tk
from tkinter import filedialog
from abc import ABC, abstractmethod

class Screen:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

    def fill(self, color):
        self.screen.fill(color)

    def flip(self):
        pygame.display.flip()

class Grid:
    def __init__(self, n_cells_x, n_cells_y, cell_width, cell_height):
        self.n_cells_x = n_cells_x
        self.n_cells_y = n_cells_y
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

    def draw(self, screen):
        for y in range(0, screen.height, self.cell_height):
            for x in range(0, screen.width, self.cell_width):
                cell = pygame.Rect(x, y, self.cell_width, self.cell_height)
                pygame.draw.rect(screen.screen, gray, cell, 1)

    def draw_cells(self, screen):
        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                cell = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height)
                if self.game_state[x, y] == 1:
                    pygame.draw.rect(screen.screen, black, cell)

    def next_generation(self):
        new_state = np.copy(self.game_state)

        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                n_neighbors = self.game_state[(x - 1) % self.n_cells_x, (y - 1) % self.n_cells_y] + \
                              self.game_state[(x) % self.n_cells_x, (y - 1) % self.n_cells_y] + \
                              self.game_state[(x + 1) % self.n_cells_x, (y - 1) % self.n_cells_y] + \
                              self.game_state[(x - 1) % self.n_cells_x, (y) % self.n_cells_y] + \
                              self.game_state[(x + 1) % self.n_cells_x, (y) % self.n_cells_y] + \
                              self.game_state[(x - 1) % self.n_cells_x, (y + 1) % self.n_cells_y] + \
                              self.game_state[(x) % self.n_cells_x, (y + 1) % self.n_cells_y] + \
                              self.game_state[(x + 1) % self.n_cells_x, (y + 1) % self.n_cells_y]

                if self.game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                    new_state[x, y] = 0
                elif self.game_state[x, y] == 0 and n_neighbors == 3:
                    new_state[x, y] = 1

        self.game_state = new_state

class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen.screen, green, (self.x, self.y, button_width, button_height))
        font = pygame.font.Font(None, 36)
        if callable(self.text):
            text = font.render(self.text(), True, black)
        else:
            text = font.render(self.text, True, black)
        screen.screen.blit(text, (self.x + 10, self.y + 10))

    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + button_width and self.y <= pos[1] <= self.y + button_height


class FileHandler(ABC):
    @abstractmethod
    def save(self, file_path, data):
        pass

    @abstractmethod
    def load(self, file_path):
        pass

class PickleFileHandler(FileHandler):
    def save(self, file_path, data):
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)

    def load(self, file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)


class GameFileHandler:
    def __init__(self, file_handler: FileHandler):
        self.file_handler = file_handler

    def save_game_state(self, file_path, data):
        self.file_handler.save(file_path, data)

    def load_game_state(self, file_path):
        return self.file_handler.load(file_path)


class FileDialogHandler(ABC):
    @abstractmethod
    def ask_saveas_filename(self, defaultextension=".pkl"):
        pass

    @abstractmethod
    def ask_open_filename(self, filetypes=[("Pickle files", "*.pkl")]):
        pass

class TkinterFileDialogHandler(FileDialogHandler):
    def ask_saveas_filename(self, defaultextension=".pkl"):
        return filedialog.asksaveasfilename(defaultextension=defaultextension)

    def ask_open_filename(self, filetypes=[("Pickle files", "*.pkl")]):
        return filedialog.askopenfilename(filetypes=filetypes)

class GameTkinterFileDialogHandler:
    def __init__(self, file_dialog_handler: FileDialogHandler):
        self.file_dialog_handler = file_dialog_handler

    def ask_saveas_filename(self, defaultextension=".pkl"):
        return self.file_dialog_handler.ask_saveas_filename(defaultextension=defaultextension)

    def ask_open_filename(self, filetypes=[("Pickle files", "*.pkl")]):
        return self.file_dialog_handler.ask_open_filename(filetypes=filetypes)


class Renderer:
    def __init__(self, screen, grid, buttons, tick_time):
        self.screen = screen
        self.grid = grid
        self.buttons = buttons
        self.tick_time = tick_time

    def render(self):
        self.screen.fill(white)
        self.grid.draw(self.screen)
        self.grid.draw_cells(self.screen)

        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event.pos):
                        button.click_action()
                else:
                    x, y = event.pos[0] // self.grid.cell_width, event.pos[1] // self.grid.cell_height
                    self.grid.game_state[x, y] = not self.grid.game_state[x, y]

        return True

    def update(self):
        if not game.paused:
            self.grid.next_generation()

    def run(self):
        while True:
            if not self.handle_events():
                break
            self.update()
            self.render()
            pygame.time.delay(self.tick_time)

class Game:
    def __init__(self, renderer, grid, file_handler, file_dialog_handler):
        self.renderer = renderer
        self.file_handler = file_handler
        self.file_dialog_handler = file_dialog_handler
        self.clock = pygame.time.Clock()
        self.paused = False
        self.grid = grid

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event.pos):
                        button.click_action()
                else:
                    x, y = event.pos[0] // self.grid.cell_width, event.pos[1] // self.grid.cell_height
                    self.grid.game_state[x, y] = not self.grid.game_state[x, y]

        return True

    def run(self):
        self.renderer.run()

    def toggle_pause(self):
        self.paused = not self.paused

    def save_game_state(self):
        self.paused = True
        file_path = self.file_dialog_handler.ask_saveas_filename(defaultextension=".pkl")
        self.file_handler.save_game_state(file_path, self.grid.game_state)

    def load_game_state(self):
        self.paused = True
        file_path = self.file_dialog_handler.ask_open_filename(filetypes=[("Pickle files", "*.pkl")])
        loaded_game_state = self.file_handler.load_game_state(file_path)
        if loaded_game_state is not None:
            self.grid.game_state[:] = loaded_game_state



# Create instances
screen = Screen(800, 600)
grid = Grid(40, 30, screen.width // 40, screen.height // 30)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)

# Button dimensions
button_width, button_height = 200, 50
button_x, button_y = (screen.width - button_width) // 2, screen.height - button_height - 10

#tick
tick_time = 1000 #ms

# Create file handlers
file_handler = GameFileHandler(PickleFileHandler())
file_dialog_handler = GameTkinterFileDialogHandler(TkinterFileDialogHandler())

# Create button instances
pause_button = Button(lambda: 'Play' if game.paused else 'Pause', (screen.width - button_width) // 2, screen.height - button_height - 10)
save_button = Button('Save', (screen.width - button_width) // 2 + 120, screen.height - button_height - 10)
load_button = Button('Load', (screen.width - button_width) // 2 + 320, screen.height - button_height - 10)


# Create game instance
renderer = Renderer(screen, grid, [pause_button, save_button, load_button], tick_time)
game = Game(renderer, grid, file_handler, file_dialog_handler)

# Set button actions
pause_button.click_action = game.toggle_pause
save_button.click_action = game.save_game_state
load_button.click_action = game.load_game_state

# Run the game
game.run()
