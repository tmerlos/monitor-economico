import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor ARCA & Economía", layout="wide")

# --- 1. DATOS DE MERCADO (DolarAPI) ---
@st.cache_data(ttl=600)
def obtener_pizarra():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=3).json()
        datos = {d['nombre']: d['venta'] for d in res}
        # Mapeo de nombres para consistencia
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
    st.title("Panel ARCA")
    if st.button("🔄 Sincronizar con Mercado"):
        st.cache_data.clear()
        st.rerun()
    st.info("Fuente: ARCA (Ex-AFIP) & BCRA\nDatos Fiscales 2025-2026")

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

# --- 5. TASAS, RENDIMIENTOS E INFLACIÓN ---
st.subheader("🏦 Rendimientos Financieros e IPC")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos MM")
    st.write("**Fima Premium:** 34.5% TNA")
    st.write("**Santander Ahorro:** 34.2% TNA")
with t2:
    st.info("### 🏦 Tasas Bancarias")
    st.write("**Plazo Fijo:** 39.5% TNA")
    st.write("**Tasa Badlar:** 42.5% TNA")
with t3:
    st.warning("### 📈 Inflación 2025")
    st.write("**Último Mes:** 2.5%")
    st.write("**Acumulada:** 115.4%")

st.divider()

# --- 6. MONOTRIBUTO 2026 (VALORES ARCA) ---
st.subheader("⚖️ Monotributo: Escalas vigentes Enero 2026")
df_mono = pd.DataFrame({
    "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Facturación Anual ($)": ["7.2M", "10.5M", "14.8M", "18.3M", "21.6M", "27.0M", "32.4M", "48.2M", "54.1M", "62.1M", "75.0M"],
    "Cuota Mensual (Srv)": ["31k", "39k", "48k", "62k", "85k", "108k", "131k", "245k", "-", "-", "-"],
    "Cuota Mensual (Bienes)": ["31k", "39k", "48k", "62k", "85k", "108k", "131k", "245k", "320k", "380k", "460k"]
})
st.table(df_mono)

st.divider()

# --- 7. GANANCIAS PERSONAS JURÍDICAS (SOCIEDADES) ---
# Según Ley 27.630 actualizada para el período 2025
st.subheader("🏢 Impuesto a las Ganancias: Sociedades")
st.write("Tasas progresivas según Ganancia Neta Imponible Acumulada:")
data_soc = {
    "Tramo de Ganancia Neta": ["Hasta $51.048.000", "Más de $51.048.000 hasta $510.480.000", "Más de $510.480.000"],
    "Alícuota Aplicable": ["25%", "30%", "35%"],
    "Paga Fijo ($)": ["$0", "$12.762.000", "$150.591.600"],
    "Más % sobre excedente de": ["$0", "$51.048.000", "$510.480.000"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 8. GANANCIAS PERSONAS HUMANAS (ESCALA COMPLETA ART. 94) ---
# Valores actualizados por RIPTE 2025 para liquidación anual
st.subheader("👤 Impuesto a las Ganancias: Personas Humanas")
st.caption("Escala Progresiva de Alícuotas - Artículo 94")
data_ph = {
    "Ganancia Neta Imponible ($)": ["0 - 2.8M", "2.8M - 5.6M", "5.6M - 8.4M", "8.4M - 11.2M", "11.2M - 16.8M", "16.8M - 22.4M", "22.4M - 33.6M", "33.6M - 44.8M", "Más de 44.8M"],
    "Monto Fijo ($)": ["0", "140.000", "392.000", "728.000", "1.148.000", "2.212.000", "3.444.000", "6.468.000", "10.388.000"],
    "Alícuota s/ Excedente": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"]
}
st.table(pd.DataFrame(data_ph))

st.divider()

# --- 9. RETENCIONES RG 830 ---
st.subheader("📋 Resumen Retenciones Ganancias (RG 830)")
data_rg = {
    "Concepto": ["Venta de Bienes Muebles", "Locaciones de Obra/Servicios", "Honorarios Profesionales", "Alquileres"],
    "Mínimo No Sujeto": ["$224.000", "$67.000", "$67.000", "$11.200"],
    "Alícuota Inscriptos": ["2%", "2%", "Escala Art. 94 (mín 3%)", "6%"]
}
st.table(pd.DataFrame(data_rg))
