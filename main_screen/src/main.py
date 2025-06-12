import pygame

pygame.init()

# Configuració de la pantalla

amplada_pantalla = 800
altura_pantalla = 600
pantalla = pygame.display.set_mode((amplada_pantalla, altura_pantalla))
pygame.display.set_caption("Minigames")

# Importació de les imatges

play_button = pygame.image.load("main_screen/images/Buttons/Play_button.png").convert_alpha()
difficulty_button_easy = pygame.image.load("main_screen/images/Buttons/Difficulty_easy_button.png").convert_alpha()
difficulty_button_medium = pygame.image.load("main_screen/images/Buttons/Difficulty_medium_button.png").convert_alpha()
difficulty_button_hard = pygame.image.load("main_screen/images/Buttons/Difficulty_hard_button.png").convert_alpha()

# Configuració del rellotge

clock = pygame.time.Clock()

# Bucle principal del joc

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pantalla.fill("blue")

    
    pygame.display.update()
    clock.tick(60)

pygame.quit()