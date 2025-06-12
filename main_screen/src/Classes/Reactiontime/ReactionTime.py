import pygame
import random

class ReactionTimeGame:
    def __init__(self):
        self.time = random.randint(1, 5) * 1000
        self.amplada_pantalla = 1270
        self.altura_pantalla = 720
        self.pantalla = pygame.display.set_mode((self.amplada_pantalla, self.altura_pantalla))
        pygame.display.set_caption("Reaction Time Game")
        self.fish = pygame.image.load("main_screen/images/Fish.png")
        self.ja = False

    def run(self):
        runin = True
        while runin:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runin = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.ja = True

            if not self.ja:
                self.pantalla.fill("Red")
            else:
                self.pantalla.fill("Green")

            pygame.display.update()
        pygame.quit()

# Ara pots utilitzar la classe dins de main:
if __name__ == "__main__":
    joc = ReactionTimeGame()
    joc.run()