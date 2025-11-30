import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

import random
import maps
import config

# Funciones de generación de mundo
def select_next_random_map():
    """Selecciona un mapa aleatorio de los que aún no se han completado"""
    available_maps = [m for m in maps.predefined_maps if m["level"] not in config.completed_levels]
    
    if not available_maps:
        return False # Si no quedan mapas, el jugador ha ganado

    selected_map_data = random.choice(available_maps)
    
    config.current_level = selected_map_data["level"]
    config.world_map = selected_map_data["layout"]
    config.player_pos = list(selected_map_data["start_pos"])
    config.MAP_HEIGHT = len(config.world_map)
    config.MAP_WIDTH = len(config.world_map[0]) if config.MAP_HEIGHT > 0 else 0
    
    return True # Se ha cargado un nuevo mapa con éxito

# Funciones de carga y configuración
def load_gif_animation(filename):
    """Carga los fotogramas de un GIF y los convierte en texturas de OpenGL"""
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
        pass # Si el archivo no existe, la animación no se cargará
    return frames

def load_texture(filename):
    """Carga una imagen y la prepara como textura de OpenGL"""
    img = Image.open(filename).convert("RGBA")
    img_data = img.tobytes("raw", "RGBA", 0, -1)
    
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    
    return tex_id

def setup_opengl():
    """Configura el estado inicial de OpenGL"""
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    
    # Habilitar transparencia
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, (config.SCREEN_WIDTH / config.SCREEN_HEIGHT), 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)

    # Cargar texturas
    try:
        config.texture_ids['wall'] = load_texture('wall.png')
        config.texture_ids['floor'] = load_texture('floor.png')
        config.texture_ids['sky'] = load_texture('sky.png')
        config.texture_ids['enemy'] = load_texture('enemy.png')
        config.texture_ids['shells'] = load_texture('shells.png')
        config.texture_ids['boxshells'] = load_texture('boxshells.png')
        
        config.enemy_attack_frames = load_gif_animation('enemy_attack.gif')
        config.reload_frames = load_gif_animation('reload.gif')
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar: {e.filename}")
        pygame.quit()
        quit()