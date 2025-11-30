import pygame
import random

import config
from utils import (vec_add, vec_sub, vec_mul_scalar, vec_norm, vec_normalize,
                   calculate_bezier_point)

# Clases de entidades
class Enemy:
    def __init__(self, pos):
        self.pos = list(pos)
        self.health = 100
        self.alive = True
        self.size = 0.7 # Radio para colisión de disparo
        self.path_points = None
        self.path_progress = 0.0
        self.path_speed = 0.004
        self.shoot_cooldown = 2000 # 2 segundos
        self.last_shot_time = 0
        self.animation_state = 'IDLE' # IDLE, ATTACKING
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100 # por fotograma
        self.generate_new_path()

    def generate_new_path(self):
        """Genera una nueva curva de Bézier aleatoria para el enemigo"""
        p0 = self.pos
        
        # Elige un punto final aleatorio que no esté en una pared
        while True:
            p3_x = random.uniform(1, config.MAP_WIDTH - 2)
            p3_z = random.uniform(1, config.MAP_HEIGHT - 2)
            if config.world_map[int(p3_z)][int(p3_x)] == 0:
                p3 = [p3_x, 0.0, p3_z]
                break
        
        # Puntos de control aleatorios para dar forma a la curva
        p1 = vec_add(p0, [random.uniform(-5, 5), 0, random.uniform(-5, 5)])
        p2 = vec_add(p3, [random.uniform(-5, 5), 0, random.uniform(-5, 5)])

        self.path_points = [p0, p1, p2, p3]
        self.path_progress = 0.0

    def has_line_of_sight(self, target_pos):
        """Comprueba si hay una línea de visión clara hacia el jugador"""
        direction = vec_sub(target_pos, self.pos)
        distance = vec_norm(direction)
        if distance == 0: return False
        direction = vec_mul_scalar(direction, 1.0 / distance)

        steps = int(distance / 0.5) # Comprobar cada medio bloque
        for i in range(1, steps):
            check_pos = vec_add(self.pos, vec_mul_scalar(direction, i * 0.5))
            map_x = int(check_pos[0])
            map_z = int(check_pos[2])
            if config.world_map[map_z][map_x] == 1:
                return False # Hay una pared en el camino
        return True

    def update(self, player_pos_np):
        """Mueve al enemigo a lo largo de la curva de Bézier y comprueba colisiones"""
        if not self.alive or not self.path_points:
            return

        current_time = pygame.time.get_ticks()

        # Lógica de disparo
        dist_to_player = vec_norm(vec_sub(player_pos_np, self.pos))

        if dist_to_player < 15 and current_time - self.last_shot_time > self.shoot_cooldown:
            if self.has_line_of_sight(player_pos_np):
                direction = vec_sub(player_pos_np, self.pos)
                direction[1] = 0 # Disparar en el plano horizontal
                direction = vec_normalize(direction)
                
                start_pos = vec_add(self.pos, vec_mul_scalar(direction, 0.5))
                config.projectiles.append(Projectile(start_pos, direction))
                
                if config.enemy_shot_sound:
                    config.enemy_shot_sound.play()

                self.animation_state = 'ATTACKING'
                self.animation_frame = 0
                self.animation_timer = current_time
                self.last_shot_time = current_time

        # Lógica de movimiento
        if dist_to_player > 8:
            if self.path_progress < 1.0:
                next_progress = self.path_progress + self.path_speed
                potential_pos = calculate_bezier_point(min(next_progress, 1.0), *self.path_points)

                # Detección de colisiones del enemigo
                dx = potential_pos[0] - self.pos[0]
                dz = potential_pos[2] - self.pos[2]

                # Comprueba la colisión en el eje X y Z por separado para permitir el deslizamiento
                check_x = int(self.pos[0] + dx + self.size * (1 if dx > 0 else -1))
                check_z = int(self.pos[2] + dz + self.size * (1 if dz > 0 else -1))

                # Si la siguiente posición en la curva no choca con una pared
                if config.world_map[int(self.pos[2])][check_x] == 0 and config.world_map[check_z][int(self.pos[0])] == 0:
                    self.path_progress = next_progress
                    self.pos = potential_pos
                else:
                    self.generate_new_path()
            else:
                self.generate_new_path()
        
        # Lógica de animación
        if self.animation_state == 'ATTACKING':
            if current_time - self.animation_timer > self.animation_speed:
                self.animation_frame += 1
                if self.animation_frame >= len(config.enemy_attack_frames):
                    self.animation_state = 'IDLE' # Terminar animación
                self.animation_timer = current_time

class Projectile:
    def __init__(self, pos, direction):
        self.pos = list(pos)
        self.dir = direction
        self.speed = 0.15
        self.alive = True
        self.radius = 0.15

class Pickup:
    def __init__(self, pos, pickup_type):
        self.pos = list(pos)
        self.type = pickup_type # shells o boxshells
        self.alive = True
        self.size = 0.2 # Radio para colisión
        self.pos[1] = -0.5 
