from curves import Vector
import pygame

class UIElement:

    def __init__(self, pos: Vector, width, height, **kwargs):
        self.selected = False
        self.__clicked = False
        self.pos = pos
        self.width = width
        self.height = height
        self.color = kwargs.get('color', (255, 255, 255))
        self.img_path = kwargs.get('img_path', None)
        self.padding = kwargs.get('padding', (20, 20))

        self.__set_img()

    @property
    def clicked(self) -> bool: #returns True if button was clicked
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if pygame.Rect(self.pos.x, self.pos.y, self.width, self.height).collidepoint(self.pos.v):
                return True
        return False

    def show(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.v[0], self.pos.v[1], self.width, self.height), 2 if not self.selected else 3)
        if self.img:
            screen.blit(self.img, pygame.Rect(round(self.pos.x) + self.img_rect.x, round(self.pos.y) + self.img_rect.y, self.img_rect.width, self.img_rect.height))

    def __set_img(self):
        if self.img_path:
            self.img = pygame.transform.scale(pygame.image.load(self.img_path), (self.width - self.padding[0], self.height - self.padding[1])) # change image size based on width and height
            self.img_rect = self.img.get_rect()
            self.img_rect.x += self.padding[0]//2
            self.img_rect.y += self.padding[1]//2

    def tick(self):
        pass

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
        self.trigger = kwargs.get('trigger', lambda: None)

    def tick(self):
        if self.clicked:
            self.selected = not self.selected if not self.__clicked else self.selected
            self.__clicked = True
            self.trigger()
        else:
            self.__clicked = False

class ToolBar(Interface):

    def __init__(self, *args, **kwargs):
        super(ToolBar, self).__init__(*args, **kwargs)
        self.objects = []

    def __add_tool_buttons(self):
        self.objects.append()