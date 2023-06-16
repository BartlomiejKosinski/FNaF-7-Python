import pygame

class MenuButton:
    def __init__(self, x : int, y : int, font_name : str, font_size : int, text : str, sound = None, color = (255,255,255), resolution = (1920, 1080)) -> None:
        self.scale_x = float(float(resolution[0]) / 1920.0)
        self.scale_y = float(float(resolution[1]) / 1080.0)

        self.x = x * self.scale_x
        self.y = y * self.scale_y
        
        self.font_name = font_name 
        self.font_size = int(font_size * self.scale_x)
        self.text = text
        self.sound = sound
       
        self.color = color

        self.font = pygame.font.SysFont(self.font_name, self.font_size)

        self.text_surface = self.font.render(self.text, True, self.color)

        self.rect = pygame.Rect(self.x, self.y, self.text_surface.get_width(), self.text_surface.get_height())

        self.clicked = False
        self.hovered = False

    def get_clicked(self, mx, my, btn):
        if self.rect.collidepoint(mx, my):
            if pygame.mouse.get_pressed()[btn] and self.clicked == False:
                self.clicked = True
                return True
        if pygame.mouse.get_pressed()[btn] == 0:
            self.clicked = False
            return False
        

    def draw(self, screen, mx, my, hover_x_offset = 0):
        if self.rect.collidepoint(mx, my) and self.hovered == False:
            if self.sound is not None:
                self.sound.play()
            self.hovered = True
        if not self.rect.collidepoint(mx, my):
            self.hovered = False

        if self.hovered:
            screen.blit(self.text_surface, (self.x + hover_x_offset, self.y))
        else:
            screen.blit(self.text_surface, (self.x, self.y))