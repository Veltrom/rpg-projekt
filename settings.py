# Kõik vajalikud konstandid

HELEHALL = (100, 100, 100)

WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Seiklus Deltasse"
BGCOLOR = HELEHALL

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_SPEED = 150
PLAYER_IMG = "kass_idle.png"
MURU_IMG = "muru.png"
POOSAS_IMG = "poosas.png"

PLAYER_ANIMATIONS = {
    "up": ["kass_back_walk2.png","kass_back_stand.png" ,"kass_back_walk1.png"],
    "down": ["kass_front_walk1.png","kass_front_stand.png" , "kass_front_walk2.png"],
    "left": ["kass_left_walk1.PNG","kass_left_stand.PNG" , "kass_left_walk2.PNG"],
    "right": ["kass_side_walk1.png","kass_side_stand.png" ,"kass_side_walk2.png"],
}
