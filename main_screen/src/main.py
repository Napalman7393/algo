import pygame
import random
import math
import requests
import json

pygame.init()

# Constants de pantalla
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Col·lecció de Mini-Jocs")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 220, 50) # El verd important per al joc de reacció
BLUE = (50, 50, 220)
YELLOW = (255, 230, 50)
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0) # Per la llum quan no és verda

# Fonts del joc
font_title = pygame.font.SysFont(None, 64)
font_info = pygame.font.SysFont(None, 32)
font_menu_button = pygame.font.SysFont(None, 40)
font_reacció_gran = pygame.font.SysFont(None, 80) # Nova font per temps de reacció

# Configuració del joc
clock = pygame.time.Clock()
FPS = 60

# --- Càrrega d'Imatges Globals (Només les necessàries per al joc de dianes) ---
try:
    TARGET_IDLE_IMAGE_1 = pygame.image.load("main_screen/images/Dianes/Diana1.png").convert_alpha()
    TARGET_IDLE_IMAGE_2 = pygame.image.load("main_screen/images/Dianes/Diana2.png").convert_alpha() 
    
    TARGET_HIT_IMAGE_1 = pygame.image.load("main_screen/images/Dianes/Diana_Trencada.png").convert_alpha()
    TARGET_HIT_IMAGE_2 = pygame.image.load("main_screen/images/Dianes/Diana2_Trencada.png").convert_alpha() 

except pygame.error as e:
    print(f"ERROR: No s'han pogut carregar totes les imatges necessàries per al Joc de Dianes. Assegura't que els fitxers existeixen i les rutes són correctes:")
    print(f"  - main_screen/images/Dianes/Diana1.png")
    print(f"  - main_screen/images/Dianes/Diana2.png")
    print(f"  - main_screen/images/Dianes/Diana_Trencada.png")
    print(f"  - main_screen/images/Dianes/Diana2_Trencada.png")
    print(f"Detall de l'error: {e}")
    pygame.quit()
    exit()

# --- Configuració de les Dianes (per al Joc de Dianes) ---
DIANA_NORMAL_1 = {   
    "name": "Normal1",
    "idle_image": TARGET_IDLE_IMAGE_1,
    "hit_image": TARGET_HIT_IMAGE_1,
    "base_radius": (40, 50),
    "base_speed_factor": 1,
    "points": 10,
}
DIANA_NORMAL_2 = {   
    "name": "Normal2",
    "idle_image": TARGET_IDLE_IMAGE_2,
    "hit_image": TARGET_HIT_IMAGE_2,
    "base_radius": (30, 40),
    "base_speed_factor": 1.5,
    "points": 30,
}

# --- Configuració dels Modes de Joc (Els dos Jocs) ---
GAME_MODES = {
    "dianes_classiques": {
        "name": "Joc de Dianes",
        "game_class": "JocDianes",
        "allowed_diana_types": [DIANA_NORMAL_1, DIANA_NORMAL_2],
    },
    "reaccio_llum": {
        "name": "Joc de Reacció a la Llum",
        "game_class": "JocReaccioLlum",
    }
}

# --- Configuració del Servidor per al Progrés del Joc ---
SERVER_URL = "https://fun.codelearn.cat/hackathon/game/store_progress"
GAME_ID = 76 # L'identificador únic del teu joc

# --- Classes dels Jocs ---

class Diana:
    """Representa una diana al joc de dianes."""
    def __init__(self, x, y, speed, diana_type_config):
        self.x = x
        self.y = y
        self.speed = speed
        self.active = True
        self.hit_animation_counter = 0

        self.radius = random.randint(diana_type_config["base_radius"][0], diana_type_config["base_radius"][1])
        self.points_value = diana_type_config["points"]
        
        self.image = pygame.transform.scale(diana_type_config["idle_image"], (self.radius * 2, self.radius * 2))
        self.hit_image = pygame.transform.scale(diana_type_config["hit_image"], (self.radius * 2, self.radius * 2))

    def draw(self, surface):
        """Dibuixa la diana a la superfície especificada."""
        if not self.active:
            return

        if self.hit_animation_counter > 0:
            current_hit_image = self.hit_image.copy()
            alpha = int(255 * (self.hit_animation_counter / 15))
            current_hit_image.set_alpha(alpha) 
            image_rect = current_hit_image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(current_hit_image, image_rect)
            
            self.hit_animation_counter -= 1
            if self.hit_animation_counter == 0:
                self.active = False 
        else:
            image_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.image, image_rect)

    def update(self):
        """Actualitza la posició de la diana."""
        self.x += self.speed
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.speed = -self.speed

    def colisiona(self, pos):
        """Comprova si una posició (clic) col·lisiona amb la diana."""
        if not self.active:
            return False
        dx = self.x - pos[0]
        dy = self.y - pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        return dist <= self.radius

    def colpejar(self):
        """Activa l'animació de colpeig de la diana i retorna els punts que atorga."""
        self.hit_animation_counter = 15
        return self.points_value


class JocDianes:
    """Gestiona la lògica principal del joc de dianes."""
    def __init__(self, screen_ref, game_mode_config):
        self.screen = screen_ref
        self.game_mode = game_mode_config # Rep la configuració del mode (diana_classiques)
        self.nivell = 1
        self.score = 0
        self.dianes = []
        self.temps_limit = 30_000 # 30 segons per nivell
        self.inici_nivell = pygame.time.get_ticks()
        self.crear_nivell()

    def crear_nivell(self):
        """Crea les dianes per al nivell actual."""
        self.dianes.clear()
        num_dianes = min(3 + self.nivell, 10)
        
        allowed_dianas_for_spawn = self.game_mode["allowed_diana_types"]
        
        for _ in range(num_dianes):
            diana_config = random.choice(allowed_dianas_for_spawn)
            
            base_speed = random.choice([-3, -2, 2, 3])
            speed = base_speed * (1 + self.nivell * 0.2) * diana_config["base_speed_factor"] 

            x = random.randint(50, WIDTH - 50)
            y = random.randint(100, HEIGHT - 50)
            diana = Diana(x, y, speed, diana_config)
            self.dianes.append(diana)
        
        random.shuffle(self.dianes) 
        self.inici_nivell = pygame.time.get_ticks()

    def actualitzar(self):
        """Actualitza l'estat de totes les dianes."""
        for diana in self.dianes:
            diana.update()

    def dibuixar(self):
        """Dibuixa tots els elements del joc a la pantalla."""
        self.screen.fill(GRAY)
        for diana in self.dianes:
            diana.draw(self.screen)

        temps_passat = pygame.time.get_ticks() - self.inici_nivell
        temps_rest = max(0, self.temps_limit - temps_passat)
        
        segons = temps_rest // 1000
        decimes = (temps_rest % 1000) // 100
        
        dibuixar_text(f"Nivell: {self.nivell}", font_info, BLACK, 20, 10, self.screen)
        dibuixar_text(f"Punts: {self.score}", font_info, BLACK, 20, 40, self.screen)
        dibuixar_text(f"Temps: {segons}.{decimes}s", font_info, BLACK, WIDTH - 160, 10, self.screen)
        dibuixar_text(f"Joc: {self.game_mode['name']}", font_info, BLACK, WIDTH//2 - 70, 10, self.screen)


    def clicar(self, pos):
        """Gestiona el clic del ratolí: colpeja dianes i actualitza la puntuació."""
        hit = False
        for diana in self.dianes:
            if diana.colisiona(pos) and diana.active:
                points_gained = diana.colpejar() 
                self.score += points_gained
                hit = True
                break
        
        if not hit:
            self.score = max(0, self.score - 3)
        return hit

    def nivell_complet(self):
        """Comprova si totes les dianes del nivell actual han estat colpejades."""
        return all(not diana.active for diana in self.dianes)

    def temps_acabat(self):
        """Comprova si el temps límit del nivell s'ha esgotat."""
        return pygame.time.get_ticks() - self.inici_nivell >= self.temps_limit


class JocReaccioLlum:
    """Gestiona la lògica principal del joc de reacció a la llum."""
    def __init__(self, screen_ref, game_mode_config):
        self.screen = screen_ref
        self.game_mode = game_mode_config # Rep la configuració del mode (reaccio_llum)
        self.score = 0
        self.num_rondes = 5 # Nombre de rondes per joc
        self.ronda_actual = 0
        self.temps_total_reaccio = 0 # Per calcular la mitjana
        self.ultim_temps_reaccio = 0 # El temps de la darrera reacció

        self.circle_color = ORANGE # Color inicial del cercle
        self.light_on_time = 0      # Moment en què la llum es posa verda
        self.waiting_for_click = False # Estem esperant que es posi verda i cliqui
        self.last_state_change = pygame.time.get_ticks() # Per controlar els intervals d'espera

        self.estat_joc = "espera_llum" # "espera_llum", "llum_verda", "resultat_ronda"
        self.missatge_ronda = ""

        self.reset_ronda() # Inicialitza la primera ronda

    def reset_ronda(self):
        """Reseteja l'estat per a una nova ronda."""
        self.ronda_actual += 1
        if self.ronda_actual > self.num_rondes:
            self.estat_joc = "joc_acabat"
            return

        self.circle_color = ORANGE
        self.light_on_time = 0
        self.waiting_for_click = False
        self.last_state_change = pygame.time.get_ticks()
        self.estat_joc = "espera_llum"
        self.missatge_ronda = f"Ronda {self.ronda_actual}/{self.num_rondes}"

    def actualitzar(self):
        """Actualitza l'estat del joc de reacció."""
        current_time = pygame.time.get_ticks()

        if self.estat_joc == "espera_llum":
            # Espera un temps aleatori abans de posar la llum verda
            if current_time - self.last_state_change > random.randint(1500, 3500): # Espera entre 1.5 i 3.5 segons
                self.circle_color = GREEN
                self.light_on_time = current_time
                self.waiting_for_click = True
                self.estat_joc = "llum_verda"
                self.missatge_ronda = "CLICA!"
        
        elif self.estat_joc == "llum_verda":
            # Si el jugador no clica a temps (exemple: 2 segons de límit per reacció)
            if current_time - self.light_on_time > 2000: # 2 segons de límit per reaccionar
                self.score = max(0, self.score - 20) # Penalització per reacció lenta
                self.missatge_ronda = "Massa lent! -20 punts"
                self.estat_joc = "resultat_ronda"
                self.last_state_change = current_time # Temps per mostrar missatge
        
        elif self.estat_joc == "resultat_ronda":
            # Espera un moment abans de la següent ronda
            if current_time - self.last_state_change > 1500: # Espera 1.5 segons
                self.reset_ronda()

    def dibuixar(self):
        """Dibuixa els elements del joc de reacció a la pantalla."""
        self.screen.fill(BLACK) # Fons negre per al joc de reacció

        # Dibuixa el cercle al centre
        pygame.draw.circle(self.screen, self.circle_color, (WIDTH // 2, HEIGHT // 2), 100)

        dibuixar_text(f"Punts: {self.score}", font_info, WHITE, 20, 10, self.screen)
        dibuixar_text(f"Joc: {self.game_mode['name']}", font_info, WHITE, WIDTH//2 - 100, 10, self.screen)
        dibuixar_text(f"Ronda: {self.ronda_actual}/{self.num_rondes}", font_info, WHITE, WIDTH - 180, 10, self.screen)

        # Missatge de la ronda actual
        text_ronda_surf = font_reacció_gran.render(self.missatge_ronda, True, WHITE)
        text_ronda_rect = text_ronda_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        self.screen.blit(text_ronda_surf, text_ronda_rect)

        # Mostrar l'últim temps de reacció
        if self.ultim_temps_reaccio > 0 and self.estat_joc != "espera_llum": # Només el mostra si hi ha hagut una reacció i no estem esperant
            dibuixar_text(f"Reacció: {self.ultim_temps_reaccio}ms", font_info, YELLOW, WIDTH//2 - 100, HEIGHT - 50, self.screen)

    def clicar(self, pos):
        """Gestiona el clic del ratolí en el joc de reacció."""
        current_time = pygame.time.get_ticks()

        if self.estat_joc == "llum_verda" and self.waiting_for_click:
            if self.circle_color == GREEN: # Clic correcte
                reaction_time = current_time - self.light_on_time
                self.ultim_temps_reaccio = reaction_time
                self.temps_total_reaccio += reaction_time
                
                # Punts inversament proporcionals al temps de reacció
                points = max(1, 200 - reaction_time // 5) # Més ràpid = més punts (max 200)
                self.score += points
                self.missatge_ronda = f"Ben fet! {reaction_time}ms +{points} punts!"
                self.waiting_for_click = False
                self.estat_joc = "resultat_ronda"
                self.last_state_change = current_time
            else: # Clic incorrecte (llum no verda)
                self.score = max(0, self.score - 50) # Penalització gran
                self.missatge_ronda = "CLIC INCORRECTE! -50 punts!"
                self.estat_joc = "resultat_ronda" # Passa al resultat per esperar
                self.last_state_change = current_time
        elif self.estat_joc == "espera_llum": # Clic massa aviat
            self.score = max(0, self.score - 30) # Penalització per clic anticipat
            self.missatge_ronda = "Massa aviat! -30 punts!"
            self.estat_joc = "resultat_ronda"
            self.last_state_change = current_time
        
        # Ignora clics durant "resultat_ronda" o "joc_acabat"

    def joc_acabat(self):
        """Retorna True si totes les rondes s'han completat."""
        return self.estat_joc == "joc_acabat"

    def get_final_score(self):
        """Retorna la puntuació final i la mitjana de temps de reacció."""
        avg_reaction = 0
        if self.ronda_actual > 1: # Si hi ha hagut almenys una ronda de reacció
             avg_reaction = self.temps_total_reaccio / (self.ronda_actual - 1)
        
        return {
            "score": self.score,
            "avg_reaction_time": int(avg_reaction)
        }


# --- Funcions Auxiliars de Dibuix ---

def dibuixar_text(text, font, color, x, y, surface):
    """Funció genèrica per dibuixar text a una superfície."""
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

def dibuixar_boto(text, font, color_text, color_fons, x, y, amplada, altura, surface):
    """Dibuixa un botó rectangular amb text i retorna el seu rectangle."""
    rect = pygame.Rect(x, y, amplada, altura)
    pygame.draw.rect(surface, color_fons, rect, border_radius=10) 
    text_surf = font.render(text, True, color_text)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)
    return rect


def pantalla_menu(surface):
    """Mostra el menú principal del joc."""
    surface.fill(GRAY) 
    
    text_width, _ = font_title.size("Selecciona el Joc")
    dibuixar_text("Selecciona el Joc", font_title, BLACK, WIDTH//2 - text_width//2, HEIGHT//2 - 150, surface)

    boto_dianes_rect = dibuixar_boto(
        GAME_MODES["dianes_classiques"]["name"], font_menu_button, WHITE, BLUE, 
        WIDTH//2 - 150, HEIGHT//2 - 30, 300, 70, surface
    )

    boto_reaccio_rect = dibuixar_boto(
        GAME_MODES["reaccio_llum"]["name"], font_menu_button, WHITE, GREEN, 
        WIDTH//2 - 175, HEIGHT//2 + 60, 350, 70, surface
    )
    
    return {"dianes_classiques": boto_dianes_rect, "reaccio_llum": boto_reaccio_rect}


def pantalla_final(score_info, surface, game_mode_name):
    """Mostra la pantalla de final de joc amb la puntuació final i detalls del joc."""
    surface.fill(WHITE)
    text_width, _ = font_title.size("Joc Acabat!")
    dibuixar_text("Joc Acabat!", font_title, BLACK, WIDTH//2 - text_width//2, HEIGHT//2 - 150, surface)
    
    # Mostrar puntuació segons el joc
    if game_mode_name == "dianes_classiques":
        text_score = f"Puntuació final: {score_info['score']}"
    elif game_mode_name == "reaccio_llum":
        text_score = f"Puntuació total: {score_info['score']}"
        if score_info['avg_reaction_time'] > 0:
            dibuixar_text(f"Temps de reacció mitjà: {score_info['avg_reaction_time']}ms", font_info, BLACK, WIDTH//2 - 200, HEIGHT//2 + 20, surface)
        else:
            dibuixar_text("No hi ha temps de reacció per mostrar.", font_info, BLACK, WIDTH//2 - 200, HEIGHT//2 + 20, surface)

    text_width_score, _ = font_info.size(text_score)
    dibuixar_text(text_score, font_info, BLACK, WIDTH//2 - text_width_score//2, HEIGHT//2 - 30, surface)
    
    dibuixar_text("Prem ESPAI per tornar al menú o ESC per sortir", font_info, BLACK, WIDTH//2 - 250, HEIGHT//2 + 90, surface)


# --- Funció per Enviar Progrés al Servidor ---
def send_progress_to_server(level, score, total_time_in_game, is_final=False, game_mode_name="unknown", extra_data=None):
    """
    Envia les dades de progrés del joc al servidor.
    Args:
        level (int): Nivell actual del joc (o ronda per al joc de reacció).
        score (int): Puntuació actual del joc.
        total_time_in_game (int): Temps total que el jugador ha estat a l'estat "jugant" (en ms).
        is_final (bool): True si és l'enviament final al final del joc.
        game_mode_name (str): Nom del mode de joc actual ("dianes_classiques", "reaccio_llum").
        extra_data (dict): Dades addicionals específiques del joc (e.g., avg_reaction_time).
    """
    game_data = {
        "level": level,
        "score": score,
        "time_in_game_ms": total_time_in_game,
        "is_final": is_final,
        "game_mode": game_mode_name
    }
    if extra_data:
        game_data.update(extra_data) # Afegeix dades addicionals si existeixen
    
    payload = {
        "game_id": GAME_ID,
        "data": json.dumps(game_data)
    }
    
    print("\n--- Iniciant enviament de dades de progrés al servidor ---")
    print(f"  URL: {SERVER_URL}")
    print(f"  Payload complet (tal com s'envia, format JSON):")
    print(json.dumps(payload, indent=2)) 
    
    print(f"  Contingut del camp 'data' (JSON intern sense escapar):")
    print(json.dumps(game_data, indent=2)) 
    print("-----------------------------------------------------")

    try:
        response = requests.post(SERVER_URL, json=payload, timeout=5)
        response.raise_for_status() 
        print(f"Progrés enviat amb èxit! Codi de resposta: {response.status_code}")
        
        if response.content:
            try:
                server_response_json = response.json()
                print(f"  Resposta JSON completa del servidor:")
                print(json.dumps(server_response_json, indent=2)) 
                
                if 'data' in server_response_json and isinstance(server_response_json['data'], str):
                    inner_data = json.loads(server_response_json['data'])
                    print(f"  Contingut del camp 'data' de la resposta (desempaquetat per tu):")
                    print(json.dumps(inner_data, indent=2))
                else:
                    print("  El camp 'data' no és una cadena o no existeix a la resposta del servidor.")

            except json.JSONDecodeError:
                print(f"  La resposta del servidor no és un JSON vàlid: {response.text}")
        else:
            print("  Resposta buida del servidor.")

    except requests.exceptions.RequestException as e:
        print(f"Error en enviar progrés: {e}")
    print("--- Finalitzat enviament de dades ---")


# --- Bucle Principal del Joc ---

estat = "menu" 
joc_actual = None # Variable per guardar l'objecte del joc que s'està executant
final_score_info = {"score": 0} # Diccionari per guardar la info de la puntuació final (inclou avg_reaction)
current_game_mode_name = "unknown" 

last_progress_send_time = pygame.time.get_ticks() 
next_send_interval = random.randint(5, 30) * 1000 
total_time_in_game = 0 

running = True 
while running:
    current_time = pygame.time.get_ticks() 

    # --- Gestió d'Esdeveniments ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        if estat == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if "menu_buttons" in locals(): 
                    if menu_buttons["dianes_classiques"].collidepoint(mouse_pos):
                        current_game_mode_name = "dianes_classiques"
                        joc_actual = JocDianes(screen, GAME_MODES[current_game_mode_name]) 
                        estat = "jugant" 
                        last_progress_send_time = current_time 
                        total_time_in_game = 0
                        next_send_interval = random.randint(5, 30) * 1000 
                    elif menu_buttons["reaccio_llum"].collidepoint(mouse_pos):
                        current_game_mode_name = "reaccio_llum"
                        joc_actual = JocReaccioLlum(screen, GAME_MODES[current_game_mode_name]) 
                        estat = "jugant" 
                        last_progress_send_time = current_time 
                        total_time_in_game = 0
                        next_send_interval = random.randint(5, 30) * 1000 

        elif estat == "jugant":
            if event.type == pygame.MOUSEBUTTONDOWN:
                clic_pos = pygame.mouse.get_pos()
                if joc_actual: # Assegura't que hi ha un joc actiu
                    joc_actual.clicar(clic_pos)

        elif estat == "final":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False 
                elif event.key == pygame.K_SPACE: 
                    estat = "menu"
                    joc_actual = None 
                    final_score_info = {"score": 0}
                    current_game_mode_name = "unknown"
                    last_progress_send_time = pygame.time.get_ticks() 
                    total_time_in_game = 0
                    next_send_interval = random.randint(5, 30) * 1000 


    # --- Actualització i Dibuix del Joc segons l'Estat ---
    if estat == "menu":
        menu_buttons = pantalla_menu(screen) 
    
    elif estat == "jugant":
        if joc_actual:
            joc_actual.actualitzar()
            joc_actual.dibuixar()

            total_time_in_game += clock.get_time() 

            # Envia progrés al servidor (ara depèn del tipus de joc)
            if current_time - last_progress_send_time >= next_send_interval:
                current_level = 0
                current_score = 0
                extra_server_data = None

                if current_game_mode_name == "dianes_classiques":
                    current_level = joc_actual.nivell
                    current_score = joc_actual.score
                elif current_game_mode_name == "reaccio_llum":
                    current_level = joc_actual.ronda_actual
                    current_score = joc_actual.score
                    # Envia la mitjana de reacció en els enviaments de progrés intermedis si ja hi ha hagut reaccions
                    if joc_actual.ronda_actual > 1:
                        extra_server_data = {"avg_reaction_time": int(joc_actual.temps_total_reaccio / (joc_actual.ronda_actual -1))}

                send_progress_to_server(current_level, current_score, total_time_in_game, is_final=False, 
                                        game_mode_name=current_game_mode_name, extra_data=extra_server_data)
                last_progress_send_time = current_time
                next_send_interval = random.randint(5, 30) * 1000 
            
            # Comprova si el joc actual ha acabat
            if (current_game_mode_name == "dianes_classiques" and joc_actual.temps_acabat()) or \
               (current_game_mode_name == "reaccio_llum" and joc_actual.joc_acabat()):
                
                estat = "final"
                
                if current_game_mode_name == "dianes_classiques":
                    final_score_info["score"] = joc_actual.score 
                    send_progress_to_server(joc_actual.nivell, joc_actual.score, total_time_in_game, is_final=True, 
                                            game_mode_name=current_game_mode_name)
                elif current_game_mode_name == "reaccio_llum":
                    final_data = joc_actual.get_final_score()
                    final_score_info["score"] = final_data["score"]
                    final_score_info["avg_reaction_time"] = final_data["avg_reaction_time"]
                    send_progress_to_server(joc_actual.ronda_actual, final_data["score"], total_time_in_game, is_final=True, 
                                            game_mode_name=current_game_mode_name, extra_data={"avg_reaction_time": final_data["avg_reaction_time"]})

    elif estat == "final":
        pantalla_final(final_score_info, screen, current_game_mode_name)

    # --- Actualització de Pantalla i Control de FPS ---
    pygame.display.flip() 
    clock.tick(FPS) 

pygame.quit()