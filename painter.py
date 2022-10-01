import pygame as pg
from pygame import display, time, event, mouse
from torch import zeros, uint8
from sys import exit

class Painter():
    def __init__(self):
        pg.init()
        display.set_caption('Painter')
        self.size = (640, 640)
        self.grid_size = (64, 64)
        self.grid = zeros(self.grid_size, dtype=uint8)
        self.pixels_size = (self.size[0] // self.grid_size[0], self.size[1] // self.grid_size[1])
        self.fps = 480
        self.screen = display.set_mode(self.size)
        self.clock = time.Clock()

    def draw_stuff(self):
        for i, row in enumerate(self.grid):
            for j, whiteValue in enumerate(row):
                color = (whiteValue, whiteValue, whiteValue)
                rect = (
                    j * self.pixels_size[0], 
                    i * self.pixels_size[1], 
                    self.pixels_size[0], 
                    self.pixels_size[1],
                )
                pg.draw.rect(self.screen, color, rect)

    def paint(self, pos):
        x, y = pos
        col, row = x // self.pixels_size[0], y // self.pixels_size[1]
        self.grid[row, col] = 255
        self.grid[row - 1, col] = 255
        self.grid[row, col - 1] = 255

    def clear_canvas(self):
        self.grid = zeros(self.grid_size, dtype=uint8)

    def start(self):
        while True:
            self.draw_stuff()
            events = event.get()
            for e in events:
                match e.type:
                    case pg.QUIT: exit()
                    case pg.MOUSEBUTTONDOWN:
                        match e.button:
                            case 3: self.clear_canvas()
                    case pg.MOUSEMOTION:
                        left_mouse_button_pressed = mouse.get_pressed()[0]
                        if left_mouse_button_pressed:
                            pos = mouse.get_pos()
                            self.paint(pos)

            display.update()
            self.clock.tick(self.fps)
