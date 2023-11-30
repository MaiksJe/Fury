import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game, difficulty="rookie"):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures(difficulty)
        self.sky_image = self.get_texture('textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('textures/blood_screen.png', RES)
        self.shotgun_small = self.get_texture('sprites/weapons/shotgun_s.png', (61, 13))
        self.list_bg = self.get_texture('buttons/Play Rect.png', (200, 100))
        self.health_icon = self.get_texture('controls/pharmacy.png', (65, 65))
        self.star_icon = self.get_texture('sprites/star.png', (65, 65))
        self.digit_size = 70
        self.digit_images = [self.get_texture(f'digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.score_images = [self.get_texture(f'scores/{i}.png', [self.digit_size+20] * 2)
                             for i in range(11)]
        self.scores = dict(zip(map(str, range(11)), self.score_images))
        self.game_over_image = self.get_texture('textures/game_over.png', RES)
        self.win_image = self.get_texture('textures/win.png', RES)

    def draw(self):
        self.draw_sky()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_player_score()

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0,0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (75 + i * self.digit_size, 15))
        self.screen.blit(self.health_icon, (7,20))
        self.screen.blit(self.digits['10'], ((i + 2) * self.digit_size, 15))

    def draw_player_score(self):
        score = str(self.game.player.score)
        for i, char in enumerate(score):
            self.screen.blit(self.scores[char], (975 + i * self.digit_size, 15))
        self.screen.blit(self.star_icon, (900, 20))

    def draw_weapons_list(self):
        self.screen.blit(self.list_bg, (1000, 600))
        self.screen.blit(self.shotgun_small, (1100, 650))

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0,0))

    def draw_sky(self):
        self.sky_offset = (self.sky_offset + 4.5*self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self, difficulty):
        match difficulty:
            case "rookie":
                return {
                    1: self.get_texture('textures/normal_wall.png'),
                }
            case "regular":
                return {
                    1: self.get_texture('textures/moldy_wall.png'),
                    2: self.get_texture('textures/moldy_wall.png'),
                    3: self.get_texture('textures/moldy_wall.png'),
                    4: self.get_texture('textures/moldy_wall.png'),
                    5: self.get_texture('textures/moldy_wall.png'),
                }
            case "asian":
                return {
                    1: self.get_texture('textures/moldy_wall.png'),
                    2: self.get_texture('textures/demon_wall.png'),
                    3: self.get_texture('textures/demon_wall.png'),
                    4: self.get_texture('textures/normal_wall.png'),
                    5: self.get_texture('textures/moldy_wall.png'),
                }

