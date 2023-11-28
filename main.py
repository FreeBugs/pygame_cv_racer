import random
import time

import pygame

from pygame_gesture_kit import hand_visualizer
from pygame_gesture_kit import GestureRecognizer, Camera

from car import Car
from player import Player
from street import Street


def show_fps(surf, font, clock):
    fps = f'FPS: {clock.get_fps():.2f}'
    rendered_fps = font.render(fps, 1, pygame.Color("darkslateblue"))
    x = surf.get_rect().w - font.size(fps)[0]
    surf.blit(rendered_fps, (x, 0))


if __name__ == '__main__':
    preferred_cam = 0
    screen_width = 896
    screen_height = 504
    vertical_threshold = 100
    max_obstacles = 3
    spawn_probability = .5
    player_speed = 2
    max_speed_diff = 3

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height),
                                     flags=pygame.SCALED | pygame.RESIZABLE,
                                     vsync=1)
    pygame.display.set_caption("PyGame ComputerVision Racer")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("monospace", 24, bold=True)
    large_font = pygame.font.SysFont("monospace", 48, bold=True)
    small_font = pygame.font.SysFont("monospace", 20)

    capture_device = Camera()
    try:
        capture_device.open_camera(preferred_cam)
    except Exception as e:
        print(e)
        exit(1)
    gesture_recognizer = GestureRecognizer(capture_device, max_hands=4)
    gesture_recognizer.start()

    street = Street()

    player = Player()
    player.set_lanes(street.lanes)
    player.current_lane = 1
    friendly = pygame.sprite.Group()
    friendly.add(player)

    obstacles = pygame.sprite.Group()

    is_running = True
    cam_image = None
    while is_running:
        screen.fill(pygame.Color('white'))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                is_running = False
                break
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    is_running = False
                if e.key == pygame.K_LEFT:
                    player.switch_lane(player.current_lane - 1)
                if e.key == pygame.K_RIGHT:
                    player.switch_lane(player.current_lane + 1)

        street.position += player_speed
        street.draw_tiles(screen)

        if len(obstacles) < max_obstacles and random.random() > spawn_probability:
            positions = [o.rect.y for o in obstacles]
            if len(positions) == 0 or min(positions) > player.rect.h * 2:  # leave enough space to pass
                lane = random.randint(0, len(street.lanes) - 1)
                cars_in_lane = [o.speed for o in obstacles]
                if len(cars_in_lane) > 0:
                    max_speed = max(cars_in_lane) - player_speed - 1
                else:
                    max_speed = max_speed_diff
                if max_speed <= 1:
                    speed = 1 + player_speed
                else:
                    speed = random.randint(1, max_speed) + player_speed
                new_car = Car(street.lanes,
                              car_type='01',
                              lane=lane,
                              speed=speed)
                obstacles.add(new_car)

        obstacles.update()
        for o in obstacles:
            if o.passed:
                obstacles.remove(o)
        obstacles.draw(screen)

        friendly.update()
        friendly.draw(screen)

        if len(obstacles) > 0 and player.rect.collidelist([o.rect for o in obstacles]) > -1:
            txt = 'You crashed - Try again!'
            game_over = large_font.render(txt, 1, pygame.Color('red'), pygame.Color('black'))
            w, h = large_font.size(txt)
            screen.blit(game_over, (screen_width / 2 - w / 2, screen_height / 2 - h / 2))
            pygame.display.flip()
            time.sleep(5)
            obstacles.empty()
            player.current_lane = 1
            street.position = 0

        hands = gesture_recognizer.get_hands()
        for hand in hands:
            hand_visualizer.draw_bones(screen, hand, color=(255, 255, 255, 128))  # , joint_label_font=small_font)

        wrists = [h.landmarks[0] for h in hands]
        if len(wrists) == 2:
            x1, y1 = wrists[0]
            x2, y2 = wrists[1]
            if x1 < x2:
                vertical_distance = y2 - y1
            else:
                vertical_distance = y1 - y2
            if vertical_distance > vertical_threshold:
                player.switch_lane(player.current_lane + 1)
            if vertical_distance < -vertical_threshold:
                player.switch_lane(player.current_lane - 1)

        show_fps(screen, font, clock)
        pygame.display.flip()
        clock.tick(60)

    gesture_recognizer.stop()
    capture_device.close_camera()
    pygame.quit()
