import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor Senior - Auditoría Fiscal 2025", layout="wide")

# --- 1. CARGA DE DATOS (MERCADOS Y CLIMA) ---
@st.cache_data(ttl=600)
def obtener_datos_externos():
    try:
        res_d = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        pizarra = {d['nombre']: d['venta'] for d in res_d}
    except:
        pizarra = {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00}
    
    try:
        url_w = "https://api.open-meteo.com/v1/forecast?latitude=-34.61&longitude=-58.38&current_weather=true&hourly=precipitation_probability"
        res_w = requests.get(url_w).json()
        temp = res_w['current_weather']['temperature']
        prob_lluvia = res_w['hourly']['precipitation_probability'][datetime.now().hour]
        clima = f"{temp}°C - CABA (Lluvia: {prob_lluvia}%)"
    except:
        clima = "27°C - CABA (Lluvia: 71%)"
        
    return pizarra, clima

pizarra, clima_actual = obtener_datos_externos()

# --- 2. SIDEBAR CON ÍNDICES CRÍTICOS ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.markdown(f"🌡️ **{clima_actual}**")
    st.markdown(f"📅 **{datetime.now().strftime('%d/%m/%Y')}**")
    st.sidebar.info("**ESTADO: CONTROL DE AUDITORÍA**")
    
    st.divider()
    st.markdown("### 🔍 Índices Críticos")
    st.metric("Riesgo País", "754 bps", "-31") 
    st.metric("Dólar Futuro (Dic-26)", "$1.645,50", "+2.1%")
    st.metric("Índice Merval", "2.140.580", "▲ 2.4%")
    st.metric("Nasdaq 100", "20.150,45", "▲ 1.1%")
    st.metric("Balanza Comercial", "USD +2.498M")
    
    if st.button("🔄 Forzar Recarga"):
        st.cache_data.clear()
        st.rerun()

# --- 3. ENCABEZADO Y DIVISAS ---
st.title("Monitor Económico e Impositivo Integral")
cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 4. SECCIÓN DE ACTUALIDAD (NUEVO TAB PARA BOLETÍN) ---
st.subheader("📰 Actualidad y Alertas")
t_not_eco, t_not_imp, t_resol_arca = st.tabs(["📈 Economía (6)", "⚖️ Impuestos (6)", "📜 Resoluciones ARCA (B.O.)"])

with t_not_eco:
    c1, c2 = st.columns(2)
    eco_list = [
        ("Dólar Blue: Cotización $1.485 sostenida", "https://www.ambito.com"),
        ("Reservas BCRA: Cierre u$s 42.413M", "https://www.bcra.gob.ar"),
        ("Caputo: Preadjudicación hidroeléctricas", "https://www.cronista.com"),
        ("Brecha Cambiaria: MEP en 3,1%", "https://www.infobae.com"),
        ("Informalidad: 70% de jóvenes sin registro", "https://www.lanacion.com.ar"),
        ("Agenda USA: Demoras en acuerdos", "https://www.clarin.com")
    ]
    for i, (t, l) in enumerate(eco_list):
        with (c1 if i < 3 else c2): st.markdown(f"• [{t}]({l})")

with t_not_imp:
    c3, c4 = st.columns(2)
    imp_list = [
        ("Inocencia Fiscal: Nuevo piso evasión", "https://www.ambito.com"),
        ("Bienes Personales: Mínimo $384,7M", "https://www.afip.gob.ar"),
        ("Moratoria CABA: Hasta 9 de enero", "https://www.agip.gob.ar"),
        ("Retenciones: Baja Soja y Trigo", "https://www.infocampo.com.ar"),
        ("ARCA: Topes Impuesto PAIS", "https://servicioscf.afip.gob.ar"),
        ("Ley Tarifaria 2026: Escalas Prov.", "https://www.boletinoficial.gob.ar")
    ]
    for i, (t, l) in enumerate(imp_list):
        with (c3 if i < 3 else c4): st.markdown(f"• [{t}]({l})")

with t_resol_arca:
    st.markdown("#### Resoluciones Generales Recientes")
    st.warning("⚠️ **RG 5612/2025:** Actualización de retenciones por movilidad y viáticos.")
    st.warning("⚠️ **RG 5613/2025:** Modificación de plazos para regímenes informativos de terceros.")
    st.markdown("---")
    st.link_button("Ver todas en Boletín Oficial", "https://www.boletinoficial.gob.ar/seccion/primera")

st.divider()

# --- 5. INDICADORES ECONÓMICOS ---
st.subheader("📊 Indicadores Económicos")
tab_tasas, tab_inflacion = st.tabs(["🏦 Tasas y Fondos", "📊 Inflación"])

with tab_tasas:
    ta, tp = st.columns(2)
    with ta:
        st.error("#### Costo (Activas)")
        st.write("• **Adelanto Cta Cte:** 62.00% TNA")
        st.write("• **Tarjetas (Ley):** 122.00% TNA")
    with tp:
        st.success("#### Rendimiento (Pasivas)")
        st.write("**Fima Ahorro Pesos (Galicia):** 28.21% TNA")
        st.write("**Santander Super Ahorro $:** 19.23% TNA")
        st.write("**Plazo Fijo:** 39.00% TNA")

with tab_inflacion:
    df_inf = pd.DataFrame({
        "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
        "IPC (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
    })
    st.table(df_inf.T)

st.divider()

# --- 6. CUADROS DE IMPUESTOS (REVISADOS) ---
st.subheader("📊 Cuadros de Impuestos Auditados")
t_ph, t_bbpp, t_deduc, t_soc, t_mon = st.tabs(["Ganancias PH", "Bienes Personales", "Deducciones", "Sociedades", "Monotributo"])

with t_ph:
    st.markdown("#### Escala Art. 94 LIG - 2025")
    df_ph = pd.DataFrame({
        "Desde ($)": ["0,00", "1.636.568,36", "3.273.136,72", "4.909.705,08", "7.364.557,62", "14.729.115,24", "22.093.672,86", "33.140.509,29", "49.667.273,02"],
        "Monto Fijo ($)": ["0,00", "81.828,42", "229.119,57", "425.507,77", "793.735,65", "2.193.001,60", "3.886.949,85", "6.869.585,69", "11.992.882,45"],
        "Alícuota": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"]
    })
    st.table(df_ph)

with t_bbpp:
    st.markdown("#### Bienes Personales - 2025")
    st.write("**MNI:** $384.728.044,56 | **Casa-Habitación:** $1.346.548.155,99")
    df_bbpp = pd.DataFrame({
        "Sobre el MNI ($)": ["0 a 52.6M", "52.6M a 114.1M", "Más de 114.1M"],
        "Alícuota": ["0,50%", "0,75%", "1,00%"],
        "Fijo ($)": ["0,00", "263.321,42", "724.133,90"]
    })
    st.table(df_bbpp)

with t_deduc:
    df_ded = pd.DataFrame({
        "Concepto": ["MNI", "Cónyuge", "Hijo", "Especial Emp/Jub"],
        "Anual 2025 ($)": ["4.093.923,60", "3.858.913,56", "1.946.069,52", "19.650.833,28"]
    })
    st.table(df_ded)

with t_soc:
    df_soc = pd.DataFrame({
        "Tramo Ganancia": ["Hasta $101.6M", "$101.6M a $1.016M", "Más de $1.016M"],
        "Alícuota": ["25%", "30%", "35%"]
    })
    st.table(df_soc)

with t_mon:
    df_mon = pd.DataFrame({
        "Cat": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
        "Ingresos Brutos ($)": ["8.9M", "13.3M", "18.6M", "23.2M", "27.3M", "34.1M", "40.8M", "62.0M", "69.4M", "79.4M", "94.8M"],
        "Cuota ($)": ["37.085", "42.216", "49.435", "63.357", "81.412", "104.256", "127.108", "244.135", "302.510", "359.845", "428.100"]
    })
    st.table(df_mon)

st.divider()

# --- 7. TEMA ESTADOS UNIDOS (IDIOMA ORIGEN) ---
st.subheader("🇺🇸 US Tax Update: Corporate Transparency Act (CTA)")
st.info("""
**New Reporting Requirement: Beneficial Ownership Information (BOI)**
Starting in 2024, most small entities (including LLCs often used by foreign investors) must report information about their beneficial owners to FinCEN. 

* **Key Deadline:** Companies created before Jan 1, 2024, have until **Jan 1, 2025**, to file. New companies have 90 days.
* **Non-compliance:** Civil penalties up to **$500 per day** and criminal fines.
* **Source:** [FinCEN.gov - BOI Reporting](https://www.fincen.gov/boi)
""")
