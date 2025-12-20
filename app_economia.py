import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor Económico Profesional", layout="wide")

# --- 1. DATOS DE MERCADO ---
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
    st.title("Control de Datos")
    if st.button("🔄 Refrescar Cotizaciones"):
        st.cache_data.clear()
        st.rerun()
    st.info("Periodo Fiscal: 2025\nActualizado a Dic 2025")

# --- 3. ENCABEZADO ---
col_tit1, col_tit2 = st.columns([1, 15])
with col_tit1: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_tit2: st.title("Monitor Económico e Impositivo Integral")

st.success(f"🏛️ **Dólar Oficial BCRA (Referencia): ${pizarra['Oficial']:,.2f}**")
st.divider()

# --- 4. PIZARRA DE DÓLARES ---
st.subheader("💵 Cotizaciones de Divisas")
cols = st.columns(6)
nombres_d = ["Blue", "MEP", "CCL", "Tarjeta", "Cripto", "Oficial"]
for i, n in enumerate(nombres_d):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${pizarra[n]:,.2f}")

st.divider()

# --- 5. TASAS Y RENDIMIENTOS ---
st.subheader("🏦 Rendimientos Financieros")
c1, c2, c3 = st.columns(3)
with c1:
    st.info("### 💰 Fondos Money Market")
    st.write("**Fima Premium:** 34.5% TNA")
    st.write("**Santander Ahorro:** 34.2% TNA")
with c2:
    st.info("### 🏦 Plazos Fijos")
    st.write("**TNA Minorista:** 39.5% (Promedio)")
    st.write("**Tasa Badlar:** 42.5% anual")
with c3:
    st.warning("### 💳 Tasas Activas")
    st.write("**Préstamos Personales:** 78% TNA")
    st.write("**Adelanto Cta Cte:** 62% TNA")

st.divider()

# --- 6. INFLACIÓN ---
st.subheader("📊 Historial de Inflación INDEC")
df_inf = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"],
    "IPC (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5],
})
st.dataframe(df_inf.T, use_container_width=True)

st.divider()

# --- 7. MONOTRIBUTO 2026 ---
st.subheader("⚖️ Escalas Monotributo (Vigencia Ene-2026)")
data_mono = {
    "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Brutos Anuales": ["$7.200.000", "$10.500.000", "$14.800.000", "$18.300.000", "$21.600.000", "$27.000.000", "$32.400.000", "$48.200.000", "$54.100.000", "$62.100.000", "$75.000.000"],
    "Cuota Mensual (Prom.)": ["$31.200", "$39.400", "$48.100", "$62.500", "$85.300", "$108.200", "$131.000", "$245.000", "$320.000", "$380.000", "$460.000"]
}
st.table(pd.DataFrame(data_mono))

st.divider()

# --- 8. GANANCIAS SOCIEDADES (PERSONAS JURÍDICAS) ---
st.subheader("🏢 Impuesto a las Ganancias: Sociedades")
st.write("Alícuotas vigentes para el ejercicio 2025 (Escala Progresiva):")
data_juridica = {
    "Ganancia Neta Imponible Acumulada": ["Hasta $50.000.000", "Más de $50.000.000 a $500.000.000", "Más de $500.000.000"],
    "Alícuota / Pago": ["25%", "$12.500.000 + 30% sobre el excedente de $50M", "$147.500.000 + 35% sobre el excedente de $500M"]
}
st.table(pd.DataFrame(data_juridica))

st.divider()

# --- 9. GANANCIAS PERSONAS HUMANAS (ART. 94) ---
st.subheader("👤 Impuesto a las Ganancias: Personas Humanas")
st.caption("Escala Progresiva Anualizada - Período Fiscal 2025")
data_humana = {
    "Ganancia Neta Imponible Acumulada ($)": [
        "0 a 2.500.000", "2.500.000 a 5.000.000", "5.000.000 a 10.000.000", 
        "10.000.000 a 20.000.000", "20.000.000 a 40.000.000", "40.000.000 a 80.000.000", 
        "80.000.000 a 160.000.000", "160.000.000 a 320.000.000", "Más de 320.000.000"
    ],
    "Paga Fijo ($)": ["0", "125.000", "350.000", "950.000", "2.550.000", "6.350.000", "15.950.000", "39.150.000", "93.550.000"],
    "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"],
    "Sobre Excedente de": ["$0", "$2.5M", "$5M", "$10M", "$20M", "$40M", "$80M", "$160M", "$320M"]
}
st.table(pd.DataFrame(data_humana))

st.divider()

# --- 10. RETENCIONES RG 830 ---
st.subheader("📋 Retenciones Ganancias RG 830")
data_rg = {
    "Concepto": ["Bienes Muebles", "Servicios", "Comisiones", "Alquileres"],
    "Mínimo No Sujeto": ["$224.000", "$67.000", "$31.000", "$11.200"],
    "Inscriptos": ["2%", "2%", "3%", "6%"]
}
st.table(pd.DataFrame(data_rg))
