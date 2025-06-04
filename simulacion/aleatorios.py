import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import simulacion.vector_estado as v_est

def generar_uniforme(a, b):
    rnd = random.random()
    rnd = v_est.truncar_decimales(rnd)
    valor = a + (b - a) * rnd
    return valor, rnd

def elegir_servidor(colorista, peluquero_a, peluquero_b, prob_colorista, prob_a):
    rnd = random.random()
    rnd = v_est.truncar_decimales(rnd)

    if rnd < prob_colorista:
        return colorista, rnd
    elif rnd < prob_colorista + prob_a:
        return peluquero_a, rnd
    else:
        return peluquero_b, rnd