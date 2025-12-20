import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor ARCA & Economía", layout="wide")

# --- 1. CARGA DE DATOS DE MERCADO ---
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

# --- 2. BARRA LATERAL ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Control")
    if st.button("🔄 Refrescar Todo"):
        st.cache_data.clear()
        st.rerun()
    st.info("Datos Fiscales: 2025-2026\nFuente: ARCA & INDEC")

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

# --- 5. NOTICIAS ---
st.subheader("📰 Actualidad Económica e Impositiva")
ce, ci = st.columns(2)
with ce:
    st.markdown("**📈 Economía**")
    for n in ["Reservas: Compras por USD 180M.", "Superávit Comercial: USD 1.200M.", "Riesgo País: 790 puntos.", "Consumo: Suba del 2%.", "Cosecha: Récord de soja.", "Tasas: BCRA estable en 40%."]:
        st.write(f"• {n}")
with ci:
    st.markdown("**⚖️ Impositivas (ARCA)**")
    for n in ["Monotributo: Nuevas tablas 2026.", "Ganancias: Ajuste RIPTE.", "Bienes Personales: Prórroga anticipo.", "Facturación: Nuevos controladores.", "Exportación: Baja de retenciones.", "Moratoria: Últimos días."]:
        st.write(f"• {n}")

st.divider()

# --- 6. TASAS Y RENDIMIENTOS ---
st.subheader("🏦 Rendimientos Financieros")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos MM")
    st.write("**Fima Premium:** 34.5% TNA")
    st.write("**Santander Ahorro:** 34.2% TNA")
with t2:
    st.info("### 🏦 Plazos Fijos")
    st.write("**TNA Minorista:** 39.5%")
    st.write("**Tasa Badlar:** 42.5%")
with t3:
    st.warning("### 💳 Crédito")
    st.write("**Préstamos Pers.:** 78% TNA")
    st.write("**Adelanto Cta Cte:** 62% TNA")

st.divider()

# --- 7. TABLA DE INFLACIÓN ---
st.subheader("📊 Historial de Inflación INDEC 2025")
data_inf = {
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5]
}
df_inf = pd.DataFrame(data_inf)
df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100

st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))
st.info(f"📈 **Inflación Acumulada Anual (Ene-Nov): {df_inf['IPC Acumulado (%)'].iloc[-1]:.1f}%**")

st.divider()

# --- 8. MONOTRIBUTO 2026 (VALORES ACTUALIZADOS ARCA) ---
st.subheader("⚖️ Monotributo: Categorías y Topes (Vigencia Enero 2026)")
st.caption("Valores oficiales de ARCA actualizados para la recategorización de enero.")
df_mono = pd.DataFrame({
    "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Brutos Anuales ($)": ["8.500.000", "12.600.000", "17.700.000", "22.000.000", "26.000.000", "32.400.000", "38.900.000", "57.800.000", "64.900.000", "74.500.000", "90.000.000"],
    "Cuota Mensual Total ($)": ["31.200", "39.400", "48.100", "62.500", "85.300", "108.200", "131.000", "245.000", "320.000", "380.000", "460.000"]
})
st.table(df_mono)

st.divider()

# --- 9. GANANCIAS JURÍDICAS (SOCIEDADES) ---
st.subheader("🏢 Ganancias: Personas Jurídicas (ARCA 2025)")
data_soc = {
    "Ganancia Neta Imponible Acumulada": ["Hasta $51.048.000", "$51.048.000 a $510.480.000", "Más de $510.480.000"],
    "Alícuota s/ excedente": ["25%", "30%", "35%"],
    "Monto Fijo": ["$0", "$12.762.000", "$150.591.600"],
    "Sobre excedente de": ["$0", "$51.048.000", "$510.480.000"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 10. GANANCIAS HUMANAS (ESCALA ART. 94 COMPLETA) ---
st.subheader("👤 Ganancias: Personas Humanas (Escala Art. 94)")
data_ph = {
    "Ganancia Neta Imponible ($)": ["0 - 2.8M", "2.8M - 5.6M", "5.6M - 8.4M", "8.4M - 11.2M", "11.2M - 16.8M", "16.8M - 22.4M", "22.4M - 33.6M", "33.6M - 44.8M", "Más de 44.8M"],
    "Fijo ($)": ["0", "140.000", "392.000", "728.000", "1.148.000", "2.212.000", "3.444.000", "6.468.000", "10.388.000"],
    "Alícuota s/ Exc.": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"]
}
st.table(pd.DataFrame(data_ph))

st.divider()

# --- 11. RETENCIONES RG 830 ---
st.subheader("📋 Retenciones Ganancias (RG 830)")
data_rg = {
    "Concepto": ["Bienes", "Servicios", "Honorarios", "Alquileres"],
    "Mínimo No Sujeto": ["$224.000", "$67.000", "$67.000", "$11.200"],
    "Alícuota Insc.": ["2%", "2%", "Escala Art. 94", "6%"]
}
st.table(pd.DataFrame(data_rg))
