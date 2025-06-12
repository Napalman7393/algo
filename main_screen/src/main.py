import pygame
from buttons import play_button, play_button_rect, difficulty_button_easy, difficulty_button_easy_rect, difficulty_button_medium, difficulty_button_medium_rect, difficulty_button_hard, difficulty_button_hard_rect

pygame.init()

# Configuració de la pantalla

amplada_pantalla = 1200
altura_pantalla = 720
pantalla = pygame.display.set_mode((amplada_pantalla, altura_pantalla))
pygame.display.set_caption("Minigames")

# Configuració del rellotge

clock = pygame.time.Clock()

# Creació de les variables principals

any_game_running = False

# Bucle principal del joc

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pantalla.fill("white")

# Dibuixar els botons a la pantalla si no hi ha cap joc actiu

    if any_game_running == False:
        pantalla.blit(play_button, play_button_rect)
        pantalla.blit(difficulty_button_easy, difficulty_button_easy_rect)
        pantalla.blit(difficulty_button_medium, difficulty_button_medium_rect)
        pantalla.blit(difficulty_button_hard, difficulty_button_hard_rect)

    
    pygame.display.update()
    clock.tick(60)

pygame.quit()