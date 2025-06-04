def mostrar_resultados(n, x, total_recaudacion, total_gastos, dias_que_superan_x, vectores_por_dia):
    total_ganancia = total_recaudacion - total_gastos
    probabilidad = dias_que_superan_x / n

    for dia, vector in enumerate(vectores_por_dia, start=1):
        print(f"\n--- D\u00eda {dia} ---")
        for fila in vector:
            print("-----")
            for clave, valor in fila.items():
                print(f"{clave}: {valor}")

    print("\n=== Resultados Finales ===")
    print(f"Recaudaci\u00f3n total: ${total_recaudacion}, promedio diario: ${round(total_recaudacion/n,2)}")
    print(f"Gastos totales: ${total_gastos}, promedio diario: ${round(total_gastos/n,2)}")
    print(f"Ganancia total: ${total_ganancia}, promedio diario: ${round(total_ganancia/n,2)}")
    print(f"Probabilidad de superar {x} personas en espera: {probabilidad:.2%}")
    