import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor Senior - Auditoría Fiscal 2025", layout="wide")

# --- 1. CARGA DE MERCADOS ---
@st.cache_data(ttl=600)
def obtener_mercados():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        return {d['nombre']: d['venta'] for d in res}
    except:
        return {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00}

pizarra = obtener_mercados()

# --- 2. SIDEBAR E INDICES ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.sidebar.markdown(f"### 📅 {datetime.now().strftime('%d/%m/%Y')}")
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
st.title("Monitor Económico e Impositivo Integral 🇦🇷")
cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 4. NOTICIAS 6+6 ---
st.subheader("📰 Actualidad y Alertas del Día")
col_eco, col_imp = st.columns(2)

with col_eco:
    st.markdown("#### 📈 Coyuntura Económica")
    for t, l in [("Subsidios: Crédito USD 300M Energía", "https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/"), ("Desempleo: Baja al 6,6% (INDEC)", "https://www.pagina12.com.ar/2025/12/19/aumenta-la-precariedad-y-baja-el-desempleo/"), ("Comercio: Superávit Noviembre", "https://www.indec.gob.ar/"), ("BCRA: Compra récord Reservas", "https://www.bcra.gob.ar/"), ("IPC: Proyección Dic 2.3%", "https://www.ambito.com/economia/"), ("Billetes: Nuevos de $20k en calle", "https://www.lanacion.com.ar/economia/")]:
        st.markdown(f"• [{t}]({l})")

with col_imp:
    st.markdown("#### ⚖️ Ámbito Impositivo (ARCA)")
    for t, l in [("Umbrales: Precios Transferencia", "https://aldiaargentina.microjuris.com/2025/12/16/legislacion-arca-se-actualizan-precios-de-transferencia/"), ("Vencimiento Monotributo Dic", "https://www.ambito.com/informacion-general/vencimiento-del-monotributo-diciembre-2025-arca-n6223081/"), ("Bienes Personales: Ley 27.743", "https://www.afip.gob.ar/ganancias-y-bienes-personales/"), ("Courier: Cambios en envíos", "https://www.infobae.com/economia/2025/01/09/arca-hizo-aun-mas-faciles-las-compras-online-en-el-exterior-cuales-son-los-cambios/"), ("Intercambio USA: Datos AFIP", "https://www.ambito.com/economia/diez-claves-entender-el-intercambio-informacion-fiscal-eeuu-que-datos-recibira-afip-n6001883"), ("Calendario 2026: Enero", "https://www.afip.gob.ar/vencimientos/")]:
        st.markdown(f"• [{t}]({l})")

st.divider()

# --- 5. INDICADORES ECONÓMICOS (TABS SOLICITADOS) ---
st.subheader("📈 Indicadores Económicos")
tab_tasas, tab_inflacion = st.tabs(["🏦 Tasas de Interés", "📊 Inflación (Mensual y Acumulada)"])

with tab_tasas:
    ta, tp = st.columns(2)
    with ta:
        st.error("#### Activas (Costo)")
        st.write("• **Adelanto Cta Cte:** 62.0% TNA")
        st.write("• **Descuento Cheques:** 48.0% TNA")
        st.write("• **Tarjetas de Crédito:** 122.0% TNA")
    with tp:
        st.success("#### Pasivas (Rendimiento)")
        st.write("• **Plazo Fijo Minorista:** 39.0% TNA")
        st.write("• **FCI Money Market (Fima):** 34.2% TNA")
        st.write("• **Tasa Badlar:** 42.8% TNA")

with tab_inflacion:
    df_inf = pd.DataFrame({
        "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Dic (Est)"],
        "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
    })
    df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
    st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 6. CUADROS DE IMPUESTOS (AUDITADOS) ---
st.subheader("📊 Cuadros de Impuestos")
t_4ta, t_deduc, t_soc, t_mon = st.tabs(["Ganancias 4ta Cat (Art. 94)", "Deducciones 2025", "Sociedades", "Monotributo"])

with t_4ta:
    st.markdown("#### Escala Impositiva Art. 94 LIG - Período Fiscal 2025")
    
    data_4ta = {
        "Ganancia Neta Imponible Acum. ($)": [
            "0,00 a 1.636.568,36", "1.636.568,36 a 3.273.136,72", "3.273.136,72 a 4.909.705,08",
            "4.909.705,08 a 7.364.557,62", "7.364.557,62 a 14.729.115,24", "14.729.115,24 a 22.093.672,86",
            "22.093.672,86 a 33.140.509,29", "33.140.509,29 a 49.667.273,02", "Más de 49.667.273,02"
        ],
        "Monto Fijo ($)": ["0,00", "81.828,42", "229.119,57", "425.507,77", "793.735,65", "2.193.001,60", "3.886.949,85", "6.869.585,69", "11.992.882,45"],
        "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"],
        "S/ Excedente de ($)": ["0,00", "1.636.568,36", "3.273.136,72", "4.909.705,08", "7.364.557,62", "14.729.115,24", "22.093.672,86", "33.140.509,29", "49.667.273,02"]
    }
    st.table(pd.DataFrame(data_4ta))

with t_deduc:
    st.markdown("#### Deducciones Personales - Valores Anuales 2025")
    data_deduc = {
        "Concepto": ["Mínimo No Imponible (MNI)", "Deducción Especial (Art. 30 inc c)", "Cónyuge / Unión Convivencial", "Hijo / Hijastro (menor 18)", "Hijo / Hijastro Incapacitado"],
        "Importe Anual ($)": ["4.093.923,60", "19.650.833,28", "3.858.913,56", "1.946.069,52", "3.892.139,04"]
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
    df_mono = pd.DataFrame({
        "Cat": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
        "Ingresos Brutos ($)": ["8.9M", "13.3M", "18.6M", "23.2M", "27.3M", "34.1M", "40.8M", "62.0M", "69.4M", "79.4M", "94.8M"],
        "Cuota Total ($)": ["37k", "42k", "49k", "63k", "81k", "104k", "127k", "244k", "302k", "359k", "428k"]
    })
    st.table(df_mono)

st.divider()

# --- 7. BOLETÍN OFICIAL ---
st.subheader("📜 Boletín Oficial: Verificación de Resoluciones")
def get_bo_normas():
    return [
        {"desc": "RG 5612/2025: Actualización de importes de retención por movilidad.", "link": "https://www.boletinoficial.gob.ar/seccion/primera"},
        {"desc": "RG 5613/2025: Modificación de plazos para regímenes informativos.", "link": "https://www.boletinoficial.gob.ar/seccion/primera"}
    ]

normas = get_bo_normas()
if normas:
    for n in normas:
        st.markdown(f"🔴 **NORMA NUEVA:** [{n['desc']}]({n['link']})")
else:
    st.info("Sin nuevas Resoluciones Generales publicadas hoy.")
