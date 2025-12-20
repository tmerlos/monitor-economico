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
        res_w = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-34.61&longitude=-58.38&current_weather=true").json()
        temp = res_w['current_weather']['temperature']
        clima = f"{temp}°C - CABA"
    except:
        clima = "24°C - CABA"
        
    return pizarra, clima

pizarra, clima_actual = obtener_datos_externos()

# --- 2. SIDEBAR E INDICES ---
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
    
    if st.button("🔄 Forzar Recarga"):
        st.cache_data.clear()
        st.rerun()

# --- 3. ENCABEZADO Y DIVISAS ---
st.title("Monitor Económico e Impositivo Integral")
cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 4. SECCIÓN DE ACTUALIDAD CON TABS ---
st.subheader("📰 Actualidad y Alertas")
t_eco, t_imp, t_bo = st.tabs(["📈 Noticias Económicas", "⚖️ Impuestos (ARCA)", "📜 Boletín Oficial"])

with t_eco:
    c1, c2 = st.columns(2)
    noticias_eco = [
        ("Subsidios: Crédito USD 300M Energía", "https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/"),
        ("Desempleo: Baja al 6,6% (INDEC)", "https://www.pagina12.com.ar/2025/12/19/aumenta-la-precariedad-y-baja-el-desempleo/"),
        ("IPC: Proyección Dic 2.3%", "https://www.ambito.com/economia/")
    ]
    for i, (t, l) in enumerate(noticias_eco):
        with (c1 if i < 2 else c2): st.markdown(f"• [{t}]({l})")

with t_imp:
    c3, c4 = st.columns(2)
    noticias_imp = [
        ("Vencimiento Monotributo Dic", "https://www.ambito.com/informacion-general/vencimiento-del-monotributo-diciembre-2025-arca-n6223081/"),
        ("Bienes Personales: Ley 27.743", "https://www.afip.gob.ar/ganancias-y-bienes-personales/"),
        ("Calendario 2026: Enero", "https://www.afip.gob.ar/vencimientos/")
    ]
    for i, (t, l) in enumerate(noticias_imp):
        with (c3 if i < 2 else c4): st.markdown(f"• [{t}]({l})")

with t_bo:
    st.markdown("🔴 **RG 5612/2025:** Actualización de retenciones.")
    st.markdown("🔴 **RG 5613/2025:** Modificación de plazos informativos.")

st.divider()

# --- 5. INDICADORES ECONÓMICOS ---
st.subheader("📈 Indicadores Económicos")
tab_tasas, tab_inflacion = st.tabs(["🏦 Tasas de Interés", "📊 Inflación (Mensual y Acumulada)"])

with tab_tasas:
    ta, tp = st.columns(2)
    with ta:
        st.error("#### Activas (Costo)")
        st.write("• **Adelanto Cta Cte:** 62.00% TNA")
        st.write("• **Descuento Cheques:** 48.00% TNA")
    with tp:
        st.success("#### Pasivas (Rendimiento)")
        st.write("• **Plazo Fijo:** 39.00% TNA")
        st.write("• **Tasa Badlar:** 42.80% TNA")

with tab_inflacion:
    df_inf = pd.DataFrame({
        "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Dic (Est)"],
        "IPC Mensual (%)": [2.20, 2.40, 3.70, 2.80, 1.50, 1.60, 1.90, 1.90, 2.10, 2.30, 2.50, 2.30]
    })
    df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
    st.table(df_inf.style.format({"IPC Mensual (%)": "{:.2f}%", "IPC Acumulado (%)": "{:.2f}%"}))

st.divider()

# --- 6. CUADROS DE IMPUESTOS (AUDITADOS) ---
st.subheader("📊 Cuadros de Impuestos")
t_ph, t_deduc, t_soc, t_mon = st.tabs(["Impuesto Personas Humanas", "Deducciones Personales", "Sociedades", "Monotributo 2025"])

with t_ph:
    st.markdown("#### Escala Art. 94 LIG - Período Fiscal 2025 (Valores Exactos)")
    data_ph = {
        "Ganancia Neta Imponible Acum. ($)": [
            "0,00 a 1.636.568,36", "1.636.568,36 a 3.273.136,72", "3.273.136,72 a 4.909.705,08",
            "4.909.705,08 a 7.364.557,62", "7.364.557,62 a 14.729.115,24", "14.729.115,24 a 22.093.672,86",
            "22.093.672,86 a 33.140.509,29", "33.140.509,29 a 49.667.273,02", "Más de 49.667.273,02"
        ],
        "Monto Fijo ($)": ["0,00", "81.828,42", "229.119,57", "425.507,77", "793.735,65", "2.193.001,60", "3.886.949,85", "6.869.585,69", "11.992.882,45"],
        "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"],
        "S/ Excedente de ($)": ["0,00", "1.636.568,36", "3.273.136,72", "4.909.705,08", "7.364.557,62", "14.729.115,24", "22.093.672,86", "33.140.509,29", "49.667.273,02"]
    }
    st.table(pd.DataFrame(data_ph))

with t_deduc:
    st.markdown("#### Importes Art. 30 LIG - Período Fiscal 2025")
    data_deduc = {
        "Concepto (Deducciones Personales)": [
            "Ganancia No Imponible (Art. 30, inc. a)", 
            "Cónyuge / Unión Convivencial (Art. 30, inc. b, pto 1)", 
            "Hijo / Hijastro (Art. 30, inc. b, pto 2)", 
            "Hijo / Hijastro Incapacitado para el trabajo", 
            "Deducción Especial (Art. 30, inc. c, pto 1)", 
            "Deducción Especial Empleados/Jubilados (Art. 30, inc. c, pto 2)"
        ],
        "Monto Anual ($)": [
            "4.093.923,60", 
            "3.858.913,56", 
            "1.946.069,52", 
            "3.892.139,04", 
            "8.187.847,20", 
            "19.650.833,28"
        ]
    }
    st.table(pd.DataFrame(data_deduc))

with t_soc:
    data_soc = {
        "Tramo Ganancia Neta": ["Hasta $101.679.575,26", "De $101.679.575,26 a $1.016.795.752,60", "Más de $1.016.795.752,60"],
        "Alícuota": ["25%", "30%", "35%"],
        "Monto Fijo": ["$0,00", "$25.419.893,82", "$299.954.747,02"]
    }
    st.table(pd.DataFrame(data_soc))

with t_mon:
    st.markdown("#### Escala de Categorías Completa")
    df_mono_full = pd.DataFrame({
        "Cat": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
        "Ingresos Brutos Anuales ($)": [
            "8.987.312,20", "13.345.101,40", "18.677.202,30", "23.211.504,10", "27.321.405,80", 
            "34.112.508,40", "40.876.310,10", "62.011.514,50", "69.455.618,20", "79.445.820,10", "94.805.682,90"
        ],
        "Cuota Total Mensual ($)": ["37.085,00", "42.216,00", "49.435,00", "63.357,00", "81.412,00", "104.256,00", "127.108,00", "244.135,00", "302.510,00", "359.845,00", "428.100,00"]
    })
    st.table(df_mono_full)
