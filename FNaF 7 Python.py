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

    def play(self, screen):
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


class MainMenu:
    def __init__(self) -> None:
        with open(resource_path("config.json"), "r") as f:
            self.data = json.load(f)

        # with open(resource_path("config.json"), "w") as f:
        #    json.dump(data, f)

        self.data_resolution = self.data['resolution'][0]
        self.RESOLUTION = (self.data_resolution['WIDTH'], self.data_resolution['HEIGHT'])

        self.screen = pygame.display.set_mode(self.RESOLUTION, pygame.FULLSCREEN)
        self.icon = pygame.image.load(resource_path('assets/icon.png'))

        pygame.display.set_caption("FNaF 7 Python")
        pygame.display.set_icon(self.icon)

        self.fps = 240
        self.clock = pygame.time.Clock()

        self.done = False

        self.new_game_button = Button(600, 200, 600, 50, resource_path("assets/cam_button"), False, self.RESOLUTION)

        self.static = AnimationObject(0, 0, 100, self.RESOLUTION)
        self.static.append_frames(resource_path("assets/static.png"))
        self.static.append_frames(resource_path("assets/static2.png"))
        self.static.append_frames(resource_path("assets/static3.png"))
        self.static.append_frames(resource_path("assets/static4.png"))
        self.static.append_frames(resource_path("assets/static5.png"))

        self.main_menu_background = Panel(0, 0, 1920, 1080, resource_path("assets/main_menu_background.png"), self.RESOLUTION)

        self.new_game_button = Button(30, 400, 581, 111, resource_path("assets/new_game"), True, self.RESOLUTION)
        self.continue_button = Button(30, 520, 581, 111, resource_path("assets/continue"), True, self.RESOLUTION)
        self.custom_night_button = Button(30, 640, 581, 111, resource_path("assets/custom_night"), True, self.RESOLUTION)
        self.extras_button = Button(30, 760, 581, 111, resource_path("assets/extras"), True, self.RESOLUTION)
        self.exit_button = Button(30, 950, 581, 111, resource_path("assets/exit"), True, self.RESOLUTION)


        self.update()

    
    def update(self):
        while not self.done:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       self.done = True
            mx, my = pygame.mouse.get_pos()

            if self.new_game_button.get_clicked(mx, my, 0):
                Night(1)
                break
            
            if self.exit_button.get_clicked(mx, my, 0):
                self.done = True

            self.main_menu_background.draw(self.screen)

            self.new_game_button.draw(self.screen, mx, my)
            self.continue_button.draw(self.screen, mx, my)
            self.custom_night_button.draw(self.screen, mx, my)
            self.extras_button.draw(self.screen, mx, my)
            self.exit_button.draw(self.screen, mx, my)

            self.static.play(self.screen)
            pygame.display.update()


class Night:
    def __init__(self, difficulty : int) -> None:
        with open(resource_path("config.json"), "r") as f:
            self.data = json.load(f)

        # with open(resource_path("config.json"), "w") as f:
        #    json.dump(data, f)

        self.data_resolution = self.data['resolution'][0]
        self.RESOLUTION = (self.data_resolution['WIDTH'], self.data_resolution['HEIGHT'])
        self.difficulty = difficulty

        self.screen = pygame.display.set_mode(self.RESOLUTION, pygame.FULLSCREEN)
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

        self.update()


    def office_invisible_buttons(self, mx, my):
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

            if mx < (400 * self.offset_x) and self.office.x < 0 and not self.in_cameras:
                self.office.x += self.speed_x
                self.office_door_button.x += self.speed_x
                self.office_front_vent_button.x += self.speed_x
                self.office_right_vent_button.x += self.speed_x

            elif mx > (1620 * self.offset_x) and self.office.x > (-580 * self.offset_x) and not self.in_cameras:
                self.office.x -= self.speed_x
                self.office_door_button.x -= self.speed_x
                self.office_front_vent_button.x -= self.speed_x
                self.office_right_vent_button.x -= self.speed_x

            self.office_door.x = self.office.x
            self.office_front_vent.x = self.office.x
            self.office_right_vent.x = self.office.x

            self.office_invisible_buttons(mx, my)

            self.cam1.set_visible(self.cam_button.get_value())
            self.office.set_visible(not self.cam_button.get_value())
            self.in_cameras = self.cam_button.get_value()

            self.cam_button.update()

            self.screen.fill((10,5,5))

            self.office.draw(self.screen)
            self.office_door.draw(self.screen)
            self.office_front_vent.draw(self.screen)
            self.office_right_vent.draw(self.screen)

            self.cam1.draw(self.screen)
            self.cam_button.draw(self.screen)

            pygame.display.update()


if __name__ == "__main__":
    MainMenu()