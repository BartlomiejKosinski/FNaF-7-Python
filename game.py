import pygame


class HoverButton:
    def __init__(self, x : int, y : int, width : int, height : int, source : str = None) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.source = source

        self.color = (255,0,0)
        self.enabled = True
        self.value = False
        self.state = 0

        self.images = []

        if source is not None:
            try:
                self.images.append(pygame.image.load(self.source))
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


class Panel:
    def __init__(self, x : int, y : int, width : int, height : int, source : str = None) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.source = source

        self.visible = True

        self.images = []

        if source is not None:
            try:
                self.images.append(pygame.image.load(self.source))
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
    def __init__(self, x : int, y : int, width : int, height : int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_clicked = False

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, mx, my):
        if self.rect.collidepoint(mx, my) and pygame.mouse.get_pressed()[0]:
            self.is_clicked = True
        else:
            self.is_clicked = False
        
    def get_clicked(self):
        return self.is_clicked
    
    def test_draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect)


class Game:
    def __init__(self) -> None:
        self.RESOLUTION = (1920, 1080)
        self.screen = pygame.display.set_mode(self.RESOLUTION, pygame.FULLSCREEN)
        pygame.display.set_caption("Fnaf Python")

        self.cam_button = HoverButton(660, 1020, 600, 60, "assets/cam_button.png")
        self.done = False

        self.office = Panel(0, 0, 1920, 1080, "assets/office.png")

        self.office_door = Panel(0, 0, 1920, 1080, "assets/office_door.png")
        self.office_door_button = InvisibleButton(230,190,190,700)

        self.office_front_vent = Panel(0, 0, 1920, 1080, "assets/office_front_vent.png")
        self.office_front_vent_button = InvisibleButton(840, 320, 340, 200)

        self.office_right_vent = Panel(0, 0, 1920, 1080, "assets/office_right_vent.png")
        self.office_right_vent_button = InvisibleButton(1585, 545, 140, 340)


        self.panel = Panel(0, 0, 1920, 1080, "assets/cam1.png")

        self.office_door.set_visible(False)
        self.office_front_vent.set_visible(False)
        self.office_right_vent.set_visible(False)

        self.update()


    def office_invisible_buttons(self, mx, my):
        self.office_door_button.update(mx, my)
        self.office_front_vent_button.update(mx, my)
        self.office_right_vent_button.update(mx, my)

        
        if self.office_door_button.get_clicked():
            self.office_door.set_visible(True)
            self.office.set_visible(False)
        else:
            self.office_door.set_visible(False)
            self.office.set_visible(True)

        if self.office_front_vent_button.get_clicked():
            self.office_front_vent.set_visible(True)
            self.office.set_visible(False)
        else:
            self.office_front_vent.set_visible(False)
            self.office.set_visible(True)

        if self.office_right_vent_button.get_clicked():
            self.office_right_vent.set_visible(True)
            self.office.set_visible(False)
        else:
            self.office_right_vent.set_visible(False)
            self.office.set_visible(True)


    def update(self) -> None:
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       self.done = True

            mx, my = pygame.mouse.get_pos()
            self.office_invisible_buttons(mx, my)

            self.panel.set_visible(self.cam_button.get_value())
            self.office.set_visible(not self.cam_button.get_value())

            self.cam_button.update()

            self.screen.fill((10,5,5))

            self.office.draw(self.screen)
            self.office_door.draw(self.screen)
            self.office_front_vent.draw(self.screen)
            self.office_right_vent.draw(self.screen)

            self.panel.draw(self.screen)
            self.cam_button.draw(self.screen)

            pygame.display.update()


if __name__ == "__main__":
    Game()