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
        # Redondear todos los números flotantes a 2 decimales
        for col in df.select_dtypes(include=['float', 'float64']).columns:
            df[col] = df[col].round(2)
        sheet_name = f"Día {i+1}"
        df.to_excel(escritor, sheet_name=sheet_name, index=False)

        worksheet = escritor.sheets[sheet_name]
        number_format = escritor.book.add_format({'num_format': '0.00'})
        for idx, col in enumerate(df.columns):
            max_len = max(
                df[col].astype(str).map(len).max(),
                len(str(col))
            )
            min_width = 50  # Aumenta este valor si sigue el problema
            ancho = max(int(max_len * 2) + 2, min_width)
            if pd.api.types.is_numeric_dtype(df[col]):
                worksheet.set_column(idx, idx, ancho, number_format)
            else:
                worksheet.set_column(idx, idx, ancho)

    escritor.close()