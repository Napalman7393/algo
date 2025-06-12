import pygame

pygame.init()

# Configuració de la pantalla

amplada_pantalla = 800
altura_pantalla = 600
pantalla = pygame.display.set_mode((amplada_pantalla, altura_pantalla))
pygame.display.set_caption("Minigames")

# Importació de les imatges

play_button = pygame.image.load("assets/play_button.png")

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