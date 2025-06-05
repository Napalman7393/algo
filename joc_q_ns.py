import pygame
import random
import sys

# Inicialització
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trenca-Dianes Matemàtic")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

# Configuració joc
score = 0
lives = 3
FPS = 60

# Classe Diana
class Target:
    def __init__(self, x, y, value, correct):
        self.rect = pygame.Rect(x, y, 80, 80)
        self.value = value
        self.correct = correct
        self.color = GREEN if correct else RED
        self.speed = random.randint(1, 3)

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)
        text = font.render(str(self.value), True, BLACK)
        screen.blit(text, (self.rect.x + 20, self.rect.y + 20))

    def move(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = -80

# Generar operació i dianes
def generate_question():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    answer = a + b
    question = f"{a} + {b} = ?"

    correct_index = random.randint(0, 3)
    targets = []
    for i in range(4):
        if i == correct_index:
            value = answer
            correct = True
        else:
            value = random.randint(answer - 5, answer + 5)
            while value == answer:
                value = random.randint(answer - 5, answer + 5)
            correct = False
        targets.append(Target(150 + i * 150, random.randint(50, 200), value, correct))
    return question, targets

# Joc principal
question, targets = generate_question()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for target in targets:
                if target.rect.collidepoint(event.pos):
                    if target.correct:
                        score += 1
                        question, targets = generate_question()
                    else:
                        lives -= 1
                        if lives <= 0:
                            running = False

    for target in targets:
        target.move()
        target.draw()

    # Dibuixa puntuació i vides
    score_text = font.render(f"Punts: {score}", True, BLACK)
    lives_text = font.render(f"Vides: {lives}", True, BLACK)
    question_text = font.render(question, True, BLUE)

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 60))
    screen.blit(question_text, (WIDTH//2 - 100, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
