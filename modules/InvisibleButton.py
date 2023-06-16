import pygame

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