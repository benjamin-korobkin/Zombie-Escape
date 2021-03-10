# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 1
# Project setup
# Video link: https://youtu.be/3UxnelT9aCo
import pygame as pg
import sys
from os import path
from settings import *
from tilemap import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)  # Allows you to hold down a key
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)  # Where our game is running from
        img_folder = path.join(game_folder, 'img')
        # Grab our game layout file (map)
        self.map = Map(path.join(game_folder, 'map3.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()  # Surface
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()  # Surface
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))  # can scale image
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()  # Surface
        # pg.draw.circle(surface, color, center, radius)  # Each image is a Surface
        self.bullet_img = pg.Surface((5, 5))
            #pg.draw.circle(self.screen, BLACK, (0, 0), 5)  # pg.image.load(path.join(img_folder,
        # BULLET_IMG)).convert_alpha()


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for row,tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.kill()

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, TILESIZE):
            pg.draw.line(self.screen, WHITE, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, TILESIZE):
            pg.draw.line(self.screen, WHITE, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # for wall in self.walls:
        #    pg.draw.rect(self.screen, WHITE, wall.rect, 2)
        # Draw player's rect. Good for debugging.   Thickness of 2
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()


    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()



    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()