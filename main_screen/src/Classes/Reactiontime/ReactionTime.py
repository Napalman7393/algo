import pygame
pygame.init()
import random
class ReactionTimeGame:
    def __init__(self,):
        self.time = random.randint(1, 5) * 1000 


    amplada_pantalla = 1270
    altura_pantalla = 720
    pantalla = pygame.display.set_mode((amplada_pantalla, altura_pantalla))
    pygame.display.set_caption("Reaction Time Game")
    fish = pygame.image.load("main_screen/images/Fish.png")

    #ja es la variable que indica si es el momento de clicar o no
    Ja = False
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