import pygame

amplada_pantalla = 1200
altura_pantalla = 720

# Importació de les imatges

play_image = pygame.image.load("main_screen/images/Buttons/Play_button.png")
difficulty_button_easy_image = pygame.image.load("main_screen/images/Buttons/Difficulty_easy_button.png")
difficulty_button_medium_image = pygame.image.load("main_screen/images/Buttons/Difficulty_medium_button.png")
difficulty_button_hard_image = pygame.image.load("main_screen/images/Buttons/Difficulty_hard_button.png")

# Escalatge de les imatges

play_button = pygame.transform.scale(play_image, ((play_image.get_width() * 9), (play_image.get_width() * 3)))
difficulty_button_easy = pygame.transform.scale(difficulty_button_easy_image, ((difficulty_button_easy_image.get_width() * 9), ((pygame.image.load("main_screen/images/Buttons/Play_button.png")).get_width() * 3)))
difficulty_button_medium = pygame.transform.scale(difficulty_button_medium_image, ((difficulty_button_medium_image.get_width() * 9), (difficulty_button_medium_image.get_width() * 3)))
difficulty_button_hard = pygame.transform.scale(difficulty_button_hard_image, ((difficulty_button_hard_image.get_width() * 9), (difficulty_button_hard_image.get_width() * 3)))

# Agafar els rects de les imatges
play_button_rect = play_button.get_rect(center = (amplada_pantalla // 2, altura_pantalla // 2))
difficulty_button_easy_rect = difficulty_button_easy.get_rect(topleft = (50, 50))
difficulty_button_medium_rect = difficulty_button_medium.get_rect(topleft = (50, 150))
difficulty_button_hard_rect = difficulty_button_hard.get_rect(topleft = (50, 250))
