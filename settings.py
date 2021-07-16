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
TITLE = "Zombie Top-down Shooter"
BGCOLOR = LIGHTGREY

# Usu. in pows of 2 e.g. 8, 16, 32, 64, etc.
TILESIZE = 64
GRIDWIDTH = WINDOW_WIDTH / TILESIZE
GRIDHEIGHT = WINDOW_HEIGHT / TILESIZE

WALL_IMG = 'tile_179.png'

# Player settings
PLAYER_MAX_HEALTH = 100
PLAYER_SPEED = 500  # TODO: Reduce in final game
PLAYER_ROT_SPEED = 250  # degrees per second
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)  # needs to be Rect to get center (not Surface)
# By default, player facing right, so offset the bullet 30 to the right (x) and 10 down (y)
BARREL_OFFSET = vec(30, 10)
PLAYER_HEALTH_BAR_HEIGHT = 20
PLAYER_HEALTH_BAR_WIDTH = 100

# Weapon settings
# BULLET_IMG = 'bullet.png' # Using Surface instead.
# MAYBE: Create a Weapon class instead of dictionaries in our settings file
WEAPONS = {}
WEAPONS['pistol'] = {
    'bullet_speed': 750,
    'bullet_lifetime': 1250,
    'fire_rate': 250,  # todo: Increase in final game
    'kickback': 200,
    'bullet_spread': 6,
    'damage': 10,
    'bullet_count': 1,
    'bullet_usage': 1

}
WEAPONS['shotgun'] = {
    'bullet_speed': 500,
    'bullet_lifetime': 500,
    'fire_rate': 900,
    'kickback': 500,
    'bullet_spread': 24,
    'damage': 5,
    'bullet_count': 5,
    'bullet_usage': 1
}
WEAPONS['uzi'] = {
    'bullet_speed': 1000,
    'bullet_lifetime': 750,
    'fire_rate': 100,
    'kickback': 300,
    'bullet_spread': 16,
    'damage': 4,
    'bullet_count': 1,
    'bullet_usage': 1
}

LANDMINE_DAMAGE = 35
LANDMINE_KNOCKBACK = 50
# 'bullet_size': 'lg'
# 'bullet_size': 'sm'

# Mob settings
MOB_IMG = 'zoimbie1_hold.png'
MOB_SPEEDS = [120, 135, 150, 160]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_DAMAGE = 10
MOB_KNOCKBACK = 25
MOB_AVOID_RADIUS = 70  # in px
MOB_DETECT_RADIUS = 400

# Items
ITEM_IMAGES = {
    "health": "health_icon.png",
    "pistol_ammo": "pistol_ammo.png",
    "shotgun_ammo": "shotgun_ammo.png",
    "uzi_ammo": "uzi_ammo.png",
    "landmine": "mine_icon.png",
    "bonus": "bonus.png",
    "comms": "comms_icon.png",
    "shotgun": "shotgun.png",
    "pistol": "pistol.png",
    "uzi": "uzi.png",
    "placed_mine": "landmine.png",
    "tower": "cell_tower.png"
}

GUN_IMAGES = {
    "pistol": "pistol.png",
    "shotgun": "shotgun.png",
    "uzi": "uzi.png"
}

# Item effectiveness
HEALTH_PICKUP_AMT = 20
PISTOL_AMMO_PICKUP_AMT = 7
SHOTGUN_AMMO_PICKUP_AMT = 6
UZI_AMMO_PICKUP_AMT = 14

# Effects
MUZZLE_FLASHES = ["whitePuff15.png", "whitePuff16.png", "whitePuff17.png", "whitePuff18.png"]
FLASH_DURATION = 40  # ms
SPLAT_IMAGES = ['blood-splatter1.png', 'blood-splatter3.png', 'blood-splatter4.png']

ITEM_BOB_RANGE = 50
ITEM_BOB_SPEED = 3

DAMAGE_ALPHA = [i for i in range(0, 255, 20)]
ITEM_ALPHA = [i for i in range(0, 255, 2)]
ITEM_FADE_MIN = 50
ITEM_FADE_MAX = 245
NIGHT_COLOR = (25, 25, 25)
LIGHT_RADIUS = (525, 525)
LIGHT_MASK = 'light_350_med.png'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Sounds
BG_MUSIC = 'Disturbed-Soundscape.ogg'
MENU_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_DEATH_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {
    'pistol': ['pistol.wav'],
    'shotgun': ['shotgun.wav'],
    'uzi': ['pistol.wav']  # TODO
}
EFFECTS_SOUNDS = {
    'level_start': 'level_start.wav',
    'health_up': 'item_pickup.ogg',
    'item_pickup': 'item_pickup.ogg',
    'ammo_pickup': 'ammo_pickup.ogg',
    'gun_pickup': 'gun_pickup.wav',
    'explosion': 'short_explosion.ogg',
    'place_mine1': 'drop_sound.wav',
    'place_mine2': '1beep.mp3'
}

# Dict of level names
LEVELS = {
    'tutorial': 'tutorial.tmx',
    'level1': 'level1.tmx'
}