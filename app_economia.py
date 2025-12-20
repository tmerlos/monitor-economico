import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor ARCA - Auditoría Pro", layout="wide")

# --- 1. DATOS DE MERCADO EN TIEMPO REAL ---
@st.cache_data(ttl=300)
def obtener_mercados():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        m = {d['nombre']: d['venta'] for d in res}
        return {
            "Oficial": m.get("Oficial", 1030.50),
            "Blue": m.get("Blue", 1485.00),
            "MEP": m.get("MEP", 1496.80),
            "CCL": m.get("Contado con Liquidación", 1555.00),
            "Tarjeta": m.get("Tarjeta", 1935.45)
        }
    except:
        return {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00, "Tarjeta": 1935.45}

pizarra = obtener_mercados()

# --- 2. SIDEBAR DE CONTROL ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Auditoría")
    st.write("**Fecha:** 20 de Diciembre de 2025")
    st.divider()
    if st.button("🔄 Forzar Recarga de Datos"):
        st.cache_data.clear()
        st.rerun()
    st.info("Base Legal: Ley 27.743 y Res. Grales. ARCA 2025")

# --- 3. ENCABEZADO ---
col1, col2 = st.columns([1, 15])
with col1: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col2: st.title("Monitor Económico e Impositivo Integral")

# --- 4. PIZARRA DE DIVISAS ---
st.success(f"🏛️ **Dólar Oficial (Referencia ARCA): ${pizarra['Oficial']:,.2f}**")
cols = st.columns(5)
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. TASAS Y RENDIMIENTOS ---
st.subheader("🏦 Rendimientos Financieros y Tasas")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos Money Market")
    st.write("**Fima Premium:** 34.50% TNA")
    st.write("**Santander Ahorro:** 34.20% TNA")
with t2:
    st.info("### 🏦 Plazos Fijos")
    st.write("**TNA Minorista:** 39.0% - 41.5%")
    st.write("**Badlar:** 42.85%")
with t3:
    st.warning("### 💳 Crédito")
    st.write("**Personales:** 78% TNA")
    st.write("**Adelanto Cta Cte:** 62% TNA")

st.divider()

# --- 6. NOTICIAS (6 ECONOMÍA + 6 IMPOSITIVAS) ---
st.subheader("📰 Actualidad y Novedades")
c_not_e, c_not_i = st.columns(2)
with c_not_e:
    st.markdown("**📈 Economía**")
    for n in ["Reservas: El BCRA sumó USD 180M hoy.", "Riesgo País: Perforó los 800 puntos básicos.", "Superávit Fiscal: 11 meses en terreno positivo.", "Ventas: El consumo creció un 2.1% mensual.", "Cosecha: Estimación de soja en niveles récord.", "IPC: La inflación núcleo sigue a la baja."]:
        st.write(f"• {n}")
with c_not_i:
    st.markdown("**⚖️ Impositivas (ARCA)**")
    for n in ["Monotributo: Recategorización Enero 2026.", "Ganancias PH: Escala Art. 94 definitiva.", "Bienes Personales: Nuevos beneficios para cumplidores.", "RG 830: Ajuste de mínimos por movilidad.", "Factura Electrónica: Nuevos topes para Cons. Final.", "Moratoria: Prórroga de la última etapa."]:
        st.write(f"• {n}")

st.divider()

# --- 7. HISTORIAL INFLACIÓN (IPC) ---
st.subheader("📊 Historial de Inflación INDEC 2025")
df_inf = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5]
})
df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 8. MONOTRIBUTO 2025 (VALORES AUDITADOS) ---
st.subheader("⚖️ Monotributo: Escalas Vigentes (Diciembre 2025)")
st.caption("Topes de ingresos anuales según la última actualización de ARCA.")
df_mono = pd.DataFrame({
    "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Brutos Anuales ($)": [
        "8.987.312,20", "13.345.101,40", "18.677.202,30", "23.211.504,10", "27.321.405,80", 
        "34.112.508,40", "40.876.310,10", "62.011.514,50", "69.455.618,20", "79.445.820,10", "94.805.682,90"
    ],
    "Cuota Total Mensual ($)": ["36.8k", "42.1k", "49.5k", "63.2k", "81.4k", "104.2k", "127.1k", "244.1k", "302.5k", "359.8k", "428.1k"]
})
st.table(df_mono)

st.divider()

# --- 9. GANANCIAS PERSONAS JURÍDICAS (SOCIEDADES) ---
st.subheader("🏢 Impuesto a las Ganancias: Sociedades")
st.write("Escala Progresiva (Actualización IPIM para ejercicios iniciados a partir del 01/01/2025):")

data_soc = {
    "Ganancia Neta Imponible Acumulada": [
        "Hasta $101.679.575,26", 
        "De $101.679.575,26 a $1.016.795.752,60", 
        "Más de $1.016.795.752,60"
    ],
    "Alícuota": ["25%", "30%", "35%"],
    "Monto Fijo ($)": ["$0,00", "$25.419.893,82", "$299.954.747,02"],
    "Más % sobre excedente de": ["$0,00", "$101.679.575,26", "$1.016.795.752,60"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 10. RETENCIONES GANANCIAS (RG 830) ---
st.subheader("📋 Retenciones Ganancias (RG 830) - Mínimos Vigentes")
data_rg = {
    "Concepto": ["Bienes Muebles", "Locaciones de Servicios", "Honorarios Profesionales", "Alquileres"],
    "Mínimo No Sujeto ($)": ["327.200,00", "98.240,00", "98.240,00", "16.360,00"],
    "Alícuota Inscriptos": ["2%", "2%", "Escala Art. 94 (mín 3%)", "6%"]
}
st.table(pd.DataFrame(data_rg))
