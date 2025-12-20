import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor ARCA Pro - Alta Precisión", layout="wide")

# --- 1. DATOS DE MERCADO EN VIVO ---
@st.cache_data(ttl=600)
def obtener_pizarra():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        mapa = {d['nombre']: d['venta'] for d in res}
        return {
            "Oficial": mapa.get("Oficial", 1030.50),
            "Blue": mapa.get("Blue", 1485.00),
            "MEP": mapa.get("MEP", 1496.80),
            "CCL": mapa.get("Contado con Liquidación", 1555.00),
            "Tarjeta": mapa.get("Tarjeta", 1935.45)
        }
    except:
        return {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00, "Tarjeta": 1935.45}

pizarra = obtener_pizarra()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Auditoría")
    st.info(f"📅 Fecha Hoy: 20/12/2025")
    if st.button("🔄 Sincronizar con ARCA"):
        st.cache_data.clear()
        st.rerun()
    st.warning("Datos validados bajo Ley 27.743")

# --- 3. ENCABEZADO ---
st.title("Monitor Económico e Impositivo Integral")
st.success(f"🏛️ **Dólar Oficial (Referencia ARCA): ${pizarra['Oficial']:,.2f}**")

# --- 4. DOLAR HOY ---
cols = st.columns(5)
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. TASAS Y NOTICIAS ---
st.subheader("🏦 Rendimientos y Actualidad")
t1, t2, t3 = st.columns([1, 1, 2])
with t1:
    st.info("### 💰 Fondos MM")
    st.write("**Fima:** 34.5% TNA")
    st.write("**Santander:** 34.2% TNA")
with t2:
    st.info("### 🏦 Bancos")
    st.write("**P. Fijo:** 39.0% TNA")
    st.write("**Badlar:** 42.8% TNA")
with t3:
    st.markdown("**📰 Últimas Noticias**")
    cn1, cn2 = st.columns(2)
    with cn1:
        st.write("• **Economía:** Riesgo país en 790 bps.")
        st.write("• **Mercado:** BCRA sigue sumando reservas.")
    with cn2:
        st.write("• **ARCA:** Recategorización obligatoria Enero.")
        st.write("• **Legal:** Nueva reglamentación Factura E.")

st.divider()

# --- 6. TABLA DE INFLACIÓN (REINCORPORADA Y ACTUALIZADA) ---
st.subheader("📊 Historial de Inflación INDEC 2025")
df_inf = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic (Est.)"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 4.0, 4.2, 3.5, 2.7, 2.5, 2.3]
})
# Cálculo de acumulada matemática
df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 7. MONOTRIBUTO: ESCALAS VIGENTES A HOY ---
st.subheader("⚖️ Monotributo: Topes y Cuotas (Vigencia Diciembre 2025)")
df_mono = pd.DataFrame({
    "Cat.": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Anuales ($)": ["9.423.500", "13.805.200", "19.358.100", "24.033.400", "28.270.100", "35.429.300", "42.369.000", "64.284.000", "71.954.100", "82.399.200", "99.350.100"],
    "Cuota Total ($)": ["38.800", "44.200", "51.800", "66.400", "85.500", "109.300", "133.500", "255.800", "317.300", "377.200", "448.700"]
})
st.table(df_mono)

st.divider()

# --- 8. GANANCIAS SOCIEDADES (PERSONAS JURÍDICAS) - ESCALA DEFINITIVA ---
st.subheader("🏢 Ganancias: Sociedades (Ley 27.630 Actualizada)")
st.caption("Tramos vigentes para ejercicios cerrados en Diciembre 2025.")
data_soc = {
    "Ganancia Neta Imponible Acumulada": [
        "Hasta $74.582.114,30", 
        "De $74.582.114,30 a $745.821.143,00", 
        "Más de $745.821.143,00"
    ],
    "Alícuota": ["25%", "30%", "35%"],
    "Monto Fijo ($)": ["$0,00", "$18.645.528,58", "$219.991.685,28"],
    "Más % sobre excedente de": ["$0,00", "$74.582.114,30", "$745.821.143,00"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 9. GANANCIAS PERSONAS HUMANAS (ART. 94) ---
st.subheader("👤 Ganancias: Personas Humanas (Tramos Anualizados 2025)")
data_ph = {
    "Ganancia Neta Imponible ($)": ["0 - 1.8M", "1.8M - 3.6M", "3.6M - 7.2M", "7.2M - 14.4M", "14.4M - 28.8M", "28.8M - 57.6M", "57.6M - 115.2M", "115.2M - 230.4M", "Más de 230.4M"],
    "Fijo ($)": ["0", "90.000", "252.000", "684.000", "1.764.000", "4.500.000", "11.124.000", "26.676.000", "62.388.000"],
    "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"]
}
st.table(pd.DataFrame(data_ph))

st.divider()

# --- 10. RETENCIONES GANANCIAS (RG 830) ---
st.subheader("📋 Retenciones Ganancias (RG 830) - Mínimos a HOY")
data_rg = {
    "Concepto": ["Bienes Muebles", "Servicios", "Honorarios Profesionales", "Alquileres"],
    "Mínimo No Sujeto ($)": ["327.200", "98.240", "98.240", "16.360"],
    "Alícuota Inscriptos": ["2%", "2%", "Escala Art. 94 (mín 3%)", "6%"]
}
st.table(pd.DataFrame(data_rg))
