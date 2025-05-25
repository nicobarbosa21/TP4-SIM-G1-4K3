import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from simulacion.control import simular_n_dias

def ejecutar_simulacion():
    try:
        n = int(entry_dias.get())
        i = int(entry_filas.get())
        j = int(entry_desde_hora.get())
        x = int(entry_umbral.get())
        simular_n_dias(n, i, j, x)
    except ValueError:
        messagebox.showerror("Error", "Todos los valores deben ser números enteros")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Simulador - Peluquería Look")
ventana.geometry("400x300")

# Etiquetas y entradas
frame = ttk.Frame(ventana, padding=20)
frame.pack(expand=True)

etiqueta_dias = ttk.Label(frame, text="Cantidad de días a simular:")
etiqueta_dias.grid(row=0, column=0, sticky="w")
entry_dias = ttk.Entry(frame)
entry_dias.grid(row=0, column=1)

etiqueta_filas = ttk.Label(frame, text="Filas del vector de estado (i):")
etiqueta_filas.grid(row=1, column=0, sticky="w")
entry_filas = ttk.Entry(frame)
entry_filas.grid(row=1, column=1)

etiqueta_desde_hora = ttk.Label(frame, text="Desde qué minuto mostrar (j):")
etiqueta_desde_hora.grid(row=2, column=0, sticky="w")
entry_desde_hora = ttk.Entry(frame)
entry_desde_hora.grid(row=2, column=1)

etiqueta_umbral = ttk.Label(frame, text="Umbral máximo de espera (x):")
etiqueta_umbral.grid(row=3, column=0, sticky="w")
entry_umbral = ttk.Entry(frame)
entry_umbral.grid(row=3, column=1)

# Botón de ejecución
boton = ttk.Button(frame, text="Ejecutar Simulación", command=ejecutar_simulacion)
boton.grid(row=4, column=0, columnspan=2, pady=20)

ventana.mainloop()
