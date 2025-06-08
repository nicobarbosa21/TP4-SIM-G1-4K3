import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
from simulacion.motor import simular_dia

st.set_page_config(layout="wide")
st.title("Simulador de Peluquería Look")

# --- Función para expandir clientes activos como columnas ---
def expandir_clientes(filas):
    nuevas_filas = []
    max_id = 0
    for fila in filas:
        ids = [c["id"] for c in fila.get("clientes_activos", [])]
        if ids:
            max_id = max(max_id, max(ids))
    for fila in filas:
        base = {k: v for k, v in fila.items() if k != "clientes_activos"}
        estado_por_id = {
            c["id"]: f'{c["estado"]} ({c["hora_refrigerio"]})' if c["hora_refrigerio"] else c["estado"]
            for c in fila.get("clientes_activos", [])
        }
        for i in range(1, max_id + 1):
            base[f"cliente_{i}"] = estado_por_id.get(i, "")
        nuevas_filas.append(base)
    return nuevas_filas

# --- SIDEBAR: PARÁMETROS DE ENTRADA ---
with st.sidebar:
    st.header("Parámetros de Simulación")
    dias = st.number_input("Cantidad de días a simular", min_value=1, value=1)
    filas = st.number_input("Filas a mostrar (i)", min_value=1, value=10)
    desde_minuto = st.number_input("Desde qué minuto mostrar (j)", min_value=0.0, value=0.0, step=1.0)
    umbral = st.number_input("Umbral máximo de personas esperando (x)", min_value=0, value=10)
    st.subheader("Probabilidades")
    prob_colorista = st.number_input("Probabilidad de Colorista (0-1)", min_value=0.0, max_value=1.0, value=0.15)
    prob_a = st.number_input("Probabilidad de Peluquero A (0-1)", min_value=0.0, max_value=1.0, value=0.45)
    if prob_colorista + prob_a > 1:
        st.error("La suma de probabilidades de Colorista y A debe ser menor o igual a 1")
    st.subheader("Distribuciones de Tiempo")
    llegada_min = st.number_input("Llegada - Mínimo", min_value=0.0, value=2.0)
    llegada_max = st.number_input("Llegada - Máximo", min_value=llegada_min, value=12.0)
    st.divider()
    colorista_min = st.number_input("Colorista - Mínimo", min_value=0.0, value=30.0)
    colorista_max = st.number_input("Colorista - Máximo", min_value=colorista_min, value=50.0)
    st.divider()
    a_min = st.number_input("Peluquero A - Mínimo", min_value=0.0, value=21.0)
    a_max = st.number_input("Peluquero A - Máximo", min_value=a_min, value=25.0)
    st.divider()
    b_min = st.number_input("Peluquero B - Mínimo", min_value=0.0, value=22.0)
    b_max = st.number_input("Peluquero B - Máximo", min_value=b_min, value=38.0)
    st.divider()
    simular_btn = st.button("Simular")

# Inicializar vectores en session_state
if "vectores_por_dia" not in st.session_state:
    st.session_state.vectores_por_dia = []
    st.session_state.total_rec = 0
    st.session_state.total_gastos = 0
    st.session_state.dias_superan_x = 0

# --- SIMULACIÓN ---
if simular_btn:
    if prob_colorista + prob_a <= 1:
        st.session_state.vectores_por_dia = []
        st.session_state.total_rec = 0
        st.session_state.total_gastos = 0
        st.session_state.dias_superan_x = 0

        for dia in range(1, dias + 1):
            vec, rec, gastos, supera = simular_dia(
                numero_dia=dia,
                i=filas,
                j=desde_minuto,
                x=umbral,
                llegada=(llegada_min, llegada_max),
                colorista_tiempo=(colorista_min, colorista_max),
                peluquero_a_tiempo=(a_min, a_max),
                peluquero_b_tiempo=(b_min, b_max),
                prob_colorista=prob_colorista,
                prob_a=prob_a
            )
            for fila in vec:
                fila["nro_fila"] = str(fila["nro_fila"])  # evitar error de conversión a int
            st.session_state.vectores_por_dia.append(vec)
            st.session_state.total_rec += rec
            st.session_state.total_gastos += gastos
            st.session_state.dias_superan_x += supera

        st.success("Simulación completada.")

# --- MOSTRAR RESULTADOS SI EXISTEN ---
if st.session_state.vectores_por_dia:
    st.subheader("Resumen Global")
    total_rec = st.session_state.total_rec
    total_gastos = st.session_state.total_gastos
    st.markdown(f"- Recaudación total: ${total_rec:,.2f}")
    st.markdown(f"- Promedio diario de recaudacion: ${total_rec/dias:,.2f}")
    st.markdown(f"- Gastos totales: ${total_gastos:,.2f}")
    st.markdown(f"- Promedio diario de gastos: ${total_gastos/dias:,.2f}")
    st.markdown(f"- Ganancia: ${(total_rec - total_gastos):,.2f}")
    st.markdown(f"- Promedio diario de ganancia: ${(total_rec - total_gastos)/dias:,.2f}")
    st.markdown(f"- Probabilidad de superar {umbral}: {st.session_state.dias_superan_x / len(st.session_state.vectores_por_dia):.2%}")

    st.subheader("Vector de Estado por Día")
    dia_sel = st.selectbox("Seleccionar Día", range(1, len(st.session_state.vectores_por_dia) + 1))
    vec_dia = st.session_state.vectores_por_dia[dia_sel - 1]

    data_expandida = expandir_clientes(vec_dia)
    df_dia = pd.DataFrame(data_expandida)

    # Forzar columnas booleanas a tipo bool para que se vean como True/False
    for col in ["se_puede_recibir_clientes", "termino_dia"]:
        if col in df_dia.columns:
            df_dia[col] = df_dia[col].astype(bool)

    # Eliminar columna 'index' si existe
    if "index" in df_dia.columns:
        df_dia = df_dia.drop(columns=["index"])

    # Configurar ancho de columnas de clientes
    column_config = {}
    for col in df_dia.columns:
        if col.startswith("cliente_"):
            column_config[col] = st.column_config.TextColumn(width=100)

    # Reasignar el índice para que empiece en 1
    df_dia.index = range(1, len(df_dia) + 1)

    # Mostrar la tabla con el índice iniciando en 1
    st.dataframe(
        df_dia,
        use_container_width=True,
        height=min(20, len(df_dia)) * 35 + 40,
        column_config=column_config
    )

    # Exportar
    if st.button("Exportar a Excel"):
        with pd.ExcelWriter("simulacion_peluqueria.xlsx") as writer:
            for i, vec in enumerate(st.session_state.vectores_por_dia, start=1):
                expandido = expandir_clientes(vec)
                pd.DataFrame(expandido).to_excel(writer, sheet_name=f"Día {i}", index=False)
        st.success("Simulación exportada a 'simulacion_peluqueria.xlsx'.")