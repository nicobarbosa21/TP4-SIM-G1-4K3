import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
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

    # Llegada
    llegada_min_default = 2.0
    llegada_max_default = 12.0
    llegada_min = st.number_input("Llegada - Mínimo", min_value=0.0, value=llegada_min_default)
    llegada_max = st.number_input("Llegada - Máximo", min_value=llegada_min, value=max(llegada_min + 1.0, llegada_max_default))

    st.divider()

    # Colorista
    colorista_min_default = 30.0
    colorista_max_default = 50.0
    colorista_min = st.number_input("Colorista - Mínimo", min_value=0.0, value=colorista_min_default)
    colorista_max = st.number_input("Colorista - Máximo", min_value=colorista_min, value=max(colorista_min + 1.0, colorista_max_default))

    st.divider()

    # Peluquero A
    a_min_default = 21.0
    a_max_default = 25.0
    a_min = st.number_input("Peluquero A - Mínimo", min_value=0.0, value=a_min_default)
    a_max = st.number_input("Peluquero A - Máximo", min_value=a_min, value=max(a_min + 1.0, a_max_default))

    st.divider()

    # Peluquero B
    b_min_default = 22.0
    b_max_default = 38.0
    b_min = st.number_input("Peluquero B - Mínimo", min_value=0.0, value=b_min_default)
    b_max = st.number_input("Peluquero B - Máximo", min_value=b_min, value=max(b_min + 1.0, b_max_default))

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
    ganancia = total_rec - total_gastos
    prob = st.session_state.dias_superan_x / len(st.session_state.vectores_por_dia)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Recaudación", f"${total_rec:,.2f}", f"Prom: ${total_rec/dias:,.2f}")
    col2.metric("Gastos", f"${total_gastos:,.2f}", f"Prom: ${total_gastos/dias:,.2f}")
    col3.metric("Ganancia", f"${ganancia:,.2f}", f"Prom: ${ganancia/dias:,.2f}")
    col4.metric(f"Prob. > {umbral}", f"{prob:.2%}")

    st.subheader("Vector de Estado por Día")
    dia_sel = st.selectbox("Seleccionar Día", range(1, len(st.session_state.vectores_por_dia) + 1))
    vec_dia = st.session_state.vectores_por_dia[dia_sel - 1]

    data_expandida = expandir_clientes(vec_dia)
    df_dia = pd.DataFrame(data_expandida)

    for col in ["se_puede_recibir_clientes", "termino_dia"]:
        if col in df_dia.columns:
            df_dia[col] = df_dia[col].astype(bool)

    if "index" in df_dia.columns:
        df_dia = df_dia.drop(columns=["index"])

    column_config = {col: st.column_config.TextColumn(width=100) for col in df_dia.columns if col.startswith("cliente_")}

    df_dia.index = range(1, len(df_dia) + 1)

    st.dataframe(
        df_dia,
        use_container_width=True,
        height=min(15, len(df_dia)) * 35 + 40,
        column_config=column_config
    )

    if st.button("Exportar a Excel"):
        with pd.ExcelWriter("simulacion_peluqueria.xlsx") as writer:
            for i, vec in enumerate(st.session_state.vectores_por_dia, start=1):
                expandido = expandir_clientes(vec)
                pd.DataFrame(expandido).to_excel(writer, sheet_name=f"Día {i}", index=False)
        st.success("Simulación exportada a 'simulacion_peluqueria.xlsx'.")
