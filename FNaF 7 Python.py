import pygame
import os
import sys
import json

pygame.init()

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class AnimationObject:
    def __init__(self, x : int, y : int, frame_delay : int, resolution = (1920, 1080)) -> None:
        self.scale_x = float(float(resolution[0]) / 1920.0)
        self.scale_y = float(float(resolution[1]) / 1080.0)
        
        self.x = x * self.scale_x
        self.y = y * self.scale_y
        self.frame_delay = frame_delay

        self.frames = []
        self.frame = 0
        self.last_tick = pygame.time.get_ticks()

    def append_frames(self, resource_path : str):
        self.frames.append(pygame.transform.scale_by(pygame.image.load(resource_path).convert_alpha(), (self.scale_x, self.scale_y)))

    def play_reverse(self, screen):
        self.current_tick = pygame.time.get_ticks()
        if self.current_tick - self.last_tick > self.frame_delay:
            if self.frame > 0:
                self.frame -= 1
            self.last_tick = pygame.time.get_ticks()
        screen.blit(self.frames[self.frame], (self.x, self.y))

    def play_loop(self, screen):
        self.current_tick = pygame.time.get_ticks()
        if self.current_tick - self.last_tick > self.frame_delay:
            if (self.frame + 1) > (len(self.frames) - 1):
                self.frame = 0
            else:
                self.frame += 1
            self.last_tick = pygame.time.get_ticks()
        screen.blit(self.frames[self.frame], (self.x, self.y))


class HoverButton:
    def __init__(self, x : int, y : int, width : int, height : int, source : str = None, resolution = (1920, 1080)) -> None:
        self.scale_x = float(float(resolution[0]) / 1920.0)
        self.scale_y = float(float(resolution[1]) / 1080.0)
        
        self.x = x * self.scale_x
        self.y = y * self.scale_y
        self.width = width * self.scale_x
        self.height = height * self.scale_y
        self.source = source

        self.color = (255,0,0)
        self.enabled = True
        self.value = False
        self.state = 0

        self.images = []

        if source is not None:
            try:
                self.images.append(pygame.transform.scale_by(pygame.image.load(self.source).convert_alpha(), (self.scale_x, self.scale_y)))
            except:
                print(f"Something went wrong while adding image using '{source}'")

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def get_value(self) -> bool:
        return self.value


    def set_enabled(self, value : bool) -> None:
        self.enabled = value


    def add_image(self, source : str) -> None:
        try:
            self.images.append(pygame.image.load(source))
        except:
            print(f"Something went wrong while adding image using '{source}'")


    def update(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if not self.enabled:
            return None
        
        if self.rect.collidepoint(mouse_x, mouse_y):
            if self.state == 0:
                self.state = 1
                self.value = not self.value
        else:
            self.state = 0


    def draw(self, screen : pygame.surface, image_number : int = None) -> None:
        if self.source is not None:
            if not self.state:
                if image_number is not None and image_number < len(self.images):
                    screen.blit(self.images[image_number], (self.x, self.y))
                else:
                    screen.blit(self.images[0], (self.x, self.y))
        else:
            if self.state:
                pygame.draw.rect(screen, self.color, self.rect)
            else:
                pygame.draw.rect(screen, (0,255,0), self.rect)


class Button:
    def __init__(self, x : int, y : int, width : int, height : int, source : str, hover_ready : bool, resolution = (1920, 1080)) -> None:
        self.scale_x = float(float(resolution[0]) / 1920.0)
        self.scale_y = float(float(resolution[1]) / 1080.0)

        self.x = x * self.scale_x
        self.y = y * self.scale_y
        self.width = width * self.scale_x
        self.height = height * self.scale_y
        self.source = source
        self.hover_ready = hover_ready
        self.clicked = False
        self.hovered = False

        self.image = pygame.transform.scale_by(pygame.image.load(resource_path(f"{self.source}.png")).convert_alpha(), (self.scale_x, self.scale_y))
        if self.hover_ready:
            self.hover_image = pygame.transform.scale_by(pygame.image.load(resource_path(f"{self.source}_hover.png")).convert_alpha(), (self.scale_x, self.scale_y))

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def get_clicked(self, mx, my, btn):
        if self.rect.collidepoint(mx, my):
            if pygame.mouse.get_pressed()[btn] and self.clicked == False:
                self.clicked = True
                return True
        if pygame.mouse.get_pressed()[btn] == 0:
            self.clicked = False
            return False
        

    def draw(self, screen, mx, my):
        if self.rect.collidepoint(mx, my) and self.hover_ready:
            screen.blit(self.hover_image, (self.x, self.y))
            self.hovered = True
        else:
            screen.blit(self.image, (self.x, self.y))
            self.hovered = False


class Checkbox:
    def __init__(self, x : int, y : int, width : int, height : int, source : str, checked_ready : bool, resolution = (1920, 1080)) -> None:
        self.scale_x = float(float(resolution[0]) / 1920.0)
        self.scale_y = float(float(resolution[1]) / 1080.0)

        self.x = x * self.scale_x
        self.y = y * self.scale_y
        self.width = width * self.scale_x
        self.height = height * self.scale_y
        self.source = source
        self.checked_ready = checked_ready
        self.clicked = False
        self.state = False

        self.image = pygame.transform.scale_by(pygame.image.load(resource_path(f"{self.source}.png")).convert_alpha(), (self.scale_x, self.scale_y))
        if self.checked_ready:
            self.checked_image = pygame.transform.scale_by(pygame.image.load(resource_path(f"{self.source}_x.png")).convert_alpha(), (self.scale_x, self.scale_y))

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def get_check_state(self, mx, my, btn):
        if self.rect.collidepoint(mx, my):
            if pygame.mouse.get_pressed()[btn] and self.clicked == False:
                self.clicked = True
                self.state = not self.state
                return self.state
        if pygame.mouse.get_pressed()[btn] == 0:
            self.clicked = False
            return self.state
        

    def draw(self, screen):
        if self.state:
            screen.blit(self.checked_image, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))


class Panel:
    def __init__(self, x : int, y : int, width : int, height : int, source : str = None, resolution = (1920, 1080)) -> None:
        self.scale_x = float(float(resolution[0]) / 1920.0)
        self.scale_y = float(float(resolution[1]) / 1080.0)
        
        self.x = x * self.scale_x
        self.y = y * self.scale_y
        self.width = width * self.scale_x
        self.height = height * self.scale_y
        self.source = source

        self.visible = True

        self.images = []

        if source is not None:
            try:
                self.images.append(pygame.transform.scale_by(pygame.image.load(self.source).convert_alpha(), (self.scale_x, self.scale_y)))
            except:
                print(f"Something went wrong while adding image using '{source}'")

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def set_visible(self, value : bool) -> None:
        self.visible = value


    def add_image(self, source : str) -> None:
        try:
            self.images.append(pygame.image.load(source))
        except:
            print(f"Something went wrong while adding image using '{source}'")


    def draw(self, screen:  pygame.surface, image_number : int = None) -> None:
        if self.visible:
            if self.source is not None:
                if image_number is not None and image_number < len(self.images):
                    screen.blit(self.images[image_number], (self.x, self.y))
                else:
                    screen.blit(self.images[0], (self.x, self.y))
            else:
                pygame.draw.rect(screen, (0,0,0), self.rect)


class InvisibleButton:
    def __init__(self, x : int, y : int, width : int, height : int, resolution = (1920, 1080)):
        self.scale_x = float(float(resolution[0]) / 1920.0)
        self.scale_y = float(float(resolution[1]) / 1080.0)

        self.x = x * self.scale_x
        self.y = y * self.scale_y
        self.width = width * self.scale_x
        self.height = height * self.scale_y
        self.is_clicked = False

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, mx, my):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.rect.collidepoint(mx, my) and pygame.mouse.get_pressed()[0]:
            self.is_clicked = True
        else:
            self.is_clicked = False
        
    def get_clicked(self):
        return self.is_clicked
    
    def test_draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect)


class Text:
    def __init__(self, x : int, y : int, font_name : str, font_size : int, text : str, color = (255, 255, 255), resolution = (1920, 1080)) -> None:
        self.scale_x = float(float(resolution[0]) / 1920.0)
        self.scale_y = float(float(resolution[1]) / 1080.0)
        self.x = x * self.scale_x
        self.y = y * self.scale_y
        self.font_name = font_name
        self.font_size = int(font_size * self.scale_x)

        self.font = pygame.font.SysFont(self.font_name, self.font_size)

        self.text = text
        self.color = color

        self.text_surface = self.font.render(self.text, True, self.color)


    def change_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)


    def draw_text(self, screen):
        screen.blit(self.text_surface, (self.x, self.y))


class Game:
    def __init__(self) -> None:
        with open(resource_path("config.json"), "r") as f:
            self.data = json.load(f)

        # with open(resource_path("config.json"), "w") as f:
        #    json.dump(data, f)

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
        self.state = 'MainMenu'

        self.init_game()
        self.init_main_menu()
        self.init_options()

        self.update()


    def init_game(self):
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

        self.new_game_button = Button(600, 200, 600, 50, resource_path("assets/cam_button"), False, self.RESOLUTION)

        self.static = AnimationObject(0, 0, 100, self.RESOLUTION)
        self.static.append_frames(resource_path("assets/static.png"))
        self.static.append_frames(resource_path("assets/static2.png"))
        self.static.append_frames(resource_path("assets/static3.png"))
        self.static.append_frames(resource_path("assets/static4.png"))
        self.static.append_frames(resource_path("assets/static5.png"))

        self.main_menu_background = Panel(0, 0, 1920, 1080, resource_path("assets/main_menu_background.png"), self.RESOLUTION)

        self.new_game_button = Button(30, 390, 581, 111, resource_path("assets/new_game"), True, self.RESOLUTION)
        self.continue_button = Button(30, 511, 581, 111, resource_path("assets/continue"), True, self.RESOLUTION)

        self.options_button = Button(30, 632, 581, 111, resource_path("assets/options"), True, self.RESOLUTION)
        self.custom_night_button = Button(30, 753, 581, 111, resource_path("assets/custom_night"), True, self.RESOLUTION)
        self.extras_button = Button(30, 874, 581, 111, resource_path("assets/extras"), True, self.RESOLUTION)

        self.exit_button = Button(30, 980, 581, 111, resource_path("assets/exit"), True, self.RESOLUTION)

        self.copyright_text = Text(1250, 1040, 'Arial', 32, "© 2023 KosaQDev Inspired By Scott Cawthon.", (255,255,255), self.RESOLUTION)

        self.button_swipe_sound = pygame.mixer.Sound(resource_path('sounds/menu_swipe.wav'))
        self.button_swipe_sound.set_volume(self.data_volume['VOLUME'])

        self.sound_played_new_game = False
        self.sound_played_continue = False
        self.sound_played_options = False
        self.sound_played_extras = False
        self.sound_played_custom_night = False
        self.sound_played_exit = False


    def init_options(self):
        self.resolutions = ['1920 x 1080', '1600 x 900', '1366 x 768', '1280 x 720']
        self.fullscreen = True

        self.resolution_index = 0
        self.resolution_text = Text(400, 300, 'Arial', 62, self.resolutions[self.resolution_index], (255,255,255), self.RESOLUTION)
        self.resolution_left = Button(200, 300, 64, 64, resource_path('assets/blank_l'), False, self.RESOLUTION)
        self.resolution_right = Button(300, 300, 64, 64, resource_path('assets/blank_r'), False, self.RESOLUTION)

        self.fullscreen_checkbox = Checkbox(200, 200, 64, 64, resource_path("assets/blank"), True, self.RESOLUTION)
        self.fullscreen_text = Text(300, 200, 'Arial', 62, "Fullscreen", (255,255,255), self.RESOLUTION)

        self.volume_left = Button(200, 400, 64, 64, resource_path('assets/blank_l'), False, self.RESOLUTION)
        self.volume_right = Button(300, 400, 64, 64, resource_path('assets/blank_r'), False, self.RESOLUTION)
        self.volume_text = Text(400, 400, 'Arial', 62, str(self.data_volume['VOLUME']), (255,255,255), self.RESOLUTION)
        self.volume = self.data_volume['VOLUME']
        self.volume_text.change_text(str(int(self.data_volume['VOLUME'] * 100)))

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


    def handle_main_menu_sounds(self):
        if self.new_game_button.hovered and self.sound_played_new_game == False:
            self.button_swipe_sound.play()
            self.sound_played_new_game = True
        if self.continue_button.hovered and self.sound_played_continue == False:
            self.button_swipe_sound.play()
            self.sound_played_continue = True
        if self.options_button.hovered and self.sound_played_options == False:
            self.button_swipe_sound.play()
            self.sound_played_options = True
        if self.extras_button.hovered and self.sound_played_extras == False:
            self.button_swipe_sound.play()
            self.sound_played_extras = True
        if self.custom_night_button.hovered and self.sound_played_custom_night == False:
            self.button_swipe_sound.play()
            self.sound_played_custom_night = True
        if self.exit_button.hovered and self.sound_played_exit == False:
            self.button_swipe_sound.play()
            self.sound_played_exit = True

        if self.new_game_button.hovered == False: 
            self.sound_played_new_game = False
        if self.continue_button.hovered == False: 
            self.sound_played_continue = False
        if self.options_button.hovered == False: 
            self.sound_played_options = False
        if self.extras_button.hovered == False: 
            self.sound_played_extras = False
        if self.custom_night_button.hovered == False: 
            self.sound_played_custom_night = False
        if self.exit_button.hovered == False: 
            self.sound_played_exit = False


    def handle_main_menu(self, mx, my):
        self.handle_main_menu_sounds()
        if self.new_game_button.get_clicked(mx, my, 0):
            self.state = 'Game'

        if self.options_button.get_clicked(mx, my, 0):
            self.state = 'Options'
        
        if self.exit_button.get_clicked(mx, my, 0):
            self.done = True

        self.main_menu_background.draw(self.screen)

        self.new_game_button.draw(self.screen, mx, my)


        self.continue_button.draw(self.screen, mx, my)
        self.options_button.draw(self.screen, mx, my)

        if self.stars == 1:
            self.custom_night_button.draw(self.screen, mx, my)
            self.extras_button.draw(self.screen, mx, my)

        self.exit_button.draw(self.screen, mx, my)
        self.copyright_text.draw_text(self.screen)
        self.static.play_loop(self.screen)

    
    def handle_options(self, mx, my):
        if self.exit_button.get_clicked(mx, my, 0):
            self.state = 'MainMenu'
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

                self.data['options'][2]['VOLUME'] = self.volume

                json.dump(self.data, f)

        if self.resolution_left.get_clicked(mx, my, 0) and self.resolution_index > 0:
            self.resolution_index -= 1
            self.resolution_text.change_text(self.resolutions[self.resolution_index])
        if self.resolution_right.get_clicked(mx, my, 0) and self.resolution_index < (len(self.resolutions) -1):
            self.resolution_index += 1
            self.resolution_text.change_text(self.resolutions[self.resolution_index])

        if self.volume_left.get_clicked(mx, my, 0) and self.volume > 0:
            self.volume -= 0.1
            self.volume_text.change_text(str(int(self.volume * 100)))
        if self.volume_right.get_clicked(mx, my, 0) and self.volume < 1:
            self.volume += 0.1
            self.volume_text.change_text(str(int(self.volume * 100)))

        self.main_menu_background.draw(self.screen)
        self.fullscreen = self.fullscreen_checkbox.get_check_state(mx, my, 0)
        self.exit_button.draw(self.screen, mx, my)
        
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