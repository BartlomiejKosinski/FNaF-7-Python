import pygame

class Button:
    def __init__(self, x : int, y : int, width : int, height : int, source : str, hover_source = None, resolution = (1920, 1080)) -> None:
        self.scale_x = float(float(resolution[0]) / 1920.0)
        self.scale_y = float(float(resolution[1]) / 1080.0)

        self.x = x * self.scale_x
        self.y = y * self.scale_y
        self.width = width * self.scale_x
        self.height = height * self.scale_y
        self.source = source
        self.hover_source = hover_source

        self.clicked = False
        self.hovered = False

        self.image = pygame.transform.scale_by(pygame.image.load(self.source).convert_alpha(), (self.scale_x, self.scale_y))
        if self.hover_source is not None:
            self.hover_image = pygame.transform.scale_by(pygame.image.load(self.hover_source).convert_alpha(), (self.scale_x, self.scale_y))

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
        if self.rect.collidepoint(mx, my) and self.hover_source is not None:
            screen.blit(self.hover_image, (self.x, self.y))
            self.hovered = True
        else:
            screen.blit(self.image, (self.x, self.y))
            self.hovered = False