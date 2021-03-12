import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
# Ensure no partial squares with these values
WINDOW_WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
WINDOW_HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Dungeon Adventure"
BGCOLOR = LIGHTGREY

# Usu. in pows of 2 e.g. 8, 16, 32, 64, etc.
TILESIZE = 64
GRIDWIDTH = WINDOW_WIDTH / TILESIZE
GRIDHEIGHT = WINDOW_HEIGHT / TILESIZE

WALL_IMG = 'tile_179.png'

# Player settings
PLAYER_MAX_HEALTH = 100
PLAYER_SPEED = 250
PLAYER_ROT_SPEED = 250  # degrees per second
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
# By default, player facing right, so offset the bullet 30 to the right (x) and 10 down (y)
BARREL_OFFSET = vec(30, 10)
PLAYER_HEALTH_BAR_HEIGHT = 20
PLAYER_HEALTH_BAR_WIDTH = 100

# Gun settings
# BULLET_IMG = 'bullet.png' # Using Surface instead.
BULLET_SPEED = 1000
BULLET_LIFETIME = 1250
BULLET_RATE = 300  # How fast we can shoot bullets
BULLET_KICKBACK = 200
BULLET_SPREAD = 5
BULLET_DAMAGE = 10

# Mob settings
MOB_IMG = 'zoimbie1_hold.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_DAMAGE = 10
MOB_KNOCKBACK = 25