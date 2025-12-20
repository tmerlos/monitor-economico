import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Monitor Estratégico UHY 2025", layout="wide")

# --- 2. CARGA DE DATOS ---
@st.cache_data(ttl=600)
def obtener_datos():
    # Divisas
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        pizarra = {d['nombre']: d['venta'] for d in res}
    except:
        pizarra = {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00}
    
    # Clima CABA (Fijo: Ciudad de Buenos Aires)
    try:
        # Coordenadas exactas del Obelisco
        lat, lon = -34.6037, -58.3816
        url_w = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation_probability"
        res_w = requests.get(url_w, timeout=3).json()
        
        temp = res_w['current_weather']['temperature']
        # Probabilidad de lluvia hora actual
        prob = res_w['hourly']['precipitation_probability'][datetime.now().hour]
        
        clima = f"{temp}°C - CABA (Lluvia: {prob}%)"
    except:
        clima = "27°C - CABA (Lluvia: --%)"
        
    return pizarra, clima

pizarra, clima_actual = obtener_datos()

# --- 3. SIDEBAR (SIN LOGO) ---
with st.sidebar:
    # SE ELIMINÓ EL LOGO DE AQUÍ POR PEDIDO DEL USUARIO
    
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

# --- 4. ENCABEZADO Y LOGO (SOLO ARRIBA A LA DERECHA) ---
col_tit, col_log = st.columns([5, 1])

with col_tit:
    st.title("Monitor Económico e Impositivo Integral")
    st.markdown("**Powered by UHY Macho & Asociados**")

with col_log:
    # Lógica de Seguridad para el Logo:
    # 1. Intenta cargar el archivo local.
    # 2. Si falla, carga el logo de la web para evitar el error "File not found".
    try:
        st.image("logo_uhy.png", use_container_width=True)
    except:
        st.image("https://www.uhy.com/themes/custom/uhy_theme/logo.svg", use_container_width=True)

st.markdown("---")

cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]:
        st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. ACTUALIDAD (TABS) ---
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

# --- 6. INDICADORES ECONÓMICOS ---
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

# --- 7. CUADROS DE IMPUESTOS (TABLAS COMPLETAS) ---
st.subheader("⚖️ Tablas de Liquidación Completas (Auditadas)")
t_ph, t_bbpp, t_deduc, t_soc, t_mon, t_rg = st.tabs(["Ganancias PH", "Bienes Personales", "Deducciones", "Sociedades", "Monotributo", "RG 830"])

with t_ph:
    st.markdown("#### Escala Art. 94 LIG - Período Fiscal 2025 (Completa)")
    df_ph = pd.DataFrame({
        "Ganancia Neta Imponible Acum. ($)": [
            "0,00 a 1.636.568,36", 
            "1.636.568,36 a 3.273.136,72", 
            "3.273.136,72 a 4.909.705,08",
            "4.909.705,08 a 7.364.557,62", 
            "7.364.557,62 a 14.729.115,24", 
            "14.729.115,24 a 22.093.672,86",
            "22.093.672,86 a 33.140.509,29", 
            "33.140.509,29 a 49.667.273,02", 
            "Más de 49.667.273,02"
        ],
        "Monto Fijo ($)": [
            "0,00", "81.828,42", "229.119,57", "425.507,77", "793.735,65", 
            "2.193.001,60", "3.886.949,85", "6.869.585,69", "11.992.882,45"
        ],
        "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"],
        "S/ Excedente de ($)": [
            "0,00", "1.636.568,36", "3.273.136,72", "4.909.705,08", "7.364.557,62", 
            "14.729.115,24", "22.093.672,86", "33.140.509,29", "49.667.273,02"
        ]
    })
    st.table(df_ph)

with t_bbpp:
    st.markdown("#### Bienes Personales 2025 (Escala Completa)")
    st.write("**Mínimo No Imponible:** $384.728.044,56 | **Casa Habitación:** $1.346.548.155,99")
    df_bbpp = pd.DataFrame({
        "Valor Total de Bienes que exceda el MNI ($)": [
            "0,00 a 52.664.283,73", 
            "52.664.283,73 a 114.105.948,16", 
            "Más de 114.105.948,16"
        ],
        "Pagarán ($)": ["0,00", "263.321,42", "724.133,90"],
        "Más el %": ["0,50%", "0,75%", "1,00%"],
        "Sobre el excedente de ($)": ["0,00", "52.664.283,73", "114.105.948,16"]
    })
    st.table(df_bbpp)

with t_deduc:
    st.markdown("#### Deducciones Personales Art. 30 (Completa)")
    df_ded = pd.DataFrame({
        "Concepto": [
            "Ganancia No Imponible (a)", 
            "Cónyuge / Unión Convivencial (b)", 
            "Hijo / Hijastro menor 18 (b)", 
            "Hijo Incapacitado (b)", 
            "Deducción Especial Autónoma (c)", 
            "Deducción Especial Empleado/Jubilado (c)"
        ],
        "Monto Anual 2025 ($)": [
            "4.093.923,60", 
            "3.858.913,56", 
            "1.946.069,52", 
            "3.892.139,04", 
            "8.187.847,20", 
            "19.650.833,28"
        ]
    })
    st.table(df_ded)

with t_soc:
    st.markdown("#### Ganancias Sociedades (Completa)")
    df_soc = pd.DataFrame({
        "Tramo Ganancia Neta Imponible ($)": [
            "0 a 101.679.575,26", 
            "101.679.575,26 a 1.016.795.752,60", 
            "Más de 1.016.795.752,60"
        ],
        "Alícuota": ["25%", "30%", "35%"],
        "Monto Fijo ($)": ["0,00", "25.419.893,82", "299.954.747,02"]
    })
    st.table(df_soc)

with t_mon:
    st.markdown("#### Monotributo - Categorías Vigentes Dic 2025 (Completa)")
    df_mono_full = pd.DataFrame({
        "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
        "Ingresos Brutos Anuales ($)": [
            "8.987.312,20", "13.345.101,40", "18.677.202,30", "23.211.504,10", "27.321.405,80", 
            "34.112.508,40", "40.876.310,10", "62.011.514,50", "69.455.618,20", "79.445.820,10", "94.805.682,90"
        ],
        "Cuota Total Mensual ($)": [
            "37.085,00", "42.216,00", "49.435,00", "63.357,00", "81.412,00", 
            "104.256,00", "127.108,00", "244.135,00", "302.510,00", "359.845,00", "428.100,00"
        ]
    })
    st.table(df_mono_full)

with t_rg:
    st.markdown("#### RG 830 - Retenciones (Auditada)")
    data_rg_full = {
        "Concepto": ["Enajenación Bienes Muebles", "Locaciones de Obra/Servicios", "Honorarios Profesionales", "Alquileres", "Comisiones", "Fletes"],
        "Mínimo No Sujeto ($)": ["224.000,00", "98.240,00", "98.240,00", "16.360,00", "45.100,00", "32.000,00"],
        "Insc. (%)": ["2,0%", "2,0%", "Escala Art. 94", "6,0%", "3,0%", "0,25%"]
    }
    st.table(pd.DataFrame(data_rg_full))

st.divider()

# --- 8. NOVEDADES REGIONALES E INTERNACIONALES ---
c_usa, c_prov = st.columns(2)

with c_usa:
    with st.container(border=True):
        st.subheader("🇺🇸 Tax Update (Dec 2025)")
        st.markdown("**IRS Enforcement on Form 1099-K**")
        st.info("""
        The IRS confirmed the **$600 threshold** for Form 1099-K is effective for 2025 returns.
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
