import pygame
pygame.init()
import random
class ReactionTimeGame:
    def __init__(self, time,):
        self.time = time


amplada_pantalla = 1270
altura_pantalla = 720
pantalla = pygame.display.set_mode((amplada_pantalla, altura_pantalla))
pygame.display.set_caption("Reaction Time Game")


#ja es la variable que indica si es el momento de clicar o no
Ja = False
joc = ReactionTimeGame(time=random.randint(1, 30))
pygame.time.get_ticks()
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