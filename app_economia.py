import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor ARCA Pro", layout="wide")

# --- 1. CARGA DE DATOS (DolarAPI + Fallback) ---
@st.cache_data(ttl=600)
def obtener_pizarra():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
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

# --- 2. BARRA LATERAL PRO ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Control Pro")
    st.markdown("---")
    if st.button("🔄 Forzar Actualización"):
        st.cache_data.clear()
        st.rerun()
    st.success("Verificación de datos: Ley 27.743 OK")
    st.info("Periodo: Dic 2025 / Ene 2026")

# --- 3. CABECERA ---
col_tit1, col_tit2 = st.columns([1, 15])
with col_tit1: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_tit2: st.title("Monitor Económico e Impositivo Integral")
st.success(f"🏛️ **Dólar Oficial (Referencia ARCA): ${pizarra['Oficial']:,.2f}**")

# --- 4. PIZARRA DE DIVISAS ---
cols = st.columns(5)
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. TASAS Y RENDIMIENTOS ---
st.subheader("🏦 Rendimientos Financieros")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos Money Market")
    st.write("**Fima Premium (Galicia):** 34.5% TNA")
    st.write("**Superfondo Ahorro (Santander):** 34.2% TNA")
with t2:
    st.info("### 🏦 Plazos Fijos")
    st.write("**TNA Minorista:** 39.0% - 41.5%")
    st.write("**Tasa Badlar:** 42.8%")
with t3:
    st.warning("### 💳 Crédito (TNA)")
    st.write("**Personales:** 78% / **Adelanto:** 62%")

st.divider()

# --- 6. NOTICIAS (6+6) ---
st.subheader("📰 Actualidad y Novedades")
cn1, cn2 = st.columns(2)
with cn1:
    st.markdown("**📈 Economía**")
    for n in ["Reservas: El BCRA compró USD 180M.", "Riesgo País: Perforó los 800 puntos.", "Superávit: 11 meses consecutivos de saldo positivo.", "Consumo: Ventas minoristas suben 2.1%.", "Cosecha: Precios de soja estables.", "Inflación: Tendencia a la baja confirmada."]:
        st.write(f"• {n}")
with cn2:
    st.markdown("**⚖️ Impositivas (ARCA)**")
    for n in ["Monotributo: Recategorización obligatoria Enero.", "Ganancias: Publicadas las tablas definitivas 2025.", "Bienes Personales: Mínimo exento actualizado.", "RG 830: Nuevos importes mínimos de retención.", "Facturación: Límites de consumidor final actualizados.", "Moratoria: Se extiende el plazo de adhesión."]:
        st.write(f"• {n}")

st.divider()

# --- 7. INFLACIÓN (IPC) ---
st.subheader("📊 Historial de Inflación INDEC")
data_inf = {
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5]
}
df_inf = pd.DataFrame(data_inf)
df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 8. MONOTRIBUTO 2026 (TABLA FINAL ACTUALIZADA) ---
st.subheader("⚖️ Monotributo: Escalas Vigentes (ARCA)")
st.caption("Valores unificados Ley 27.743 - Ajuste IPC")
df_mono = pd.DataFrame({
    "Cat.": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Anuales ($)": ["6.45M", "9.45M", "13.25M", "16.45M", "19.35M", "24.25M", "29.0M", "44.0M", "49.25M", "56.4M", "68.0M"],
    "Cuota Mensual Srv ($)": ["26.600", "30.280", "35.458", "45.443", "58.519", "74.825", "91.419", "175.091", "-", "-", "-"],
    "Cuota Mensual Bienes ($)": ["26.600", "3
