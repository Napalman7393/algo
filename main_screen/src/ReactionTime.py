import pygame
import random

class ReactionTimeGame:
    def __init__(self,):

        self.amplada_pantalla = 1270
        self.altura_pantalla = 720
        self.pantalla = pygame.display.set_mode((self.amplada_pantalla, self.altura_pantalla))
        pygame.display.set_caption("Reaction Time Game")

       
        self.ja = False
        self.temps_espera = random.randint(1, 5) * 1000
        self.inici = pygame.time.get_ticks()
        self.score = None
        self.panSco = False
        self.font = pygame.font.SysFont(None, 74)
        self.waitButton = pygame.image.load("Retry.ReactionTime2.png")
        # PanSco és una variable per controlar si s'ha de mostrar el text del temps de reacció a la pantalla o no.

    def run(self):
        runin = True
        while runin:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runin = False
                if self.ja and event.type == pygame.MOUSEBUTTONDOWN and not self.panSco:
                    self.score = pygame.time.get_ticks() - (self.inici + self.temps_espera)
                    self.font = pygame.font.SysFont(None, 74)
                    self.score_text = self.font.render(f"Temps de reacció: {self.score} ms", True, (0, 0, 0))
                    self.panSco = True

                if not self.ja and event.type == pygame.MOUSEBUTTONDOWN:
                    self.perFont = pygame.font.SysFont(None, 74)
                    self.perdTxt = self.font.render(f"Massa d'hora", True, (0, 0, 0))


            temps_actual = pygame.time.get_ticks()
            if not self.ja and temps_actual - self.inici >= self.temps_espera:
                self.ja = True

            if not self.ja:
                self.pantalla.fill("Red")
                self.pantalla.blit(self.waitButton, (self.amplada_pantalla // 2 - self.waitButton.get_width() // 2, self.altura_pantalla // 2 - self.waitButton.get_height() // 2))
            elif self.panSco:
                self.pantalla.fill("lightblue")
                self.pantalla.blit(self.score_text, (0, 0))
            else:
                self.pantalla.fill("Green")
                    

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    joc = ReactionTimeGame()
    joc.run()