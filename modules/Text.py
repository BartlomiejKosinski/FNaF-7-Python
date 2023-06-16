import pygame

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