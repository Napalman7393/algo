import pygame
import time

from Reaction_time.ReactionTime import ReactionTimeGame
from buttons import (
    play_button, play_button_rect, play_button_apretat, play_button_apretat_rect,
    difficulty_button_easy_rect,
    difficulty_button_medium_rect,
    difficulty_button_hard_rect,
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
# any_game_running is now handled by estat_actual
difficulty_mode = 0  # 0: easy, 1: medium, 2: hard

# Variables per controlar cooldown clics dificultat
temps_ultima_dificultat = 0
temps_cooldown = 300  # mil·lisegons

# Game instance
reaction_time_game_instance = None # Will be initialized when game starts

def dibuixa_menu():
    pantalla.fill("white")
    pantalla.blit(reaction_time_button, reaction_time_button_rect)

def dibuixa_reaction_game_setup():
    pantalla.fill("white")
    pantalla.blit(difficulty_buttons_list[difficulty_mode], difficulty_buttons_list_rects[difficulty_mode])
    
    # Check if mouse is over play button for visual feedback
    mouse_position = pygame.mouse.get_pos()
    if play_button_rect.collidepoint(mouse_position):
        pantalla.blit(play_button_apretat, play_button_apretat_rect)
    else:
        pantalla.blit(play_button, play_button_rect)

# Bucle principal
running = True


while running:
    temps_actual = pygame.time.get_ticks()
    mouse_position = pygame.mouse.get_pos()
    
    # Collect all events for the current frame
    events = pygame.event.get() 

    for event in events: # Iterate through all collected events
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if estat_actual == "menu":
                if reaction_time_button_rect.collidepoint(mouse_position):
                    estat_actual = "reaction_time_game_setup" # Anem a la pantalla de configuració del joc de reacció
                    reaction_time_game_instance = ReactionTimeGame(pantalla) # Inicialitzem el joc aquí (per primera vegada o si venim del menú)
            
            elif estat_actual == "reaction_time_game_setup":
                if play_button_rect.collidepoint(mouse_position):
                    # **** AQUÍ ÉS EL CANVI CLAU ****
                    reaction_time_game_instance = ReactionTimeGame(pantalla) 
                    estat_actual = "playing_reaction_time_game"
                
                # Check for difficulty changes
                if difficulty_button_easy_rect.collidepoint(mouse_position): # All difficulty buttons share same rect
                    if temps_actual - temps_ultima_dificultat > temps_cooldown:
                        difficulty_mode = (difficulty_mode + 1) % 3
                        temps_ultima_dificultat = temps_actual

    # Drawing based on current state
    if estat_actual == "menu":
        dibuixa_menu()

    elif estat_actual == "reaction_time_game_setup":
        dibuixa_reaction_game_setup()

    elif estat_actual == "playing_reaction_time_game":
        # Update and draw the reaction time game
        if reaction_time_game_instance:
            # Pass ALL collected events to the game instance's update method
            game_active = reaction_time_game_instance.update(events) 
            if not game_active:
                # Game finished (retry or again was clicked), return to setup
                estat_actual = "reaction_time_game_setup" 
                # reaction_time_game_instance will be re-initialized when 'play' is clicked again
        else:
            # Should not happen if logic is followed, but as a fallback
            estat_actual = "menu" 
            
    pygame.display.update()
    clock.tick(60)

pygame.quit()