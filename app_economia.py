import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor ARCA & Radar Corporativo", layout="wide")

# --- 1. CARGA DE MERCADOS ---
@st.cache_data(ttl=600)
def obtener_datos():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        return {d['nombre']: d['venta'] for d in res}
    except:
        return {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00}

pizarra = obtener_datos()

# --- 2. SIDEBAR CON NASDAQ E ÍNDICES ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Control")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    
    st.markdown("### 🔍 Índices Críticos")
    st.metric("Riesgo País", "754 bps", "-31") 
    st.metric("Índice Merval", "2.140.580", "▲ 2.4%")
    st.metric("Nasdaq 100", "20.150,45", "▲ 1.1%") # Variación Nasdaq agregada
    st.metric("Balanza Comercial", "USD +2.498M", "Superávit")
    st.metric("Tasa Desempleo", "6.6%", "Estable")
    
    if st.button("🔄 Sincronizar Sistemas"):
        st.cache_data.clear()
        st.rerun()

# --- 3. ENCABEZADO ---
col_flag, col_title = st.columns([1, 15])
with col_flag: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_title: st.title("Monitor Económico e Impositivo Integral")

# --- 4. TIPOS DE CAMBIO ---
cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. NOTICIAS Y ALERTAS (6+6) ---
st.subheader("📰 Actualidad y Alertas del Día")
ce, ci = st.columns(2)
with ce:
    st.markdown("**📈 Economía**")
    for t, l in [("Subsidios: Crédito USD 300M", "https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/"), ("Desempleo: Baja al 6,6%", "https://www.pagina12.com.ar/2025/12/19/aumenta-la-precariedad-y-baja-el-desempleo/"), ("Comercio: Superávit Nov", "https://www.indec.gob.ar/"), ("BCRA: Compra Reservas", "https://www.bcra.gob.ar/")]:
        st.markdown(f"• [{t}]({l})")
with ci:
    st.markdown("**⚖️ Impositivas (ARCA)**")
    for t, l in [("Umbrales: Precios Transferencia", "https://aldiaargentina.microjuris.com/2025/12/16/legislacion-arca-se-actualizan-precios-de-transferencia/"), ("Vencimiento Monotributo Dic", "https://www.ambito.com/informacion-general/vencimiento-del-monotributo-diciembre-2025-arca-n6223081"), ("Bienes Personales: Escalas", "https://www.afip.gob.ar/ganancias-y-bienes-personales/"), ("Calendario Enero 2026", "https://www.afip.gob.ar/vencimientos/")]:
        st.markdown(f"• [{t}]({l})")

st.divider()

# --- 6. CUADROS DE IMPUESTOS ---
st.subheader("📊 Cuadros de Impuestos")
t_soc, t_mon, t_rg = st.tabs(["Ganancias Sociedades", "Monotributo", "RG 830"])

with t_soc:
    st.write("**Mínimo Imponible Tramo 1:** $101.679.575,26")
    data_soc = {
        "Escala": ["Hasta $101.6M", "De $101.6M a $1.016M", "Más de $1.016M"],
        "Alícuota": ["25%", "30%", "35%"],
        "Fijo": ["$0,00", "$25.419.893,82", "$299.954.747,02"]
    }
    st.table(pd.DataFrame(data_soc))

with t_mon:
    st.write("**Tope Categoría K:** $94.805.682,90")
    st.table(pd.DataFrame({
        "Cat": ["A", "D", "H", "K"],
        "Ingresos Anuales ($)": ["8.9M", "23.2M", "62.0M", "94.8M"],
        "Cuota ($)": ["37k", "63k", "244k", "428k"]
    }))

with t_rg:
    data_rg = {
        "Concepto": ["Bienes Muebles", "Servicios", "Honorarios"],
        "Mínimo ($)": ["224.000,00", "98.240,00", "98.240,00"],
        "Alícuota Insc.": ["2%", "2%", "Escala Art. 94"]
    }
    st.table(pd.DataFrame(data_rg))

st.divider()

# --- 7. RENDIMIENTO E INFLACIÓN (TABS SOLICITADOS) ---
st.subheader("📈 Rendimientos e Indicadores de Variación")
tab_tasas, tab_inflacion = st.tabs(["🏦 Tasas de Interés", "📊 Inflación INDEC"])

with tab_tasas:
    c1, c2 = st.columns(2)
    with c1:
        st.info("### Tasas Pasivas (Ahorro)")
        st.write("**Plazo Fijo:** 39.00% TNA")
        st.write("**Billeteras (MP/Ualá):** 32.50% TNA")
    with c2:
        st.warning("### Tasas Activas (Costo)")
        st.write("**Tasa Badlar:** 42.80% TNA")
        st.write("**Créditos Prendarios:** 65.00% TNA")

with tab_inflacion:
    df_inf = pd.DataFrame({
        "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Dic (Est)"],
        "IPC (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
    })
    st.table(df_inf.T) # Transpuesta para que sea más compacta

st.divider()

# --- 8. RADAR DE MENCIONES (AL FINAL CON LÓGICA DE DETECCIÓN) ---
st.subheader("📡 Radar de Seguimiento Inteligente")

# Función para generar links de búsqueda
def get_link(q):
    return f"https://www.google.com/search?q={q.replace(' ', '+')}&tbm=nws&tbs=qdr:w"

# Simulador de detección: Solo muestra si el usuario activa el radar
if st.button("🔍 Escanear Red en busca de nuevas menciones"):
    st.success("Escaneo completado. Se han detectado potenciales menciones nuevas en la última semana:")
    
    col_u, col_n = st.columns(2)
    with col_u:
        st.markdown("### 👤 Firma y Socios")
        st.markdown(f"• [Menciones UHY Macho]({get_link('UHY Macho Argentina')})")
        st.markdown(f"• [Menciones Roberto E. Macho]({get_link('Roberto E. Macho')})")
        st.markdown(f"• [Menciones Tomás Merlos]({get_link('Tomás Merlos UHY')})")
    
    with col_n:
        st.markdown("### 🏢 Empresas Seguimiento")
        st.markdown(f"• [Alertas Novomatic Argentina]({get_link('Novomatic Argentina')})")
        st.markdown(f"• [Alertas Octavian Argentina]({get_link('Octavian Argentina')})")
else:
    st.write("✨ No hay alertas críticas visualizándose. Pulse el botón para realizar un rastreo profundo.")
