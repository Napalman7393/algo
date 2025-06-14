import pygame
import random
import math
import requests
import json

pygame.init()

# Constants de pantalla
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joc de Trencar Dianes")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 50, 220)
YELLOW = (255, 230, 50)
GRAY = (200, 200, 200)

# Fonts del joc
font_title = pygame.font.SysFont(None, 64)
font_info = pygame.font.SysFont(None, 32)
font_score = pygame.font.SysFont(None, 28)

# Configuració del joc
clock = pygame.time.Clock()
FPS = 60

# --- Càrrega d'Imatges Globals ---
try:
    TARGET_IDLE_IMAGE_1 = pygame.image.load("main_screen/images/Dianes/Diana1.png").convert_alpha()
    TARGET_IDLE_IMAGE_2 = pygame.image.load("main_screen/images/Dianes/Diana2.png").convert_alpha() 
    
    TARGET_HIT_IMAGE_1 = pygame.image.load("main_screen/images/Dianes/Diana_Trencada.png").convert_alpha()
    TARGET_HIT_IMAGE_2 = pygame.image.load("main_screen/images/Dianes/Diana2_Trencada.png").convert_alpha() 

except pygame.error as e:
    print(f"Error carregant imatge: {e}")
    print("Assegura't que les rutes de les imatges:")
    print("- main_screen/images/Dianes/Diana1.png")
    print("- main_screen/images/Dianes/Diana2.png")
    print("- main_screen/images/Dianes/Diana_Trencada.png")
    print("- main_screen/images/Dianes/Diana2_Trencada.png")
    print("existeixen i són correctes.")
    pygame.quit()
    exit()

# --- Configuració de les Dianes ---
# Definició de les propietats per a cada tipus de diana
DIANA_TYPES = [
    {   # Diana 1 (més fàcil, menys punts)
        "idle_image": TARGET_IDLE_IMAGE_1,
        "hit_image": TARGET_HIT_IMAGE_1,
        "base_radius": (40, 50),  # Rang de radi (min, max)
        "base_speed_factor": 1,   # Factor per a la velocitat base
        "points": 10              # Punts que atorga
    },
    {   # Diana 2 (més difícil, més punts)
        "idle_image": TARGET_IDLE_IMAGE_2,
        "hit_image": TARGET_HIT_IMAGE_2,
        "base_radius": (30, 40),  # Radi més petit, més difícil de tocar
        "base_speed_factor": 1.5, # Més ràpida
        "points": 30              # Més punts!
    }
]


# --- Configuració del Servidor per al Progrés del Joc ---
SERVER_URL = "https://fun.codelearn.cat/hackathon/game/store_progress"
GAME_ID = 76 # L'identificador únic del teu joc

# --- Classes del Joc ---

class Diana:
    """Representa una diana al joc."""
    def __init__(self, x, y, speed, diana_type_config):
        self.x = x
        self.y = y
        self.speed = speed
        self.active = True
        self.hit_animation_counter = 0

        # Assignar propietats de la diana segons la configuració rebuda
        self.radius = random.randint(diana_type_config["base_radius"][0], diana_type_config["base_radius"][1])
        self.points_value = diana_type_config["points"]

        # Escalar les imatges segons el radi escollit
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
        return self.points_value # Retorna els punts específics d'aquesta diana


class JocDianes:
    """Gestiona la lògica principal del joc."""
    def __init__(self, screen_ref):
        self.screen = screen_ref
        self.nivell = 1
        self.score = 0
        self.dianes = []
        self.temps_limit = 30_000
        self.inici_nivell = pygame.time.get_ticks()
        self.crear_nivell()

    def crear_nivell(self):
        """Crea les dianes per al nivell actual."""
        self.dianes.clear()
        num_dianes = min(3 + self.nivell, 10)
        for _ in range(num_dianes):
            # Escollim un tipus de diana aleatori de la nostra llista de configuracions
            diana_config = random.choice(DIANA_TYPES)
            
            # Calculem el radi i la velocitat base segons la configuració escollida i el nivell
            # El radi s'estableix dins de la classe Diana a partir de base_radius
            
            base_speed = random.choice([-3, -2, 2, 3])
            # La velocitat global del nivell i el factor de velocitat de la diana
            speed = base_speed * (1 + self.nivell * 0.2) * diana_config["base_speed_factor"] 

            x = random.randint(50, WIDTH - 50) # Coordenada X inicial
            y = random.randint(100, HEIGHT - 50) # Coordenada Y inicial

            diana = Diana(x, y, speed, diana_config) # Passem la configuració a la diana
            self.dianes.append(diana)
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

    def clicar(self, pos):
        """Gestiona el clic del ratolí: colpeja dianes i actualitza la puntuació."""
        hit = False
        for diana in self.dianes:
            if diana.colisiona(pos) and diana.active:
                points_gained = diana.colpejar() # La diana retorna els punts
                self.score += points_gained # Suma els punts específics de la diana
                hit = True
                break # Important: sortir del bucle un cop colpejada una diana
        
        if not hit: # Si no s'ha colpejat cap diana
            self.score = max(0, self.score - 3) # Penalització per fallar
        return hit

    def nivell_complet(self):
        """Comprova si totes les dianes del nivell actual han estat colpejades."""
        return all(not diana.active for diana in self.dianes)

    def temps_acabat(self):
        """Comprova si el temps límit del nivell s'ha esgotat."""
        return pygame.time.get_ticks() - self.inici_nivell >= self.temps_limit


# --- Funcions Auxiliars de Dibuix ---

def dibuixar_text(text, font, color, x, y, surface):
    """Funció genèrica per dibuixar text a una superfície."""
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def pantalla_inici(surface):
    """Mostra la pantalla d'inici del joc."""
    surface.fill(WHITE)
    text_width, _ = font_title.size("Joc de Trencar Dianes")
    dibuixar_text("Joc de Trencar Dianes", font_title, BLACK, WIDTH//2 - text_width//2, HEIGHT//2 - 100, surface)
    
    text_width, _ = font_info.size("Fes clic per començar")
    dibuixar_text("Fes clic per començar", font_info, BLACK, WIDTH//2 - text_width//2, HEIGHT//2, surface)

def pantalla_final(score, surface):
    """Mostra la pantalla de final de joc amb la puntuació final."""
    surface.fill(WHITE)
    text_width, _ = font_title.size("Final del joc!")
    dibuixar_text("Final del joc!", font_title, BLACK, WIDTH//2 - text_width//2, HEIGHT//2 - 100, surface)
    
    text_width, _ = font_info.size(f"Puntuació final: {score}")
    dibuixar_text(f"Puntuació final: {score}", font_info, BLACK, WIDTH//2 - text_width//2, HEIGHT//2, surface)
    
    text_width, _ = font_info.size("Prem ESC per sortir")
    dibuixar_text("Prem ESC per sortir", font_info, BLACK, WIDTH//2 - text_width//2, HEIGHT//2 + 40, surface)


# --- Funció per Enviar Progrés al Servidor ---
def send_progress_to_server(level, score, total_time_in_game, is_final=False):
    """
    Envia les dades de progrés del joc al servidor.
    Args:
        level (int): Nivell actual del joc.
        score (int): Puntuació actual del joc.
        total_time_in_game (int): Temps total que el jugador ha estat a l'estat "jugant" (en ms).
        is_final (bool): True si és l'enviament final al final del joc.
    """
    game_data = {
        "level": level,
        "score": score,
        "time_in_game_ms": total_time_in_game,
        "is_final": is_final
    }
    
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

estat = "inici"
joc = None 
final_score_to_display = 0 

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

        if estat == "inici":
            if event.type == pygame.MOUSEBUTTONDOWN:
                joc = JocDianes(screen) 
                estat = "jugant" 
                last_progress_send_time = current_time 
                total_time_in_game = 0
                next_send_interval = random.randint(5, 30) * 1000 

        elif estat == "jugant":
            if event.type == pygame.MOUSEBUTTONDOWN:
                clic_pos = pygame.mouse.get_pos()
                joc.clicar(clic_pos)

        elif estat == "final":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False 

    # --- Actualització i Dibuix del Joc segons l'Estat ---
    if estat == "inici":
        pantalla_inici(screen)

    elif estat == "jugant":
        joc.actualitzar()
        joc.dibuixar()

        total_time_in_game += clock.get_time() 

        # Comprova si és el moment d'enviar el progrés regularment
        if current_time - last_progress_send_time >= next_send_interval:
            send_progress_to_server(joc.nivell, joc.score, total_time_in_game, is_final=False)
            last_progress_send_time = current_time
            next_send_interval = random.randint(5, 30) * 1000 

        # Comprova si el nivell s'ha completat
        if joc.nivell_complet():
            joc.nivell += 1
            joc.crear_nivell() 

        # Comprova si el temps del nivell s'ha acabat (Fi del joc)
        if joc.temps_acabat():
            estat = "final"
            final_score_to_display = joc.score 
            send_progress_to_server(joc.nivell, joc.score, total_time_in_game, is_final=True)

    elif estat == "final":
        pantalla_final(final_score_to_display, screen)

    # --- Actualització de Pantalla i Control de FPS ---
    pygame.display.flip() 
    clock.tick(FPS) 

pygame.quit()