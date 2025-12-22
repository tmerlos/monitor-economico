import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Monitor Estratégico UHY 2025", layout="wide")

# --- CSS PERSONALIZADO (PANTONE 3302 Y TEXTO BLANCO EN SIDEBAR) ---
st.markdown("""
    <style>
    /* Fondo del Sidebar - Pantone 3302 C aprox (#004B39) */
    [data-testid="stSidebar"] {
        background-color: #004B39;
    }
    /* Texto blanco en Sidebar */
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    /* Ajuste para que los inputs o botones dentro del sidebar se vean bien */
    [data-testid="stSidebar"] .stButton button {
        color: #004B39 !important;
        background-color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CARGA DE DATOS ---
@st.cache_data(ttl=600)
def obtener_datos():
    # Divisas
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        pizarra = {d['nombre']: d['venta'] for d in res}
    except:
        pizarra = {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00}
    
    # Clima CABA (Fijo)
    try:
        lat, lon = -34.6037, -58.3816
        url_w = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation_probability"
        res_w = requests.get(url_w, timeout=3).json()
        temp = res_w['current_weather']['temperature']
        prob = res_w['hourly']['precipitation_probability'][datetime.now().hour]
        clima = f"{temp}°C - CABA (Lluvia: {prob}%)"
    except:
        clima = "27°C - CABA (Lluvia: --%)"
        
    return pizarra, clima

pizarra, clima_actual = obtener_datos()

# --- 3. SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo_uhy.png", use_container_width=True)
    except:
        st.image("https://www.uhy.com/themes/custom/uhy_theme/logo.svg", use_container_width=True)
    
    st.markdown(f"### 🌡️ {clima_actual}")
    st.markdown(f"📅 **{datetime.now().strftime('%d/%m/%Y')}**")
    st.divider()
    
    st.markdown("### 🔍 Índices Críticos")
    st.metric("Riesgo País", "754 bps", "-31") 
    st.metric("Dólar Futuro (Dic-26)", "$1.645,50", "+2.1%")
    st.metric("Índice Merval", "2.140.580", "▲ 2.4%")
    st.metric("Nasdaq 100", "20.150,45", "▲ 1.1%")
    st.metric("Balanza Comercial", "USD +2.498M")
    st.metric("Tasa Desempleo", "6.6%")
    
    if st.button("🔄 Actualizar Todo"):
        st.cache_data.clear()
        st.rerun()

# --- 4. ENCABEZADO ---
st.title("Monitor Económico e Impositivo Integral")
st.markdown("**Powered by UHY Macho & Asociados**")
st.markdown("---")

cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]:
        st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. ACTUALIDAD ---
st.subheader("📰 Centro de Novedades y Alertas")
t_eco, t_imp, t_bo = st.tabs(["📈 Noticias Económicas (6)", "⚖️ Noticias Impositivas (6)", "📜 Boletín Oficial"])

with t_eco:
    c1, c2 = st.columns(2)
    eco_list = [
        ("Dólar Blue: $1.485 sostenida", "https://www.ambito.com"),
        ("Reservas BCRA: u$s 42.413M", "https://www.bcra.gob.ar"),
        ("Caputo: Preadjudicación hidroeléctricas", "https://www.cronista.com"),
        ("Brecha Cambiaria: MEP en 3,1%", "https://www.infobae.com"),
        ("Informalidad: 70% sin registro", "https://www.lanacion.com.ar"),
        ("Agenda USA: Demoras en acuerdos", "https://www.clarin.com")
    ]
    for i, (t, l) in enumerate(eco_list):
        with (c1 if i < 3 else c2): st.markdown(f"• [{t}]({l})")

with t_imp:
    c3, c4 = st.columns(2)
    imp_list = [
        ("Inocencia Fiscal: Nuevo piso evasión", "https://www.ambito.com"),
        ("Bienes Personales: Mínimo $384,7M", "https://www.afip.gob.ar"),
        ("Moratoria CABA: Hasta 9 enero", "https://www.agip.gob.ar"),
        ("Retenciones: Baja Soja y Trigo", "https://www.infocampo.com.ar"),
        ("ARCA: Topes Impuesto PAIS", "https://servicioscf.afip.gob.ar"),
        ("Ley Tarifaria 2026: Escalas Prov.", "https://www.boletinoficial.gob.ar")
    ]
    for i, (t, l) in enumerate(imp_list):
        with (c3 if i < 3 else c4): st.markdown(f"• [{t}]({l})")

with t_bo:
    with st.container(border=True):
        st.info("🔎 **Publicaciones del Día en Boletín Oficial**")
        st.markdown("🔴 **RG 5612/2025:** Actualización de retenciones por movilidad y viáticos.")
        st.markdown("🔴 **RG 5613/2025:** Modificación de plazos para regímenes informativos.")
        st.markdown("---")
        st.link_button("Ir al Boletín Oficial (1ra Sección)", "https://www.boletinoficial.gob.ar/seccion/primera")

st.divider()

# --- 6. INDICADORES ---
st.subheader("📊 Indicadores Financieros")
tab_tasas, tab_inflacion = st.tabs(["🏦 Tasas y Fondos", "📊 Inflación (Tabla Completa)"])

with tab_tasas:
    c_act, c_pas = st.columns(2)
    with c_act:
        st.error("#### Tasas Activas (Costo)")
        st.write("• **Adelanto Cta Cte:** 62.00% TNA")
        st.write("• **Descuento Cheques:** 48.00% TNA")
        st.write("• **Tarjetas (Ley):** 122.00% TNA")
    with c_pas:
        st.success("#### Tasas Pasivas (Rendimiento)")
        st.write("• **Fima Ahorro Pesos (Galicia):** 28.21% TNA")
        st.write("• **Santander Super Ahorro $:** 19.23% TNA")
        st.write("• **Plazo Fijo Minorista:** 39.00% TNA")
        st.write("• **Tasa Badlar:** 42.80% TNA")

with tab_inflacion:
    st.markdown("**Evolución del Índice de Precios al Consumidor (2025)**")
    df_inf = pd.DataFrame({
        "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre (Est)"],
        "IPC Mensual (%)": [2.20, 2.40, 3.70, 2.80, 1.50, 1.60, 1.90, 1.90, 2.10, 2.30, 2.50, 2.30]
    })
    df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
    st.table(df_inf.style.format({"IPC Mensual (%)": "{:.2f}%", "IPC Acumulado (%)": "{:.2f}%"}))

st.divider()

# --- 7. TABLAS DE IMPUESTOS Y CALCULADORA ---
st.subheader("⚖️ Tablas de Liquidación Completas (Auditadas)")
t_ph, t_bbpp, t_deduc, t_soc, t_mon, t_rg, t_calc = st.tabs(["Ganancias PH", "Bienes Personales", "Deducciones", "Sociedades", "Monotributo", "RG 830", "🧮 Calculadora"])

with t_ph:
    st.markdown("#### Escala Art. 94 LIG - Período Fiscal 2025 (Completa)")
    df_ph = pd.DataFrame({
        "Ganancia Neta Imponible Acum. ($)": ["0 a 1.636.568,36", "1.636.568,36 a 3.273.136,72", "3.273.136,72 a 4.909.705,08", "4.909.705,08 a 7.364.557,62", "7.364.557,62 a 14.729.115,24", "14.729.115,24 a 22.093.672,86", "22.093.672,86 a 33.140.509,29", "33.140.509,29 a 49.667.273,02", "Más de 49.667.273,02"],
        "Monto Fijo ($)": ["0,00", "81.828,42", "229.119,57", "425.507,77", "793.735,65", "2.193.001,60", "3.886.949,85", "6.869.585,69", "11.992.882,45"],
        "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"],
        "S/ Excedente de ($)": ["0,00", "1.636.568,36", "3.273.136,72", "4.909.705,08", "7.364.557,62", "14.729.115,24", "22.093.672,86", "33.140.509,29", "49.667.273,02"]
    })
    st.table(df_ph)

with t_bbpp:
    st.markdown("#### Bienes Personales 2025")
    st.write("**Mínimo No Imponible:** $384.728.044,56 | **Casa Habitación:** $1.346.548.155,99")
    df_bbpp = pd.DataFrame({
        "Valor Total de Bienes que exceda el MNI ($)": ["0 a 52.664.283,73", "52.664.283,73 a 114.105.948,16", "Más de 114.105.948,16"],
        "Pagarán ($)": ["0,00", "263.321,42", "724.133,90"],
        "Más el %": ["0,50%", "0,75%", "1,00%"],
        "Sobre el excedente de ($)": ["0,00", "52.664.283,73", "114.105.948,16"]
    })
    st.table(df_bbpp)

with t_deduc:
    st.markdown("#### Deducciones Personales Art. 30")
    df_ded = pd.DataFrame({
        "Concepto": ["Ganancia No Imponible (a)", "Cónyuge (b)", "Hijo menor 18 (b)", "Hijo Incapacitado (b)", "Ded. Especial Autónoma (c)", "Ded. Especial Empleado (c)"],
        "Monto Anual 2025 ($)": ["4.093.923,60", "3.858.913,56", "1.946.069,52", "3.892.139,04", "8.187.847,20", "19.650.833,28"]
    })
    st.table(df_ded)

with t_soc:
    st.markdown("#### Ganancias Sociedades")
    df_soc = pd.DataFrame({
        "Tramo Ganancia Neta ($)": ["0 a 101.679.575,26", "101.679.575,26 a 1.016.795.752,60", "Más de 1.016.795.752,60"],
        "Alícuota": ["25%", "30%", "35%"],
        "Monto Fijo ($)": ["0,00", "25.419.893,82", "299.954.747,02"]
    })
    st.table(df_soc)

with t_mon:
    st.markdown("#### Monotributo Dic 2025")
    df_mono_full = pd.DataFrame({
        "Cat": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
        "Ingresos Brutos ($)": ["8.9M", "13.3M", "18.6M", "23.2M", "27.3M", "34.1M", "40.8M", "62.0M", "69.4M", "79.4M", "94.8M"],
        "Cuota Total ($)": ["37.085", "42.216", "49.435", "63.357", "81.412", "104.256", "127.108", "244.135", "302.510", "359.845", "428.100"]
    })
    st.table(df_mono_full)

with t_rg:
    st.markdown("#### RG 830 - Retenciones")
    data_rg_full = {
        "Concepto": ["Bienes Muebles", "Obras/Servicios", "Honorarios", "Alquileres", "Comisiones", "Fletes"],
        "Mínimo No Sujeto ($)": ["224.000", "98.240", "98.240", "16.360", "45.100", "32.000"],
        "Insc. (%)": ["2,0%", "2,0%", "Escala", "6,0%", "3,0%", "0,25%"]
    }
    st.table(pd.DataFrame(data_rg_full))

with t_calc:
    st.markdown("### 🧮 Calculadora de Impuesto a las Ganancias (Estimación)")
    st.info("Ingrese los datos mensuales para proyectar la retención acumulada.")

    # Inputs
    c1, c2, c3 = st.columns(3)
    with c1:
        meses = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
        mes_sel = st.selectbox("Mes de Cálculo", list(meses.keys()), format_func=lambda x: meses[x])
    with c2:
        sueldo = st.number_input("Sueldo Bruto Mensual ($)", min_value=0.0, step=10000.0, format="%.2f")
    with c3:
        sac_op = st.radio("¿Incluye SAC?", ["Sí", "No"], horizontal=True)
        sac = True if sac_op == "Sí" else False

    # Cálculos Impuesto
    bruto_acum = sueldo * mes_sel
    if sac: bruto_acum += (sueldo / 12) * mes_sel

    mni_anual = 4093923.60
    ded_esp_anual = 19650833.28
    ded_acum = ((mni_anual + ded_esp_anual) / 12) * mes_sel
    
    neto_sujeto = max(0, bruto_acum - ded_acum)

    # Cálculo Base Imponible Máxima Seguridad Social (Estimado 2025)
    # Base estimada inicio 2025: $3.800.000 aprox con ajuste mensual del 3%
    base_max_aportes = 3800000 * (1.03 ** (mes_sel - 1))

    # Búsqueda en escala
    escala = [
        {"d": 0, "h": 1636568.36, "f": 0, "p": 5, "exc": 0},
        {"d": 1636568.36, "h": 3273136.72, "f": 81828.42, "p": 9, "exc": 1636568.36},
        {"d": 3273136.72, "h": 4909705.08, "f": 229119.57, "p": 12, "exc": 3273136.72},
        {"d": 4909705.08, "h": 7364557.62, "f": 425507.77, "p": 15, "exc": 4909705.08},
        {"d": 7364557.62, "h": 14729115.24, "f": 793735.65, "p": 19, "exc": 7364557.62},
        {"d": 14729115.24, "h": 22093672.86, "f": 2193001.60, "p": 23, "exc": 14729115.24},
        {"d": 22093672.86, "h": 33140509.29, "f": 3886949.85, "p": 27, "exc": 22093672.86},
        {"d": 33140509.29, "h": 49667273.02, "f": 6869585.69, "p": 31, "exc": 33140509.29},
        {"d": 49667273.02, "h": float('inf'), "f": 11992882.45, "p": 35, "exc": 49667273.02},
    ]

    tramo = next((t for t in escala if t["d"] <= neto_sujeto < t["h"]), None)
    impuesto = 0
    if tramo:
        impuesto = tramo["f"] + ((neto_sujeto - tramo["exc"]) * (tramo["p"] / 100))

    st.markdown("---")
    
    # RECUADRO ROJO CON RESULTADOS
    with st.container(border=True):
        st.markdown(f"### 📉 Resultado a {meses[mes_sel]}")
        
        c_res1, c_res2, c_res3 = st.columns(3)
        c_res1.metric("Bruto Acumulado", f"${bruto_acum:,.2f}")
        c_res2.metric("Deducciones (MNI+Esp)", f"${ded_acum:,.2f}")
        c_res3.metric("Neto Sujeto a Impuesto", f"${neto_sujeto:,.2f}")
        
        st.divider()
        
        if tramo:
            st.write(f"**Ubicación en Escala:** Tramo de ${tramo['d']:,.2f} a ${tramo['h'] if tramo['h']!=float('inf') else '...':,.2f}")
            st.write(f"**Monto Fijo:** ${tramo['f']:,.2f} + **{tramo['p']}%** sobre excedente de ${tramo['exc']:,.2f}")
        
        st.error(f"### Impuesto Determinado Estimado: ${impuesto:,.2f}")
        
        # Base Máxima Aportes (Nuevo)
        st.info(f"ℹ️ **Base Imponible Máxima para Aportes ({meses[mes_sel]} 2025):** ${base_max_aportes:,.2f}")

st.divider()

# --- 8. NOVEDADES ---
c_usa, c_prov = st.columns(2)

with c_usa:
    with st.container(border=True):
        st.subheader("🇺🇸 Tax Update (Dec 2025)")
        st.markdown("**📍 Estados Unidos**")
        st.info("""
        **IRS Enforcement on Form 1099-K**
        * The IRS confirmed the **$600 threshold** for Form 1099-K is effective for 2025 returns.
        * **Impact:** Third-party settlement organizations must report gross payments > $600.
        * **Action:** Reconcile US-source income for LLCs.
        * **Deadline:** Check filings before Jan 2026.
        """)

with c_prov:
    with st.container(border=True):
        st.subheader("Novedades Provinciales (Dic 2025)")
        st.markdown("**📍 Provincia de Santa Fe**")
        st.success("""
        * **Ley Impositiva 2026:** Aprobada. Tope aumento inmobiliario 140%.
        * **IIBB:** Alícuota reducida (2.5%) para PyMEs industriales.
        """)
        st.markdown("**📍 Provincia de Tucumán**")
        st.warning("""
        * **Moratoria:** Prórroga hasta el 30/12/2025 (Dto. 3584/3). 
        * **Sellos:** Exención para contratos de alquiler de vivienda.
        """)
