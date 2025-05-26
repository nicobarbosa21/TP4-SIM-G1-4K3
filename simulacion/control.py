from .motor import simular_dia
from salida.resumen import mostrar_resultados

def simular_n_dias(n, i, j, x):
    total_recaudacion = 0
    total_gastos = 0
    dias_que_superan_x = 0
    vectores_por_dia = []

    for dia in range(1, n + 1):
        vector, rec, gastos, supera = simular_dia(dia, i, j, x)

        vectores_por_dia.append(vector)
        total_recaudacion += rec
        total_gastos += gastos
        dias_que_superan_x += supera

    mostrar_resultados(n, x, total_recaudacion, total_gastos, dias_que_superan_x, vectores_por_dia)
