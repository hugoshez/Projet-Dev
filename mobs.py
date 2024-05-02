import random
import os
import math
import pygame as pg
import settings as s
import sprites

vec = pg.math.Vector2

# Moving objects (technically sprites)


class Mob(pg.sprite.Sprite):
    def __init__(self, game, img_dim, spritesheet_file, stop_game, spawn=(0, 0)):
        super().__init__()
        self.game = game
        # stop game if hit
        self.stop_game = stop_game

        self.img_dim = img_dim
        self.animation = None
        self.last_anim = pg.time.get_ticks()
        self.anim_data = {
            "melee": {
                "time": 100,
                "coords": [(0, 0), (0, img_dim[1])]
            },
            "weapon": {
                "time": 100,
                "coords": [(img_dim[0], 0), (img_dim[0], img_dim[1])]
            }
        }
        self.anim_frame = 0

        self.spritesheet = sprites.Spritesheet(os.path.join(s.img_folder, spritesheet_file))
        self.image_orig = self.spritesheet.get_image(self.anim_data["melee"]["coords"][0], img_dim)
        self.image_orig.set_colorkey(s.BLACK)
        self.image = self.image_orig
        self.rect_orig = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.hitbox = pg.rect.Rect(self.rect.x, self.rect.y, self.rect_orig.width - 2 * s.PIXEL_MULT,
                                   self.rect_orig.height - 2 * s.PIXEL_MULT)
        self.hitbox.center = self.rect_orig.center

        self.last_punch = pg.time.get_ticks()

        self.pos = vec(spawn[0], spawn[1])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0

        self.current_weapon = None
        # add to group
        self.game.all_sprites.add(self)
        self.game.mobs.add(self)

    def update(self):
        self.act()
        self.animate()
        self.move()
        # move also includes rotating
        self.check_hit()

    def move_calc(self):
        # apply friction
        self.acc += self.vel * s.PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc

        # first move x then y for better collision detection
        if self.vel.x != 0:
            self.pos.x += round(self.vel.x + 0.5 * self.acc.x, 1)
            self.hitbox.center = self.pos
            self.check_collision('x')

        if self.vel.y != 0:
            self.pos.y += round(self.vel.y + 0.5 * self.acc.y, 1)
            self.hitbox.center = self.pos
            self.check_collision('y')

        # set rect to new calculated pos
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def check_collision(self, axis):
        for wall in self.game.walls:
            if axis == 'x':
                if abs(wall.rect.centerx - self.pos.x) < 100:
                    if self.hitbox.colliderect(wall):
                        if self.vel.x < 0:
                            self.hitbox.left = wall.rect.right
                        elif self.vel.x > 0:
                            self.hitbox.right = wall.rect.left
                        self.pos.x = self.hitbox.centerx
            else:
                if abs(wall.rect.centery - self.pos.y) < 100:
                    if self.hitbox.colliderect(wall):
                        if self.vel.y < 0:
                            self.hitbox.top = wall.rect.bottom
                        elif self.vel.y > 0:
                            self.hitbox.bottom = wall.rect.top
                        self.pos.y = self.hitbox.centery

    def check_hit(self):
        for bullet in self.game.bullets:
            if self.hitbox.colliderect(bullet):
                s.hit.play()
                bullet.kill()
                self.kill()

    def attack(self):
        if self.current_weapon is not None:
            if self.current_weapon.shoot(self.rect.centerx, self.rect.centery, self.rot):
                # checks if can shoot only, then wil animate
                self.animation = "weapon"
        else:
            self.punch()

    def punch(self):
        now = pg.time.get_ticks()
        if now - self.last_punch > 300:
            self.animation = "melee"
            self.last_punch = now
            s.punch.play()
            for mob in self.game.mobs:
                if mob is not self:
                    if self.hitbox.colliderect(mob):
                        s.hit.play()
                        mob.kill()

    def rotate(self, point):
        # turns sprite to face towards player
        # calculate relative offset from point
        offset = (point[0] - self.pos.x, point[1] - self.pos.y)
        # rotate
        self.rot = 180 + round(math.degrees(math.atan2(offset[0], offset[1])), 1)
        # make sure image keeps center
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.image_orig, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def kill(self):
        super().kill()
        if self.stop_game:
            self.game.playing = False
        if self.current_weapon is not None:
            self.current_weapon.toggle_item()
            self.current_weapon.rect.center = self.pos
            self.current_weapon = None

    def animate(self):
        if self.animation is not None:
            now = pg.time.get_ticks()
            if now - self.last_anim > self.anim_data[self.animation]["time"]:
                self.last_anim = now
                self.anim_frame = (self.anim_frame + 1) % len(self.anim_data[self.animation]["coords"])
                self.image_orig = self.spritesheet.get_image(self.anim_data[self.animation]["coords"][self.anim_frame],
                                                             self.img_dim)
                self.image_orig.set_colorkey(s.BLACK)
                if self.anim_frame == 0:
                    self.animation = None


class Player(Mob):  #class parent
    def __init__(self, game, spawn):
        super().__init__(game, (11, 13), "gunguy.png", True, spawn)
        self.mouse_offset = 0

    def move(self):
        self.rotate(pg.mouse.get_pos())
        # set acc to 0 when not pressing so it will stop accelerating
        self.acc = vec(0, 0)

        # move on buttonpress
        key_state = pg.key.get_pressed()
        if key_state[s.move_up]:
            self.vel.y -= s.PLAYER_ACCELERATION
        if key_state[s.move_down]:
            self.vel.y += s.PLAYER_ACCELERATION
        if key_state[s.move_left]:
            self.vel.x -= s.PLAYER_ACCELERATION
        if key_state[s.move_right]:
            self.vel.x += s.PLAYER_ACCELERATION

        self.move_calc()

    def act(self):
        for event in self.game.all_events:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.attack()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    if self.current_weapon is not None:
                        self.current_weapon.reload()
                elif event.key == pg.K_e:
                    if self.current_weapon is None:
                        # pick up weapon
                        hits = pg.sprite.spritecollide(self, self.game.items, False)
                        if hits:
                            self.current_weapon = hits[0]
                            self.current_weapon.toggle_item()
                            self.image_orig = self.spritesheet.get_image(self.anim_data["weapon"]["coords"][0],
                                                       (self.img_dim))
                            self.image_orig.set_colorkey(s.BLACK)
                            # will kill() itself if not an item anymore
                    else:
                        # throw away weapon
                        self.current_weapon.toggle_item()
                        self.current_weapon.rect.center = self.pos
                        self.current_weapon = None
                        self.image_orig = self.spritesheet.get_image(self.anim_data["melee"]["coords"][0],
                                                                     (self.img_dim))
                        self.image_orig.set_colorkey(s.BLACK)





class Player2(Mob): #class enfant
    def __init__(self, game, spawn):
        super().__init__(game, (11, 13), "gunguy.png", True, spawn)
        self.mouse_offset = 0

    def move(self):
        self.rotate(pg.mouse.get_pos())
        # set acc to 0 when not pressing so it will stop accelerating
        self.acc = vec(0, 0)

        # move on buttonpress
        key_state = pg.key.get_pressed()
        if key_state[s.move_up2]:
            self.vel.y -= s.PLAYER_ACCELERATION
        if key_state[s.move_down2]:
            self.vel.y += s.PLAYER_ACCELERATION
        if key_state[s.move_left2]:
            self.vel.x -= s.PLAYER_ACCELERATION
        if key_state[s.move_right2]:
            self.vel.x += s.PLAYER_ACCELERATION

        self.move_calc()

    def act(self):
        for event in self.game.all_events:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.attack()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    if self.current_weapon is not None:
                        self.current_weapon.reload()
                elif event.key == pg.K_e:
                    if self.current_weapon is None:
                        # pick up weapon
                        hits = pg.sprite.spritecollide(self, self.game.items, False)
                        if hits:
                            self.current_weapon = hits[0]
                            self.current_weapon.toggle_item()
                            self.image_orig = self.spritesheet.get_image(self.anim_data["weapon"]["coords"][0],
                                                       (self.img_dim))
                            self.image_orig.set_colorkey(s.BLACK)
                            # will kill() itself if not an item anymore
                    else:
                        # throw away weapon
                        self.current_weapon.toggle_item()
                        self.current_weapon.rect.center = self.pos
                        self.current_weapon = None
                        self.image_orig = self.spritesheet.get_image(self.anim_data["melee"]["coords"][0],
                                                                     (self.img_dim))
                        self.image_orig.set_colorkey(s.BLACK)
