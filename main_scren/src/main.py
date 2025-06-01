import pygame


pygame.init()

#pantalla

amp_pantalla = 1280
alt_pantalla = 720
pantalla = pygame.display.set_mode((amp_pantalla, alt_pantalla))
pygame.display.set_caption("Projecte Hackton")

fish = pygame.image.load("main_scren/images/Fish.png")
fish_rect = fish.get_rect() 
pene = 640





#main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#objectes
    pantalla.fill("chartreuse2")
    pene -= 1
    pantalla.blit(fish, fish_rect)
    fish_rect.center = (pene, alt_pantalla // 2)
    
    


    pygame.display.update()


pygame.quit()