# KidsCanCode - Game Development with Pygame video series
# Tile-based game
# Video link: https://youtu.be/3UxnelT9aCo
# Credit to Kenney for Game Art
# Credit to Eric Matyas for Music
import pygame as pg
import sys
from os import path
from settings import *
from tilemap import *
from sprites import *

def draw_health(surface, x, y, health_pct, ammo, landmines):
    if health_pct < 0:
        health_pct = 0
    fill = health_pct * PLAYER_HEALTH_BAR_WIDTH
    outline_rect = pg.Rect(x, y, PLAYER_HEALTH_BAR_WIDTH, PLAYER_HEALTH_BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, PLAYER_HEALTH_BAR_HEIGHT)
    if health_pct > 0.65:
        col = GREEN
    elif health_pct > 0.45:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surface, col, fill_rect)
    pg.draw.rect(surface, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)  # Allows you to hold down a key
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align='nw'):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == 'nw':
            text_rect.topleft = (x, y)
        elif align == 'ne':
            text_rect.topright = (x, y)
        elif align == 'sw':
            text_rect.bottomleft = (x, y)
        elif align == 'se':
            text_rect.bottomright = (x, y)
        elif align == 'n':
            text_rect.midtop = (x, y)
        elif align == 'e':
            text_rect.midright = (x, y)
        elif align == 's':
            text_rect.midbottom = (x, y)
        elif align == 'w':
            text_rect.midleft = (x, y)
        elif align == 'center':
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)  # Where our game is running from
        img_folder = path.join(game_folder, 'img')
        sound_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        map_folder = path.join(game_folder, 'maps')
        # Grab our game layout file (map)
        self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.title_font = path.join(img_folder, 'DemonSker-zyzD.ttf')  # TTF = True Type Font
        self.menu_font = path.join(img_folder, 'DemonSker-zyzD.ttf')  # TODO: Experiment
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()  # Surface
        # self.player_img.set_colorkey(BLACK)  # Doesn't work
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()  # Surface
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))  # can scale image
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()  # Surface
        # pg.draw.circle(surface, color, center, radius)  # Each image is a Surface
        self.bullet_img = pg.Surface((5, 5))
            #pg.draw.circle(self.screen, BLACK, (0, 0), 5)  # pg.image.load(path.join(img_folder,
        # BULLET_IMG)).convert_alpha()
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = (pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha())
        self.splat_images = []
        for img in SPLAT_IMAGES:
            i = pg.image.load(path.join(img_folder, img)).convert_alpha()
            i = pg.transform.scale(i, (64, 64))
            self.splat_images.append(i)
        # Load sounds
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(sound_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        self.weapon_sounds['gun'] = []
        for snd in WEAPON_SOUNDS_GUN:
            self.weapon_sounds['gun'].append(pg.mixer.Sound(path.join(sound_folder, snd)))
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(sound_folder, snd)))
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(sound_folder, snd))
            s.set_volume(0.1)
            self.zombie_moan_sounds.append(s)
        self.zombie_death_sounds = []
        for snd in ZOMBIE_DEATH_SOUNDS:
            self.zombie_death_sounds.append(pg.mixer.Sound(path.join(sound_folder, snd)))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()  #Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        # for row,tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.music_off = False  # placeholders for future option to turn off/on music/sounds
        self.sound_off = False
        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        # TODO: Give player temp invincibility when hit
        self.all_sprites.update()
        self.camera.update(self.player)
        # Mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # Bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
        # Player touches item
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_MAX_HEALTH:
                # self.effects_sounds['health_up'].play()  # TODO: Find different sound
                self.player.health = min(self.player.health + HEALTH_PICKUP_AMT, PLAYER_MAX_HEALTH)
                hit.kill()

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, TILESIZE):
            pg.draw.line(self.screen, WHITE, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, TILESIZE):
            pg.draw.line(self.screen, WHITE, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            # if isinstance(sprite, Mob):  # I put this in the Mob.update instead
            #    sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply_sprite(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, GREEN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, GREEN, self.camera.apply_rect(wall.rect), 1)
        # for wall in self.walls:
        #    pg.draw.rect(self.screen, WHITE, wall.rect, 2)
        # Draw player's rect. Good for debugging.   Thickness of 2
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD
        draw_health(self.screen, 5, 5, self.player.health / PLAYER_MAX_HEALTH,
                    self.player.ammo, self.player.landmines)
        if self.paused:
            self.draw_text("PAUSED", self.title_font, 128, RED, WINDOW_WIDTH / 2,
                           WINDOW_HEIGHT / 2, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_g:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        self.paused = True
        self.screen.fill(BLACK)
        self.draw_text("PRESS ANY KEY TO BEGIN", self.menu_font, 48, RED,
                       WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, align="center")
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        pass

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()