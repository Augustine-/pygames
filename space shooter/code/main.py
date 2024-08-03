import pygame
import random

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
WINDOW_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
pygame.display.set_caption("space")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True

# plain
surf = pygame.Surface((100, 200))
surf.fill('orange')

# player
player_surf = pygame.image.load('images/player.png').convert_alpha()
player_rect = player_surf.get_frect(center = WINDOW_CENTER)
p_x = 100

# stars
star_surf = pygame.image.load('images/star.png').convert_alpha()
stars = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]

# meteor
meteor_surf = pygame.image.load('images/meteor.png').convert_alpha()
meteor_rect = meteor_surf.get_frect(center = WINDOW_CENTER)

# laser
laser_surf = pygame.image.load('images/laser.png').convert_alpha()
laser_rect = laser_surf.get_frect(left = 20, bottom = WINDOW_HEIGHT - 20)

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # render game
    # background
    screen.fill('darkblue')
    # block image transfer, put one surf on another
    for star in stars:
        screen.blit(star_surf, (star[0], star[1]))

    # meteor
    screen.blit(meteor_surf, meteor_rect)

    # laser
    screen.blit(laser_surf, laser_rect)

    # player
    player_rect.left += 0.1
    screen.blit(player_surf, player_rect)

    pygame.display.update()
pygame.quit()