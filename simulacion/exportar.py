import pandas as pd

def exportar_simulacion_a_excel(vectores_por_dia, ruta="simulacion_peluqueria.xlsx"):
    escritor = pd.ExcelWriter(ruta, engine='xlsxwriter')

    for i, vector in enumerate(vectores_por_dia):
        filas = []
        for fila in vector:
            fila_salida = dict(fila)  # copia base
            clientes = fila_salida.pop("clientes_activos", [])
            for cliente in clientes:
                col = f"cliente_{cliente['id']}"
                desc = f"{cliente['estado']} ({cliente['hora_refrigerio']})" if cliente['hora_refrigerio'] else cliente['estado']
                fila_salida[col] = desc
            filas.append(fila_salida)
        
        df = pd.DataFrame(filas)
        df.to_excel(escritor, sheet_name=f"Día {i+1}", index=False)

    escritor.close()