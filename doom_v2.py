import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
 
import config
from utils import vec_sub, vec_mul_scalar, vec_norm, vec_dot, vec_add
from entities import Enemy
from game_setup import setup_opengl, select_next_random_map
from rendering import (draw_sky, draw_map, draw_entities, draw_hit_pulse,
                     draw_weapon, draw_crosshair, draw_hud)

# Lógica de niveles
def start_next_level():
    """Prepara y carga el siguiente nivel del juego"""
    if not select_next_random_map():
        config.game_state = "VICTORY" # Si no hay más niveles, el jugador gana
    else:
        config.player_health = 100
        config.enemies.clear()
        config.projectiles.clear()
        config.player_clip_ammo = config.player_clip_size
        config.is_reloading = False

# Lógica principal del juego
def reset_game():
    """Reinicia el estado del juego a sus valores iniciales"""
    config.completed_levels.clear()
    start_next_level()
    config.player_health = 1000
    config.score = 0
    config.enemies.clear()
    config.projectiles.clear()
    config.game_state = "RUNNING"
    config.weapon_animation_state = 'IDLE'
    config.player_clip_ammo = config.player_clip_size
    config.is_reloading = False

def main():
    """Bucle principal del juego"""
    pygame.init()
    pygame.mixer.init() # Inicializar el mezclador de sonido
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Doom")
    
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
        config.shot_sound = pygame.mixer.Sound('shot.wav')
    except pygame.error:
        pass # El juego continuará sin sonido

    # Cargar sonido de impacto en enemigo
    try:
        config.enemy_hit_sound = pygame.mixer.Sound('enemy_hit.wav')
    except pygame.error:
        pass

    # Cargar sonido de impacto en jugador
    try:
        config.player_hit_sound = pygame.mixer.Sound('player_hit.wav')
    except pygame.error:
        pass

    # Cargar sonido de disparo enemigo
    try:
        config.enemy_shot_sound = pygame.mixer.Sound('enemy_shot.wav')
    except pygame.error:
        pass

    # Cargar sonido de muerte
    try:
        config.death_sound = pygame.mixer.Sound('death.wav')
    except pygame.error:
        pass

    clock = pygame.time.Clock()

    # Temporizador para generar enemigos
    enemy_spawn_timer = pygame.time.get_ticks()

    reset_game() # Establecer el estado inicial del juego

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            
            if event.type == KEYDOWN:
                # Lógica de pausa
                if event.key == K_p:
                    if config.game_state == "RUNNING":
                        config.game_state = "PAUSED"
                        pygame.mixer.music.pause()
                    elif config.game_state == "PAUSED":
                        config.game_state = "RUNNING"
                        pygame.mixer.music.unpause()
                
                # Lógica de reaparición
                if event.key == K_RETURN and config.game_state == "GAME_OVER":
                    reset_game()
                
                # Lógica de recarga manual
                if event.key == K_r and config.game_state == "RUNNING" and not config.is_reloading:
                    if config.player_clip_ammo < config.player_clip_size:
                        config.is_reloading = True
                        config.weapon_animation_state = 'RELOADING'
                        config.reload_timer = pygame.time.get_ticks()
                        config.reload_animation_timer = config.reload_timer
                        config.reload_animation_frame = 0

                # Lógica de disparo
                if event.key == K_SPACE and config.game_state == "RUNNING" and not config.is_reloading:
                    if config.player_clip_ammo > 0 and pygame.time.get_ticks() - config.last_shot_time > config.shoot_cooldown:
                        if config.shot_sound:
                            config.shot_sound.play()
                            
                        config.last_shot_time = current_time
                        config.player_clip_ammo -= 1

                        ray_dir = [math.cos(config.player_angle), 0, math.sin(config.player_angle)]

                        # Iniciar animación del arma
                        config.weapon_animation_state = 'SHOOTING'
                        config.weapon_animation_frame = 0
                        config.weapon_animation_timer = config.last_shot_time

                        # Detección de impacto
                        for enemy in config.enemies:
                            if not enemy.alive:
                                continue
                            
                            vec_to_enemy = vec_sub(enemy.pos, config.player_pos)
                            projection = vec_dot(vec_to_enemy, ray_dir)
                            proj_vec = vec_mul_scalar(ray_dir, projection)
                            dist_perp = vec_norm(vec_sub(vec_to_enemy, proj_vec))
                            
                            # Comprueba si el rayo pasa cerca del enemigo
                            # y si el enemigo está delante del jugador
                            if dist_perp < enemy.size and projection > 0:
                                if config.enemy_hit_sound:
                                    config.enemy_hit_sound.play()
                                enemy.health -= config.PLAYER_SHOT_DAMAGE
                                if enemy.health <= 0:
                                    enemy.alive = False
                                    config.score += 100
                                    enemy.path_points = None 
                                break # La bala solo golpea a un enemigo

        # Lógica de progresión de nivel
        if config.score >= 1000 and config.game_state == "RUNNING":
            config.completed_levels.add(config.current_level)
            config.score = 0 # Reiniciar puntuación para el siguiente nivel
            start_next_level()

        # Lógica del Juego (solo si no está pausado o terminado)
        if config.game_state == "RUNNING":
            keys = pygame.key.get_pressed()
            
            # Movimiento y rotación
            dx, dz = 0, 0
            if keys[K_w]:
                dx += config.MOVE_SPEED * math.cos(config.player_angle)
                dz += config.MOVE_SPEED * math.sin(config.player_angle)
            if keys[K_s]:
                dx -= config.MOVE_SPEED * math.cos(config.player_angle)
                dz -= config.MOVE_SPEED * math.sin(config.player_angle)
            strafe_angle = config.player_angle - math.pi / 2
            if keys[K_a]:
                dx += config.MOVE_SPEED * math.cos(strafe_angle)
                dz += config.MOVE_SPEED * math.sin(strafe_angle)
            if keys[K_d]:
                dx -= config.MOVE_SPEED * math.cos(strafe_angle)
                dz -= config.MOVE_SPEED * math.sin(strafe_angle)
            if keys[K_LEFT]:
                config.player_angle -= config.ROT_SPEED
            if keys[K_RIGHT]:
                config.player_angle += config.ROT_SPEED

            # Actualizar estado de los enemigos
            player_pos_list = list(config.player_pos)
            for enemy in config.enemies:
                enemy.update(player_pos_list)
            
            # Limpiar la lista de enemigos muertos
            config.enemies[:] = [enemy for enemy in config.enemies if enemy.alive]

            # Actualizar proyectiles
            for proj in config.projectiles:
                if not proj.alive: continue
                proj.pos = vec_add(proj.pos, vec_mul_scalar(proj.dir, proj.speed))
                
                map_x, map_z = int(proj.pos[0]), int(proj.pos[2])
                if config.world_map[map_z][map_x] == 1:
                    proj.alive = False
                    continue
                
                # Colisión del proyectil con el jugador
                if vec_norm(vec_sub(proj.pos, player_pos_list)) < config.player_radius + proj.radius:
                    proj.alive = False
                    config.player_health -= config.ENEMY_PROJECTILE_DAMAGE
                    config.player_hit_timer = current_time # Activar el pulso rojo
                    if config.player_hit_sound: config.player_hit_sound.play()
                    if config.player_health <= 0 and config.game_state != "GAME_OVER":
                        config.game_state = "GAME_OVER"
                        if config.death_sound:
                            config.death_sound.play()

            # Limpiar proyectiles muertos
            config.projectiles[:] = [p for p in config.projectiles if p.alive]

            # Generación de enemigos
            if current_time - enemy_spawn_timer > config.ENEMY_SPAWN_INTERVAL:
                if len(config.enemies) < config.MAX_ENEMIES:
                    while True:
                        spawn_x = random.uniform(1, config.MAP_WIDTH - 2)
                        spawn_z = random.uniform(1, config.MAP_HEIGHT - 2)
                        if config.world_map[int(spawn_z)][int(spawn_x)] == 0:
                            new_enemy = Enemy(pos=[spawn_x, 0.0, spawn_z])
                            config.enemies.append(new_enemy)
                            break
                enemy_spawn_timer = current_time

            # Lógica de recarga
            if config.is_reloading and current_time - config.reload_timer > config.reload_duration:
                config.is_reloading = False
                config.player_clip_ammo = config.player_clip_size
                if config.weapon_animation_state == 'RELOADING':
                    config.weapon_animation_state = 'IDLE'

            # Lógica de animación del arma
            if config.weapon_animation_state == 'SHOOTING':
                if current_time - config.weapon_animation_timer > config.weapon_animation_speed:
                    config.weapon_animation_frame += 1
                    if config.weapon_animation_frame >= 8: # La animación de disparo dura 8 frames
                        config.weapon_animation_state = 'IDLE'
                    config.weapon_animation_timer = current_time
            elif config.weapon_animation_state == 'RELOADING':
                if current_time - config.reload_animation_timer > config.reload_animation_speed:
                    config.reload_animation_frame += 1
                    config.reload_animation_timer = current_time

            # Detección de colisiones del jugador
            new_pos_x = config.player_pos[0] + dx
            if config.world_map[int(config.player_pos[2])][int(new_pos_x + config.player_radius * (1 if dx > 0 else -1))] == 0:
                config.player_pos[0] = new_pos_x

            new_pos_z = config.player_pos[2] + dz
            if config.world_map[int(new_pos_z + config.player_radius * (1 if dz > 0 else -1))][int(config.player_pos[0])] == 0:
                config.player_pos[2] = new_pos_z

        # Renderizado
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Configurar la cámara
        look_at_x = config.player_pos[0] + math.cos(config.player_angle)
        look_at_z = config.player_pos[2] + math.sin(config.player_angle)
        gluLookAt(
            config.player_pos[0], config.player_pos[1], config.player_pos[2],  # Posición del ojo (cámara)
            look_at_x, config.player_pos[1], look_at_z,          # Punto al que se mira
            0, 1, 0                                       # Vector arriba
        )

        # Dibujar el cielo primero para que esté en el fondo
        draw_sky()

        # Dibujar el mundo estático
        draw_map()
        
        # Dibujar entidades
        draw_entities()

        # Dibujar pulso de daño si es necesario
        draw_hit_pulse()

        # Dibujar el arma
        draw_weapon()

        # Dibujar la mira
        draw_crosshair()

        # Dibujar el HUD
        draw_hud(hud_font)

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.quit()
    pygame.quit()

if __name__ == '__main__':
    main()