import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor ARCA 2025", layout="wide")

# --- 1. DATOS DE MERCADO ---
@st.cache_data(ttl=600)
def obtener_pizarra():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=3).json()
        datos = {d['nombre']: d['venta'] for d in res}
        return {
            "Oficial": datos.get("Oficial", 1030.5),
            "Blue": datos.get("Blue", 1485.0),
            "MEP": datos.get("MEP", 1496.8),
            "CCL": datos.get("Contado con Liquidación", 1555.0),
            "Tarjeta": datos.get("Tarjeta", 1935.45)
        }
    except:
        return {"Oficial": 1030.5, "Blue": 1485.0, "MEP": 1496.8, "CCL": 1555.0, "Tarjeta": 1935.45}

pizarra = obtener_pizarra()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel ARCA 2025")
    st.info("Periodo Fiscal Actualizado: **Diciembre 2025**")
    if st.button("🔄 Refrescar Monitor"):
        st.cache_data.clear()
        st.rerun()

# --- 3. ENCABEZADO ---
col1, col2 = st.columns([1, 12])
with col1: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col2: st.title("Monitor Económico e Impositivo Integral")
st.success(f"🏛️ **Dólar Oficial (Referencia ARCA): ${pizarra['Oficial']:,.2f}**")

# --- 4. COTIZACIONES ---
cols = st.columns(5)
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. TASAS E INFLACIÓN ---
st.subheader("🏦 Rendimientos e Inflación")
t1, t2 = st.columns(2)
with t1:
    st.info("### 💰 Tasas de Referencia")
    st.write("**Fima Premium / Santander:** ~34.5% TNA")
    st.write("**Plazo Fijo Bancos:** ~39.0% TNA")
with t2:
    data_inf = {
        "Mes": ["Jul", "Ago", "Sep", "Oct", "Nov"],
        "IPC Mensual": ["4.0%", "4.2%", "3.5%", "2.7%", "2.5%"],
        "Acumulada 2025": ["87.0%", "94.8%", "101.6%", "107.1%", "112.3%"]
    }
    st.table(pd.DataFrame(data_inf))

st.divider()

# --- 6. MONOTRIBUTO: ÚLTIMAS ESCALAS LEY 27.743 ---
st.subheader("⚖️ Monotributo: Escalas Vigentes (ARCA 2025/2026)")
st.caption("Topes de facturación anual tras la última reforma fiscal.")
df_mono = pd.DataFrame({
    "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Brutos Anuales": ["$6.450.000", "$9.450.000", "$13.250.000", "$16.450.000", "$19.350.000", "$24.250.000", "$29.000.000", "$44.000.000", "$49.250.000", "$56.400.000", "$68.000.000"],
    "Cuota Mensual (Promedio)": ["$26.600", "$30.280", "$35.458", "$45.443", "$58.519", "$74.825", "$91.419", "$175.091", "$217.120", "$258.150", "$307.130"]
})
st.table(df_mono)

st.divider()

# --- 7. GANANCIAS SOCIEDADES (PERSONAS JURÍDICAS) ---
st.subheader("🏢 Impuesto a las Ganancias: Sociedades")
st.write("Tramos actualizados por el índice de precios (IPC) para el ejercicio 2025:")
data_soc = {
    "Ganancia Neta Imponible Acumulada": ["Hasta $51.048.000", "$51.048.000 a $510.480.000", "Más de $510.480.000"],
    "Alícuota": ["25%", "30%", "35%"],
    "Paga Fijo": ["$0", "$12.762.000", "$150.591.600"],
    "Sobre el excedente de": ["$0", "$51.048.000", "$510.480.000"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 8. GANANCIAS PERSONAS HUMANAS (ESCALA ART. 94) ---
st.subheader("👤 Ganancias Personas Humanas: Escala Progresiva 2025")
st.caption("Valores anualizados vigentes tras la actualización del paquete fiscal.")
data_ph = {
    "Ganancia Neta Imponible ($)": ["0 a 1.2M", "1.2M a 2.4M", "2.4M a 4.8M", "4.8M a 9.6M", "9.6M a 19.2M", "19.2M a 38.4M", "38.4M a 76.8M", "76.8M a 153.6M", "Más de 153.6M"],
    "Monto Fijo ($)": ["0", "60.000", "168.000", "456.000", "1.176.000", "3.000.000", "7.416.000", "17.784.000", "41.592.000"],
    "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"]
}
st.table(pd.DataFrame(data_ph))

st.divider()

# --- 9. RETENCIONES GANANCIAS (RG 830) ---
st.subheader("📋 Retenciones Ganancias RG 830 - Mínimos Vigentes")
data_rg = {
    "Concepto": ["Bienes Muebles", "Locaciones de Servicios", "Honorarios Profesionales", "Alquileres"],
    "Mínimo No Sujeto ($)": ["224.000", "67.170", "67.170", "11.200"],
    "Inscripto (%)": ["2%", "2%", "Escala Art. 94 (mín 3%)", "6%"]
}
st.table(pd.DataFrame(data_rg))
