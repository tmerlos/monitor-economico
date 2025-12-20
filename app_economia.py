import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor Senior - Auditoría Fiscal 2025", layout="wide")

# --- 1. CARGA DE DATOS ---
@st.cache_data(ttl=600)
def obtener_datos_externos():
    try:
        res_d = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        pizarra = {d['nombre']: d['venta'] for d in res_d}
    except:
        pizarra = {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00}
    
    # Clima CABA con Probabilidad de Lluvia
    clima = "27°C - CABA (Prob. Lluvia: 71%)"
    return pizarra, clima

pizarra, clima_actual = obtener_datos_externos()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.markdown(f"🌡️ **{clima_actual}**")
    st.markdown(f"📅 **{datetime.now().strftime('%d/%m/%Y')}**")
    st.divider()
    st.metric("Riesgo País", "629 bps", "-12") 
    st.metric("Dólar Futuro", "$1.645,50", "+2.1%")

# --- 3. ENCABEZADO ---
st.title("Monitor Económico e Impositivo Integral")
cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 4. ACTUALIDAD (TABS 6+6) ---
st.subheader("📰 Actualidad y Alertas del Día")
t_not_eco, t_not_imp = st.tabs(["📈 Noticias Económicas (6)", "⚖️ Noticias Impositivas (6)"])

with t_not_eco:
    c1, c2 = st.columns(2)
    noticias_eco = ["Dólar Blue: $1.485 con demanda sostenida", "Reservas BCRA: Cierre en u$s 42.413M", "Caputo: Preadjudicación de hidroeléctricas", "Brecha Cambiaria: MEP estable en 3,1%", "Informalidad: 7 de cada 10 jóvenes sin registro", "Agenda USA: Demoras en acuerdos estratégicos"]
    for i, t in enumerate(noticias_eco):
        with (c1 if i < 3 else c2): st.markdown(f"• {t}")

with t_not_imp:
    c3, c4 = st.columns(2)
    noticias_imp = ["Inocencia Fiscal: Dictamen para elevar piso de evasión", "Bienes Personales 2025: Mínimo en $384,7M", "Moratoria CABA: Extensión hasta el 9 de enero", "Retenciones: Baja arancelaria para Soja y Trigo", "ARCA: Nuevos topes Impuesto PAIS y Digitales", "Ley Tarifaria 2026: Publican escalas provinciales"]
    for i, t in enumerate(noticias_imp):
        with (c3 if i < 3 else c4): st.markdown(f"• {t}")

st.divider()

# --- 5. TASAS Y FONDOS ---
st.subheader("🏦 Mercado de Tasas y Fondos")
ta, tp = st.columns(2)
with ta:
    st.error("#### Costo Financiación")
    st.write("• **Adelanto Cta Cte:** 62.00% TNA")
    st.write("• **Tarjetas (Ley):** 122.00% TNA")
with tp:
    st.success("#### Rendimientos Actualizados")
    # Tasa corregida de Fima Ahorro Pesos (Clase A)
    st.write("**Fima Ahorro Pesos (Galicia):** 28.21% TNA (Neto Est.)")
    st.write("**Santander Super Ahorro $ (MM):** 19.23% TNA")
    st.write("**Plazo Fijo Minorista:** 39.00% TNA")

st.divider()

# --- 6. SECCIÓN IMPOSITIVA (CON TABLA BBPP 2025) ---
st.subheader("📊 Cuadros de Impuestos Auditados")
t_ph, t_bbpp, t_deduc, t_soc, t_mon = st.tabs(["Ganancias PH", "Bienes Personales 2025", "Deducciones", "Sociedades", "Monotributo"])

with t_bbpp:
    st.info("#### Bienes Personales - Período Fiscal 2025 (Estimado ARCA)")
    st.markdown("""
    * **Mínimo No Imponible (MNI) General:** $ 384.728.044,56
    * **Exención Casa-Habitación:** $ 1.346.548.155,99
    """)
    
    st.write("**Escala Progresiva (Bienes en el país):**")
    data_bbpp = {
        "Valor sobre el MNI ($)": ["0 a 52.664.283,73", "52.664.283,73 a 114.105.948,16", "Más de 114.105.948,16"],
        "Pagarán ($)": ["0,00", "263.321,42", "724.133,90"],
        "Más el %": ["0,50%", "0,75%", "1,00%"],
        "Sobre el excedente de ($)": ["0,00", "52.664.283,73", "114.105.948,16"]
    }
    st.table(pd.DataFrame(data_bbpp))
    st.caption("Nota: Para contribuyentes cumplidores, las alícuotas se reducen al 0.25%, 0.50% y 0.75% respectivamente.")

with t_ph:
    st.markdown("#### Escala Art. 94 LIG - Período Fiscal 2025")
    data_ph = {
        "Ganancia Neta Imponible Acum. ($)": ["0 a 1.636.568,36", "1.636.568,36 a 3.273.136,72", "3.273.136,72 a 4.909.705,08", "Más de 49.667.273,02"],
        "Monto Fijo ($)": ["0,00", "81.828,42", "229.119,57", "11.992.882,45"],
        "Alícuota %": ["5%", "9%", "12%", "35%"]
    }
    st.table(pd.DataFrame(data_ph))

with t_deduc:
    data_deduc = {"Concepto": ["MNI", "Cónyuge", "Hijo"], "Monto Anual 2025 ($)": ["4.507.505,52", "4.245.166,13", "2.140.852,77"]}
    st.table(pd.DataFrame(data_deduc))

with t_soc:
    data_soc = {"Tramo Ganancia Neta": ["Hasta $101.6M", "De $101.6M a $1016M", "Más de $1016M"], "Alícuota": ["25%", "30%", "35%"]}
    st.table(pd.DataFrame(data_soc))

with t_mon:
    st.markdown("#### Escala Monotributo 2025")
    df_mono = pd.DataFrame({
        "Cat": ["A", "B", "K"],
        "Ingresos Brutos Anuales ($)": ["8.987.312,20", "13.345.101,40", "94.805.682,90"],
        "Cuota Mensual ($)": ["37.085", "42.216", "428.100"]
    })
    st.table(df_mono)
