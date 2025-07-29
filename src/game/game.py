from .window import Window
from .objects import Cursor

import ctypes
import pygame


class Game:
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()
        pygame.init()
        self.window = Window()
        window_size = pygame.display.get_window_size()
        print("Window size:", window_size) 
        self.cursor = Cursor(window_size[0] // 2, window_size[1] // 2)
        self.running = True

    def run(self):
        while self.running and not self.window.closed:
            self.window.poll_events()
            self.window.render([self.cursor])
        self.window.close()
