from .motor import simular_dia
import time

def simular_n_dias(n, i, j, x):
    #sacar esta linea cuando le hagamos la interfaz (confio en vos agos lambda)
    mostrar_vector = n == 1

    #Variables que nos sirven para calcular las consignas
    total_recaudacion = 0
    total_gastos = 0
    total_ganancia = 0
    dias_que_superan_x = 0

    for dia in range(1, n + 1):
        print(f"\n--- Día {dia} ---")
        vector, rec, gastos, supera = simular_dia(i, j, x)

        total_recaudacion += rec
        total_gastos += gastos
        total_ganancia += (rec - gastos)
        dias_que_superan_x += supera

        #Sacar esta linea cuando le hagamos la interfaz
        time.sleep(5)
        if mostrar_vector:
            for fila in vector:
                print("-----")
            for clave, valor in fila.items():
                print(f"{clave}: {valor}")

    probabilidad = dias_que_superan_x / n

    print("\n=== Resultados Finales ===")
    print(f"Recaudación total: ${total_recaudacion}")
    print(f"Gastos totales: ${total_gastos}")
    print(f"Ganancia total: ${total_ganancia}")
    print(f"Probabilidad de superar {x} personas en espera: {probabilidad:.2%}")
