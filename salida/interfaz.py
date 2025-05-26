import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk, messagebox
from simulacion.motor import simular_dia

def simular():
    try:
        dias = int(entry_dias.get())
        filas = int(entry_filas.get())
        desde_minuto = float(entry_desde.get())
        umbral = int(entry_umbral.get())

        for tab in notebook.tabs():
            notebook.forget(tab)

        total_recaudacion = 0
        total_gastos = 0
        total_ganancia = 0
        dias_que_superan_x = 0

        for dia in range(1, dias + 1):
            vector, rec, costos, supera = simular_dia(dia, filas, desde_minuto, umbral)

            max_id = 0
            for fila in vector:
                for c in fila.get("clientes_activos", []):
                    if c["id"] > max_id:
                        max_id = c["id"]

            cliente_columns = [f"cliente_{i}" for i in range(1, max_id + 1)]

            frame_dia = ttk.Frame(notebook)
            notebook.add(frame_dia, text=f"Día {dia}")

            scroll_x = tk.Scrollbar(frame_dia, orient="horizontal")
            scroll_y = tk.Scrollbar(frame_dia, orient="vertical")
            scroll_x.pack(side="bottom", fill="x")
            scroll_y.pack(side="right", fill="y")

            tree = ttk.Treeview(frame_dia, columns=columns + cliente_columns, show="headings", xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
            for col in columns + cliente_columns:
                tree.heading(col, text=col.replace("_", " ").title())
                tree.column(col, width=120, anchor='center')

            tree.pack(side="left", expand=True, fill="both")
            scroll_x.config(command=tree.xview)
            scroll_y.config(command=tree.yview)

            for fila in vector:
                base = [fila.get(col, '') for col in columns]
                estado_por_id = {
                    c['id']: f"{c['estado']} ({c['hora_refrigerio']})" if c['hora_refrigerio'] else c['estado']
                    for c in fila.get("clientes_activos", [])
                }
                cliente_info = [estado_por_id.get(i, '') for i in range(1, max_id + 1)]
                tree.insert("", "end", values=base + cliente_info)

            total_recaudacion += rec
            total_gastos += costos
            total_ganancia += (rec - costos)
            dias_que_superan_x += supera

        probabilidad = dias_que_superan_x / dias
        resumen_var.set(
            f"Recaudación total: ${total_recaudacion} | Gastos: ${total_gastos} | Ganancia: ${total_ganancia} | Prob. superar {umbral}: {probabilidad:.2%}"
        )

    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese números válidos.")

root = tk.Tk()
root.title("Simulador Peluquería Look")
root.geometry("1400x750")
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

btn = tk.Button(root, text="Simular", command=simular, bg="#ffffff", fg="black", font=("Arial", 11, "bold"))
btn.pack(pady=10)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

columns = [
    "nro_fila", "reloj", "evento", "cliente_id", "rnd_cliente", "tiempo_entre_llegadas", "proxima_llegada",
    "rnd_atencion", "servidor_a_atender", "se_puede_recibir_clientes", "termino_dia",
    "rnd_peluquero_a", "tiempo_atencion_a", "fin_atencion_a", "peluquero_a_estado", "cola_a",
    "rnd_peluquero_b", "tiempo_atencion_b", "fin_atencion_b", "peluquero_b_estado", "cola_b",
    "rnd_colorista", "tiempo_atencion_c", "fin_atencion_c", "colorista_estado", "cola_colorista",
    "recaudacion", "costos", "ganancia", "numero_dia", "personas_esperando", "maximo_cola", "supero_umbral_x"
]

resumen_var = tk.StringVar()
tk.Label(root, textvariable=resumen_var, font=("Arial", 13, "bold"), bg="#1e1e2f", fg="#00FFAA").pack(pady=10)

root.mainloop()
