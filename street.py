from pathlib import Path

import pygame.image


# [ side ][   street   ][ side ] -128
# ------------------------------ 0
# [ side ][   street   ][ side ] 128
# [ side ][   street   ][ side ] 256
# [ side ][   street   ][ side ] 384
# [ side ][   street   ][ side ] 512
# [ side ][   street   ][ side ] 640
# ------------------------------ 768        768

class Street:
    def __init__(self, street_name='good_asphalt', side_name='grass', lanes=None):
        if lanes is None:
            lanes = [100, 264, 418]
        self.position = 0
        self.view_width, self.view_height = pygame.display.get_surface().get_size()
        assets_dir = Path('assets').joinpath(Path('streets'))
        street_texture_path = assets_dir.joinpath(Path(f'street_{street_name}.png'))
        left_side_texture_path = assets_dir.joinpath(Path(f'side_left_{side_name}.png'))
        right_side_texture_path = assets_dir.joinpath(Path(f'side_right_{side_name}.png'))
        self.street_texture = pygame.image.load(street_texture_path).convert()
        self.left_side_texture = pygame.image.load(left_side_texture_path).convert()
        self.right_side_texture = pygame.image.load(right_side_texture_path).convert()
        self.tile_height = self.street_texture.get_height()
        if (self.tile_height != self.left_side_texture.get_height() or
                self.tile_height != self.right_side_texture.get_height()):
            raise ValueError('Street and side tiles do not have the same height.')
        self.lanes = [l + self.left_side_texture.get_width() for l in lanes]

    def reset(self):
        self.position = 0

    def draw_tiles(self, surface: pygame.Surface):
        offset = self.position % self.tile_height
        for i in range(0, self.view_height % self.tile_height + 2):
            surface.blit(self.left_side_texture, (0,
                                                  self.view_height - i * self.tile_height + offset))
            surface.blit(self.street_texture, (self.left_side_texture.get_width(),
                                               self.view_height - i * self.tile_height + offset))
            surface.blit(self.right_side_texture, (self.left_side_texture.get_width() + self.street_texture.get_width(),
                                                   self.view_height - i * self.tile_height + offset))
