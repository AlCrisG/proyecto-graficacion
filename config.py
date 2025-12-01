# Configuración inicial
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768

# Constantes del juego
MOVE_SPEED = 0.12
ROT_SPEED = 0.04
ENEMY_SPAWN_INTERVAL = 5000 # ms (5 segundos)
PLAYER_SHOT_DAMAGE = 50
ENEMY_PROJECTILE_DAMAGE = 20
MAX_ENEMIES = 15

# Variables globales del jugador
player_pos = [2.5, 0.0, 2.5]  # x, y, z
player_angle = 0.0  # Ángulo de visión en el plano XZ
player_health = 100
player_radius = 0.8
score = 0
game_state = "RUNNING" # RUNNING, PAUSED, GAME_OVER, VICTORY
high_score = 0
current_level = 0
completed_levels = set()

# Sistema de munición del jugador
player_ammo = 20 # Munición inicial
shoot_cooldown = 300 # 0.3 segundos
last_shot_time = 0

# Efectos visuales
player_hit_timer = 0
player_hit_duration = 300 # 0.3 segundos

# Listas de entidades
enemies = []
projectiles = []
pickups = []

# Sonido
music = None
shot_sound = None
enemy_hit_sound = None
player_hit_sound = None
enemy_shot_sound = None
death_sound = None

# Recursos de texturas y animación
texture_ids = {}
enemy_attack_frames = []
reload_frames = []
weapon_animation_state = 'IDLE' # IDLE, SHOOTING, RELOADING
weapon_animation_frame = 0
weapon_animation_timer = 0
weapon_animation_speed = 30

# Mapa de iluminación para optimización
light_map = []
base_ambient = 0.7 # Nivel de luz ambiental base para el mapa