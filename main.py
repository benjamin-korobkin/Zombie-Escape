# KidsCanCode - Game Development with Pygame video series
# Tile-based game
# Video link: https://youtu.be/3UxnelT9aCo
# Credit to Kenney for Game Art
# Credit to Eric Matyas for Music
# Weapon icons from Flaticon (attribution required)
# (Credit creator of icons.svg, opengameart)
import pygame as pg
import sys
from os import path
from settings import *
from tilemap import *
from sprites import *

# MAJOR FIX NEEDED FOR FILE STRUCTURING RELATED TO MAPS
# Pygame keeps complaining about not finding certain files related to our map/tiles
# FIXED, see tilemap::render. They keep changing to black boxes when other things drawn over them. Same with blood splats

def draw_health(surface, x, y, health_pct):
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
        # pg.mixer.pre_init(44100, -16, 1, 2048) # change last value to increase buffer size to load
        # sounds properly before playing them. Must be power of 2 (512, 1024, 2048, etc.)
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
        self.game_folder = path.dirname(__file__)  # Where our game is running from
        img_folder = path.join(self.game_folder, 'img')
        sound_folder = path.join(self.game_folder, 'snd')
        music_folder = path.join(self.game_folder, 'music')
        self.map_folder = path.join(self.game_folder, 'maps')

        self.title_font = path.join(img_folder, 'DemonSker-zyzD.ttf')  # TTF = True Type Font
        self.menu_font = path.join(img_folder, 'DemonSker-zyzD.ttf')  # TODO: Experiment
        self.hud_font = path.join(img_folder, 'DemonSker-zyzD.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))  # BLACK with 180 transparency
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()  # Surface
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()  # Surface
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))  # can scale image
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()  # Surface
        # pg.draw.circle(surface, color, center, radius)  # Each image is a Surface
        self.gun_images = {}
        for gun in GUN_IMAGES:
            gun_img = (pg.image.load(path.join(img_folder, GUN_IMAGES[gun])).convert_alpha())
            gun_img = pg.transform.scale(gun_img, (32, 32))
            self.gun_images[gun] = gun_img

        self.bullet_images = {}
        self.pistol_bullet_img = pg.Surface((7, 7))
        self.bullet_images['pistol'] = self.pistol_bullet_img
        self.shotgun_bullet_img = pg.Surface((3, 3))
        self.bullet_images['shotgun'] = self.shotgun_bullet_img
        self.uzi_bullet_img = pg.Surface((4, 4))
        self.bullet_images['uzi'] = self.uzi_bullet_img
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())

        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = (pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha())

        self.splat_images = []
        for img in SPLAT_IMAGES:
            i = pg.image.load(path.join(img_folder, img)).convert_alpha()
            i.set_colorkey(BLACK)
            i = pg.transform.scale(i, (64, 64))
            self.splat_images.append(i)

        # lighting effect
        self.fog = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        # Load sounds
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            snd = pg.mixer.Sound(path.join(sound_folder, EFFECTS_SOUNDS[type]))
            snd.set_volume(0.7)
            self.effects_sounds[type] = snd

        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(sound_folder, snd))
                s.set_volume(0.5)
                self.weapon_sounds[weapon].append(s)

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

        # Grab our game layout file (map)
        self.map = TiledMap(path.join(self.map_folder, 'tutorial.tmx')) #'level1.tmx'
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.texts = pg.sprite.Group()  # Created sprite group of texts, and apply the camera on them

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
            elif tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            elif tile_object.name == 'zombie':
                pass#Mob(self, obj_center.x, obj_center.y)
            elif tile_object.name in ITEM_IMAGES.keys():
                if tile_object.name == 'bonus':
                    ratio = (32, 32)
                    if tile_object.type == 'x':
                        BonusItem(self, obj_center, 'x', ratio)
                    else:
                        BonusItem(self, obj_center, 'y', ratio)
                    continue
                elif tile_object.name == 'health':
                    ratio = (32, 32)
                elif tile_object.name == 'comms':
                    ratio = (48, 48)
                elif tile_object.name in GUN_IMAGES:
                    ratio = (48, 48)
                elif tile_object.name == 'pistol_ammo' or tile_object.name == 'shotgun_ammo' \
                        or tile_object.name == 'uzi_ammo':
                    ratio = (32, 32)
                Item(self, obj_center, tile_object.name, ratio)
            elif tile_object.type == 'text':  # putting text in object name
                #print(tile_object.name)
                Text(self, tile_object.x, tile_object.y, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.music_off = False  # placeholders for future option to turn off/on music/sounds
        self.sound_off = False
        self.is_night = False
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
        self.all_sprites.update()
        self.camera.update(self.player)
        # Game over
        if len(self.mobs) == 0: # TODO: Change game over condition
            pass
            #self.playing = False
        # Mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        if not self.player.is_damaged and hits:
            self.player.got_hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            for hit in hits:
                    self.player.health -= MOB_DAMAGE
                    if random() < 0.9:
                        choice(self.player_hit_sounds).play()
                    hit.vel = vec(0, 0)
                    if self.player.health <= 0:
                        self.playing = False

        # Bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            # Multiply dmg by amount of bullets that hit the mob using len(hits[hit]) keep in mind hits is a dict
            # hit.health -= WEAPONS[self.player.curr_weapon]['damage'] * len(hits[hit])  # TODO: ensure correctness
            # Purpose for doing it this way to ensure that the bullet damage doesn't depend on which gun the player is
            # holding
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)
        # Player touches item
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:  # TODO: Put sounds in an object instead of a dictionary
            if hit.type == 'health' and self.player.health < PLAYER_MAX_HEALTH:
                # self.effects_sounds['health_up'].play()  # TODO: Find different sound
                self.player.health = min(self.player.health + HEALTH_PICKUP_AMT, PLAYER_MAX_HEALTH)
                hit.kill()
            elif hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapons.append('shotgun')
                self.player.weapon_selection += 1
                self.player.curr_weapon = 'shotgun'
                self.player.shotgun_ammo += SHOTGUN_AMMO_PICKUP_AMT
            elif hit.type == 'uzi':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapons.append('uzi')
                self.player.weapon_selection += 1
                self.player.curr_weapon = 'uzi'
                self.player.uzi_ammo += UZI_AMMO_PICKUP_AMT
            elif hit.type == 'pistol_ammo':
                hit.kill()
                self.player.pistol_ammo += PISTOL_AMMO_PICKUP_AMT
                # TODO, get sound: self.effects_sounds['ammo_pickup'].play()
            elif hit.type == 'shotgun_ammo':
                hit.kill()
                self.player.shotgun_ammo += SHOTGUN_AMMO_PICKUP_AMT
            elif hit.type == 'uzi_ammo':
                hit.kill()
                self.player.uzi_ammo += UZI_AMMO_PICKUP_AMT
            elif hit.type == 'landmine':
                hit.kill()
                self.player.landmines += 1

        # Bullet touches BonusItem
        hits = pg.sprite.groupcollide(self.items, self.bullets, False, True)
        for hit in hits:
            if hit.type == 'bonus':
                hit.kill()

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, TILESIZE):
            pg.draw.line(self.screen, WHITE, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, TILESIZE):
            pg.draw.line(self.screen, WHITE, (0, y), (WINDOW_WIDTH, y))

    def render_fog(self):
        # draw the light mask (gradient) onto the fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply_sprite(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)  # mask -> light_rect
        # BLEND_MULT blends somehow by multiplying adjacent pixels color's (int values)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

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
        if self.is_night:
            self.render_fog()
        draw_health(self.screen, 5, 5, self.player.health / PLAYER_MAX_HEALTH)

        # Display current weapon
        self.screen.blit(self.gun_images[self.player.curr_weapon], (10, 25))
        # Display current ammo
        curr_weapon_ammo_amt = self.player.get_ammo(self.player.curr_weapon)
        self.draw_text(' - {}'.format((curr_weapon_ammo_amt)), self.hud_font, 30, BLACK, 45, 30, align='nw')

         # display zombies left
        self.draw_text('ZOMBIES - {}'.format(len(self.mobs)), self.hud_font, 30, WHITE,
                       WINDOW_WIDTH - 10, 10, align='ne')

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))  # top left of rect position
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
                if event.key == pg.K_c:
                    self.player.change_weapon()
                if event.key == pg.K_j:
                    self.is_night = not self.is_night

    def show_start_screen(self):
        self.paused = True
        self.screen.fill(BLACK)
        self.draw_text("PRESS ANY KEY TO BEGIN", self.menu_font, 48, RED,
                       WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, align="center")
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 120, RED,
                       WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, align="center")
        self.draw_text("PRESS ANY KEY TO BEGIN", self.title_font, 48, WHITE,
                       WINDOW_WIDTH / 2, WINDOW_HEIGHT * 3/4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                # Use KEYUP instead of KEYDOWN so that player isn't pressing a key as we're starting
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    #g.show_go_screen()