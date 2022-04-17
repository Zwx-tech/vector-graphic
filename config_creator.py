from configparser import ConfigParser
import os

cp = ConfigParser()

cp["COLOR_PALETTE"] = {
    "bg": (106, 140, 175), # 6A8CAF
    "interface": (96, 130, 165), # 6A8CAF
    "outline": (255, 255, 255), # FFFFFF
    "lines": (0, 0, 0) # 000000
}

with open(os.path.join(os.getcwd(), "config", "main.ini"), "w") as f:
    cp.write(f)
