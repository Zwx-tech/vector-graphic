import math
import pygame

# precision with which the curve is drawn
PRECISION = 1 / 100


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot_product(self, vector) -> int:
        return self.x * vector.x + self.y * vector.y

    @property
    def v(self):
        return round(self.x), round(self.y)

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x + other.x, self.y + other.y)

        elif isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

        else:
            raise Exception("Invalid opertation")

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other)
        else:
            raise Exception("Invalid opertation")

    def __str__(self):
        return f"V({self.x}, {self.y})"

    def intersect(self, other, d) -> bool:
        return bool(math.sqrt(pow(abs(other.x - self.x) + abs(other.y - self.y), 2)) <= d)


class Bezier:
    workspace = None

    def __init__(
            self,
            starting_point: Vector,
            ending_point: Vector,
            a: Vector, b: Vector,
            workspace=None,
            color=(0, 0, 0)
    ):
        assert isinstance(starting_point, Vector) and isinstance(ending_point, Vector) and isinstance(a, Vector) and isinstance(b, Vector)
        # assert isinstance(workspace, Workspace) or workspace is None

        self.start = starting_point  # P0
        self.end = ending_point  # P3
        self.a = a  # P1
        self.b = b  # P2

        self.color = color

        self.clicked = False  # to change (by using button class)
        self.n = int(10 ** -math.log10(PRECISION))
        self.k = round(PRECISION * self.n)

        if workspace is not None:
            workspace.add_object(self)

    def P(self, t) -> Vector:
        return self.start * (-t ** 3 + 3 * t ** 2 - 3 * t + 1) + \
               self.a * (3 * t ** 3 - 6 * t ** 2 + 3 * t) + \
               self.b * (-3 * t ** 3 + 3 * t ** 2) + \
               self.end * (t ** 3)

    def tick(self):
        # get user input
        if pygame.mouse.get_pressed()[0]:
            self.show()
            mouse_pos = self.workspace.translate_to_units(Vector(*pygame.mouse.get_pos()))

            if self.a.intersect(mouse_pos, 4):
                if not self.clicked:
                    self.clicked = "a"
            elif self.b.intersect(mouse_pos, 4):
                if not self.clicked:
                    self.clicked = "b"
            elif self.start.intersect(mouse_pos, 4):
                if not self.clicked:
                    self.clicked = "s"
            elif self.end.intersect(mouse_pos, 4):
                if not self.clicked:
                    self.clicked = "e"
            if self.clicked:
                if self.clicked == "a":
                    self.a = mouse_pos
                elif self.clicked == "b":
                    self.b = mouse_pos
                elif self.clicked == "s":
                    self.start = mouse_pos
                elif self.clicked == "e":
                    self.end = mouse_pos
        else:
            self.clicked = False

    def show(self):
        screen = pygame.display.get_surface()
        pygame.draw.line(screen, (200, 200, 200),
                         self.workspace.translate_to_pixels(self.start).v, self.workspace.translate_to_pixels(self.a).v)
        pygame.draw.line(screen, (200, 200, 200),
                         self.workspace.translate_to_pixels(self.end).v, self.workspace.translate_to_pixels(self.b).v)
        pygame.draw.circle(screen, (255, 0, 0),
                           self.workspace.translate_to_pixels(self.start).v, 4, 1)
        pygame.draw.circle(screen, (0, 255, 0),
                           self.workspace.translate_to_pixels(self.end).v, 4, 1)
        pygame.draw.circle(screen, (0, 0, 200),
                           self.workspace.translate_to_pixels(self.a).v, 4, 1)
        pygame.draw.circle(screen, (0, 160, 200),
                           self.workspace.translate_to_pixels(self.b).v, 4, 1)

    def draw(self):
        screen = pygame.display.get_surface()

        v1 = self.workspace.translate_to_pixels(self.P(0))

        for i in range(self.k, self.n + 1, self.k):
            v2 = self.workspace.translate_to_pixels(self.P(i / self.n))
            pygame.draw.line(screen, self.color, v1.v, v2.v)
            v1 = v2


class Shape:

    def __init__(self):
        self.curves = []

    def show(self):
        pass

    def tick(self):
        pass
