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
    content = config[_type]
    return  content


def get_screen_resolution(y_offset):
    monitors = [m for m in get_monitors()]
    return  monitors[0].width, monitors[0].height - y_offset

if __name__ == "__main__":
    # set up DISPLAY
    WIDTH, HEIGHT = get_screen_resolution(Y_OFFSET)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("UwUctory")
    # get colors from config file
    colors = load_config("main.ini", "COLOR_PALETTE")
    BG_COLOR = tuple(map(int, colors['bg'].replace(",", "")[1:-1].split()))
    OUTLINE_COLOR = tuple(map(int, colors['outline'].replace(",", "")[1:-1].split()))
    LINE_COLOR = tuple(map(int, colors['outline'].replace(",", "")[1:-1].split()))
    # set up workspace and interface
    nav = Navigation()
    workspace = Workspace((100, 100), (WIDTH, HEIGHT), nav)
    interface = Interface()
    interface.add_object(Button(
        width=85,
        height=85,
        pos=Vector(10, 10),
        img_path=os.path.join(os.getcwd(), "icons", "curve.png")
    ))
    # TEMP add test object to workspace
    b = Bezier(Vector(0, 50), Vector(40, 75), Vector(50, 25), Vector(70, 50))
    # workspace.add_object(b)
    clock = pygame.time.Clock() # clock to control FPS
    while True:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_SPACE]:
                exit(0)
            nav.process_event(event)
        screen.fill(BG_COLOR)
        workspace.tick()
        nav.tick()
        interface.tick()
        pygame.display.update()

        clock.tick(180)