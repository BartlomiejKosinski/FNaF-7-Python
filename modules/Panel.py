import pygame

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