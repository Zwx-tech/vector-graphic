import pygame, os
from screeninfo import get_monitors
from curves import *

Y_OFFSET = 50

def get_screen_resolution(y_offset):
    monitors = [m for m in get_monitors()]
    return  monitors[0].width, monitors[0].height - y_offset

if __name__ == "__main__":
    WIDTH, HEIGHT = get_screen_resolution(Y_OFFSET)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("UwUctory")
    b = Bezier(Vector(50, 100), Vector(100, 150), Vector(150, 50), Vector(200, 100))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit(0)

        screen.fill((0, 0, 0))
        b.tick()
        b.draw()
        pygame.display.update()

        clock.tick(180)