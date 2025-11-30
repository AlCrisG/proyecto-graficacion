import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

import config

# Funciones de renderizado
def draw_enemy(enemy):
    """Dibuja un enemigo"""
    if not enemy.alive:
        return

    glPushMatrix()
    # Trasladar a la posición del enemigo
    glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])

    # Obtener la matriz ModelView actual que contiene la orientación de la cámara
    modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
    
    # La rotación de la cámara está en las primeras 3x3 filas/columnas
    # Para que el sprite mire a la cámara, necesitamos cancelar esa rotación
    # La transpuesta de una matriz de rotación es su inversa
    for i in range(3):
        for j in range(3):
            if i == j:
                modelview[i][j] = 1.0
            else:
                modelview[i][j] = 0.0
    glLoadMatrixf(modelview)

    # Seleccionar la textura correcta basada en el estado de animación
    if enemy.animation_state == 'ATTACKING' and config.enemy_attack_frames:
        frame_id = config.enemy_attack_frames[min(enemy.animation_frame, len(config.enemy_attack_frames) - 1)]
        glBindTexture(GL_TEXTURE_2D, frame_id)
    else:
        glBindTexture(GL_TEXTURE_2D, config.texture_ids['enemy'])

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-0.5, -1, 0)
    glTexCoord2f(1, 0); glVertex3f(0.5, -1, 0)
    glTexCoord2f(1, 1); glVertex3f(0.5, 1, 0)
    glTexCoord2f(0, 1); glVertex3f(-0.5, 1, 0)
    glEnd()

    glPopMatrix()

def draw_projectile(projectile):
    """Dibuja un proyectil como una esfera roja"""
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

def draw_pickup(pickup):
    """Dibuja un objeto recogible"""
    if not pickup.alive:
        return

    glPushMatrix()
    glTranslatef(pickup.pos[0], pickup.pos[1], pickup.pos[2])

    modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
    for i in range(3):
        for j in range(3):
            if i == j:
                modelview[i][j] = 1.0
            else:
                modelview[i][j] = 0.0
    glLoadMatrixf(modelview)

    # Usar la textura correspondiente al tipo de objeto
    glBindTexture(GL_TEXTURE_2D, config.texture_ids[pickup.type])

    glBegin(GL_QUADS)
    s = pickup.size
    glTexCoord2f(0, 0); glVertex3f(-s, -s, 0)
    glTexCoord2f(1, 0); glVertex3f(s, -s, 0)
    glTexCoord2f(1, 1); glVertex3f(s, s, 0)
    glTexCoord2f(0, 1); glVertex3f(-s, s, 0)
    glEnd()

    glPopMatrix()

def update_light_map(light_radius=5.0, base_ambient=0.3):
    """
    Calcula la iluminación de todo el mapa
    Primero reinicia el mapa de luz y luego agrega la luz de cada proyectil
    """
    # 1. Reiniciar el mapa de luz a la luz ambiental base
    for z in range(config.MAP_HEIGHT + 1):
        for x in range(config.MAP_WIDTH + 1):
            config.light_map[z][x] = base_ambient

    # 2. Iterar sobre los proyectiles y aplicar su luz a los vértices cercanos
    for projectile in config.projectiles:
        if not projectile.alive:
            continue

        # Determinar el área de influencia (bounding box) del proyectil
        min_x = max(0, int(projectile.pos[0] - light_radius))
        max_x = min(config.MAP_WIDTH, int(projectile.pos[0] + light_radius))
        min_z = max(0, int(projectile.pos[2] - light_radius))
        max_z = min(config.MAP_HEIGHT, int(projectile.pos[2] + light_radius))

        # Iterar solo sobre los vértices dentro del área de influencia
        for z in range(min_z, max_z + 1):
            for x in range(min_x, max_x + 1):
                vertex_pos = (x, -1, z)
                dist_sq = (vertex_pos[0] - projectile.pos[0])**2 + (vertex_pos[2] - projectile.pos[2])**2
                
                if dist_sq < light_radius**2:
                    distance = math.sqrt(dist_sq)
                    light_intensity = (1.0 - (distance / light_radius))
                    config.light_map[z][x] += light_intensity
                    # Limitar la luz a un máximo de 1.0
                    if config.light_map[z][x] > 1.0:
                        config.light_map[z][x] = 1.0

def draw_map():
    """Dibuja el suelo y las paredes del mapa"""
    glBindTexture(GL_TEXTURE_2D, config.texture_ids['floor'])
    glBegin(GL_QUADS)
    for z in range(config.MAP_HEIGHT):
        for x in range(config.MAP_WIDTH):
            if config.world_map[z][x] == 0:
                # Leer la iluminación precalculada del light_map
                l1 = config.light_map[z][x]; l2 = config.light_map[z][x+1]; l3 = config.light_map[z+1][x+1]; l4 = config.light_map[z+1][x]
                
                glColor3f(l1, l1, l1); glTexCoord2f(x, z); glVertex3f(x, -1, z)
                glColor3f(l2, l2, l2); glTexCoord2f(x + 1, z); glVertex3f(x + 1, -1, z)
                glColor3f(l3, l3, l3); glTexCoord2f(x + 1, z + 1); glVertex3f(x + 1, -1, z + 1)
                glColor3f(l4, l4, l4); glTexCoord2f(x, z + 1); glVertex3f(x, -1, z + 1)
    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, config.texture_ids['wall'])
    glBegin(GL_QUADS)
    for row in range(config.MAP_HEIGHT):
        for col in range(config.MAP_WIDTH):
            if config.world_map[row][col] == 1:
                if row > 0 and config.world_map[row - 1][col] == 0:
                    l1 = config.light_map[row][col]; l2 = config.light_map[row][col+1]
                    glColor3f(l1, l1, l1); glTexCoord2f(0, 0); glVertex3f(col, -1, row)
                    glColor3f(l2, l2, l2); glTexCoord2f(1, 0); glVertex3f(col + 1, -1, row)
                    glColor3f(l2, l2, l2); glTexCoord2f(1, 1); glVertex3f(col + 1, 1, row)
                    glColor3f(l1, l1, l1); glTexCoord2f(0, 1); glVertex3f(col, 1, row)

                if row < config.MAP_HEIGHT - 1 and config.world_map[row + 1][col] == 0:
                    l1 = config.light_map[row+1][col+1]; l2 = config.light_map[row+1][col]
                    glColor3f(l1, l1, l1); glTexCoord2f(0, 0); glVertex3f(col + 1, -1, row + 1)
                    glColor3f(l2, l2, l2); glTexCoord2f(1, 0); glVertex3f(col, -1, row + 1)
                    glColor3f(l2, l2, l2); glTexCoord2f(1, 1); glVertex3f(col, 1, row + 1)
                    glColor3f(l1, l1, l1); glTexCoord2f(0, 1); glVertex3f(col + 1, 1, row + 1)

                if col > 0 and config.world_map[row][col - 1] == 0:
                    l1 = config.light_map[row+1][col]; l2 = config.light_map[row][col]
                    glColor3f(l1, l1, l1); glTexCoord2f(0, 0); glVertex3f(col, -1, row + 1)
                    glColor3f(l2, l2, l2); glTexCoord2f(1, 0); glVertex3f(col, -1, row)
                    glColor3f(l2, l2, l2); glTexCoord2f(1, 1); glVertex3f(col, 1, row)
                    glColor3f(l1, l1, l1); glTexCoord2f(0, 1); glVertex3f(col, 1, row + 1)

                if col < config.MAP_WIDTH - 1 and config.world_map[row][col + 1] == 0:
                    l1 = config.light_map[row][col+1]; l2 = config.light_map[row+1][col+1]
                    glColor3f(l1, l1, l1); glTexCoord2f(0, 0); glVertex3f(col + 1, -1, row)
                    glColor3f(l2, l2, l2); glTexCoord2f(1, 0); glVertex3f(col + 1, -1, row + 1)
                    glColor3f(l2, l2, l2); glTexCoord2f(1, 1); glVertex3f(col + 1, 1, row + 1)
                    glColor3f(l1, l1, l1); glTexCoord2f(0, 1); glVertex3f(col + 1, 1, row)
    glEnd()
    # Restaurar el color a blanco para el resto de los objetos
    glColor3f(1.0, 1.0, 1.0)
    
def draw_sky():
    """Dibuja un cilindro grande alrededor del jugador para simular el cielo"""
    glPushMatrix()
    
    # Centrar el cielo en la posición X, Z del jugador para que parezca infinito
    glTranslatef(config.player_pos[0], 0, config.player_pos[2])
    
    # Mover el cilindro hacia arriba para que el horizonte del cielo se vea más alto
    glTranslatef(0, 1, 0)
    
    glBindTexture(GL_TEXTURE_2D, config.texture_ids['sky'])
    
    # Deshabilitar la escritura en el buffer de profundidad para que el cielo siempre esté detrás
    glDepthMask(GL_FALSE)
    
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    
    # Rotar el cilindro 90 grados para que la textura se mapee correctamente en el interior
    glRotatef(-90, 1, 0, 0)
    
    # Dibujar un cilindro grande. El radio debe ser menor que el plano de recorte lejano
    # Se usa 40, que es menor que 100 definido en gluPerspective
    # La altura del cilindro será la altura del cielo
    gluCylinder(quad, 40.0, 40.0, 30.0, 32, 1)
    
    gluDeleteQuadric(quad)
    
    # Volver a habilitar la escritura en el buffer de profundidad para el resto de la escena
    glDepthMask(GL_TRUE)
    
    glPopMatrix()

def draw_entities():
    """Dibuja todas las entidades"""
    for enemy in config.enemies:
        draw_enemy(enemy)
    
    for projectile in config.projectiles:
        draw_projectile(projectile)

    for pickup in config.pickups:
        draw_pickup(pickup)

def draw_crosshair():
    """Dibuja una mira en el centro de la pantalla"""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)

    glColor3f(1, 1, 1)
    glLineWidth(2.0)
    
    center_x, center_y = config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2
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
    """Dibuja la interfaz de usuario"""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)

    health_text = f"SALUD: {max(int(config.player_health), 0)}"
    text_surface = font.render(health_text, True, (255, 0, 0), (0, 0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    score_text = f"PUNTOS: {config.score}"
    score_surface = font.render(score_text, True, (255, 255, 0), (0, 0, 0, 0))
    score_data = pygame.image.tostring(score_surface, "RGBA", True)

    ammo_text = f"MUNICIÓN: {config.player_ammo}"
    ammo_surface = font.render(ammo_text, True, (255, 255, 255), (0, 0, 0, 0))
    ammo_data = pygame.image.tostring(ammo_surface, "RGBA", True)
    
    glRasterPos2d(10, config.SCREEN_HEIGHT - 40)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    if config.player_health <= 0:
        game_over_text = "HAS MUERTO"
        text_surface = font.render(game_over_text, True, (255, 0, 0), (0, 0, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        glRasterPos2d((config.SCREEN_WIDTH - text_width) / 2, (config.SCREEN_HEIGHT - text_height) / 2)
        glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        respawn_text = "Presiona ENTER para reaparecer"
        respawn_surface = font.render(respawn_text, True, (255, 255, 255), (0, 0, 0, 0))
        respawn_data = pygame.image.tostring(respawn_surface, "RGBA", True)
        glRasterPos2d((config.SCREEN_WIDTH - respawn_surface.get_width()) / 2, (config.SCREEN_HEIGHT / 2) - 50)
        glDrawPixels(respawn_surface.get_width(), respawn_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, respawn_data)
        
        respawn_text = "Presiona ESC para salir"
        respawn_surface = font.render(respawn_text, True, (255, 255, 255), (0, 0, 0, 0))
        respawn_data = pygame.image.tostring(respawn_surface, "RGBA", True)
        glRasterPos2d((config.SCREEN_WIDTH - respawn_surface.get_width()) / 2, (config.SCREEN_HEIGHT / 2) - 84)
        glDrawPixels(respawn_surface.get_width(), respawn_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, respawn_data)

    if config.game_state == "PAUSED":
        pause_text = "PAUSA"
        pause_surface = font.render(pause_text, True, (255, 255, 255), (0, 0, 0, 0))
        pause_data = pygame.image.tostring(pause_surface, "RGBA", True)
        text_width = pause_surface.get_width()
        text_height = pause_surface.get_height()
        glRasterPos2d((config.SCREEN_WIDTH - text_width) / 2, (config.SCREEN_HEIGHT - text_height) / 2)
        glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, pause_data)

    if config.game_state == "VICTORY":
        victory_text = "¡HAS GANADO!"
        victory_surface = font.render(victory_text, True, (0, 255, 0), (0, 0, 0, 0))
        victory_data = pygame.image.tostring(victory_surface, "RGBA", True)
        text_width = victory_surface.get_width()
        text_height = victory_surface.get_height()
        glRasterPos2d((config.SCREEN_WIDTH - text_width) / 2, (config.SCREEN_HEIGHT - text_height) / 2)
        glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, victory_data)

    glRasterPos2d(10, 10)
    glDrawPixels(ammo_surface.get_width(), ammo_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, ammo_data)

    glRasterPos2d(config.SCREEN_WIDTH - score_surface.get_width() - 10, config.SCREEN_HEIGHT - 40)
    glDrawPixels(score_surface.get_width(), score_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, score_data)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_weapon():
    """Dibuja el arma del jugador en la parte inferior de la pantalla"""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND) # Asegurar que la transparencia del GIF funcione

    # Seleccionar el fotograma correcto
    frame_index = 0
    frame_texture_id = None
    
    if config.reload_frames: # Solo intentar si la animación de recarga se cargó
        if config.weapon_animation_state == 'SHOOTING':
            # La animación de disparo ahora usa toda la secuencia
            frame_index = min(config.weapon_animation_frame, len(config.reload_frames) - 1)
            frame_texture_id = config.reload_frames[min(frame_index, len(config.reload_frames) - 1)]
        else: # IDLE
            frame_texture_id = config.reload_frames[0]
    
    if frame_texture_id is None:
        # Si no se cargó ninguna textura, no dibujar nada
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
    glTexCoord2f(0, 0); glVertex2f((config.SCREEN_WIDTH - width) / 2 - 160, 0)
    glTexCoord2f(1, 0); glVertex2f((config.SCREEN_WIDTH + width) / 2 - 160, 0)
    glTexCoord2f(1, 1); glVertex2f((config.SCREEN_WIDTH + width) / 2 - 160, height)
    glTexCoord2f(0, 1); glVertex2f((config.SCREEN_WIDTH - width) / 2 - 160, height)
    glEnd()

    glColor4f(1.0, 1.0, 1.0, 1.0) # Restaurar color por si acaso
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_hit_pulse():
    """Dibuja un pulso rojo en la pantalla cuando el jugador es golpeado"""
    current_time = pygame.time.get_ticks()
    elapsed = current_time - config.player_hit_timer
    
    if elapsed < config.player_hit_duration:
        # Calcular la opacidad basada en el tiempo transcurrido
        # Comienza fuerte y se desvanece
        alpha = 0.6 * (1.0 - (elapsed / config.player_hit_duration))
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)

        glColor4f(1.0, 0.0, 0.0, alpha) # Rojo con opacidad variable
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(config.SCREEN_WIDTH, 0)
        glVertex2f(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        glVertex2f(0, config.SCREEN_HEIGHT)
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)