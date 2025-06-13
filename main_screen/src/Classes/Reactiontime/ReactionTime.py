import pygame
import random

class ReactionTimeGame:
    def __init__(self):
        self.amplada_pantalla = 1270
        self.altura_pantalla = 720
        self.pantalla = pygame.display.set_mode((self.amplada_pantalla, self.altura_pantalla))
        pygame.display.set_caption("Reaction Time Game")
        self.fish = pygame.image.load("main_screen/images/Fish.png")
        self.ja = False
        self.temps_espera = random.randint(1, 5) * 1000
        self.inici = pygame.time.get_ticks()
        self.score = None

    def run(self):
        runin = True
        while runin:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runin = False
                if self.ja and event.type == pygame.MOUSEBUTTONDOWN:
                    self.score = pygame.time.get_ticks() - (self.inici + self.temps_espera)
                    self.font = pygame.font.SysFont(None, 74)
                    self.score_text = self.font.render(f"Temps de reacció: {self.score} ms", True, (255, 255, 255))
                    print(f"Temps de reacció: {self.score} ms")
                    

            temps_actual = pygame.time.get_ticks()
            if not self.ja and temps_actual - self.inici >= self.temps_espera:
                self.ja = True

            if not self.ja:
                self.pantalla.fill("Red")
            else:
                self.pantalla.fill("Green")

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    joc = ReactionTimeGame()
    joc.run()