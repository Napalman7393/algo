import pygame

pygame.init()


amplada_pantalla = 800
altura_pantalla = 600
pantalla = pygame.display.set_mode(amplada_pantalla, altura_pantalla)
pygame.display.set_caption("Minigames")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pantalla.fill("blue")

    
    pygame.display.update()
    clock.tick(60)

pygame.quit()