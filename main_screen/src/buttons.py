import pygame

amplada_pantalla = 1200
altura_pantalla = 720

# Importació de les imatges

play_image = pygame.image.load("main_screen/images/Buttons/Play_button.png")
plat_apretat_image = pygame.image.load("main_screen/images/Buttons/Play_button_apretat.png")

difficulty_button_easy_image = pygame.image.load("main_screen/images/Buttons/Difficulty_easy_button.png")
difficulty_button_medium_image = pygame.image.load("main_screen/images/Buttons/Difficulty_medium_button.png")
difficulty_button_hard_image = pygame.image.load("main_screen/images/Buttons/Difficulty_hard_button.png")

reaction_time_image = pygame.image.load("main_screen/images/Buttons/Reaction_time_button.png")

# Escalatge de les imatges

play_button = pygame.transform.scale(plat_apretat_image, ((plat_apretat_image.get_width() * 9), (plat_apretat_image.get_width() * 3)))
play_button_apretat = pygame.transform.scale(play_image, ((play_image.get_width() * 9), (play_image.get_width() * 3)))

difficulty_button_easy = pygame.transform.scale(difficulty_button_easy_image, ((difficulty_button_easy_image.get_width() * 9), ((pygame.image.load("main_screen/images/Buttons/Play_button.png")).get_width() * 3)))
difficulty_button_medium = pygame.transform.scale(difficulty_button_medium_image, ((difficulty_button_medium_image.get_width() * 9), (difficulty_button_medium_image.get_width() * 3)))
difficulty_button_hard = pygame.transform.scale(difficulty_button_hard_image, ((difficulty_button_hard_image.get_width() * 9), (difficulty_button_hard_image.get_width() * 3)))

reaction_time_button = pygame.transform.scale(reaction_time_image, ((reaction_time_image.get_width() * 9), (reaction_time_image.get_width() * 3)))

# Agafar els rects de les imatges
play_button_rect = play_button_apretat.get_rect(center = (amplada_pantalla // 2, altura_pantalla // 2))
play_button_apretat_rect = play_button.get_rect(center = (amplada_pantalla // 2, altura_pantalla // 2))

difficulty_button_easy_rect = difficulty_button_easy.get_rect(topleft = (50, 150))
difficulty_button_medium_rect = difficulty_button_medium.get_rect(topleft = (50, 150))
difficulty_button_hard_rect = difficulty_button_hard.get_rect(topleft = (50, 150))

reaction_time_button_rect = reaction_time_button.get_rect(topleft = (50, 350))


# Llista botons dificultat

difficulty_buttons_list = [difficulty_button_easy, difficulty_button_medium, difficulty_button_hard]
difficulty_buttons_list_rects = [difficulty_button_easy_rect, difficulty_button_medium_rect, difficulty_button_hard_rect]