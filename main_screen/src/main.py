import pygame

pygame.init()

# Configuració de la pantalla

amplada_pantalla = 1200
altura_pantalla = 720
pantalla = pygame.display.set_mode((amplada_pantalla, altura_pantalla))
pygame.display.set_caption("Minigames")

# Importació de les imatges

play_image = pygame.image.load("main_screen/images/Buttons/Play_button.png").convert_alpha()
difficulty_button_easy_image = pygame.image.load("main_screen/images/Buttons/Difficulty_easy_button.png").convert_alpha()
difficulty_button_medium_image = pygame.image.load("main_screen/images/Buttons/Difficulty_medium_button.png").convert_alpha()
difficulty_button_hard_image = pygame.image.load("main_screen/images/Buttons/Difficulty_hard_button.png").convert_alpha()

# Escalatge de les imatges

play_button = pygame.transform.scale(play_image, ((play_image.get_width() * 9), (play_image.get_width() * 3)))
difficulty_button_easy = pygame.transform.scale(difficulty_button_easy_image, ((difficulty_button_easy_image.get_width() * 9), ((pygame.image.load("main_screen/images/Buttons/Play_button.png").convert_alpha()).get_width() * 3)))
difficulty_button_medium = pygame.transform.scale(difficulty_button_medium_image, ((difficulty_button_medium_image.get_width() * 9), (difficulty_button_medium_image.get_width() * 3)))
difficulty_button_hard = pygame.transform.scale(difficulty_button_hard_image, ((difficulty_button_hard_image.get_width() * 9), (difficulty_button_hard_image.get_width() * 3)))

# Agafar els rects de les imatges
play_button_rect = play_button.get_rect(center = (amplada_pantalla // 2, altura_pantalla // 2))
difficulty_button_easy_rect = difficulty_button_easy.get_rect(topleft = (50, 50))
difficulty_button_medium_rect = difficulty_button_medium.get_rect(topleft = (50, 150))
difficulty_button_hard_rect = difficulty_button_hard.get_rect(topleft = (50, 250))

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