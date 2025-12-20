import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor Económico Integral", layout="wide")

# --- 1. CARGA DE DATOS ---
VALORES_BACKUP = {
    "Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80,
    "CCL": 1555.00, "Tarjeta": 1935.45, "Cripto": 1541.00
}

@st.cache_data(ttl=600)
def obtener_pizarra():
    datos = VALORES_BACKUP.copy()
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=3).json()
        for d in res:
            nombre = d['nombre']
            if nombre == "Oficial": datos["Oficial"] = d['venta']
            elif nombre == "Blue": datos["Blue"] = d['venta']
            elif nombre == "MEP": datos["MEP"] = d['venta']
            elif nombre == "Contado con Liquidación": datos["CCL"] = d['venta']
            elif nombre == "Tarjeta": datos["Tarjeta"] = d['venta']
    except: pass
    return datos

pizarra = obtener_pizarra()

# --- 2. BARRA LATERAL ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Control")
    if st.button("🔄 Actualizar Mercados"):
        st.cache_data.clear()
        st.rerun()
    st.info("Valores vigentes al: 20/12/2025")

# --- 3. ENCABEZADO ---
col_tit1, col_tit2 = st.columns([1, 15])
with col_tit1: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_tit2: st.title("Monitor Económico e Impositivo Integral")

st.success(f"🏛️ **Dólar Oficial BCRA: ${pizarra['Oficial']:,.2f}**")
st.divider()

# --- 4. PIZARRA DE DÓLARES ---
st.subheader("💵 Cotizaciones de Mercado")
cols = st.columns(6)
nombres_d = ["Blue", "MEP", "CCL", "Tarjeta", "Cripto", "Oficial"]
for i, n in enumerate(nombres_d):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${pizarra[n]:,.2f}")

st.divider()

# --- 5. RENDIMIENTOS Y TASAS (ARRIBA DE INFLACIÓN) ---
st.subheader("🏦 Rendimientos Financieros")
c1, c2, c3 = st.columns(3)
with c1:
    st.info("### 💰 Fondos Money Market")
    st.write("**Fima Premium:** 34.5% TNA")
    st.write("**Santander Ahorro:** 34.2% TNA")
with c2:
    st.info("### 🏦 Plazos Fijos")
    st.write("**TNA Minorista:** 38.0% - 41.0%")
    st.write("**Tasa Badlar:** 42.5% anual")
with c3:
    st.warning("### 💳 Tasas Activas")
    st.write("**Personales:** 65% - 82% TNA")
    st.write("**Adelanto Cta Cte:** 58% TNA")

st.divider()

# --- 6. INFLACIÓN ---
st.subheader("📊 Historial de Inflación INDEC")
df_inf = pd.DataFrame({
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre"],
    "IPC (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5],
})
st.dataframe(df_inf.T, use_container_width=True)
st.caption("Fuente: INDEC. Último dato acumulado interanual: 115.4% aprox.")

st.divider()

# --- 7. TABLA MONOTRIBUTO 2026 ---
st.subheader("⚖️ Categorías Monotributo (Enero 2026)")
data_mono = {
    "Cat.": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Brutos Anuales ($)": ["7.2M", "10.5M", "14.8M", "18.3M", "21.6M", "27.0M", "32.4M", "48.2M", "54.1M", "62.1M", "75.0M"],
    "Cuota Total Prom. ($)": ["31k", "39k", "48k", "62k", "85k", "108k", "131k", "245k", "320k", "380k", "460k"]
}
st.table(pd.DataFrame(data_mono))

st.divider()

# --- 8. IMPUESTO A LAS GANANCIAS ---
st.subheader("🏢 Impuesto a las Ganancias: Personas Jurídicas")
st.write("Alícuotas progresivas según la ganancia neta imponible acumulada:")
data_juridica = {
    "Ganancia Neta ($)": ["$0 a $25M", "Más de $25M a $250M", "Más de $250M"],
    "Pagan": ["25%", "$6.25M + 30% s/ excedente", "$73.75M + 35% s/ excedente"]
}
st.table(pd.DataFrame(data_juridica))

st.subheader("👤 Impuesto a las Ganancias: Personas Humanas")
st.caption("Escala del Art. 94 de la Ley de Impuesto a las Ganancias (Valores Actualizados)")
data_humana = {
    "Ganancia Neta Imponible ($)": ["Hasta $2M", "$2M a $4M", "$4M a $8M", "Más de $32M"],
    "Fijo ($)": ["$0", "$100k", "$350k", "$8.5M"],
    "Alícuota %": ["5%", "9%", "12%", "35%"]
}
st.table(pd.DataFrame(data_humana))

st.divider()

# --- 9. RETENCIONES RG 830 ---
st.subheader("📋 Retenciones RG 830 (Resumen)")
data_rg830 = {
    "Concepto": ["Bienes", "Servicios", "Honorarios", "Alquileres"],
    "Mínimo ($)": ["224.000", "67.000", "67.000", "11.200"],
    "Inscripto": ["2%", "2%", "Escala Art. 94", "6%"]
}
st.table(pd.DataFrame(data_rg830))
