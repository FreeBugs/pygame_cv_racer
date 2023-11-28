from pathlib import Path

import pygame


class Player(pygame.sprite.Sprite):
    lane_switch_ticks = 20

    def __init__(self, player_type='01'):
        super().__init__()
        assets_dir = Path('assets').joinpath(Path('cars'))
        car_sprite_path = assets_dir.joinpath(Path(f'player_{player_type}.png'))
        self.image = pygame.image.load(car_sprite_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = pygame.display.get_surface().get_height() - self.image.get_height() - 10
        self.sprite_offset = int(self.rect.width / 2)
        self.current_lane = 0
        self.changing_lane = 0
        self.lanes = [0]

    def set_lanes(self, lanes: list[int]):
        self.lanes = lanes

    def switch_lane(self, new_lane: int):
        if len(self.lanes) > new_lane >= 0 == self.changing_lane:  # valid lane and not currently changing
            self.changing_lane = 1 if new_lane > self.current_lane else -1

    def update(self, *args, **kwargs):
        self.rect.x = self.lanes[self.current_lane] - self.sprite_offset
        if 0 < abs(self.changing_lane) < self.lane_switch_ticks:
            new_lane_x = self.lanes[self.current_lane - 1] if self.changing_lane < 0 else self.lanes[
                self.current_lane + 1]
            lane_distance = new_lane_x - self.lanes[self.current_lane]
            interpolated_x = abs(self.changing_lane) / self.lane_switch_ticks * lane_distance
            self.rect.x += interpolated_x
            if self.changing_lane < 0:
                self.changing_lane -= 1
            else:
                self.changing_lane += 1
        if abs(self.changing_lane) == self.lane_switch_ticks:
            self.current_lane = self.current_lane + 1 if self.changing_lane > 0 else self.current_lane - 1
            self.changing_lane = 0
