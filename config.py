# Configuración inicial
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768

# Constantes del juego
MOVE_SPEED = 0.12
ROT_SPEED = 0.04
ENEMY_SPAWN_INTERVAL = 5000 # 5 segundos
PLAYER_SHOT_DAMAGE = 50
ENEMY_PROJECTILE_DAMAGE = 20
MAX_ENEMIES = 15

# Variables globales del jugador 
player_angle = 0.0  # Ángulo de visión en el plano XZ
player_health = 100
player_radius = 0.8
score = 0
game_state = "RUNNING" # Estados posibles: RUNNING, PAUSED, GAME_OVER, VICTORY
current_level = 0
completed_levels = set()

# Sistema de munición del jugador
player_clip_ammo = 10
player_clip_size = 10
is_reloading = False
reload_duration = 2000 # 2 segundos
reload_timer = 0
shoot_cooldown = 240 # 0.24 segundos
last_shot_time = 0

# Efectos visuales
player_hit_timer = 0
player_hit_duration = 300 # 0.3 segundos

# Listas de entidades
enemies = []
projectiles = []

# Sonido
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
weapon_animation_speed = 60 # por fotograma
reload_animation_frame = 0
reload_animation_timer = 0
reload_animation_speed = 35 # por fotograma