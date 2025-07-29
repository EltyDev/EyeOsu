from abc import ABC, abstractmethod
from enum import Enum

import pygame


class SliderState(Enum):
    IDLE = 0
    DRAGGING = 1
    RELEASED = 2

class Object(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self, surface):
        pass


class Circle(Object):
    def __init__(self, x, y, color=(255, 255, 255)):
        super().__init__(x, y)
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), 5)


class Slider(Object):
    def __init__(self, x, y, width=100, height=10, color=(255, 255, 255)):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.color = color
        self.state = SliderState.IDLE

    def draw(self, surface):
        match self.state:
            case SliderState.IDLE:
                pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            case SliderState.DRAGGING:
                pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, self.width, self.height))
            case SliderState.RELEASED:
                pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))