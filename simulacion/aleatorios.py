import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config as cfg

def generar_uniforme(a, b):
    rnd = random.random()
    valor = a + (b - a) * rnd
    return valor, rnd

def elegir_servidor(colorista, peluquero_a, peluquero_b):
    rnd = random.random()
    if rnd < cfg.PROB_COLORISTA:
        return colorista, rnd
    elif rnd < cfg.PROB_COLORISTA + cfg.PROB_PELUQUERO_A:
        return peluquero_a, rnd
    else:
        return peluquero_b, rnd
    