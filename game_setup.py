import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

import random
import json
import maps
import config
import sys
import os

def ruta_recurso(ruta_relativa):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, ruta_relativa)

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

    # Inicializar el mapa de luz con las dimensiones del mapa + 1 para los vértices
    config.light_map = [[config.base_ambient for _ in range(config.MAP_WIDTH + 1)] 
                        for _ in range(config.MAP_HEIGHT + 1)]
    
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
        config.texture_ids['wall'] = load_texture(ruta_recurso('images/wall.png'))
        config.texture_ids['floor'] = load_texture(ruta_recurso('images/floor.png'))
        config.texture_ids['sky'] = load_texture(ruta_recurso('images/sky.png'))
        config.texture_ids['enemy'] = load_texture(ruta_recurso('images/enemy.png'))
        config.texture_ids['shells'] = load_texture(ruta_recurso('images/shells.png'))
        config.texture_ids['boxshells'] = load_texture(ruta_recurso('images/boxshells.png'))
        
        config.enemy_attack_frames = load_gif_animation(ruta_recurso('images/enemy_attack.gif'))
        config.reload_frames = load_gif_animation(ruta_recurso('images/reload.gif'))
    except FileNotFoundError as e:
        print(e.filename)
        pygame.quit()
        quit()

def load_high_score():
    """Carga la puntuación más alta desde un archivo JSON"""
    try:
        with open(ruta_recurso('highscore.json'), 'r') as f:
            data = json.load(f)
            config.high_score = data.get('high_score', 0)
    except (FileNotFoundError, json.JSONDecodeError):
        config.high_score = 0

def save_high_score():
    """Guarda la puntuación actual si es la más alta."""
    if config.score > config.high_score:
        config.high_score = config.score
        try:
            with open(ruta_recurso('highscore.json'), 'w') as f:
                json.dump({'high_score': config.high_score}, f)
        except IOError:
            print("Error: No se pudo guardar la puntuación más alta.")