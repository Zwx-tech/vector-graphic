from curves import *

import pygame, math


class Workspace(object):
    def __init__(
            self,
            size: tuple[int, int],  # (width, height)
            window_size: tuple[int, int],  # (width, height)
            background_color=(150, 150, 150),
            **kwargs
    ):
        self.size = size
        self.window_size = window_size

        self.screen = pygame.display.get_surface()
        self.background = background_color
        self.objects = []
        self.zoom = .8
        self.x_offset = kwargs.get('offset', (10, 10))[0]
        self.y_offset = kwargs.get('offset', (10, 10))[1]
        self.multiplayer = self._calculate_multiplayer()

    def add_object(self, obj):
        if obj not in self.objects:
            self.objects.append(obj)
        self.objects[-1].workspace = self

    def _calculate_multiplayer(self) -> float:
        if self.size[0] >= self.size[1]:
            return self.window_size[0] / self.size[0]
        return self.window_size[1] / self.size[1]

    def resize_window(self, size: tuple[int, int]):
        self.window_size = size
        self.multiplayer = self._calculate_multiplayer()

    def translate_to_pixels(self, vector: Vector = None, x=None, y=None) -> Vector or tuple[int, int]:
        """Translates units to pixels. Specifies where vector should be on the pygame screen"""

        if (x is not None) and (y is not None) and (Vector is None):
            return round(self.multiplayer * self.zoom * x + self.x_offset), \
                   round(self.multiplayer * self.zoom * y + self.y_offset)

        return Vector(
            round((self.multiplayer * self.zoom * vector.x) + self.x_offset),
            round((self.multiplayer * self.zoom * vector.y) + self.y_offset)
        )

    def translate_to_units(self, vector: Vector = None, x=None, y=None) -> Vector or tuple[int, int]:
        """Translates pixels to units. Specifies where pixel should be on workspace"""

        if (x is not None) and (y is not None) and (Vector is None):
            return (x - self.x_offset) / self.multiplayer / self.zoom, \
                   (y - self.y_offset) / self.multiplayer / self.zoom

        return Vector(
            (vector.x - self.x_offset) / self.multiplayer / self.zoom,
            (vector.y - self.y_offset) / self.multiplayer / self.zoom
        )

    def zoom_in(self):
        self.zoom += .05

    def zoom_out(self):
        self.zoom -= .05

    def tick(self):
        t = self.translate_to_pixels(Vector(*self.size)).v
        pygame.draw.rect(self.screen, self.background, (self.x_offset, self.y_offset, t[0]-self.x_offset, t[1]-self.y_offset))

        for obj in self.objects:
            obj.tick()
            obj.draw()
