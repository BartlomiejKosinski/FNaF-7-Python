import pygame
from modules.Text import Text

class Checkbox:
    def __init__(self, x : int, y : int, width : int, height : int, font_name : str, font_size : int, resolution = (1920, 1080), checked_offset_x = 0, checked_offset_y = 0) -> None:
        self.scale_x = float(float(resolution[0]) / 1920.0)
        self.scale_y = float(float(resolution[1]) / 1080.0)

        self.x = x
        self.y = y
        self.width = width * self.scale_x
        self.height = height * self.scale_y

        self.font_name = font_name
        self.font_size = font_size

        self.clicked = False
        self.state = False
    
        self.text = Text(self.x + checked_offset_x, self.y + checked_offset_y, self.font_name, self.font_size, " ", (255,255,255), resolution)
        self.checked_text = Text(self.x + checked_offset_x, self.y + checked_offset_y, self.font_name, self.font_size, "X", (255,255,255), resolution)

        self.rect = pygame.Rect(self.x * self.scale_x, self.y * self.scale_y, self.width, self.height)


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
            self.checked_text.draw_text(screen)
            pygame.draw.rect(screen, (255,255,255), self.rect, 2)
        else:
            self.text.draw_text(screen)
            pygame.draw.rect(screen, (255,255,255), self.rect, 2)