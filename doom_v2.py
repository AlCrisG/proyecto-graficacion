import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PIL import Image
import random

# --- Configuración Inicial ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768

# --- Constantes del Juego ---
MOVE_SPEED = 0.08
ROT_SPEED = 0.04
ENEMY_SPAWN_INTERVAL = 5000 # ms (5 segundos)
MAX_ENEMIES = 10

# --- Mapa del Mundo ---
# 1 = Pared, 0 = Espacio vacío
world_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

MAP_WIDTH = len(world_map[0])
MAP_HEIGHT = len(world_map)

# --- Variables Globales del Jugador ---
player_pos = [2.5, 0.0, 2.5]  # x, y, z
player_angle = 0.0  # Ángulo de visión en el plano XZ
player_health = 100
player_radius = 0.3
score = 0
game_state = "RUNNING" # Estados posibles: RUNNING, PAUSED, GAME_OVER

# --- Sistema de Munición del Jugador ---
player_clip_ammo = 10
player_clip_size = 10
is_reloading = False
reload_duration = 2000 # ms (2 segundos)
reload_timer = 0
shoot_cooldown = 250 # ms (0.25 segundos)
last_shot_time = 0

# --- Listas de Entidades ---
enemies = []
projectiles = []

# --- Sonido ---
shot_sound = None
enemy_hit_sound = None
player_hit_sound = None
enemy_shot_sound = None
death_sound = None

# --- Recursos de Texturas y Animación ---
texture_ids = {}
enemy_attack_frames = []
reload_frames = []
weapon_animation_state = 'IDLE' # IDLE, SHOOTING, RELOADING
weapon_animation_frame = 0
weapon_animation_timer = 0
weapon_animation_speed = 60 # ms por fotograma
reload_animation_frame = 0
reload_animation_timer = 0
reload_animation_speed = 35 # ms por fotograma

# --- Clases de Entidades ---
class Enemy:
    def __init__(self, pos):
        self.pos = list(pos)
        self.health = 100
        self.alive = True
        self.size = 0.4 # Radio para colisión de disparo
        self.path_points = None
        self.path_progress = 0.0
        self.path_speed = 0.003
        self.shoot_cooldown = 2000 # ms
        self.last_shot_time = 0
        self.animation_state = 'IDLE' # IDLE, ATTACKING
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100 # ms por fotograma
        self.generate_new_path()

    def generate_new_path(self):
        """Genera una nueva curva de Bézier aleatoria para el enemigo."""
        p0 = self.pos
        
        # Elige un punto final aleatorio que no esté en una pared
        while True:
            p3_x = random.uniform(1, MAP_WIDTH - 2)
            p3_z = random.uniform(1, MAP_HEIGHT - 2)
            if world_map[int(p3_z)][int(p3_x)] == 0:
                p3 = [p3_x, 0.0, p3_z]
                break
        
        # Puntos de control aleatorios para dar forma a la curva
        p1 = vec_add(p0, [random.uniform(-5, 5), 0, random.uniform(-5, 5)])
        p2 = vec_add(p3, [random.uniform(-5, 5), 0, random.uniform(-5, 5)])

        self.path_points = [p0, p1, p2, p3]
        self.path_progress = 0.0

    def has_line_of_sight(self, target_pos):
        """Comprueba si hay una línea de visión clara hacia el jugador."""
        direction = vec_sub(target_pos, self.pos)
        distance = vec_norm(direction)
        if distance == 0: return False
        direction = vec_mul_scalar(direction, 1.0 / distance)

        steps = int(distance / 0.5) # Comprobar cada medio bloque
        for i in range(1, steps):
            check_pos = vec_add(self.pos, vec_mul_scalar(direction, i * 0.5))
            map_x = int(check_pos[0])
            map_z = int(check_pos[2])
            if world_map[map_z][map_x] == 1:
                return False # Hay una pared en el camino
        return True

    def update(self, player_pos_np):
        """Mueve al enemigo a lo largo de la curva de Bézier y comprueba colisiones."""
        if not self.alive or not self.path_points:
            return

        current_time = pygame.time.get_ticks()

        # --- Lógica de Disparo ---
        dist_to_player = vec_norm(vec_sub(player_pos_np, self.pos))

        if dist_to_player < 15 and current_time - self.last_shot_time > self.shoot_cooldown:
            if self.has_line_of_sight(player_pos_np):
                direction = vec_sub(player_pos_np, self.pos)
                direction[1] = 0 # Disparar en el plano horizontal
                direction = vec_normalize(direction)
                
                # Crear proyectil
                start_pos = vec_add(self.pos, vec_mul_scalar(direction, 0.5))
                projectiles.append(Projectile(start_pos, direction))
                
                # Reproducir sonido de disparo enemigo
                if enemy_shot_sound:
                    enemy_shot_sound.play()

                # Iniciar animación de ataque
                self.animation_state = 'ATTACKING'
                self.animation_frame = 0
                self.animation_timer = current_time

                self.last_shot_time = current_time

        # --- Lógica de Movimiento ---
        # Si el jugador está lejos, deambula. Si está cerca, se detiene para disparar.
        if dist_to_player > 8:
            if self.path_progress < 1.0:
                # Calcula la siguiente posición potencial en la curva
                next_progress = self.path_progress + self.path_speed
                potential_pos = calculate_bezier_point(min(next_progress, 1.0), *self.path_points)

                # Comprueba si la siguiente posición está dentro de una pared
                map_x = int(potential_pos[0])
                map_z = int(potential_pos[2])

                if 0 <= map_x < MAP_WIDTH and 0 <= map_z < MAP_HEIGHT and world_map[map_z][map_x] == 0:
                    # Si no hay pared, el movimiento es válido. Actualiza la posición.
                    self.path_progress = next_progress
                    self.pos = potential_pos
                else:
                    # Si choca con una pared, genera una nueva ruta inmediatamente.
                    self.generate_new_path()
            else:
                # Al llegar al final, genera una nueva ruta
                self.generate_new_path()
        
        # --- Lógica de Animación ---
        if self.animation_state == 'ATTACKING':
            if current_time - self.animation_timer > self.animation_speed:
                self.animation_frame += 1
                if self.animation_frame >= len(enemy_attack_frames):
                    self.animation_state = 'IDLE' # Terminar animación
                self.animation_timer = current_time

class Projectile:
    def __init__(self, pos, direction):
        self.pos = list(pos)
        self.dir = direction
        self.speed = 0.15
        self.alive = True
        self.radius = 0.15

# --- Funciones Vectoriales (reemplazo de numpy) ---
def vec_add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]

def vec_sub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]

def vec_mul_scalar(v, s):
    return [v[0] * s, v[1] * s, v[2] * s]

def vec_norm(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def vec_normalize(v):
    norm = vec_norm(v)
    if norm == 0:
        return [0, 0, 0]
    return [v[0] / norm, v[1] / norm, v[2] / norm]

def vec_dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

# --- Funciones de Curva ---
def calculate_bezier_point(t, p0, p1, p2, p3):
    """Calcula un punto en una curva de Bézier cúbica."""
    u = 1 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    
    p_p0 = vec_mul_scalar(p0, uuu)
    p_p1 = vec_mul_scalar(p1, 3 * uu * t)
    p_p2 = vec_mul_scalar(p2, 3 * u * tt)
    p_p3 = vec_mul_scalar(p3, ttt)
    p = vec_add(vec_add(p_p0, p_p1), vec_add(p_p2, p_p3))
    return p

# --- Funciones de Carga y Configuración ---
def load_gif_animation(filename):
    """Carga los fotogramas de un GIF y los convierte en texturas de OpenGL."""
    frames = []
    try:
        with Image.open(filename) as img:
            for frame_num in range(img.n_frames):
                img.seek(frame_num)
                frame_img = img.convert("RGBA")
                frame_data = frame_img.tobytes("raw", "RGBA", 0, -1)
                
                tex_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, tex_id)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, frame_img.width, frame_img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, frame_data)
                frames.append(tex_id)
    except FileNotFoundError:
        pass # El archivo no existe, la animación no se cargará
    return frames

def load_texture(filename):
    """Carga una imagen y la prepara como textura de OpenGL."""
    img = Image.open(filename).convert("RGBA")
    img_data = img.tobytes("raw", "RGBA", 0, -1)
    
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    
    return tex_id

def setup_opengl():
    """Configura el estado inicial de OpenGL."""
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    
    # --- Habilitar transparencia ---
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)

    # Cargar texturas
    global texture_ids, enemy_attack_frames, reload_frames
    try:
        texture_ids['wall'] = load_texture('wall.png')
        texture_ids['floor'] = load_texture('floor.png')
        texture_ids['sky'] = load_texture('sky.png')
        texture_ids['enemy'] = load_texture('enemy.png')
        
        # Cargar animación de ataque
        enemy_attack_frames = load_gif_animation('enemy_attack.gif')

        # Cargar animación de recarga
        reload_frames = load_gif_animation('reload.gif')
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el recurso esencial: {e.filename}")
        pygame.quit()
        quit()

# --- Funciones de Renderizado (Dibujo) ---
def draw_enemy(enemy):
    """Dibuja un enemigo como un sprite 2D que mira a la cámara (billboard)."""
    if not enemy.alive:
        return

    glPushMatrix()
    # Trasladar a la posición del enemigo
    glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])

    # --- Billboarding ---
    # Obtener la matriz ModelView actual (que contiene la orientación de la cámara)
    modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
    
    # La rotación de la cámara está en las primeras 3x3 filas/columnas.
    # Para que el sprite mire a la cámara, necesitamos cancelar esa rotación.
    # La transpuesta de una matriz de rotación es su inversa.
    for i in range(3):
        for j in range(3):
            if i == j:
                modelview[i][j] = 1.0
            else:
                modelview[i][j] = 0.0
    glLoadMatrixf(modelview)

    # Seleccionar la textura correcta basada en el estado de animación
    if enemy.animation_state == 'ATTACKING' and enemy_attack_frames:
        frame_id = enemy_attack_frames[min(enemy.animation_frame, len(enemy_attack_frames) - 1)]
        glBindTexture(GL_TEXTURE_2D, frame_id)
    else:
        glBindTexture(GL_TEXTURE_2D, texture_ids['enemy'])

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-0.5, -1, 0)
    glTexCoord2f(1, 0); glVertex3f(0.5, -1, 0)
    glTexCoord2f(1, 1); glVertex3f(0.5, 1, 0)
    glTexCoord2f(0, 1); glVertex3f(-0.5, 1, 0)
    glEnd()

    glPopMatrix()

def draw_projectile(projectile):
    """Dibuja un proyectil como una esfera roja."""
    if not projectile.alive:
        return
    
    glPushMatrix()
    glTranslatef(projectile.pos[0], projectile.pos[1], projectile.pos[2])
    
    glDisable(GL_TEXTURE_2D) # No queremos textura para la esfera
    glColor3f(1.0, 0.1, 0.1) # Color rojo brillante
    
    quad = gluNewQuadric()
    gluSphere(quad, projectile.radius, 8, 8) # Dibuja una esfera
    
    glEnable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 1.0) # Restaurar el color a blanco
    glPopMatrix()

def draw_map():
    """Dibuja el suelo, el techo y las paredes del mapa (geometría estática)."""
    # Dibujar suelo
    glBindTexture(GL_TEXTURE_2D, texture_ids['floor'])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(0, -1, 0)
    glTexCoord2f(MAP_WIDTH, 0); glVertex3f(MAP_WIDTH, -1, 0)
    glTexCoord2f(MAP_WIDTH, MAP_HEIGHT); glVertex3f(MAP_WIDTH, -1, MAP_HEIGHT)
    glTexCoord2f(0, MAP_HEIGHT); glVertex3f(0, -1, MAP_HEIGHT)
    glEnd()
    
    # --- Dibujar Paredes como Planos ---
    # Solo se dibujan las caras que dan a un espacio vacío (optimizacón)
    glBindTexture(GL_TEXTURE_2D, texture_ids['wall'])
    glBegin(GL_QUADS)
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            if world_map[row][col] == 1:
                # Comprobar vecino del NORTE (z-1)
                if row > 0 and world_map[row - 1][col] == 0:
                    glTexCoord2f(0, 0); glVertex3f(col, -1, row)
                    glTexCoord2f(1, 0); glVertex3f(col + 1, -1, row)
                    glTexCoord2f(1, 1); glVertex3f(col + 1, 1, row)
                    glTexCoord2f(0, 1); glVertex3f(col, 1, row)

                # Comprobar vecino del SUR (z+1)
                if row < MAP_HEIGHT - 1 and world_map[row + 1][col] == 0:
                    glTexCoord2f(0, 0); glVertex3f(col + 1, -1, row + 1)
                    glTexCoord2f(1, 0); glVertex3f(col, -1, row + 1)
                    glTexCoord2f(1, 1); glVertex3f(col, 1, row + 1)
                    glTexCoord2f(0, 1); glVertex3f(col + 1, 1, row + 1)

                # Comprobar vecino del OESTE (x-1)
                if col > 0 and world_map[row][col - 1] == 0:
                    glTexCoord2f(0, 0); glVertex3f(col, -1, row + 1)
                    glTexCoord2f(1, 0); glVertex3f(col, -1, row)
                    glTexCoord2f(1, 1); glVertex3f(col, 1, row)
                    glTexCoord2f(0, 1); glVertex3f(col, 1, row + 1)

                # Comprobar vecino del ESTE (x+1)
                if col < MAP_WIDTH - 1 and world_map[row][col + 1] == 0:
                    glTexCoord2f(0, 0); glVertex3f(col + 1, -1, row)
                    glTexCoord2f(1, 0); glVertex3f(col + 1, -1, row + 1)
                    glTexCoord2f(1, 1); glVertex3f(col + 1, 1, row + 1)
                    glTexCoord2f(0, 1); glVertex3f(col + 1, 1, row)
    glEnd()
    
def draw_sky():
    """Dibuja un cilindro grande alrededor del jugador para simular el cielo."""
    glPushMatrix()
    
    # Centrar el cielo en la posición X, Z del jugador para que parezca infinito
    glTranslatef(player_pos[0], 0, player_pos[2])
    
    # Mover el cilindro hacia arriba para que el "horizonte" del cielo se vea más alto
    glTranslatef(0, 1, 0)
    
    glBindTexture(GL_TEXTURE_2D, texture_ids['sky'])
    
    # Deshabilitar la escritura en el buffer de profundidad para que el cielo siempre esté detrás
    glDepthMask(GL_FALSE)
    
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    
    # Rotar el cilindro 90 grados para que la textura se mapee correctamente en el interior
    glRotatef(-90, 1, 0, 0)
    
    # Dibujar un cilindro grande. El radio debe ser menor que el plano de recorte lejano (far clipping plane).
    # Usamos 40, que es menor que 100.0 definido en gluPerspective.
    # La altura del cilindro será la altura de nuestro "cielo".
    gluCylinder(quad, 40.0, 40.0, 30.0, 32, 1)
    
    gluDeleteQuadric(quad)
    
    # Volver a habilitar la escritura en el buffer de profundidad para el resto de la escena
    glDepthMask(GL_TRUE)
    
    glPopMatrix()


def draw_entities():
    """Dibuja todas las entidades dinámicas (enemigos, proyectiles)."""
    for enemy in enemies:
        draw_enemy(enemy)
    
    for projectile in projectiles:
        draw_projectile(projectile)

def draw_crosshair():
    """Dibuja una mira 2D en el centro de la pantalla."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)

    glColor3f(1, 1, 1) # Color blanco
    glLineWidth(2.0)
    
    center_x, center_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    size = 10
    
    glBegin(GL_LINES)
    glVertex2f(center_x - size, center_y)
    glVertex2f(center_x + size, center_y)
    glVertex2f(center_x, center_y - size)
    glVertex2f(center_x, center_y + size)
    glEnd()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_hud(font):
    """Dibuja la interfaz de usuario (HUD), como la salud."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)

    # Renderizar texto de salud
    health_text = f"SALUD: {int(player_health)}"
    text_surface = font.render(health_text, True, (255, 0, 0), (0, 0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    score_text = f"PUNTOS: {score}"
    score_surface = font.render(score_text, True, (255, 255, 0), (0, 0, 0, 0))
    score_data = pygame.image.tostring(score_surface, "RGBA", True)

    ammo_text = f"MUNICIÓN: {player_clip_ammo} / {player_clip_size}"
    ammo_surface = font.render(ammo_text, True, (255, 255, 255), (0, 0, 0, 0))
    ammo_data = pygame.image.tostring(ammo_surface, "RGBA", True)
    
    glRasterPos2d(10, SCREEN_HEIGHT - 40)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    if player_health <= 0:
        game_over_text = "HAS MUERTO"
        text_surface = font.render(game_over_text, True, (255, 0, 0), (0, 0, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        glRasterPos2d((SCREEN_WIDTH - text_width) / 2, (SCREEN_HEIGHT - text_height) / 2)
        glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        respawn_text = "Presiona ENTER para reaparecer"
        respawn_surface = font.render(respawn_text, True, (255, 255, 255), (0, 0, 0, 0))
        respawn_data = pygame.image.tostring(respawn_surface, "RGBA", True)
        glRasterPos2d((SCREEN_WIDTH - respawn_surface.get_width()) / 2, (SCREEN_HEIGHT / 2) - 50)
        glDrawPixels(respawn_surface.get_width(), respawn_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, respawn_data)
        
        respawn_text = "Presiona ESC para salir"
        respawn_surface = font.render(respawn_text, True, (255, 255, 255), (0, 0, 0, 0))
        respawn_data = pygame.image.tostring(respawn_surface, "RGBA", True)
        glRasterPos2d((SCREEN_WIDTH - respawn_surface.get_width()) / 2, (SCREEN_HEIGHT / 2) - 84)
        glDrawPixels(respawn_surface.get_width(), respawn_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, respawn_data)

    if game_state == "PAUSED":
        pause_text = "PAUSA"
        pause_surface = font.render(pause_text, True, (255, 255, 255), (0, 0, 0, 0))
        pause_data = pygame.image.tostring(pause_surface, "RGBA", True)
        text_width = pause_surface.get_width()
        text_height = pause_surface.get_height()
        glRasterPos2d((SCREEN_WIDTH - text_width) / 2, (SCREEN_HEIGHT - text_height) / 2)
        glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, pause_data)

    if is_reloading:
        pass # La animación del arma reemplaza el texto

    glRasterPos2d(10, 10)
    glDrawPixels(ammo_surface.get_width(), ammo_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, ammo_data)

    glRasterPos2d(SCREEN_WIDTH - score_surface.get_width() - 10, SCREEN_HEIGHT - 40)
    glDrawPixels(score_surface.get_width(), score_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, score_data)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_weapon():
    """Dibuja el arma del jugador en la parte inferior de la pantalla."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND) # Asegurar que la transparencia del GIF funcione

    # Seleccionar el fotograma correcto
    frame_index = 0
    frame_texture_id = None
    
    if reload_frames: # Solo intentar si la animación de recarga se cargó
        if weapon_animation_state == 'SHOOTING':
            # Animación de disparo: usa los primeros 8 frames (índices 0-7)
            frame_index = min(weapon_animation_frame, 7)
            frame_texture_id = reload_frames[min(frame_index, len(reload_frames) - 1)]
        elif weapon_animation_state == 'RELOADING':
            # Animación de recarga: usa los frames 10 a 55 (índices 9-54)
            start_frame = 9
            end_frame = 54
            num_frames = end_frame - start_frame + 1
            frame_index = start_frame + (reload_animation_frame % num_frames)
            frame_texture_id = reload_frames[min(frame_index, len(reload_frames) - 1)]
        else: # IDLE
            frame_texture_id = reload_frames[0]
    
    if frame_texture_id is None:
        # Si no se cargó ninguna textura (ej. reload_frames está vacío), no dibujar nada
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        return

    glBindTexture(GL_TEXTURE_2D, frame_texture_id)
    
    # Necesitamos obtener el tamaño de la textura para dibujarla correctamente
    width = glGetTexLevelParameteriv(GL_TEXTURE_2D, 0, GL_TEXTURE_WIDTH)
    height = glGetTexLevelParameteriv(GL_TEXTURE_2D, 0, GL_TEXTURE_HEIGHT)
    
    # Aumentar el tamaño de la animación de recarga y disparo
    scale_factor = 0.6
    width *= scale_factor
    height *= scale_factor
    
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f((SCREEN_WIDTH - width) / 2 - 160, 0)
    glTexCoord2f(1, 0); glVertex2f((SCREEN_WIDTH + width) / 2 - 160, 0)
    glTexCoord2f(1, 1); glVertex2f((SCREEN_WIDTH + width) / 2 - 160, height)
    glTexCoord2f(0, 1); glVertex2f((SCREEN_WIDTH - width) / 2 - 160, height)
    glEnd()

    glColor4f(1.0, 1.0, 1.0, 1.0) # Restaurar color por si acaso
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# --- Lógica Principal del Juego ---
def reset_game():
    """Reinicia el estado del juego a sus valores iniciales."""
    global player_health, player_pos, score, enemies, projectiles, game_state, player_clip_ammo, is_reloading, weapon_animation_state
    player_health = 100
    player_pos = [2.5, 0.0, 2.5]
    score = 0
    enemies.clear()
    projectiles.clear()
    game_state = "RUNNING"
    weapon_animation_state = 'IDLE'
    player_clip_ammo = player_clip_size
    is_reloading = False

def main():
    """Bucle principal del juego."""
    global player_pos, player_angle, player_health, score, game_state, player_clip_ammo, is_reloading, reload_timer, last_shot_time, death_sound, weapon_animation_state, weapon_animation_frame, weapon_animation_timer, reload_animation_frame, reload_animation_timer
    global shot_sound, enemy_hit_sound, player_hit_sound, enemy_shot_sound, enemies, projectiles

    pygame.init()
    pygame.mixer.init() # Inicializar el mezclador de sonido
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Doom Piratón")
    
    setup_opengl()

    # Cargar fuente para el HUD
    hud_font = pygame.font.SysFont('Arial', 30, True)

    # Cargar y reproducir música de fondo
    try:
        pygame.mixer.music.load('music.wav')
        pygame.mixer.music.play(-1)  # El argumento -1 hace que la música se repita indefinidamente
    except pygame.error as e:
        print(f"No se pudo cargar o reproducir music.wav: {e}")

    # Cargar sonido de disparo
    try:
        shot_sound = pygame.mixer.Sound('shot.wav')
    except pygame.error:
        pass # El juego continuará sin sonido

    # Cargar sonido de impacto en enemigo
    try:
        enemy_hit_sound = pygame.mixer.Sound('enemy_hit.wav')
    except pygame.error:
        pass

    # Cargar sonido de impacto en jugador
    try:
        player_hit_sound = pygame.mixer.Sound('player_hit.wav')
    except pygame.error:
        pass

    # Cargar sonido de disparo enemigo
    try:
        enemy_shot_sound = pygame.mixer.Sound('enemy_shot.wav')
    except pygame.error:
        pass

    # Cargar sonido de muerte
    try:
        death_sound = pygame.mixer.Sound('death.wav')
    except pygame.error:
        pass

    clock = pygame.time.Clock()

    # --- Temporizador para generar enemigos ---
    enemy_spawn_timer = pygame.time.get_ticks()

    reset_game() # Establecer el estado inicial del juego

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            
            if event.type == KEYDOWN:
                # --- Lógica de Pausa ---
                if event.key == K_p:
                    if game_state == "RUNNING":
                        game_state = "PAUSED"
                        pygame.mixer.music.pause()
                    elif game_state == "PAUSED":
                        game_state = "RUNNING"
                        pygame.mixer.music.unpause()
                
                # --- Lógica de Reaparición ---
                if event.key == K_RETURN and game_state == "GAME_OVER":
                    reset_game()
                
                # --- Lógica de Recarga Manual ---
                if event.key == K_r and game_state == "RUNNING" and not is_reloading:
                    if player_clip_ammo < player_clip_size:
                        is_reloading = True
                        weapon_animation_state = 'RELOADING'
                        reload_timer = pygame.time.get_ticks()
                        reload_animation_timer = reload_timer
                        reload_animation_frame = 0

                # --- Lógica de Disparo ---
                if event.key == K_SPACE and game_state == "RUNNING" and not is_reloading:
                    if player_clip_ammo > 0 and pygame.time.get_ticks() - last_shot_time > shoot_cooldown:
                        if shot_sound:
                            shot_sound.play()
                            
                        last_shot_time = current_time
                        player_clip_ammo -= 1

                        ray_dir = [math.cos(player_angle), 0, math.sin(player_angle)]

                        # Iniciar animación del arma
                        weapon_animation_state = 'SHOOTING'
                        weapon_animation_frame = 0
                        weapon_animation_timer = last_shot_time

                        # Detección de impacto (Ray-Cylinder intersection)
                        for enemy in enemies:
                            if not enemy.alive:
                                continue
                            
                            vec_to_enemy = vec_sub(enemy.pos, player_pos)
                            projection = vec_dot(vec_to_enemy, ray_dir)
                            proj_vec = vec_mul_scalar(ray_dir, projection)
                            dist_perp = vec_norm(vec_sub(vec_to_enemy, proj_vec))
                            
                            # Comprueba si el rayo pasa cerca del enemigo (dist_perp)
                            # y si el enemigo está delante del jugador (projection > 0)
                            if dist_perp < enemy.size and projection > 0:
                                if enemy_hit_sound:
                                    enemy_hit_sound.play()
                                enemy.health -= 50
                                if enemy.health <= 0:
                                    enemy.alive = False
                                    score += 100
                                    enemy.path_points = None 
                                break # La bala solo golpea a un enemigo

        # --- Lógica del Juego (solo si no está pausado o terminado) ---
        if game_state == "RUNNING":
            keys = pygame.key.get_pressed()
            
            # Movimiento y Rotación
            dx, dz = 0, 0
            if keys[K_w]:
                dx += MOVE_SPEED * math.cos(player_angle)
                dz += MOVE_SPEED * math.sin(player_angle)
            if keys[K_s]:
                dx -= MOVE_SPEED * math.cos(player_angle)
                dz -= MOVE_SPEED * math.sin(player_angle)
            strafe_angle = player_angle - math.pi / 2
            if keys[K_a]:
                dx += MOVE_SPEED * math.cos(strafe_angle)
                dz += MOVE_SPEED * math.sin(strafe_angle)
            if keys[K_d]:
                dx -= MOVE_SPEED * math.cos(strafe_angle)
                dz -= MOVE_SPEED * math.sin(strafe_angle)
            if keys[K_LEFT]:
                player_angle -= ROT_SPEED
            if keys[K_RIGHT]:
                player_angle += ROT_SPEED

            # Actualizar estado de los enemigos
            player_pos_list = list(player_pos) # Usar una copia para la IA
            for enemy in enemies:
                enemy.update(player_pos_list)
            
            # Limpiar la lista de enemigos muertos
            enemies[:] = [enemy for enemy in enemies if enemy.alive]

            # Actualizar proyectiles
            for proj in projectiles:
                if not proj.alive: continue
                proj.pos = vec_add(proj.pos, vec_mul_scalar(proj.dir, proj.speed))
                
                map_x, map_z = int(proj.pos[0]), int(proj.pos[2])
                if world_map[map_z][map_x] == 1:
                    proj.alive = False
                    continue
                
                # Colisión proyectil-jugador (círculo-círculo)
                if vec_norm(vec_sub(proj.pos, player_pos_list)) < player_radius + proj.radius:
                    proj.alive = False
                    player_health -= 25
                    if player_hit_sound: player_hit_sound.play()
                    if player_health <= 0 and game_state != "GAME_OVER":
                        game_state = "GAME_OVER"
                        if death_sound:
                            death_sound.play()

            # Limpiar proyectiles muertos
            projectiles[:] = [p for p in projectiles if p.alive]

            # Generación de enemigos
            if current_time - enemy_spawn_timer > ENEMY_SPAWN_INTERVAL:
                if len(enemies) < MAX_ENEMIES:
                    while True:
                        spawn_x = random.uniform(1, MAP_WIDTH - 2)
                        spawn_z = random.uniform(1, MAP_HEIGHT - 2)
                        if world_map[int(spawn_z)][int(spawn_x)] == 0:
                            new_enemy = Enemy(pos=[spawn_x, 0.0, spawn_z])
                            enemies.append(new_enemy)
                            break
                enemy_spawn_timer = current_time

            # Lógica de Recarga
            if is_reloading and current_time - reload_timer > reload_duration:
                is_reloading = False
                player_clip_ammo = player_clip_size
                if weapon_animation_state == 'RELOADING':
                    weapon_animation_state = 'IDLE'

            # Lógica de animación del arma
            if weapon_animation_state == 'SHOOTING':
                if current_time - weapon_animation_timer > weapon_animation_speed:
                    weapon_animation_frame += 1
                    if weapon_animation_frame >= 8: # La animación de disparo dura 8 frames
                        weapon_animation_state = 'IDLE'
                    weapon_animation_timer = current_time
            elif weapon_animation_state == 'RELOADING':
                if current_time - reload_animation_timer > reload_animation_speed:
                    reload_animation_frame += 1
                    reload_animation_timer = current_time

            # Detección de Colisiones del Jugador (simple, desliza por paredes)
            new_pos_x = player_pos[0] + dx
            if world_map[int(player_pos[2])][int(new_pos_x)] == 0:
                player_pos[0] = new_pos_x

            new_pos_z = player_pos[2] + dz
            if world_map[int(new_pos_z)][int(player_pos[0])] == 0:
                player_pos[2] = new_pos_z

        # --- Renderizado ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Configurar la cámara
        look_at_x = player_pos[0] + math.cos(player_angle)
        look_at_z = player_pos[2] + math.sin(player_angle)
        gluLookAt(
            player_pos[0], player_pos[1], player_pos[2],  # Posición del ojo (cámara)
            look_at_x, player_pos[1], look_at_z,          # Punto al que se mira
            0, 1, 0                                       # Vector "arriba"
        )

        # Dibujar el cielo primero para que esté en el fondo
        draw_sky()

        # Dibujar el mundo estático
        draw_map()
        
        # Dibujar entidades dinámicas
        draw_entities()

        # Dibujar el arma (HUD 3D)
        draw_weapon()

        # Dibujar la mira (HUD 2D)
        draw_crosshair()

        # Dibujar el HUD 2D
        draw_hud(hud_font)

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.quit()
    pygame.quit()

if __name__ == '__main__':
    main()