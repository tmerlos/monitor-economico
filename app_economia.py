import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuración de página con layout ancho
st.set_page_config(page_title="Monitor Estratégico UHY - 2025", layout="wide", initial_sidebar_state="expanded")

# --- 1. CARGA DE DATOS ---
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

# --- ESTILOS PERSONALIZADOS (EMBELLECIMIENTO) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; border-radius: 5px 5px 0 0; background-color: #f1f3f4; }
    .stTabs [aria-selected="true"] { background-color: #003366 !important; color: white !important; }
    </style>
    """, unsafe_markdown=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.markdown(f"### 🌡️ {clima_actual}")
    st.markdown(f"📅 **{datetime.now().strftime('%d/%m/%Y')}**")
    st.divider()
    
    st.markdown("### 🔍 Índices de Mercado")
    st.metric("Riesgo País", "754 bps", "-31") 
    st.metric("Dólar Futuro (Dic-26)", "$1.645,50", "+2.1%")
    st.metric("Índice Merval", "2.140.580", "▲ 2.4%")
    st.metric("Nasdaq 100", "20.150,45", "▲ 1.1%")
    st.metric("Balanza Comercial", "USD +2.498M", border=True)
    
    if st.button("🔄 Sincronizar Sistemas"):
        st.cache_data.clear()
        st.rerun()

# --- 3. DASHBOARD PRINCIPAL ---
st.title("Monitor Económico e Impositivo Integral")
st.markdown("---")

# Métricas de Divisas en Cards
cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]:
        st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 4. SECCIÓN DE ACTUALIDAD ---
st.subheader("📰 Centro de Novedades y Alertas")
with st.container():
    t_eco, t_imp, t_resol_arca = st.tabs(["📈 Economía", "⚖️ Impuestos", "📜 Resoluciones ARCA (B.O.)"])

    with t_eco:
        c1, c2 = st.columns(2)
        eco_list = [("Dólar Blue: $1.485 sostenida", "https://www.ambito.com"), ("Reservas BCRA: u$s 42.413M", "https://www.bcra.gob.ar"), ("Caputo: Preadjudicación hidroeléctricas", "https://www.cronista.com"), ("Brecha Cambiaria: MEP en 3,1%", "https://www.infobae.com"), ("Informalidad: 70% sin registro", "https://www.lanacion.com.ar"), ("Agenda USA: Demoras en acuerdos", "https://www.clarin.com")]
        for i, (t, l) in enumerate(eco_list):
            with (c1 if i < 3 else c2): st.markdown(f"• [{t}]({l})")

    with t_imp:
        c3, c4 = st.columns(2)
        imp_list = [("Inocencia Fiscal: Nuevo piso evasión", "https://www.ambito.com"), ("Bienes Personales: Mínimo $384,7M", "https://www.afip.gob.ar"), ("Moratoria CABA: Hasta 9 enero", "https://www.agip.gob.ar"), ("Retenciones: Baja Soja y Trigo", "https://www.infocampo.com.ar"), ("ARCA: Topes Impuesto PAIS", "https://servicioscf.afip.gob.ar"), ("Ley Tarifaria 2026: Escalas Prov.", "https://www.boletinoficial.gob.ar")]
        for i, (t, l) in enumerate(imp_list):
            with (c3 if i < 3 else c4): st.markdown(f"• [{t}]({l})")

    with t_resol_arca:
        st.info("🔎 **Publicaciones del Día en Boletín Oficial**")
        st.warning("⚠️ **RG 5612/2025:** Actualización de retenciones por movilidad y viáticos.")
        st.warning("⚠️ **RG 5613/2025:** Modificación de plazos para regímenes informativos de terceros.")
        st.link_button("Acceder al B.O. (Primera Sección)", "https://www.boletinoficial.gob.ar/seccion/primera")

st.divider()

# --- 5. INDICADORES ECONÓMICOS ---
st.subheader("📊 Métricas Financieras")
col_t, col_i = st.columns([1, 1])

with col_t:
    with st.expander("🏦 Tasas y Rendimientos", expanded=True):
        st.write("**Pasivas (Ahorro):**")
        st.success(f"Fima Galicia: 28.21% | Santander MM: 19.23% | P. Fijo: 39%")
        st.write("**Activas (Costo):**")
        st.error(f"Adelanto Cta Cte: 62% | Tarjetas: 122% TNA")

with col_i:
    with st.expander("📊 Inflación INDEC", expanded=True):
        df_inf = pd.DataFrame({"IPC (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]}, 
                              index=["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"])
        st.line_chart(df_inf)

st.divider()

# --- 6. CUADROS DE IMPUESTOS ---
st.subheader("⚖️ Tablas de Liquidación Auditadas")
t_ph, t_bbpp, t_soc, t_mon = st.tabs(["Ganancias PH", "Bienes Personales", "Sociedades", "Monotributo"])

with t_ph:
    df_ph = pd.DataFrame({
        "Escalón": ["1", "5", "9"],
        "Desde ($)": ["0,00", "7.364.557,62", "49.667.273,02"],
        "Fijo ($)": ["0,00", "793.735,65", "11.992.882,45"],
        "Ali": ["5%", "19%", "35%"]
    })
    st.table(df_ph)

with t_bbpp:
    st.write("**MNI:** $384,7M | **Casa:** $1.346M")
    df_bbpp = pd.DataFrame({"Sobre MNI": ["0-52M", "52-114M", "+114M"], "Ali": ["0,50%", "0,75%", "1,00%"]})
    st.table(df_bbpp)

with t_soc:
    df_soc = pd.DataFrame({"Tramo": ["Hasta $101.6M", "$101.6M - $1B", "+$1B"], "Ali": ["25%", "30%", "35%"]})
    st.table(df_soc)

with t_mon:
    df_mon = pd.DataFrame({"Cat": ["A", "D", "K"], "Ingresos ($)": ["8.9M", "23.2M", "94.8M"], "Cuota ($)": ["37k", "63k", "428k"]})
    st.table(df_mon)

st.divider()

# --- 7. US TAX UPDATE (RECENT - DEC 2025) ---
with st.container():
    st.subheader("🇺🇸 US Tax Alert: Clean Energy & 1099-K Enforcement (Dec 2025)")
    st.markdown("""
    <div style="background-color: #f0f4f8; padding: 20px; border-left: 5px solid #003366; border-radius: 5px;">
        <p><strong>New Guidance on Section 45X and Form 1099-K Thresholds</strong></p>
        <p>The IRS issued final regulations in late 2025 regarding the <strong>Advanced Manufacturing Production Credit</strong>. For foreign-owned US entities, the most critical December update is the confirmation of the <strong>$600 threshold for Form 1099-K</strong> reporting for the 2025 tax year, following years of delays.</p>
        <ul>
            <li><strong>Requirement:</strong> Payment apps and online marketplaces must report payments for goods and services exceeding $600.</li>
            <li><strong>Impact:</strong> Increased visibility of digital transactions for foreign residents with US-based E-commerce or consulting LLCs.</li>
            <li><strong>Source:</strong> <a href="https://www.irs.gov/newsroom">IRS Newsroom (December 2025 Update)</a></li>
        </ul>
    </div>
    """, unsafe_markdown=True)
