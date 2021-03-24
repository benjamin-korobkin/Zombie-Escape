import pygame as pg
from settings import *
from tilemap import collide_hit_rect
from random import uniform
vec = pg.math.Vector2


def collided_with_wall(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        # Stick to wall if we hit it
        # Generally bad practice to use list[0] but this works for now
        # with the yellow square we based on corner of rect, for sprite use center.
        if hits:
            if hits[0].rect.centerx >= sprite.hit_rect.centerx:  # sprite.x starts at top left of sprite
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            elif hits[0].rect.centerx <= sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        # Stick to wall if we hit it
        # Generally bad practice to use list[0] but this works for now
        if hits:
            if hits[0].rect.centery >= sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            elif hits[0].rect.centery <= sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        #self.image.set_colorkey(BLACK)
        # x and y determine where the plyr will be drawn. See update()
        # self.x = x * TILESIZE
        # self.y = y * TILESIZE
        # self.vx, self.vy = 0, 0
        self.pos = vec(x, y)  # * TILESIZE
        self.vel = vec(0, 0)
        self.rot = 270  # rotation
        self.last_shot = 0
        self.health = PLAYER_MAX_HEALTH

    def get_keys(self):
        self.rot_speed = 0
        # self.vx, self.vy = 0, 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        # Keeping this here for pre-rotate movement reference:
        # if self.vel.x != 0 and self.vel.y != 0:
        # self.vel *= 0.7071
        # self.vx *= 0.7071  # 1 / Sqrt of 2
        # self.vy *= 0.7071
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED/2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                self.vel -= vec(BULLET_KICKBACK, 0).rotate(-self.rot)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        # rotate the image using the above calculation
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        # Rotate around the center of the rect for smooth rot animation
        self.hit_rect.centerx = self.pos.x  # self.x
        collided_with_wall(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collided_with_wall(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        #self.image.set_colorkey(BLACK)


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.max_health = 50
        self.health = 50

    def draw_health(self):
        hp_percent = self.health / self.max_health
        if hp_percent > .65:
            col = GREEN
        elif hp_percent > .45:
            col = YELLOW
        else:
            col = RED
        bar_width = int(self.rect.width * self.health / 100)
        bar_height = 7
        self.health_bar = pg.Rect(0, 0, bar_width, bar_height)
        if self.health < self.max_health:
            pg.draw.rect(self.image, col, self.health_bar)

    def update(self):
        if self.health <= 0:
            self.kill()
        else:
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
            self.acc += self.vel * -1  # friction to slow down movement
            self.vel += self.acc * self.game.dt
            # Using equation of motion
            self.pos += self.vel * self.game.dt + (0.5 * self.acc * (self.game.dt ** 2))
            self.hit_rect.centerx = self.pos.x
            collided_with_wall(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collided_with_wall(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
            if self.health < self.max_health:
               self.draw_health()

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)  # create new vector so we're not referencing the player's pos directly
        self.rect.center = self.pos
        spread = uniform(-BULLET_SPREAD, BULLET_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

        # My solution: Use a Surface instead of the dumb image.

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
