import pygame
import random

pygame.init()

amp_pantalla = 1280
alt_pantalla = 720
screen = pygame.display.set_mode((amp_pantalla, alt_pantalla))

pygame.display.set_caption('Joc Hackaton')


player_idle = [
    pygame.image.load('Personatge_joc_1_idle.png'),
    pygame.image.load('idle.png'),

]

player_rect = player_idle[0].get_rect()
player_position_x = 400
player_position_y = alt_pantalla // 2

clock = pygame.time.Clock()


running = True

looking_left = True

player_idle_flip = [
    pygame.transform.flip(player_idle[0], True, False), 
    pygame.transform.flip(player_idle[-1], True, False),

]

player_actual_skin = player_idle[0]
player_actual_skin_flipped = player_idle_flip[0]

skin_count = 0
skin_change = 30


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("cyan")


    if looking_left == False:

        player_actual_skin_flipped = player_idle_flip[skin_count]
        screen.blit(player_actual_skin_flipped, player_rect)  
    else:
        player_actual_skin = player_idle[skin_count]
        screen.blit(player_actual_skin, player_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_position_x -= 5
        looking_left = True
    elif keys[pygame.K_RIGHT]:
        player_position_x += 5
        looking_left = False
    if keys[pygame.K_UP]:   
        player_position_y -= 5
    elif keys[pygame.K_DOWN]:
        player_position_y += 5
    

    
    player_rect.center = (player_position_x, player_position_y)


    skin_change -= 1
    if skin_change == 0:
        skin_count += 1
        if skin_count >= len(player_idle):
            skin_count = 0
    if skin_change <= 0:
        skin_change = 30
    

    pygame.display.update()
    clock.tick(60)

pygame.quit()