from configparser import ConfigParser

from curves import *
from workspaces import *
from ui import *
import pygame, os
from screeninfo import get_monitors

Y_OFFSET = 50

def load_config(name: str, _type: str):
    config = ConfigParser()
    config.read(os.path.join(os.getcwd(), "config", name))

    print(config.sections())
    content = config[_type]
    return  content


def get_screen_resolution(y_offset):
    monitors = [m for m in get_monitors()]
    return  monitors[0].width, monitors[0].height - y_offset

if __name__ == "__main__":
    WIDTH, HEIGHT = get_screen_resolution(Y_OFFSET)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("UwUctory")

    # get colors from config file
    colors = load_config("main.ini", "COLOR_PALETTE")
    BG_COLOR = tuple(map(int, colors['bg'].replace(",", "")[1:-1].split()))
    OUTLINE_COLOR = tuple(map(int, colors['outline'].replace(",", "")[1:-1].split()))
    LINE_COLOR = tuple(map(int, colors['outline'].replace(",", "")[1:-1].split()))
    # set up workspace and interface object
    workspace = Workspace((100, 100), (WIDTH, HEIGHT))
    interface = Interface()
    interface.add_object(Button(
        width=100,
        height=100,
        pos=Vector(10, 10),
        img_path=""
    ))
    # TEMP add test object to workspace
    b = Bezier(Vector(0, 50), Vector(40, 75), Vector(50, 25), Vector(70, 50))
    workspace.add_object(b)
    clock = pygame.time.Clock() # clock to control FPS
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

        screen.fill(BG_COLOR)
        workspace.tick()
        interface.tick()
        pygame.display.update()

        clock.tick(180)