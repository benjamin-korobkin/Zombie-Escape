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

FONT_NAME = 'arial'

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
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)  # needs to be Rect to get center (not Surface)
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
MOB_SPEEDS = [120, 135, 150, 165]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_DAMAGE = 10
MOB_KNOCKBACK = 25
MOB_AVOID_RADIUS = 70  # in px
MOB_DETECT_RADIUS = 400

# Items
ITEM_IMAGES = {
    "health": "health_icon.png",
    "ammo": "bullet_icon.png",
    "ammo_plus": "bullets_icon.png",
    "landmine": "mine_icon.png",
    "accuracy_up": "bullseye_icon.png"
}

# Item effectiveness
HEALTH_PICKUP_AMT = 20
AMMO_PICKUP_AMT = 5
AMMO_PICKUP_PLUS_AMT = 10
ACCURACY_PICKUP_AMT = 2


# Effects
MUZZLE_FLASHES = ["whitePuff15.png", "whitePuff16.png", "whitePuff17.png", "whitePuff18.png"]
FLASH_DURATION = 40  # ms
SPLAT_IMAGES = ['blood-splatter1.png', 'blood-splatter2.png', 'blood-splatter3.png', 'blood-splatter4.png']
ITEM_BOB_RANGE = 4
ITEM_BOB_SPEED = 0.15


# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Sounds
BG_MUSIC = 'Disturbed-Soundscape.ogg'  # 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_DEATH_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS_GUN = ['pistol.wav']
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav'}