# Prueba de terminal

from simulacion.control import simular_n_dias

def pedir_intervalo(nombre):
    while True:
        try:
            minimo = float(input(f"Ingrese el tiempo mínimo para {nombre}: "))
            maximo = float(input(f"Ingrese el tiempo máximo para {nombre}: "))
            if minimo > maximo:
                print("El valor mínimo no puede ser mayor al máximo.")
            else:
                return (minimo, maximo)
        except ValueError:
            print("Ingrese un número válido.")

def pedir_probabilidades():
    while True:
        try:
            prob_c = float(input("Probabilidad de elegir al colorista (entre 0 y 1): "))
            prob_a = float(input("Probabilidad de elegir al Peluquero A (entre 0 y 1): "))
            if prob_c + prob_a > 1:
                print("La suma de probabilidades no puede superar 1.")
            else:
                return prob_c, prob_a
        except ValueError:
            print("Ingrese un número válido.")

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

    print("\nIngresá las distribuciones de tiempo:")
    llegada = pedir_intervalo("la llegada de clientes")
    colorista = pedir_intervalo("el tiempo del colorista")
    peluquero_a = pedir_intervalo("el tiempo del Peluquero A")
    peluquero_b = pedir_intervalo("el tiempo del Peluquero B")
    print("\nIngresá las probabilidades de asignación:")
    prob_colorista, prob_a = pedir_probabilidades()

    simular_n_dias(n, i, j, x, llegada, colorista, peluquero_a, peluquero_b, prob_colorista, prob_a)

if __name__ == "__main__":
    main()