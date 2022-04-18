from curves import *

import pygame, math


class Navigation(object):
    def __init__(self, workspaces: list = []):
        self.workspaces = workspaces
        self.zoom = .5
        self.moving = None # False statement is more accurate

    def add_workspace(self, workspace):
        assert isinstance(workspace, Workspace)

        if workspace not in self.workspaces:
            self.workspaces.append(workspace)

        workspace.navigation = self

        if self.workspaces:
            workspace.factor = self.workspaces[0].factor

    def zoom_in(self):
        mouse_pos = pygame.mouse.get_pos()
        p = self.workspaces[0].translate_to_units(x=mouse_pos[0], y=mouse_pos[1])

        self.zoom += .1

        t = self.workspaces[0].translate_to_pixels(x=p[0], y=p[1])

        for workspace in self.workspaces:
            workspace.x_offset += (mouse_pos[0] - workspace.x_offset) - (t[0] - workspace.x_offset)
            workspace.y_offset += (mouse_pos[1] - workspace.y_offset) - (t[1] - workspace.y_offset)

    def zoom_out(self):
        mouse_pos = pygame.mouse.get_pos()
        p = self.workspaces[0].translate_to_units(x=mouse_pos[0], y=mouse_pos[1])

        self.zoom -= .1
        self.zoom = max(self.zoom, .1)

        t = self.workspaces[0].translate_to_pixels(x=p[0], y=p[1])

        for workspace in self.workspaces:
            workspace.x_offset += (mouse_pos[0] - workspace.x_offset) - (t[0] - workspace.x_offset)
            workspace.y_offset += (mouse_pos[1] - workspace.y_offset) - (t[1] - workspace.y_offset)

    def move(self):
        if self.moving is None:
            self.moving = ((self.workspaces[0].x_offset, self.workspaces[0].y_offset), pygame.mouse.get_pos())

        for workspace in self.workspaces:
            workspace.x_offset = self.moving[0][0] + (pygame.mouse.get_pos()[0] - self.moving[1][0])
            workspace.y_offset = self.moving[0][1] + (pygame.mouse.get_pos()[1] - self.moving[1][1])

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.zoom_in()
            elif event.button == 5:
                self.zoom_out()

    def tick(self):
        if pygame.mouse.get_pressed()[1]:
            self.move()
        else:
            self.moving = None


class Workspace(object):
    def __init__(
            self,
            size: tuple[int, int],  # (width, height)
            window_size: tuple[int, int],  # (width, height)
            navigation: Navigation,
            background_color=(255, 255, 255)
    ):
        self.size = size
        self.window_size = window_size

        self.screen = pygame.display.get_surface()
        self.background = background_color
        self.objects = []

        self.static_x_offset = 10
        self.static_y_offset = 10
        self.factor = self._calculate_factor()

        self.x_offset = self.static_x_offset - (size[0] - ((size[0] - self.static_x_offset) // 2) - self.window_size[0] // 2) // 10
        self.y_offset = self.static_y_offset - (size[1] - ((size[1] - self.static_y_offset) // 2) - self.window_size[1] // 2) // 10

        self.navigation: Navigation
        navigation.add_workspace(self)

    def add_object(self, obj):
        if obj not in self.objects:
            self.objects.append(obj)
        self.objects[-1].workspace = self

    def _calculate_factor(self) -> float:
        if self.size[0] >= self.size[1]:
            return self.window_size[0] / self.size[0]
        return self.window_size[1] / self.size[1]

    def translate_to_pixels(self, vector: Vector = None, x=None, y=None) -> Vector or tuple[int, int]:
        """Translates units to pixels. Specifies where vector should be on the pygame screen"""

        if (x is not None) and (y is not None):
            return round(self.factor * self.navigation.zoom * x + self.x_offset + self.static_x_offset * self.navigation.zoom), \
                   round(self.factor * self.navigation.zoom * y + self.y_offset + self.static_y_offset * self.navigation.zoom)

        return Vector(
            round((self.factor * self.navigation.zoom * vector.x) + self.x_offset + self.static_x_offset * self.navigation.zoom),
            round((self.factor * self.navigation.zoom * vector.y) + self.y_offset + self.static_y_offset * self.navigation.zoom)
        )

    def translate_to_units(self, vector: Vector = None, x=None, y=None) -> Vector or tuple[int, int]:
        """Translates pixels to units. Specifies where pixel should be on workspace"""

        if (x is not None) and (y is not None):
            return (x - self.x_offset - self.static_x_offset * self.navigation.zoom) / self.factor / self.navigation.zoom, \
                   (y - self.y_offset - self.static_y_offset * self.navigation.zoom) / self.factor / self.navigation.zoom

        return Vector(
            (vector.x - self.x_offset - self.static_x_offset * self.navigation.zoom) / self.factor / self.navigation.zoom,
            (vector.y - self.y_offset - self.static_y_offset * self.navigation.zoom) / self.factor / self.navigation.zoom
        )

    def tick(self):
        # drawing background
        t = self.translate_to_pixels(Vector(*self.size)).v
        pygame.draw.rect(
            self.screen, self.background,
            (self.x_offset + self.static_x_offset * self.navigation.zoom, self.y_offset + self.static_y_offset * self.navigation.zoom,
             t[0]-self.x_offset-self.static_x_offset * self.navigation.zoom, t[1]-self.y_offset-self.static_y_offset * self.navigation.zoom)
        )

        for obj in self.objects:
            obj.tick()
            obj.draw()