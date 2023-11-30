from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.score = PLAYER_STARTING_SCORE
        self.rel = 0
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()

    def check_game_over(self):
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.retry_game()

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sounds.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event, selected_weapon):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                match selected_weapon:
                    case 0:
                        self.game.sounds.shotgun.play()
                    case 1:
                        self.game.sounds.pistol.play()
                    case 2:
                        self.game.sounds.machine_gun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def add_to_score(self, action="hit"):
        match action:
            case "hit":
                self.score += 5
            case "kill":
                self.score += 10
            case "miss":
                if self.score > 0:
                    self.score -= 3
            case "attacked":
                if self.score > 0:
                    self.score -= 2
        print(self.score)

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin

        self.check_wall_collision(dx,dy)
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy*scale)):
            self.y += dy

    def draw(self):
        # pg.draw.line(self.game.screen, 'red', (self.x * 100, self.y * 100),
        #              (self.x * 100 + WIDTH * math.cos(self.angle),
        #               self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'black', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos(HALF_WIDTH, HALF_HEIGHT)
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)