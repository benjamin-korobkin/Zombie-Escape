import pygame as pg
from settings import *
from tilemap import collide_hit_rect
from random import uniform, choice, randint, random
import pytweening as tween
from itertools import chain
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
        self._layer = PLAYER_LAYER
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
        self.is_damaged = False
        self.weapons = ['pistol']
        self.weapon_selection = 0
        # Consider using itertools to cycle thru weapons
        self.curr_weapon = self.weapons[self.weapon_selection]
        self.ammo = 0
        self.landmines = 0

    def got_hit(self):
        self.is_damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

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
            self.shoot()

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        # rotate the image using the above calculation
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.is_damaged:
            try:
                # Use white/transparency to show damage effect. Experiment w special flags if you want.
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.is_damaged = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        # Rotate around the center of the rect for smooth rot animation
        self.hit_rect.centerx = self.pos.x  # self.x
        collided_with_wall(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collided_with_wall(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def shoot(self):
        now = pg.time.get_ticks()
        curr_weapon = WEAPONS[self.curr_weapon]
        bullet_usage = curr_weapon['bullet_count']
        if self.ammo >= bullet_usage and now - self.last_shot > curr_weapon['fire_rate']:  # TODO: else play empty gun sound
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel -= vec(curr_weapon['kickback'], 0).rotate(-self.rot)
            snd = choice(self.game.weapon_sounds[self.curr_weapon])
            # Interesting code to synchronize sounds, but won't be using it.
            #if snd.get_num_channels() > 2:
            #    snd.stop()
            snd.play()
            MuzzleFlash(self.game, pos)
            self.ammo -= bullet_usage
            for i in range(bullet_usage):
                spread = uniform(-curr_weapon['bullet_spread'], curr_weapon['bullet_spread'])
                Bullet(self.game, pos, dir.rotate(spread), curr_weapon['damage'])

    def change_weapon(self):
        self.weapon_selection += 1
        if self.weapon_selection >= len(self.weapons):
            self.weapon_selection = 0
        self.curr_weapon = self.weapons[self.weapon_selection]
        # print("switched to ", self.curr_weapon) # TODO: display weapon name

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()  # prevent bugs. E.g. duplicate health bars
        self.rect = self.image.get_rect()  # fixed bug by using mob_hit_rect.copy() where mobs disappear
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.hit_rect.center  # fixed a bug, similar to what we had earlier w plyr
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.max_health = 50
        self.health = 50
        self.speed = choice(MOB_SPEEDS)
        self.target = self.game.player
        self.is_chasing = False

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


    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                # calculate distance between self's vector and other mobs' vec
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOB_AVOID_RADIUS:
                    # normalize() returns a vector with same dir but length 1
                    self.acc += dist.normalize()  # TODO: learn how vectors work

    def update(self):
        if self.health <= 0:
            choice(self.game.zombie_death_sounds).play()
            self.kill()
            splat_img = choice(self.game.splat_images)
            self.game.map_img.blit(splat_img, self.pos - vec(32,32))
            pg.display.flip()
        else:
            target_dist = self.target.pos - self.pos
            # Prevent bug where health bar is not drawn properly
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            # See note at end of method regarding this line
            # TODO: Mob should be alerted if shot was fired near them
            if not self.is_chasing and target_dist.length_squared() < MOB_DETECT_RADIUS ** 2:
                self.is_chasing = True

            if self.is_chasing:
                if random() < 0.002:
                    choice(self.game.zombie_moan_sounds).play()
                self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                self.acc = vec(1, 0).rotate(-self.rot)
                self.avoid_mobs()
                self.acc.scale_to_length(self.speed)
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

            """Technically, the line below works. But length() of a vector is calculated with Bob's theorem.
            This means getting the square root, which is an expensive operation. sqrt(x**2 + y**2) We save time
            by comparing the squared values instead"""
            # if target_dist.length() < MOB_DETECT_RADIUS:

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.weapon = WEAPONS[game.player.curr_weapon]
        self.image = game.bullet_images[game.player.curr_weapon]  # game.pistol_bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)  # create new vector so we're not referencing the player's pos directly
        self.rect.center = self.pos
        # spread = uniform(-BULLET_SPREAD, BULLET_SPREAD)
        self.vel = dir * self.weapon['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.targets = self.game.mobs
        self.damage = damage
        # My solution: Use a Surface instead of the difficult image.

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.curr_weapon]['bullet_lifetime']:
            self.kill()
        self.alert_mobs()

    def alert_mobs(self):
        for target in self.targets:
            if not target.is_chasing:
                target_dist = target.pos - self.pos
                if target_dist.length_squared() < MOB_DETECT_RADIUS ** 2:
                    target.is_chasing = True

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 30)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
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
        self._layer = WALL_LAYER
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, item_type, ratio):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.ogImage = pg.transform.scale(game.item_images[item_type], ratio)
        self.ogImage.set_colorkey(BLACK)
        self.image = self.ogImage.copy()
        self.rect = self.image.get_rect()
        self.type = item_type
        self.rect.center = pos
        self.pos = pos
        self.is_damaged = False
        self.item_alpha = chain(ITEM_ALPHA * 4)
        #self.animate = tween.easeInBack  # TODO: Look up function to see what included arg can do
        #self.step = 0  # Value btwn 0 and 1, used to step thru animation
        #self.dir = 1  # Will be btwn 1 and -1. E.g. To bob up and down
        self.counter = ITEM_FADE_MIN
        self.increment = 3

    def update(self):
        # Fade in/out animation --> see main#draw
        self.image = self.ogImage.copy()
        self.counter += self.increment
        if self.counter > ITEM_FADE_MAX or self.counter < ITEM_FADE_MIN:
            self.increment = -self.increment
        self.image.fill((255,255,255, min(255,self.counter)), special_flags=pg.BLEND_RGBA_MULT)
        self.rect.center = self.pos

        # Bobbing animation
"""
        offset = ITEM_BOB_RANGE * (self.animate(self.step / ITEM_BOB_RANGE) - 0.5)  # - 0.5 to start 'mid-animation'
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += ITEM_BOB_SPEED
        if self.step > ITEM_BOB_RANGE:
            self.step = 0  # Restart/reposition
            self.dir *= -1  # allows us to switch btwn up and down
"""


class Text(pg.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.text = text
        font = pg.font.Font(self.game.title_font, 24)  # font_name, size
        self.image = font.render(text, True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)