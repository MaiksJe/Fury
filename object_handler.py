from sprite import *
from enemies import *

class ObjectHandler:
    def __init__(self, game, difficulty="rookie"):
        self.game = game
        self.sprite_list = []
        self.enemy_list = []
        self.enemy_sprite_path = 'sprites/enemies/'
        self.static_sprite_path = 'sprites/static_sprites/'
        self.anim_sprite_path = 'sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_enemy = self.add_enemy
        self.enemy_positions = {}

        #sprite map
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 5.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(10.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 14.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 18.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

        match difficulty:
            case "rookie":
                add_enemy(Soldier(game, pos=(10.0, 7.0)))
                add_enemy(Soldier(game, pos=(11.5, 4.5)))
                add_enemy(Soldier(game, pos=(13.5, 6.5)))
                # add_enemy(OneEyedMonster(game, pos=(5.5, 4.5)))
                # add_enemy(OneEyedMonster(game, pos=(5.5, 6.5)))
            case "regular":
                add_enemy(Soldier(game, pos=(11.0, 19.0)))
                add_enemy(Soldier(game, pos=(11.5, 4.5)))
                add_enemy(Soldier(game, pos=(13.5, 6.5)))
                add_enemy(Soldier(game, pos=(2.0, 20.0)))
                add_enemy(Soldier(game, pos=(4.0, 29.0)))
                add_enemy(OneEyedMonster(game, pos=(5.5, 14.5)))
                add_enemy(OneEyedMonster(game, pos=(5.5, 16.5)))
                add_enemy(Predator(game, pos=(14.5, 25.5)))
                add_enemy(OneEyedMonster(game, pos=(14.5, 28.5)))
            case "asian":
                add_enemy(Soldier(game, pos=(11.0, 19.0)))
                add_enemy(Soldier(game, pos=(11.5, 4.5)))
                add_enemy(Soldier(game, pos=(13.5, 6.5)))
                add_enemy(Soldier(game, pos=(2.0, 20.0)))
                add_enemy(Soldier(game, pos=(4.0, 29.0)))
                add_enemy(OneEyedMonster(game, pos=(5.5, 14.5)))
                add_enemy(OneEyedMonster(game, pos=(5.5, 16.5)))
                add_enemy(OneEyedMonster(game, pos=(5.5, 19.5)))
                add_enemy(Predator(game, pos=(7.5, 20.5)))
                add_enemy(Predator(game, pos=(14.5, 25.5)))
                add_enemy(Predator(game, pos=(14.5, 28.5)))
        #
        # add_enemy(Soldier(game, pos=(11.0, 19.0)))
        # add_enemy(Soldier(game, pos=(11.5, 4.5)))
        # add_enemy(Soldier(game, pos=(13.5, 6.5)))
        # add_enemy(Soldier(game, pos=(2.0, 20.0)))
        # add_enemy(Soldier(game, pos=(4.0, 29.0)))
        # add_enemy(OneEyedMonster(game, pos=(5.5, 14.5)))
        # add_enemy(OneEyedMonster(game, pos=(5.5, 16.5)))
        # add_enemy(OneEyedMonster(game, pos=(7.5, 20.5)))
        # add_enemy(Predator(game, pos=(14.5, 25.5)))
        # add_enemy(OneEyedMonster(game, pos=(14.5, 28.5)))

    def check_win(self):
        if not len(self.enemy_positions):
            pg.time.delay(2000)
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(2000)
            self.game.game_won()

    def update(self):
        self.enemy_positions = {enemy.map_pos for enemy in self.enemy_list if enemy.alive}
        [sprite.update() for sprite in self.sprite_list]
        [enemy.update() for enemy in self.enemy_list]
        self.check_win()

    def add_enemy(self, enemy):
        self.enemy_list.append(enemy)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)