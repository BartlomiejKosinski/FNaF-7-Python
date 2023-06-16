import pygame

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