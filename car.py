from pathlib import Path

import pygame


class Car(pygame.sprite.Sprite):
    def __init__(self, lanes, car_type, lane, speed):
        super().__init__()
        assets_dir = Path('assets').joinpath(Path('cars'))
        car_sprite_path = assets_dir.joinpath(Path(f'car_{car_type}.png'))
        self.image = pygame.image.load(car_sprite_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = lanes[lane] - self.rect.w / 2
        self.rect.y = 0 - self.image.get_height()
        self.lane = lane
        self.sprite_offset = int(self.rect.width / 2)
        self.speed = speed
        self.passed = False

    def update(self, *args, **kwargs):
        if self.rect.y < pygame.display.get_surface().get_height():
            self.rect.y += self.speed
        else:
            self.passed = True
