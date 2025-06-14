import pygame 
import time

from buttons import play_button, play_button_rect, play_button_apretat, play_button_apretat_rect
from buttons import difficulty_button_easy, difficulty_button_easy_rect, difficulty_button_medium, difficulty_button_medium_rect, difficulty_button_hard, difficulty_button_hard_rect
from buttons import reaction_time_button, reaction_time_button_rect

from buttons import difficulty_buttons_list, difficulty_buttons_list_rects

pygame.init()

# Configuració de la pantalla

amplada_pantalla = 1200
altura_pantalla = 720
pantalla = pygame.display.set_mode((amplada_pantalla, altura_pantalla))
pygame.display.set_caption("Minigames")

# Configuració del rellotge

clock = pygame.time.Clock()

# Creació de les variables principals

estat_actual = "menu"
any_game_running = False
difficulty_mode = 0 # 0: easy, 1: medium, 2: hard
difficulty_wait_change = 10

# Bucle principal del joc

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pantalla.fill("white")

# Dibuixar els botons a la pantalla si no hi ha cap joc actiu

    if estat_actual == "menu":
        pantalla.blit(reaction_time_button, reaction_time_button_rect)

    mouse_position = pygame.mouse.get_pos()

    if reaction_time_button_rect.collidepoint(mouse_position) and event.type == pygame.MOUSEBUTTONDOWN:

        estat_actual = "reaction_time_game"
        any_game_running = True
       
    if any_game_running == True:

        pantalla.blit(difficulty_buttons_list[difficulty_mode], difficulty_buttons_list_rects[difficulty_mode])
        pantalla.blit(play_button, play_button_rect)
        if play_button_rect.collidepoint(mouse_position):

            pantalla.blit(play_button_apretat, play_button_apretat_rect)

    if difficulty_wait_change == 0:
        if difficulty_button_easy_rect.collidepoint(mouse_position) and event.type == pygame.MOUSEBUTTONDOWN:
            difficulty_wait_change = 10
            if difficulty_mode == 2:
                difficulty_mode = 0
            else:
                difficulty_mode += 1
    
    if difficulty_wait_change > 0:
        difficulty_wait_change -= 1
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()