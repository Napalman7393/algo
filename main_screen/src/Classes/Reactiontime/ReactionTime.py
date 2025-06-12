import pygame
pygame.init()
import random
class ReactionTimeGame:
    def __init__(self, time, dificulty):
        self.dificulty = dificulty
        self.time = time


amplada_pantalla = 1270
altura_pantalla = 720
pantalla = pygame.display.set_mode((amplada_pantalla, altura_pantalla))
pygame.display.set_caption("Reaction Time Game")

Ja = False

runin = True
while runin:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runin = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            Ja  = True

    if not Ja:
        pantalla.fill("Red")
    else:
        pantalla.fill("Green")


    



    pygame.display.update()


pygame.quit()