# Doom-Style FPS Engine en Python

Este repositorio contiene el código fuente de un motor de juego de disparos en primera persona (FPS) estilo retro, desarrollado en Python utilizando **Pygame** y **OpenGL**. El proyecto recrea la estética y mecánicas clásicas de juegos como *Doom* o *Wolfenstein 3D*, incorporando renderizado 3D, iluminación dinámica y comportamientos de enemigos.

## 📋 Descripción

El proyecto es un juego de supervivencia donde el jugador debe navegar a través de laberintos 3D, combatir enemigos y gestionar recursos (munición y salud). El motor utiliza OpenGL para el renderizado de gráficos y Pygame para la gestión de ventanas, audio y entrada del usuario.

El sistema cuenta con generación procedimental de niveles (selección aleatoria de mapas predefinidos), persistencia de puntuaciones altas y una inteligencia artificial básica para los enemigos basada en curvas de Bézier.

## 🚀 Características Principales

* **Motor Gráfico 3D**:
    * Renderizado de muros, suelos y techos con texturas.
    * **Skybox**: Cilindro texturizado para simular el cielo.
    * **Sprites (Billboarding)**: Enemigos y objetos que siempre miran hacia la cámara.
    * **Iluminación Dinámica**: Sistema optimizado de mapas de luz que reacciona a los proyectiles.
* **Jugabilidad**:
    * Movimiento libre (WASD) y rotación de cámara.
    * Sistema de combate con disparos (Hitscan para el jugador, Proyectiles para enemigos).
    * Gestión de munición y recolección de objetos (`shells`, `boxshells`).
    * Sistema de salud y estados de juego (Juego, Pausa, Game Over, Victoria).
* **Inteligencia Artificial**:
    * Enemigos con detección de línea de visión (`Line of Sight`).
    * Movimiento suave utilizando **Curvas de Bézier** cúbicas para patrullaje.
    * Estados de animación (Idle, Attacking).
* **Sistema de Niveles**:
    * Progresión de dificultad.
    * Carga aleatoria de mapas no completados.
    * Persistencia de *High Score* mediante JSON.

## 🛠️ Requisitos del Sistema

Para ejecutar este juego necesitas tener instalado Python. Las dependencias externas son:

* **Pygame**: Para la ventana, input y sonido.
* **PyOpenGL**: Para el renderizado gráfico 3D.
* **Pillow (PIL)**: Para la carga y manipulación de texturas e imágenes.

### Instalación de dependencias
Puedes instalar todas las librerías necesarias ejecutando:

```bash
pip install pygame PyOpenGL Pillow
