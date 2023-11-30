import sys
import pygame.font

from button import Button
from map import *
from player import *
from raycasting import *
from object_renderer import *
from object_handler import *
from weapon import *
from sounds import *
from path_finding_algo import *

BG = pygame.image.load(f'buttons/background.jpg')


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("buttons/demo.otf", size)


weapons_list = [
    {'path': 'sprites/weapons/shotgun/0.png', 'scale': 0.4, 'damage': 35},
    {'path': 'sprites/weapons/pistol/0.png', 'scale': 0.25, 'damage': 20},
    {'path': 'sprites/weapons/machine_gun/0.png', 'scale': 0.2, 'damage': 50},
]


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.selected_weapon = 0
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game("rookie")

    def new_game(self, difficulty):
        self.map = Map(self, difficulty=difficulty)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self, difficulty=difficulty)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self, difficulty=difficulty)
        self.weapon = Weapon(self)
        self.sounds = Sounds(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            if self.selected_weapon < 2:
                self.selected_weapon += 1
            current_weapon = weapons_list[self.selected_weapon]
            self.weapon = Weapon(self, path=current_weapon.get("path"), scale=current_weapon.get("scale"),
                                 damage=current_weapon.get("damage"))
            self.sounds.switch_weapon.play()
        elif keys[pg.K_q]:
            if self.selected_weapon > 0:
                self.selected_weapon -= 1
            current_weapon = weapons_list[self.selected_weapon]
            self.weapon = Weapon(self, path=current_weapon.get("path"), scale=current_weapon.get("scale"),
                                 damage=current_weapon.get("damage"))
            self.sounds.switch_weapon.play()

        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def main_menu(self):
        pygame.display.set_caption("Main Menu")
        if not self.sounds.theme_channel.get_busy():
            self.sounds.theme_channel.play(self.sounds.theme)

        while True:
            self.screen.blit(BG, (0, 0))
            pg.mouse.set_visible(True)
            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 70))

            play_button = Button(image=pygame.image.load("buttons/Play Rect.png"), pos=(640, 200),
                                 text_input="PLAY", font=get_font(65), base_color="#d7fcd4", hovering_color="#ee6b6e")
            levels_button = Button(image=pygame.image.load("buttons/Options Rect.png"), pos=(640, 330),
                                   text_input="SELECT DIFFICULTY", font=get_font(65), base_color="#d7fcd4",
                                   hovering_color="#f94449")

            sound_button = Button(image=pygame.image.load("buttons/Options Rect.png"), pos=(640, 460),
                                  text_input="CONTROLS", font=get_font(65), base_color="#d7fcd4",
                                  hovering_color="#de0a26")

            quit_button = Button(image=pygame.image.load("buttons/Quit Rect.png"), pos=(640, 590),
                                 text_input="QUIT", font=get_font(65), base_color="#d7fcd4", hovering_color="#c30010")

            self.screen.blit(menu_text, menu_rect)

            for button in [play_button, levels_button, sound_button, quit_button]:
                button.changeColor(menu_mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(menu_mouse_pos):
                        self.sounds.theme.stop()
                        self.new_game("rookie")
                        self.run()
                    if levels_button.checkForInput(menu_mouse_pos):
                        self.levels()
                    if sound_button.checkForInput(menu_mouse_pos):
                        self.options(False)
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

    def game_menu(self):
        pygame.display.set_caption("Menu")
        if not self.sounds.theme_channel.get_busy():
            self.sounds.theme_channel.play(self.sounds.theme)
        while True:
            self.screen.blit(BG, (0, 0))
            pg.mouse.set_visible(True)
            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(100).render("GAME PAUSED", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 70))

            play_button = Button(image=pygame.image.load("buttons/Play Rect.png"), pos=(640, 200),
                                 text_input="RESUME", font=get_font(65), base_color="#d7fcd4", hovering_color="#ee6b6e")
            menu_button = Button(image=pygame.image.load("buttons/Options Rect.png"), pos=(640, 330),
                                 text_input="MAIN MENU", font=get_font(65), base_color="#d7fcd4",
                                 hovering_color="#f94449")

            options_button = Button(image=pygame.image.load("buttons/Options Rect.png"), pos=(640, 460),
                                    text_input="CONTROLS", font=get_font(65), base_color="#d7fcd4",
                                    hovering_color="#de0a26")
            quit_button = Button(image=pygame.image.load("buttons/Quit Rect.png"), pos=(640, 590),
                                 text_input="QUIT", font=get_font(65), base_color="#d7fcd4", hovering_color="#c30010")

            self.screen.blit(menu_text, menu_rect)

            for button in [play_button, menu_button, options_button, quit_button]:
                button.changeColor(menu_mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(menu_mouse_pos):
                        self.sounds.theme.stop()
                        self.run()
                    if menu_button.checkForInput(menu_mouse_pos):
                        self.sounds.theme.stop()
                        self.main_menu()
                    if options_button.checkForInput(menu_mouse_pos):
                        self.options()
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

    def options(self, in_game=True):
        while True:
            options_mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(BG, (0, 0))

            menu_text = get_font(100).render("CONTROLS", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 70))
            self.screen.blit(menu_text, menu_rect)

            mvmt_text = get_font(55).render("Movement", True, "White")
            mvmt_rect = mvmt_text.get_rect(center=(480, 200))
            self.screen.blit(mvmt_text, mvmt_rect)
            mvmt_img = pygame.transform.scale(pygame.image.load(f'controls/wasd.png'), (150, 150))
            self.screen.blit(mvmt_img, (750, 100))

            look_text = get_font(55).render("Look Around", True, "White")
            look_rect = look_text.get_rect(center=(480, 300))
            self.screen.blit(look_text, look_rect)
            look_img = pygame.transform.scale(pygame.image.load(f'controls/scroll.png'), (80, 80))
            self.screen.blit(look_img, (790, 250))

            fire_text = get_font(55).render("Fire Weapon", True, "White")
            fire_rect = fire_text.get_rect(center=(480, 400))
            self.screen.blit(fire_text, fire_rect)
            fire_img = pygame.transform.scale(pygame.image.load(f'controls/lmb.png'), (80, 80))
            self.screen.blit(fire_img, (775, 350))

            e_text = get_font(55).render("Next Weapon", True, "White")
            e_rect = e_text.get_rect(center=(480, 500))
            self.screen.blit(e_text, e_rect)
            e_img = pygame.transform.scale(pygame.image.load(f'controls/k_e.png'), (80, 80))
            self.screen.blit(e_img, (780, 450))

            q_text = get_font(55).render("Previous Weapon", True, "White")
            q_rect = q_text.get_rect(center=(480, 600))
            self.screen.blit(q_text, q_rect)
            q_img = pygame.transform.scale(pygame.image.load(f'controls/k_q.png'), (80, 80))
            self.screen.blit(q_img, (780, 550))

            options_back = Button(image=None, pos=(150, 80),
                                  text_input="BACK", font=get_font(75), base_color="White", hovering_color="#ee6b6e")

            options_back.changeColor(options_mouse_pos)
            options_back.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if options_back.checkForInput(options_mouse_pos) and in_game:
                        self.game_menu()
                    if options_back.checkForInput(options_mouse_pos) and not in_game:
                        # self.sounds.theme.stop()
                        self.main_menu()

            pygame.display.update()

    def levels(self):
        while True:
            levels_mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(BG, (0, 0))

            top_text = get_font(100).render("SELECT DIFFICULTY", True, "#b68f40")
            top_rect = top_text.get_rect(center=(640, 70))
            self.screen.blit(top_text, top_rect)

            rookie_img = pygame.transform.scale(pygame.image.load(f'levels/rookie.png'), (200, 200))
            self.screen.blit(rookie_img, (200, 150))
            rookie_btn = Button(image=pygame.image.load("buttons/Quit Rect.png"), pos=(300, 420),
                                text_input="ROOKIE", font=get_font(35), base_color="#d7fcd4",
                                hovering_color="#ee6b6e")

            regular_img = pygame.transform.scale(pygame.image.load(f'levels/regular.png'), (200, 200))
            self.screen.blit(regular_img, (500, 150))
            regular_btn = Button(image=pygame.image.load("buttons/Quit Rect.png"), pos=(600, 420),
                                 text_input="REGULAR", font=get_font(35), base_color="#d7fcd4",
                                 hovering_color="#de0a26")

            asian_img = pygame.transform.scale(pygame.image.load(f'levels/asian.jpg'), (200, 200))
            self.screen.blit(asian_img, (800, 150))
            asian_btn = Button(image=pygame.image.load("buttons/Quit Rect.png"), pos=(900, 420),
                               text_input="ASIAN", font=get_font(35), base_color="#d7fcd4",
                               hovering_color="#c30010")

            for button in [rookie_btn, regular_btn, asian_btn]:
                button.changeColor(levels_mouse_pos)
                button.update(self.screen)

            levels_back = Button(image=None, pos=(640, 600),
                                 text_input="BACK", font=get_font(75), base_color="White", hovering_color="#ee6b6e")

            levels_back.changeColor(levels_mouse_pos)
            levels_back.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rookie_btn.checkForInput(levels_mouse_pos):
                        self.sounds.theme.stop()
                        self.new_game("rookie")
                        self.run()
                    if regular_btn.checkForInput(levels_mouse_pos):
                        self.sounds.theme.stop()
                        self.new_game("regular")
                        self.run()
                    if asian_btn.checkForInput(levels_mouse_pos):
                        self.sounds.theme.stop()
                        self.new_game("asian")
                        self.run()
                    if levels_back.checkForInput(levels_mouse_pos):
                        self.main_menu()

            pygame.display.update()

    def game_won(self):
        while True:
            levels_mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(BG, (0, 0))
            if not self.sounds.theme_channel.get_busy():
                self.sounds.theme_channel.play(self.sounds.theme)

            top_text = get_font(100).render("YOU WON", True, "#b68f40")
            top_rect = top_text.get_rect(center=(640, 70))
            self.screen.blit(top_text, top_rect)

            score_text = get_font(80).render("You scored: " + str(self.player.score) + " points", True, "#b68f40")
            score_rect = score_text.get_rect(center=(640, 300))
            self.screen.blit(score_text, score_rect)

            if self.map.selected_difficulty == "asian":
                grass_text = get_font(60).render("Now go touch grass", True, "Green")
                grass_rect = grass_text.get_rect(center=(640, 400))
                self.screen.blit(grass_text, grass_rect)

            menu_btn = Button(image=pygame.image.load("buttons/Play Rect.png"), pos=(640, 520),
                              text_input="BACK TO MAIN MENU", font=get_font(35), base_color="#d7fcd4",
                              hovering_color="#ee6b6e")

            menu_btn.changeColor(levels_mouse_pos)
            menu_btn.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_btn.checkForInput(levels_mouse_pos):
                        self.main_menu()

            pygame.display.update()

    def retry_game(self):
        while True:
            levels_mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(BG, (0, 0))
            if not self.sounds.theme_channel.get_busy():
                self.sounds.theme_channel.play(self.sounds.theme)

            top_text = get_font(100).render("YOU LOST", True, "#b68f40")
            top_rect = top_text.get_rect(center=(640, 70))
            self.screen.blit(top_text, top_rect)

            score_text = get_font(80).render("Retry", True, "White")
            score_rect = score_text.get_rect(center=(640, 250))
            self.screen.blit(score_text, score_rect)

            retry_btn = Button(image=pygame.image.load("buttons/retry.png"), pos=(640, 350),
                              text_input="", font=get_font(35), base_color="#d7fcd4",
                              hovering_color="#ee6b6e")

            retry_btn.changeColor(levels_mouse_pos)
            retry_btn.update(self.screen)

            menu_btn = Button(image=pygame.image.load("buttons/Play Rect.png"), pos=(640, 520),
                              text_input="BACK TO MAIN MENU", font=get_font(35), base_color="#d7fcd4",
                              hovering_color="#ee6b6e")

            menu_btn.changeColor(levels_mouse_pos)
            menu_btn.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_btn.checkForInput(levels_mouse_pos):
                        self.sounds.theme.stop()
                        self.new_game(self.map.selected_difficulty)
                        self.run()
                    if menu_btn.checkForInput(levels_mouse_pos):
                        self.main_menu()

            pygame.display.update()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game_menu()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event, self.selected_weapon)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

    def sound_settings(self):
        pass


if __name__ == '__main__':
    game = Game()
    # game.run()
    game.main_menu()
