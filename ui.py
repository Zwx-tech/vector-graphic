from curves import Vector
import pygame

class UIElement:

    def __init__(self, pos: Vector, width, height):
        self.__clicked = False
        self.selected = False
        self.pos = pos
        self.width = width
        self.height = height

    @property
    def clicked(self) -> bool: #returns True if button was clicked
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if pygame.Rect(self.pos.x, self.pos.y, self.width, self.height).colliderect(pygame.Rect(x, y, 1, 1)):
                return True
        return False

    def show(self):
        pass

    def tick(self):
        pass

class Interface:

    def __init__(self):
        pass

    def show(self):
        pass

    def tick(self):
        pass

class Button(UIElement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Frame(UIElement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)