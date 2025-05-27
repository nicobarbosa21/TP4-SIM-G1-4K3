import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk, messagebox
from simulacion.motor import simular_dia

vectores_por_dia = []

columns = [
    "nro_fila", "reloj", "evento", "cliente_id", "rnd_cliente", "tiempo_entre_llegadas", "proxima_llegada",
    "rnd_atencion", "servidor_a_atender", "se_puede_recibir_clientes", "termino_dia",
    "rnd_peluquero_a", "tiempo_atencion_a", "fin_atencion_a", "peluquero_a_estado", "cola_a",
    "rnd_peluquero_b", "tiempo_atencion_b", "fin_atencion_b", "peluquero_b_estado", "cola_b",
    "rnd_colorista", "tiempo_atencion_c", "fin_atencion_c", "colorista_estado", "cola_colorista",
    "recaudacion", "costos", "ganancia", "numero_dia", "personas_esperando", "maximo_cola", "supero_umbral_x"
]

root = tk.Tk()
root.title("Simulador Peluquería Look")
root.geometry("1600x850")
root.configure(bg="#1e1e2f")

frame_titulo = tk.Frame(root, bg="#961515", padx=4, pady=4)
frame_titulo.pack(pady=10)
tk.Label(frame_titulo, text="💈 Peluquería Look - Vector de Estado 💈", bg="#1e1e2f", fg="#FFFFFF", font=("Arial", 20, "bold")).pack()

frame_entradas = tk.Frame(root, bg="#1e1e2f")
frame_entradas.pack()

etiquetas = ["Días:", "Filas a mostrar (i):", "Desde minuto (j):", "Umbral máximo (x):"]
entries = []

for i, texto in enumerate(etiquetas):
    tk.Label(frame_entradas, text=texto, bg="#1e1e2f", fg="white", font=("Arial", 11)).grid(row=i, column=0, sticky="e", padx=5, pady=5)
    entry = tk.Entry(frame_entradas, font=("Arial", 11))
    entry.grid(row=i, column=1, pady=5)
    entries.append(entry)

entry_dias, entry_filas, entry_desde, entry_umbral = entries

btn = tk.Button(root, text="Simular", bg="#ffffff", fg="black", font=("Arial", 11, "bold"))
btn.pack(pady=10)

frame_combo = tk.Frame(root, bg="#1e1e2f")
frame_combo.pack(pady=5)
tk.Label(frame_combo, text="Seleccionar Día:", bg="#1e1e2f", fg="white", font=("Arial", 11)).pack(side="left")
dia_var = tk.StringVar()
dia_combobox = ttk.Combobox(frame_combo, textvariable=dia_var, state="readonly")
dia_combobox.pack(side="left", padx=10)

frame_tabla = tk.Frame(root)
frame_tabla.pack(expand=True, fill="both", padx=10, pady=10)

scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")

tree = ttk.Treeview(frame_tabla, show="headings", xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
tree.pack(side="left", expand=True, fill="both")
scroll_x.config(command=tree.xview)
scroll_y.config(command=tree.yview)

resumen_var = tk.StringVar()
tk.Label(root, textvariable=resumen_var, font=("Arial", 13, "bold"), bg="#1e1e2f", fg="#00FFAA").pack(pady=10)

def mostrar_dia(indice):
    for i in tree.get_children():
        tree.delete(i)

    vector = vectores_por_dia[indice]
    max_id = max((c["id"] for fila in vector for c in fila.get("clientes_activos", [])), default=0)
    cliente_columns = [f"cliente_{i}" for i in range(1, max_id + 1)]
    all_columns = columns + cliente_columns

    tree["columns"] = all_columns
    tree["displaycolumns"] = all_columns
    for col in all_columns:
        ancho = 180 if col == "evento" else 120
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=ancho, anchor='center', stretch=False)
    for fila in vector:
        base = [fila.get(col, '') for col in columns]
        estado_por_id = {
            c['id']: f"{c['estado']} ({c['hora_refrigerio']})" if c['hora_refrigerio'] else c['estado']
            for c in fila.get("clientes_activos", [])
        }
        cliente_info = [estado_por_id.get(i, '') for i in range(1, max_id + 1)]
        tree.insert("", "end", values=base + cliente_info)

def simular():
    try:
        dias = int(entry_dias.get())
        filas = int(entry_filas.get())
        desde_minuto = float(entry_desde.get())
        umbral = int(entry_umbral.get())

        vectores_por_dia.clear()
        for i in tree.get_children():
            tree.delete(i)

        total_recaudacion = 0
        total_gastos = 0
        total_ganancia = 0
        dias_que_superan_x = 0

        for dia in range(1, dias + 1):
            vector, rec, gastos, supera = simular_dia(dia, filas, desde_minuto, umbral)
            vectores_por_dia.append(vector)
            total_recaudacion += rec
            total_gastos += gastos
            total_ganancia += (rec - gastos)
            dias_que_superan_x += supera

        probabilidad = dias_que_superan_x / dias
        resumen_var.set(
            f"Recaudación total: ${total_recaudacion} | Gastos: ${total_gastos} | Ganancia: ${total_ganancia} | Prob. superar {umbral}: {probabilidad:.2%}"
        )

        dia_combobox['values'] = [f"Día {i+1}" for i in range(len(vectores_por_dia))]
        dia_combobox.current(0)
        mostrar_dia(0)

    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese números válidos.")

btn.config(command=simular)
dia_combobox.bind("<<ComboboxSelected>>", lambda e: mostrar_dia(dia_combobox.current()))
root.mainloop()