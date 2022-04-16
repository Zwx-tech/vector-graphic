from curves import Vector
import pygame

class UIElement:

    def __init__(self, pos: Vector, width, height, **kwargs):
        self.__clicked = False
        self.selected = False
        self.pos = pos
        self.width = width
        self.height = height
        self.color = kwargs.get('color', (255, 255, 255))
        self.img_path = kwargs.get('img_path', None)

    @property
    def clicked(self) -> bool: #returns True if button was clicked
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if pygame.Rect(self.pos.x, self.pos.y, self.width, self.height).colliderect(pygame.Rect(x, y, 1, 1)):
                return True
        return False

    def show(self):
        screen = pygame.display.get_surface()
        if not self.clicked: # TEST PURPOSE
            pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.v[0], self.pos.v[1], self.width, self.height), 2)

    def __set_img(self):
        if self.img_path:
            self.img = pygame.image.load(self.img_path) # change image size based on width and height
            self.img_rect = self.img.get_rect()

    def tick(self):
        if self.clicked:
            self.__clicked = True
        else:
            self.clicked = False

class Interface:

    def __init__(self):
        self.objects = []

    def tick(self):
        for ob in self.objects:
            ob.show()
            ob.tick()

    def add_object(self, object):
        if not isinstance(object, UIElement):
            raise Exception("Invalid element")
        self.objects.append(object)

class Button(UIElement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tick(self):
        pass
class Frame(UIElement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)