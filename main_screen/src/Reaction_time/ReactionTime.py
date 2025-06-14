import pygame
import random

class ReactionTimeGame:
    def __init__(self, screen):
        self.screen = screen
        
        self.ja = False # Has the green signal appeared?
        self.temps_espera = random.randint(1, 5) * 1000 # Random wait time
        self.inici = pygame.time.get_ticks() # Time when the game started waiting
        self.score = None
        self.panSco = False # Is the score panel visible?
        self.font = pygame.font.SysFont(None, 74)
        self.massadora = False # Did the player click too early?

        # Load images for the game state
        self.waitButton = pygame.image.load("main_screen/src/Reaction_time/Wait_button.png")
        self.retryButton = pygame.image.load("main_screen/src/Reaction_time/Retry_ReactionTime.png")
        self.AgainButton = pygame.image.load("main_screen/src/Reaction_time/Again_Button.png")
        
        # Get rects for buttons
        # Ensure these are created after images are loaded
        self.retryButton_rect = self.retryButton.get_rect(center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))
        self.AgainButton_rect = self.AgainButton.get_rect(center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))


    def update(self, events): # Now accepts 'events' list
        """
        Updates the game state for one frame.
        Processes all events for the current frame.
        Returns True if the game is still running, False if it has finished.
        """
        game_is_running = True # Assume game continues unless specified otherwise

        for event in events: # Iterate through all events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.massadora: # If player clicked too early and sees retry
                    if self.retryButton_rect.collidepoint(mouse_pos):
                        game_is_running = False # Signal to main loop that game is done/needs reset
                elif self.panSco: # If score is displayed and player sees again button
                    if self.AgainButton_rect.collidepoint(mouse_pos):
                        game_is_running = False # Signal to main loop that game is done/needs reset
                elif self.ja and not self.panSco: # Green light and score not yet displayed
                    self.score = pygame.time.get_ticks() - (self.inici + self.temps_espera)
                    self.font = pygame.font.SysFont(None, 74) # Re-render font if needed, though usually done once
                    self.score_text = self.font.render(f"Temps de reacció: {self.score} ms", True, (0, 0, 0))
                    self.panSco = True
                elif not self.ja and not self.massadora: # Red light and player clicked too early
                    self.massadora = True # Set massadora to True to show retry
            
            # Other event handling specific to the reaction time game could go here
            # e.g., if you wanted keyboard input

        # Game logic based on time
        if not self.ja and not self.massadora and (pygame.time.get_ticks() - self.inici >= self.temps_espera):
            self.ja = True # It's time for the green light

        # Drawing logic (always draws the current state)
        if self.massadora: # Player clicked too early
            self.screen.fill("red")
            text_too_early = self.font.render("Too Early! Click Retry", True, (0, 0, 0))
            text_rect = text_too_early.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
            self.screen.blit(text_too_early, text_rect)
            self.screen.blit(self.retryButton, self.retryButton_rect)
            
        elif self.panSco: # Score is displayed
            self.screen.fill("lightblue")
            score_text_rect = self.score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
            self.screen.blit(self.score_text, score_text_rect)
            self.screen.blit(self.AgainButton, self.AgainButton_rect)
            
        elif not self.ja: # Waiting for green light (Red screen)
            self.screen.fill("red")
            self.screen.blit(self.waitButton, (self.screen.get_width() // 2 - self.waitButton.get_width() // 2, self.screen.get_height() // 2 - self.waitButton.get_height() // 2))
        else: # Green light!
            self.screen.fill("green")
            ready_text = self.font.render("CLICK!", True, (0, 0, 0))
            ready_text_rect = ready_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(ready_text, ready_text_rect)

        return game_is_running # Return whether the game should continue

# The if __name__ == "__main__": block is for testing this file independently.
# It won't be used when imported by main.py
if __name__ == "__main__":
    pygame.init()
    test_screen = pygame.display.set_mode((1200, 720))
    pygame.display.set_caption("Reaction Time Test")
    
    joc_test = ReactionTimeGame(test_screen)
    
    test_running = True
    while test_running:
        events = pygame.event.get() # Get all events for testing
        for event in events:
            if event.type == pygame.QUIT:
                test_running = False
            
        game_active_in_test = joc_test.update(events) # Pass all events to update
        if not game_active_in_test:
            # If game indicates it's finished, re-initialize for testing purposes
            joc_test = ReactionTimeGame(test_screen) 
        
        pygame.display.flip() # Use flip() instead of update() for full screen update
        
    pygame.quit()