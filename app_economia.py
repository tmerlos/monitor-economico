import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor ARCA & Economía", layout="wide")

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
    st.title("Panel de Control")
    if st.button("🔄 Sincronizar Datos"):
        st.cache_data.clear()
        st.rerun()
    st.info("Fuente: ARCA (Ex-AFIP)\nPeríodo Fiscal Vigente")

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

# --- 5. RENDIMIENTOS E INFLACIÓN ---
st.subheader("🏦 Rendimientos y Precios")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos MM")
    st.write("**Fima Premium:** 34.5% TNA")
    st.write("**Santander Ahorro:** 34.2% TNA")
with t2:
    st.info("### 🏦 Plazo Fijo")
    st.write("**TNA Promedio:** 39.5%")
with t3:
    st.warning("### 📈 Inflación (IPC)")
    st.write("**Último Mes:** 2.5%")
    st.write("**Acumulada Anual:** 115.4%")

# --- 6. TABLA DE INFLACIÓN ---
data_inf = {
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5]
}
df_inf = pd.DataFrame(data_inf)
df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 7. MONOTRIBUTO: ESCALAS VIGENTES (REFORMA FISCAL) ---
st.subheader("⚖️ Monotributo: Topes y Cuotas Mensuales")
st.caption("Valores actualizados según la Ley de Medidas Fiscales Paliativas (Vigente).")
df_mono = pd.DataFrame({
    "Cat.": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Brutos Anuales ($)": ["6.450.000", "9.450.000", "13.250.000", "16.450.000", "19.350.000", "24.250.000", "29.000.000", "44.000.000", "49.250.000", "56.400.000", "68.000.000"],
    "Cuota Total Srv ($)": ["26.600", "30.280", "35.458", "45.443", "58.519", "74.825", "91.419", "175.091", "-", "-", "-"],
    "Cuota Total Bienes ($)": ["26.600", "30.280", "34.458", "44.443", "54.119", "67.825", "80.419", "115.091", "155.120", "198.150", "246.130"]
})
st.table(df_mono)

st.divider()

# --- 8. GANANCIAS JURÍDICAS (SOCIEDADES) ---
st.subheader("🏢 Ganancias Sociedades (Ley 27.630)")
data_soc = {
    "Ganancia Neta Imponible Acumulada": ["Hasta $51.048.000", "De $51.048.000 a $510.480.000", "Más de $510.480.000"],
    "Alícuota": ["25%", "30%", "35%"],
    "Monto Fijo": ["$0", "$12.762.000", "$150.591.600"],
    "Sobre el excedente de": ["$0", "$51.048.000", "$510.480.000"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 9. GANANCIAS PERSONAS HUMANAS (ART. 94) ---
st.subheader("👤 Ganancias Personas Humanas: Escala Progresiva")
st.caption("Tramos anualizados actualizados por IPC/RIPTE.")

data_ph = {
    "Ganancia Neta Imponible ($)": ["0 - 2.853k", "2.853k - 5.706k", "5.706k - 8.559k", "8.559k - 11.412k", "11.412k - 17.118k", "17.118k - 22.824k", "22.824k - 34.236k", "34.236k - 45.648k", "Más de 45.648k"],
    "Monto Fijo ($)": ["0", "142.650", "399.420", "741.780", "1.169.730", "2.253.870", "3.566.250", "6.647.490", "10.185.210"],
    "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"]
}
st.table(pd.DataFrame(data_ph))

st.divider()

# --- 10. RETENCIONES RG 830 ---
st.subheader("📋 Retenciones Ganancias (RG 830)")
data_rg = {
    "Concepto de Pago": ["Bienes Muebles", "Locaciones de Servicios", "Honorarios Profesionales", "Alquileres"],
    "Mínimo No Sujeto ($)": ["224.000", "67.170", "67.170", "11.200"],
    "Alícuota Inscriptos": ["2%", "2%", "Escala Art. 94 (mín 3%)", "6%"]
}
st.table(pd.DataFrame(data_rg))
