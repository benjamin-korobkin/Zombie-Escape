import pygame as pg
import sys
from os import path
from settings import *
from tilemap import *
from sprites import *
from menu import *

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
        pg.mixer.pre_init(22050, -16, 2, 1024) # change last value to increase buffer size to load
        # sounds properly before playing them. Must be power of 2 (512, 1024, 2048, etc.
        pg.init()
        pg.mixer.quit()
        pg.mixer.pre_init(22050, -16, 2, 1024)
        pg.init()
        self.running = True
        self.playing = False  # Only true when player selects 'new game' or 'continue'
        self.display = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption(TITLE)
        self.fullscreen = False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, \
            self.RIGHT_KEY = False, False, False, False, False, False
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)  # Allows you to hold down a key
        self.all_sounds = []
        self.soundfx_lvl = .8
        self.music_lvl = .8
        self.load_data()
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.volume_menu = VolumeMenu(self)
        self.controls_menu = ControlsMenu(self)
        self.pause_menu = PauseMenu(self)
        self.curr_menu = self.main_menu
        self.prev_menu = self.main_menu
        pg.mixer.music.play(loops=-1)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

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
        self.sound_folder = path.join(self.game_folder, 'snd')
        self.music_folder = path.join(self.game_folder, 'music')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.explosion_sheet = pg.image.load(path.join(img_folder, 'explosion.png')).convert_alpha()
        self.explosion_frames = []
        EXPL_WIDTH = 130
        EXPL_HEIGHT = 130
        x = 0
        y = -25
        for i in range(5):
            for j in range(5):
                img = pg.Surface((EXPL_WIDTH, EXPL_HEIGHT))
                img.blit(self.explosion_sheet, (0, 0), (x, y, EXPL_WIDTH, EXPL_HEIGHT))
                img.set_colorkey(BLACK)
                img = pg.transform.scale(img, (round(EXPL_WIDTH * 2.8), round(EXPL_HEIGHT * 2.8)))
                self.explosion_frames.append(img)
                x += EXPL_WIDTH
            x = 0
            y += EXPL_HEIGHT

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
        pg.mixer.music.load(path.join(self.music_folder, MENU_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            snd = pg.mixer.Sound(path.join(self.sound_folder, EFFECTS_SOUNDS[type]))
            snd.set_volume(self.soundfx_lvl)
            self.effects_sounds[type] = snd
            self.all_sounds.append(snd)

        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(self.sound_folder, snd))
                s.set_volume(0.5)
                self.weapon_sounds[weapon].append(s)
                self.all_sounds.append(s)

        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(self.sound_folder, snd))
            self.player_hit_sounds.append(s)
            self.all_sounds.append(s)


        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(self.sound_folder, snd))
            s.set_volume(0.1)
            self.zombie_moan_sounds.append(s)
            self.all_sounds.append(s)

        self.zombie_death_sounds = []
        for snd in ZOMBIE_DEATH_SOUNDS:
            s = pg.mixer.Sound(path.join(self.sound_folder, snd))
            self.zombie_death_sounds.append(s)
            self.all_sounds.append(s)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.load_level(LEVELS['tutorial'])

    def load_level(self, level_name=LEVELS['tutorial'], stats=None):
        self.all_sprites = pg.sprite.LayeredUpdates()  # Group()
        self.walls = pg.sprite.Group()
        self.towers = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.landmines = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        # Grab our game layout file (map)
        self.current_lvl = level_name
        self.map = TiledMap(path.join(self.map_folder, level_name))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.texts = pg.sprite.Group()  # Created sprite group of texts, and apply the camera on them
        # Amount of comms needed to beat level
        self.comms_req = 0
        # load everything on map
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                if stats:
                    self.player = Player(self, obj_center.x, obj_center.y, stats)
                else:
                    self.player = Player(self, obj_center.x, obj_center.y)
            elif tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            elif tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y) # pass
            elif tile_object.name == 'tower':
                Tower(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
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
                    self.comms_req += 1
                elif tile_object.name in GUN_IMAGES:
                    ratio = (48, 48)
                elif tile_object.name == 'pistol_ammo' or tile_object.name == 'shotgun_ammo' \
                        or tile_object.name == 'uzi_ammo':
                    ratio = (32, 32)
                elif tile_object.name == 'landmine':
                    ratio = (32, 32)
                Item(self, obj_center, tile_object.name, ratio)
            elif tile_object.type == 'text':  # putting text in object name
                Text(self, tile_object.x, tile_object.y, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.music_off = False  # placeholders for future option to turn off/on music/sounds
        self.sound_off = False
        self.is_night = False
        self.effects_sounds['level_start'].play()

    def game_loop(self):
        # game loop - set self.playing = False to end the game
        pg.mixer.music.stop()
        pg.mixer.music.load(path.join(self.music_folder, BG_MUSIC))
        pg.mixer.music.play(loops=-1)
        for snd in self.all_sounds:
            snd.set_volume(self.soundfx_lvl)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.paused:
                self.pause_menu.display_menu()
            else:
                self.update()
            self.draw()
            #self.reset_keys()

    def quit(self):
        try:
            with open('savefile.txt', 'w') as f:
                for stat in self.player.stats.values():
                    f.write(str(stat))
                    f.write('\n')
                savedata = self.current_lvl
                f.write(savedata)
        except:
            print("Couldn't properly save.")
        finally:
            self.running, self.playing = False, False
            self.curr_menu.run_display = False
            pg.quit()
            sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

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

        # Player touches explosion
        hits = pg.sprite.spritecollide(self.player, self.explosions, False, collide_hit_rect)
        if not self.player.is_damaged and hits:
            self.player.got_hit()
            self.player.pos -= vec(LANDMINE_KNOCKBACK, 0).rotate(self.player.rot)
            for hit in hits:
                self.player.health -= LANDMINE_DAMAGE
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
        # Mobs touch mine
        hits = pg.sprite.groupcollide(self.mobs, self.landmines, False, True)
        if hits:
            self.effects_sounds['explosion'].play()
        for mob in hits:
            Explosion(self, mob.pos)
        # Mobs touch explosion
        hits = pg.sprite.groupcollide(self.mobs, self.explosions, False, False)
        for mob in hits:
            mob.health -= LANDMINE_DAMAGE + self.player.stats['dmg_bonus']
            mob.vel = vec(0, 0)
        # Player touches item
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:  # TODO: Put sounds in an object instead of a dictionary
            if hit.type == 'health' and self.player.health < PLAYER_MAX_HEALTH:
                self.effects_sounds['health_up'].play()  # TODO: Find different sound
                self.player.health = min(self.player.health + HEALTH_PICKUP_AMT, PLAYER_MAX_HEALTH)
                hit.kill()
            elif hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapons.append('shotgun')
                self.player.weapon_selection += 1
                self.player.curr_weapon = 'shotgun'
                self.player.ammo['shotgun_ammo'] += SHOTGUN_AMMO_PICKUP_AMT + self.player.stats['ammo_bonus']
            elif hit.type == 'uzi':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapons.append('uzi')
                self.player.weapon_selection += 1
                self.player.curr_weapon = 'uzi'
                self.player.ammo['uzi_ammo'] += UZI_AMMO_PICKUP_AMT + self.player.stats['ammo_bonus']
            elif hit.type == 'pistol_ammo':
                hit.kill()
                self.player.ammo['pistol_ammo'] += PISTOL_AMMO_PICKUP_AMT + self.player.stats['ammo_bonus']
                self.effects_sounds['ammo_pickup'].play()
            elif hit.type == 'shotgun_ammo':
                hit.kill()
                self.player.ammo['shotgun_ammo'] += SHOTGUN_AMMO_PICKUP_AMT + self.player.stats['ammo_bonus']
                self.effects_sounds['ammo_pickup'].play()
            elif hit.type == 'uzi_ammo':
                hit.kill()
                self.player.ammo['uzi_ammo'] += UZI_AMMO_PICKUP_AMT + self.player.stats['ammo_bonus']
                self.effects_sounds['ammo_pickup'].play()
            elif hit.type == 'landmine':
                hit.kill()
                self.player.ammo['landmines'] += 1 + self.player.stats['ammo_bonus']
                self.effects_sounds['ammo_pickup'].play()
            elif hit.type == 'comms':
                hit.kill()
                self.player.comms += 1
                self.effects_sounds['item_pickup'].play()

        # Bullet touches BonusItem
        hits = pg.sprite.groupcollide(self.items, self.bullets, False, False)
        for hit in hits:
            if isinstance(hit, BonusItem):
                hit.kill()
                hit.activate(self.player)
                self.player.stats['bonuses'] += 1
        # Check if we beat level (returned comms)
        hits = pg.sprite.spritecollide(self.player, self.towers, False, False)
        for hit in hits:
            if self.player.comms >= self.comms_req:
                self.player.kill()
                if self.current_lvl == LEVELS['tutorial']:
                    self.show_menu_screen("TUTORIAL COMPLETE --- PRESS ANY KEY TO CONTINUE")
                    self.load_level(LEVELS['level1'], self.player.stats)
                elif self.current_lvl == LEVELS['level1']:
                    self.playing = False

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
        self.draw_text(' - {}'.format(curr_weapon_ammo_amt), self.hud_font, 30, BLACK, 45, 30, align='nw')

        # display zombies left
        self.draw_text('ZOMBIES - {}'.format(len(self.mobs)), self.hud_font, 30, WHITE,
                       WINDOW_WIDTH - 10, 10, align='ne')

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_g:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p or event.key == pg.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pg.K_j:
                    self.is_night = not self.is_night
                # Not the best design, but for convenience putting player action keys here
                if event.key == pg.K_c:
                    self.player.change_weapon()
                if event.key == pg.K_x:
                    self.player.place_mine()
                if event.key == pg.K_F4:
                    self.toggle_fullscreen()

    def menu_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.START_KEY = True
                if event.key == pg.K_UP:
                    self.UP_KEY = True
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pg.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pg.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pg.K_BACKSPACE or event.key == pg.K_ESCAPE:
                    self.BACK_KEY = True

    def reset_keys(self):
        self.START_KEY, self.BACK_KEY, self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, \
            self.RIGHT_KEY = False, False, False, False, False, False

    def show_menu_screen(self, txt):
        self.screen.fill(BLACK)
        self.draw_text(txt, self.menu_font, 48, RED,
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
                    self.quit()
                # Use KEYUP instead of KEYDOWN so that player isn't pressing a key as we're starting
                if event.type == pg.KEYUP:
                    waiting = False