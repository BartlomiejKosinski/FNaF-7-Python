import pygame

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