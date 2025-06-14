import pygame
import time

from buttons import (
    play_button, play_button_rect, play_button_apretat, play_button_apretat_rect,
    difficulty_button_easy, difficulty_button_easy_rect,
    difficulty_button_medium, difficulty_button_medium_rect,
    difficulty_button_hard, difficulty_button_hard_rect,
    reaction_time_button, reaction_time_button_rect,
    difficulty_buttons_list, difficulty_buttons_list_rects
)

pygame.init()

# Configuració de la pantalla
amplada_pantalla = 1200
altura_pantalla = 720
pantalla = pygame.display.set_mode((amplada_pantalla, altura_pantalla))
pygame.display.set_caption("Minigames")

# Configuració del rellotge
clock = pygame.time.Clock()

# Variables principals
estat_actual = "menu"
any_game_running = False
difficulty_mode = 0  # 0: easy, 1: medium, 2: hard

# Variables per controlar cooldown clics dificultat
temps_ultima_dificultat = 0
temps_cooldown = 300  # mil·lisegons

def dibuixa_menu():
    pantalla.fill("white")
    pantalla.blit(reaction_time_button, reaction_time_button_rect)

def dibuixa_reaction_game():
    pantalla.fill("white")
    pantalla.blit(difficulty_buttons_list[difficulty_mode], difficulty_buttons_list_rects[difficulty_mode])
    pantalla.blit(play_button, play_button_rect)
    mouse_position = pygame.mouse.get_pos()
    if play_button_rect.collidepoint(mouse_position):
        pantalla.blit(play_button_apretat, play_button_apretat_rect)

# Bucle principal
running = True

while running:
    temps_actual = pygame.time.get_ticks()
    clic_detectat = False
    mouse_position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clic_detectat = True

            if estat_actual == "menu":
                if reaction_time_button_rect.collidepoint(mouse_position):
                    estat_actual = "reaction_time_game"
                    any_game_running = True

            elif any_game_running:
                # Controla canvi de dificultat amb cooldown
                if difficulty_button_easy_rect.collidepoint(mouse_position):
                    if temps_actual - temps_ultima_dificultat > temps_cooldown:
                        difficulty_mode = (difficulty_mode + 1) % 3
                        temps_ultima_dificultat = temps_actual

    # Dibuixa segons estat
    if estat_actual == "menu":
        dibuixa_menu()

    elif estat_actual == "reaction_time_game":
        dibuixa_reaction_game()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
