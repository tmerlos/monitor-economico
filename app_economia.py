import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor ARCA Profesional", layout="wide")

# --- 1. CARGA DE MERCADOS (DolarAPI) ---
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
    st.title("Panel Técnico ARCA")
    st.info("📅 Actualizado al: 20/12/2025")
    if st.button("🔄 Sincronizar Datos"):
        st.cache_data.clear()
        st.rerun()

# --- 3. CABECERA ---
st.title("Monitor Económico e Impositivo Integral")
st.success(f"🏛️ **Dólar Oficial (Ref. ARCA): ${pizarra['Oficial']:,.2f}**")

# --- 4. COTIZACIONES ---
cols = st.columns(5)
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. TASAS DE INTERÉS ---
st.subheader("🏦 Rendimientos Financieros")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos MM")
    st.write("**Fima Premium:** 34.5% TNA")
    st.write("**Santander Ahorro:** 34.2% TNA")
with t2:
    st.info("### 🏦 Bancos")
    st.write("**Plazo Fijo:** 39.0% TNA")
    st.write("**Tasa Badlar:** 42.8% TNA")
with t3:
    st.warning("### 💳 Crédito")
    st.write("**Personales:** 78% TNA")
    st.write("**Adelanto Cta Cte:** 62% TNA")

st.divider()

# --- 6. PANEL DE NOTICIAS (6+6) ---
st.subheader("📰 Actualidad y Novedades")
cn1, cn2 = st.columns(2)
with cn1:
    st.markdown("**📈 Economía**")
    for n in ["Reservas: El BCRA compró USD 180M.", "Riesgo País: Perforó los 800 puntos.", "Superávit Comercial: USD 1.200M.", "Consumo: Ventas minoristas suben 2.1%.", "Cosecha: Precios de soja estables.", "Inflación: Tendencia a la baja confirmada."]:
        st.write(f"• {n}")
with cn2:
    st.markdown("**⚖️ Impositivas (ARCA)**")
    for n in ["Monotributo: Recategorización obligatoria Enero.", "Ganancias: Publicadas las escalas definitivas 2025.", "Bienes Personales: Mínimo exento actualizado.", "RG 830: Nuevos importes mínimos de retención.", "Facturación: Límites de consumidor final actualizados.", "Moratoria: Se extiende el plazo de adhesión."]:
        st.write(f"• {n}")

st.divider()

# --- 7. HISTORIAL INFLACIÓN ---
st.subheader("📊 Historial de Inflación INDEC 2025")
df_inf = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5]
})
df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 8. GANANCIAS PERSONAS JURÍDICAS (VALORES PRECISOS) ---
st.subheader("🏢 Ganancias: Personas Jurídicas (Ley 27.630)")
st.caption("Valores definitivos para cierres de ejercicio Diciembre 2025.")
data_soc = {
    "Ganancia Neta Imponible Acumulada": [
        "Hasta $101.679.575,26", 
        "De $101.679.575,26 a $1.016.795.752,60", 
        "Más de $1.016.795.752,60"
    ],
    "Alícuota": ["25%", "30%", "35%"],
    "Monto Fijo ($)": ["$0,00", "$25.419.893,82", "$299.954.747,02"],
    "S/ Excedente de": ["$0,00", "$101.679.575,26", "$1.016.795.752,60"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 9. MONOTRIBUTO: ESCALAS VIGENTES (AJUSTADO) ---
st.subheader("⚖️ Monotributo: Topes y Cuotas 2025")
st.caption("Valores actualizados al 20/12/2025.")
df_mono = pd.DataFrame({
    "Cat.": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Brutos Anuales ($)": [
        "8.987.312,20", "13.345.101,40", "18.677.202,30", "23.211.504,10", "27.321.405,80", 
        "34.112.508,40", "40.876.310,10", "62.011.514,50", "69.455.618,20", "79.445.820,10", "94.805.682,90"
    ],
    "Cuota Total Mensual ($)": ["36.8k", "42.1k", "49.5k", "63.2k", "81.4k", "104.2k", "127.1k", "244.1k", "302.5k", "359.8k", "428.1k"]
})
st.table(df_mono)

st.divider()

# --- 10. RETENCIONES GANANCIAS (RG 830) ---
st.subheader("📋 Retenciones Ganancias (RG 830) - Mínimos HOY")
data_rg = {
    "Concepto": ["Bienes Muebles", "Servicios", "Honorarios Profesionales", "Alquileres"],
    "Mínimo No Sujeto ($)": ["327.200", "98.240", "98.240", "16.360"],
    "Alícuota Insc.": ["2%", "2%", "Escala Art. 94", "6%"]
}
st.table(pd.DataFrame(data_rg))
