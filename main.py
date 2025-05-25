from simulacion.control import simular_n_dias

def main():
    print("Simulación de Peluquería Look")

    try:
        n = int(input("¿Cuántos días querés simular? "))
        i = int(input("¿Cuántas filas del vector querés ver? (i) "))
        j = float(input("¿Desde qué minuto del día querés ver el vector? (j) "))
        j = round(j, 2)
        x = int(input("¿Cuál es el umbral máximo de personas esperando (x)? "))
    except ValueError:
        print("Entrada inválida. Asegurate de ingresar solo números.")
        return

    simular_n_dias(n, i, j, x)

if __name__ == "__main__":
    main()
