import pandas as pd
from openpyxl import load_workbook

def exportar_simulacion_a_excel(vectores_por_dia, ruta="simulacion_peluqueria.xlsx"):
    escritor = pd.ExcelWriter(ruta, engine='xlsxwriter')

    for i, vector in enumerate(vectores_por_dia):
        filas = []
        for fila in vector:
            fila_salida = dict(fila)
            clientes = fila_salida.pop("clientes_activos", [])
            for cliente in clientes:
                col = f"cliente_{cliente['id']}"
                desc = f"{cliente['estado']} ({cliente['hora_refrigerio']})" if cliente['hora_refrigerio'] else cliente['estado']
                fila_salida[col] = desc
            filas.append(fila_salida)

        df = pd.DataFrame(filas)

        # Redondear flotantes
        for col in df.select_dtypes(include=['float', 'float64']).columns:
            df[col] = df[col].round(2)

        sheet_name = f"Día {i+1}"
        df.to_excel(escritor, sheet_name=sheet_name, index=False)

    escritor.close()

    # Ajuste de columnas usando openpyxl
    wb = load_workbook(ruta)
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))
            adjusted_width = max(12, min(max_len * 1.2, 80))  # límites razonables
            ws.column_dimensions[col_letter].width = adjusted_width
    wb.save(ruta)
