from curves import *

import pygame, math


class Workspace(object):
    def __init__(
            self,
            size: tuple[int, int],  # (width, height)
            window_size: tuple[int, int],  # (width, height)
            background_color=(255, 255, 255)
    ):
        self.size = size
        self.window_size = window_size

        self.screen = pygame.display.get_surface()
        self.background = background_color
        self.objects = []
        self.zoom = .8
        self.x_offset = 10
        self.y_offset = 10
        self.factor = self._calculate_factor()

        self.x_offset -= (size[0] - ((size[0] - self.x_offset) // 2) - self.window_size[0]//2) // 10
        self.y_offset -= (size[1] - ((size[1] - self.y_offset) // 2) - self.window_size[1]//2) // 10

    def add_object(self, obj):
        if obj not in self.objects:
            self.objects.append(obj)
        self.objects[-1].workspace = self

    def _calculate_factor(self) -> float:
        if self.size[0] >= self.size[1]:
            return self.window_size[0] / self.size[0]
        return self.window_size[1] / self.size[1]

    def resize_window(self, size: tuple[int, int]):
        self.window_size = size
        self.factor = self._calculate_factor()

    def translate_to_pixels(self, vector: Vector = None, x=None, y=None) -> Vector or tuple[int, int]:
        """Translates units to pixels. Specifies where vector should be on the pygame screen"""

        if (x is not None) and (y is not None):
            return round(self.factor * self.zoom * x + self.x_offset), \
                   round(self.factor * self.zoom * y + self.y_offset)

        return Vector(
            round((self.factor * self.zoom * vector.x) + self.x_offset),
            round((self.factor * self.zoom * vector.y) + self.y_offset)
        )

    def translate_to_units(self, vector: Vector = None, x=None, y=None) -> Vector or tuple[int, int]:
        """Translates pixels to units. Specifies where pixel should be on workspace"""

        if (x is not None) and (y is not None):
            return (x - self.x_offset) / self.factor / self.zoom, \
                   (y - self.y_offset) / self.factor / self.zoom

        return Vector(
            (vector.x - self.x_offset) / self.factor / self.zoom,
            (vector.y - self.y_offset) / self.factor / self.zoom
        )

    def zoom_in(self):
        mouse_pos = pygame.mouse.get_pos()
        p = self.translate_to_units(x=mouse_pos[0], y=mouse_pos[1])

        self.zoom += .05

        t = self.translate_to_pixels(x=p[0], y=p[1])

        self.x_offset += (mouse_pos[0] - self.x_offset) - (t[0] - self.x_offset)
        self.y_offset += (mouse_pos[1] - self.y_offset) - (t[1] - self.y_offset)

    def zoom_out(self):
        mouse_pos = pygame.mouse.get_pos()
        p = self.translate_to_units(x=mouse_pos[0], y=mouse_pos[1])

        self.zoom -= .05
        self.zoom = max(self.zoom, .05)

        t = self.translate_to_pixels(x=p[0], y=p[1])

        self.x_offset += (mouse_pos[0] - self.x_offset) - (t[0] - self.x_offset)
        self.y_offset += (mouse_pos[1] - self.y_offset) - (t[1] - self.y_offset)

    def tick(self):
        t = self.translate_to_pixels(Vector(*self.size)).v
        pygame.draw.rect(self.screen, self.background,
                         (self.x_offset, self.y_offset, t[0]-self.x_offset, t[1]-self.y_offset))

        for obj in self.objects:
            obj.tick()
            obj.draw()

