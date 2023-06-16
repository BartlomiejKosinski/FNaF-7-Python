import pygame
import os
import sys
import json

from modules.AnimationObject import AnimationObject
from modules.HoverButton import HoverButton
from modules.MenuButton import MenuButton
from modules.InvisibleButton import InvisibleButton
from modules.Button import Button
from modules.Checkbox import Checkbox
from modules.Panel import Panel
from modules.Text import Text

pygame.init()

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Game:
    def __init__(self) -> None:
        self.state = 'MainMenu'

        self.init_game()
        self.init_main_menu()
        self.init_options()

        self.update()


    def init_game(self):
        with open(resource_path("config.json"), "r") as f:
            self.data = json.load(f)

        self.data_resolution = self.data['options'][0]
        self.data_fullscreen = self.data['options'][1]
        self.data_volume = self.data['options'][2]

        self.RESOLUTION = (self.data_resolution['WIDTH'], self.data_resolution['HEIGHT'])

        if self.data_fullscreen["FULLSCREEN"] == 1:
            self.screen = pygame.display.set_mode(self.RESOLUTION, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.RESOLUTION)

        self.icon = pygame.image.load(resource_path('assets/icon.png'))

        pygame.display.set_caption("FNaF 7 Python")
        pygame.display.set_icon(self.icon)

        self.fps = 144
        self.clock = pygame.time.Clock()

        self.done = False

        self.in_cameras = False

        self.offset_x = float(float(self.RESOLUTION[0]) / 1920.0)

        self.speed_x = 10

        self.cam_button = HoverButton(660, 1020, 600, 60, resource_path("assets/cam_button.png"), self.RESOLUTION)
        
        self.office = Panel(0, 0, 1920, 1080, resource_path("assets/office.png"), self.RESOLUTION)

        self.office_door = Panel(0, 0, 1920, 1080, resource_path("assets/office_door.png"), self.RESOLUTION)
        self.office_door_button = InvisibleButton(360,120,290,820, self.RESOLUTION)

        self.office_front_vent = Panel(0, 0, 1920, 1080, resource_path("assets/office_front_vent.png"), self.RESOLUTION)
        self.office_front_vent_button = InvisibleButton(1115, 250, 435, 260, self.RESOLUTION)

        self.office_right_vent = Panel(0, 0, 1920, 1080, resource_path("assets/office_right_vent.png"), self.RESOLUTION)
        self.office_right_vent_button = InvisibleButton(2060, 560, 150, 400, self.RESOLUTION)


        self.cam1 = Panel(0, 0, 1920, 1080, resource_path("assets/cam1.png"), self.RESOLUTION)

        self.office_door.set_visible(False)
        self.office_front_vent.set_visible(False)
        self.office_right_vent.set_visible(False)

        self.cam_anim = AnimationObject(0, 0, 100, self.RESOLUTION)
        self.cam_anim.append_frames(resource_path("assets/c_anim1.png"))
        self.cam_anim.append_frames(resource_path("assets/c_anim2.png"))
        self.cam_anim.append_frames(resource_path("assets/c_anim3.png"))
        self.cam_anim.append_frames(resource_path("assets/c_anim4.png"))
        self.cam_anim.append_frames(resource_path("assets/c_anim5.png"))
        self.cam_anim.append_frames(resource_path("assets/c_anim6.png"))
        self.cam_anim.append_frames(resource_path("assets/c_anim7.png"))
        self.cam_anim.append_frames(resource_path("assets/c_anim8.png"))
        self.cam_anim.append_frames(resource_path("assets/c_anim9.png"))
        self.cam_anim.append_frames(resource_path("assets/c_anim10.png"))
        self.cam_anim.append_frames(resource_path("assets/c_anim11.png"))


    def init_main_menu(self):
        self.stars = 0

        self.static = AnimationObject(0, 0, 100, self.RESOLUTION)
        self.static.append_frames(resource_path("assets/static.png"))
        self.static.append_frames(resource_path("assets/static2.png"))
        self.static.append_frames(resource_path("assets/static3.png"))
        self.static.append_frames(resource_path("assets/static4.png"))
        self.static.append_frames(resource_path("assets/static5.png"))

        self.main_menu_background = Panel(0, 0, 1920, 1080, resource_path("assets/main_menu_background.png"), self.RESOLUTION)

        self.menu_swipe = pygame.mixer.Sound(resource_path('sounds/menu_swipe.wav'))
        self.menu_swipe.set_volume(self.data_volume['VOLUME'])

        self.new_game_button = MenuButton(100, 390, 'Arial', 62, 'New Game', self.menu_swipe, (255,255,255), self.RESOLUTION)
        self.continue_button = MenuButton(100, 511, 'Arial', 62, 'Continue', self.menu_swipe, (255,255,255), self.RESOLUTION)
        self.options_button = MenuButton(100, 632, 'Arial', 62, 'Options', self.menu_swipe, (255,255,255), self.RESOLUTION)
        
        self.custom_night_button = MenuButton(100, 753, 'Arial', 62, 'Custom Night', self.menu_swipe, (255,255,255), self.RESOLUTION)
        self.extras_button = MenuButton(100, 874, 'Arial', 62, 'Extras', self.menu_swipe, (255,255,255), self.RESOLUTION)

        self.exit_button = MenuButton(100, 980, 'Arial', 62, 'Exit', self.menu_swipe, (255,255,255), self.RESOLUTION)

        self.copyright_text = Text(1250, 1040, 'Arial', 32, "© 2023 KosaQDev Inspired By Scott Cawthon.", (255,255,255), self.RESOLUTION)


    def init_options(self):
        self.resolutions = ['1920 x 1080', '1600 x 900', '1366 x 768', '1280 x 720']
        self.fullscreen = True

        self.apply_button = MenuButton(200, 780, 'Arial', 62, 'Apply', self.menu_swipe, (255,255,255), self.RESOLUTION)
        self.back_button = MenuButton(200, 900, 'Arial', 62, 'Back', self.menu_swipe, (255,255,255), self.RESOLUTION)

        self.resolution_index = 0
        self.resolution_text = Text(332, 300, 'Arial', 62, self.resolutions[self.resolution_index], (255,255,255), self.RESOLUTION)
        self.resolution_left = MenuButton(200, 300, 'Arial', 62, '<', None, (255,255,255), self.RESOLUTION)
        self.resolution_right = MenuButton(264, 300, 'Arial', 62, '>', None, (255,255,255), self.RESOLUTION)

        self.fullscreen_checkbox = Checkbox(220, 200, 64, 64, 'Arial', 62, self.RESOLUTION, checked_offset_x=10, checked_offset_y=-3)
        self.fullscreen_text = Text(332, 200, 'Arial', 62, "Fullscreen", (255,255,255), self.RESOLUTION)

        self.volume_left = MenuButton(200, 400, 'Arial', 62, '<', None, (255,255,255), self.RESOLUTION)
        self.volume_right = MenuButton(264, 400, 'Arial', 62, '>', None, (255,255,255), self.RESOLUTION)
        self.volume_text = Text(332, 400, 'Arial', 62, f"Volume: {int(self.data_volume['VOLUME'] * 100)}%", (255,255,255), self.RESOLUTION)
        self.volume = self.data_volume['VOLUME'] * 100
        self.volume_text.change_text(f"Volume: {int(self.data_volume['VOLUME'] * 100)}%")

        if self.data['options'][1]['FULLSCREEN'] == 1:
            self.fullscreen_checkbox.state = True
        else:
            self.fullscreen_checkbox.state = False

        if self.data['options'][0]['WIDTH'] == 1920:
            self.resolution_index = 0
        elif self.data['options'][0]['WIDTH'] == 1600:
            self.resolution_index = 1
        elif self.data['options'][0]['WIDTH'] == 1366:
            self.resolution_index = 2
        elif self.data['options'][0]['WIDTH'] == 1280:
            self.resolution_index = 3

        self.resolution_text.change_text(self.resolutions[self.resolution_index])


    def handle_main_menu(self, mx, my):
        if self.new_game_button.get_clicked(mx, my, 0):
            self.state = 'Game'

        if self.options_button.get_clicked(mx, my, 0):
            self.state = 'Options'
        
        if self.exit_button.get_clicked(mx, my, 0):
            self.done = True

        self.main_menu_background.draw(self.screen)

        self.new_game_button.draw(self.screen, mx, my, 32)
        self.continue_button.draw(self.screen, mx, my, 32)
        self.options_button.draw(self.screen, mx, my, 32)


        if self.stars == 1:
            self.custom_night_button.draw(self.screen, mx, my, 32)
            self.extras_button.draw(self.screen, mx, my, 32)

        self.exit_button.draw(self.screen, mx, my, 32)
        self.copyright_text.draw_text(self.screen)
        self.static.play_loop(self.screen)


    def save_data(self):
        with open(resource_path("config.json"), "w") as f:
                if self.fullscreen:
                    self.data['options'][1]['FULLSCREEN'] = 1
                else:
                    self.data['options'][1]['FULLSCREEN'] = 0

                if self.resolution_index == 0:
                    self.data['options'][0]['WIDTH'] = 1920
                    self.data['options'][0]['HEIGHT'] = 1080
                elif self.resolution_index == 1:
                    self.data['options'][0]['WIDTH'] = 1600
                    self.data['options'][0]['HEIGHT'] = 900
                elif self.resolution_index == 2:
                    self.data['options'][0]['WIDTH'] = 1366
                    self.data['options'][0]['HEIGHT'] = 768
                elif self.resolution_index == 3:
                    self.data['options'][0]['WIDTH'] = 1280
                    self.data['options'][0]['HEIGHT'] = 720

                self.data['options'][2]['VOLUME'] = float(self.volume * 0.01)

                json.dump(self.data, f)
    

    def handle_options(self, mx, my):
        if self.back_button.get_clicked(mx, my, 0):
            self.state = 'MainMenu'

        if self.apply_button.get_clicked(mx, my, 0):
            self.save_data()
            self.init_game()
            self.init_main_menu()
            self.init_options()


        if self.resolution_left.get_clicked(mx, my, 0) and self.resolution_index > 0:
            self.resolution_index -= 1
            self.resolution_text.change_text(self.resolutions[self.resolution_index])
        if self.resolution_right.get_clicked(mx, my, 0) and self.resolution_index < (len(self.resolutions) -1):
            self.resolution_index += 1
            self.resolution_text.change_text(self.resolutions[self.resolution_index])

        if self.volume_left.get_clicked(mx, my, 0) and self.volume > 0:
            self.volume -= 5
            self.volume_text.change_text(f"Volume: {int(self.volume)}%")
        if self.volume_right.get_clicked(mx, my, 0) and self.volume < 100:
            self.volume += 5
            self.volume_text.change_text(f"Volume: {int(self.volume)}%")

        self.main_menu_background.draw(self.screen)
        self.fullscreen = self.fullscreen_checkbox.get_check_state(mx, my, 0)
        self.back_button.draw(self.screen, mx, my, 32)
        self.apply_button.draw(self.screen, mx, my, 32)

        self.fullscreen_checkbox.draw(self.screen)
        self.fullscreen_text.draw_text(self.screen)

        self.resolution_left.draw(self.screen, mx, my)
        self.resolution_right.draw(self.screen, mx, my)
        self.resolution_text.draw_text(self.screen)

        self.volume_left.draw(self.screen, mx, my)
        self.volume_right.draw(self.screen, mx, my)
        self.volume_text.draw_text(self.screen)

        self.static.play_loop(self.screen)


    def handle_office_invisible_buttons(self, mx, my):
        self.office_door_button.update(mx, my)
        self.office_front_vent_button.update(mx, my)
        self.office_right_vent_button.update(mx, my)

        
        if self.office_door_button.get_clicked() and not self.in_cameras:
            self.office_door.set_visible(True)
            self.office.set_visible(False)
        else:
            self.office_door.set_visible(False)
            self.office.set_visible(True)

        if self.office_front_vent_button.get_clicked() and not self.in_cameras:
            self.office_front_vent.set_visible(True)
            self.office.set_visible(False)
        else:
            self.office_front_vent.set_visible(False)
            self.office.set_visible(True)

        if self.office_right_vent_button.get_clicked() and not self.in_cameras:
            self.office_right_vent.set_visible(True)
            self.office.set_visible(False)
        else:
            self.office_right_vent.set_visible(False)
            self.office.set_visible(True)

    
    def handle_cameras(self):
        self.cam_button.update()

        if self.in_cameras == 0 and self.cam_button.value == 1:
            self.cam_button.value = 0
            self.in_cameras = 1
        elif self.in_cameras == 1 and self.cam_button.value == 1:
            self.cam_button.value = 0
            self.in_cameras = 0

        if self.in_cameras == 1:
            self.cam1.set_visible(True)
            self.office.set_visible(False)
        elif self.in_cameras == 0:
            self.cam1.set_visible(False)
            self.office.set_visible(True)


    def handle_office_scrolling(self, mx, my):
        if mx < (400 * self.offset_x) and self.office.x < 0 and not self.in_cameras:
                self.office.x += self.speed_x
                self.office_door_button.x += self.speed_x
                self.office_front_vent_button.x += self.speed_x
                self.office_right_vent_button.x += self.speed_x

        elif mx > (1620 * self.offset_x) and self.office.x > (-570 * self.offset_x) and not self.in_cameras:
            self.office.x -= self.speed_x
            self.office_door_button.x -= self.speed_x
            self.office_front_vent_button.x -= self.speed_x
            self.office_right_vent_button.x -= self.speed_x

        self.office_door.x = self.office.x
        self.office_front_vent.x = self.office.x
        self.office_right_vent.x = self.office.x


    def update(self) -> None:
        while not self.done:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       self.done = True
            
            mx, my = pygame.mouse.get_pos()

            if self.state == 'MainMenu':
                self.handle_main_menu(mx, my)
            
            elif self.state == 'Options':
                self.handle_options(mx, my)

            elif self.state == 'Game':
                self.handle_office_scrolling(mx, my)

                self.handle_office_invisible_buttons(mx, my)

                self.handle_cameras()

                self.office.draw(self.screen)
                self.office_door.draw(self.screen)
                self.office_front_vent.draw(self.screen)
                self.office_right_vent.draw(self.screen)

                self.cam1.draw(self.screen)

                self.cam_button.draw(self.screen)

            pygame.display.update()


if __name__ == "__main__":
    Game()