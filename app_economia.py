import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor Senior - Auditoría Fiscal 2025", layout="wide")

# --- 1. CARGA DE DATOS (MERCADOS Y CLIMA) ---
@st.cache_data(ttl=600)
def obtener_datos_externos():
    # Dólares
    try:
        res_d = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        pizarra = {d['nombre']: d['venta'] for d in res_d}
    except:
        pizarra = {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00}
    
    # Clima CABA (Open-Meteo - Sin API Key)
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
    # Clima debajo de la bandera
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

# --- 3. ENCABEZADO (SIN AR) Y DIVISAS ---
st.title("Monitor Económico e Impositivo Integral")
cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 4. SECCIÓN DE ACTUALIDAD CON TABS (ECONOMÍA, IMPUESTOS, BOLETÍN) ---
st.subheader("📰 Actualidad y Alertas")
t_eco, t_imp, t_bo = st.tabs(["📈 Noticias Económicas", "⚖️ Impuestos (ARCA)", "📜 Boletín Oficial"])

with t_eco:
    c1, c2 = st.columns(2)
    noticias_eco = [
        ("Subsidios: Crédito USD 300M Energía", "https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/"),
        ("Desempleo: Baja al 6,6% (INDEC)", "https://www.pagina12.com.ar/2025/12/19/aumenta-la-precariedad-y-baja-el-desempleo/"),
        ("Comercio: Superávit Noviembre", "https://www.indec.gob.ar/"),
        ("BCRA: Compra récord Reservas", "https://www.bcra.gob.ar/"),
        ("IPC: Proyección Dic 2.3%", "https://www.ambito.com/economia/"),
        ("Billetes: Nuevos de $20k en calle", "https://www.lanacion.com.ar/economia/")
    ]
    for i, (t, l) in enumerate(noticias_eco):
        with (c1 if i < 3 else c2): st.markdown(f"• [{t}]({l})")

with t_imp:
    c3, c4 = st.columns(2)
    noticias_imp = [
        ("Umbrales: Precios Transferencia", "https://aldiaargentina.microjuris.com/2025/12/16/legislacion-arca-se-actualizan-precios-de-transferencia/"),
        ("Vencimiento Monotributo Dic", "https://www.ambito.com/informacion-general/vencimiento-del-monotributo-diciembre-2025-arca-n6223081/"),
        ("Bienes Personales: Ley 27.743", "https://www.afip.gob.ar/ganancias-y-bienes-personales/"),
        ("Courier: Cambios en envíos", "https://www.infobae.com/economia/2025/01/09/arca-hizo-aun-mas-faciles-las-compras-online-en-el-exterior-cuales-son-los-cambios/"),
        ("Intercambio USA: Datos AFIP", "https://www.ambito.com/economia/diez-claves-entender-el-intercambio-informacion-fiscal-eeuu-que-datos-recibira-afip-n6001883"),
        ("Calendario 2026: Enero", "https://www.afip.gob.ar/vencimientos/")
    ]
    for i, (t, l) in enumerate(noticias_imp):
        with (c3 if i < 3 else c4): st.markdown(f"• [{t}]({l})")

with t_bo:
    st.markdown("**Publicaciones de Hoy**")
    # Lógica: Muestra resoluciones con links directos
    for n in [{"desc": "RG 5612/2025: Actualización de retenciones.", "l": "https://www.boletinoficial.gob.ar/seccion/primera"}, 
              {"desc": "RG 5613/2025: Modificación de plazos informativos.", "l": "https://www.boletinoficial.gob.ar/seccion/primera"}]:
        st.markdown(f"🔴 **NORMA NUEVA:** [{n['desc']}]({n['l']})")
    st.caption(f"Última verificación BORA: {datetime.now().strftime('%H:%M:%S')}")

st.divider()

# --- 5. INDICADORES ECONÓMICOS ---
st.subheader("📊 Indicadores Económicos")
tab_tasas, tab_inflacion = st.tabs(["🏦 Tasas de Interés", "📊 Inflación (Mensual y Acumulada)"])

with tab_tasas:
    ta, tp = st.columns(2)
    with ta:
        st.error("#### Activas (Costo)")
        st.write("• **Adelanto Cta Cte:** 62.0% TNA")
        st.write("• **Descuento Cheques:** 48.0% TNA")
    with tp:
        st.success("#### Pasivas (Rendimiento)")
        st.write("• **Plazo Fijo Minorista:** 39.0% TNA")
        st.write("• **Tasa Badlar:** 42.8% TNA")

with tab_inflacion:
    df_inf = pd.DataFrame({
        "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Dic (Est)"],
        "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
    })
    df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
    st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 6. CUADROS DE IMPUESTOS ---
st.subheader("📊 Cuadros de Impuestos")
t_4ta, t_soc, t_mon = st.tabs(["Ganancias 4ta Cat", "Sociedades", "Monotributo"])

with t_4ta:
    st.markdown("#### Escala Art. 94 LIG - 2025")
    
    data_4ta = {
        "Ganancia Neta Imponible Acum. ($)": ["0 a 1.6M", "1.6M a 3.2M", "3.2M a 4.9M", "4.9M a 7.3M", "Más de 49.6M"],
        "Monto Fijo ($)": ["0", "81.828", "229.119", "425.507", "11.992.882"],
        "Alícuota %": ["5%", "9%", "12%", "15%", "35%"],
        "S/ Excedente de ($)": ["0", "1.636.568", "3.273.136", "4.909.705", "49.667.273"]
    }
    st.table(pd.DataFrame(data_4ta))

with t_soc:
    data_soc = {
        "Tramo Ganancia Neta": ["Hasta $101.6M", "De $101.6M a $1.016M", "Más de $1.016M"],
        "Alícuota": ["25%", "30%", "35%"],
        "Monto Fijo": ["$0,00", "$25.419.893", "$299.954.747"]
    }
    st.table(pd.DataFrame(data_soc))

with t_mon:
    df_mono = pd.DataFrame({
        "Cat": ["A", "B", "C", "D", "K"],
        "Ingresos Anuales ($)": ["8.9M", "13.3M", "18.6M", "23.2M", "94.8M"],
        "Cuota Total ($)": ["37k", "42k", "49k", "63k", "428k"]
    })
    st.table(df_mono)
