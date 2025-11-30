import math

# Funciones vectoriales
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

# Funciones de curva
def calculate_bezier_point(t, p0, p1, p2, p3):
    """Calcula un punto en una curva de Bézier cúbica"""
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