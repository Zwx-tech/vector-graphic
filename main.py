from curves import *
from workspaces import *

import pygame, os
from screeninfo import get_monitors


Y_OFFSET = 50


def get_screen_resolution(y_offset):
    monitors = [m for m in get_monitors()]
    return  monitors[0].width, monitors[0].height - y_offset


if __name__ == "__main__":
    WIDTH, HEIGHT = get_screen_resolution(Y_OFFSET)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("UwUctory")

    workspace = Workspace((100, 100), (WIDTH, HEIGHT))

    b = Bezier(Vector(0, 50), Vector(40, 75), Vector(50, 25), Vector(70, 50))
    workspace.add_object(b)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit(0)

            # zoom handle is temporary here
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    workspace.zoom_in()
                elif event.button == 5:
                    workspace.zoom_out()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    workspace.x_offset += 10
                elif event.key == pygame.K_LEFT:
                    workspace.x_offset -= 10
                elif event.key == pygame.K_UP:
                    workspace.y_offset += 10
                elif event.key == pygame.K_DOWN:
                    workspace.y_offset -= 10

        screen.fill((0, 0, 0))
        workspace.tick()
        pygame.display.update()

        clock.tick(180)