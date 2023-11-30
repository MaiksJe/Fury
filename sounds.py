import pygame as pg
import pygame.mixer


class Sounds:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'sounds/'
        pg.mixer.set_num_channels(2)
        self.theme_channel = pg.mixer.Channel(1)
        self.theme = pg.mixer.Sound(self.path + 'theme.mp3')
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.machine_gun = pg.mixer.Sound(self.path + 'machine_gun.mp3')
        self.pistol = pg.mixer.Sound(self.path + 'pistol.mp3')
        self.switch_weapon = pg.mixer.Sound(self.path + 'weapon_switch.mp3')
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        self.enemy_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.enemy_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.enemy_death = pg.mixer.Sound(self.path + 'npc_death.wav')
