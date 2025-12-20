import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor ARCA & Seguimiento UHY", layout="wide")

# --- 1. CARGA DE MERCADOS ---
@st.cache_data(ttl=600)
def obtener_datos():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        return {d['nombre']: d['venta'] for d in res}
    except:
        return {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00}

pizarra = obtener_datos()

# --- 2. SIDEBAR CON ÍNDICES CRÍTICOS ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Auditoría")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    
    st.markdown("### 🔍 Índices Críticos")
    st.metric("Riesgo País", "754 bps", "-31") 
    st.metric("Índice Merval", "2.140.580", "▲ 2.4%")
    st.metric("Balanza Comercial", "USD +2.498M", "Superávit")
    st.metric("Tasa Desempleo", "6.6%", "Estable")
    
    if st.button("🔄 Actualizar Monitor"):
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

# --- 6. TABLAS TÉCNICAS (CON VALORES AUDITADOS) ---
st.subheader("📊 Cuadros de Auditoría")
t1, t2, t3 = st.tabs(["Ganancias Sociedades", "Monotributo", "RG 830"])

with t1:
    st.write("**Escala Ley 27.630 - Primer Tramo: $101.679.575,26**")
    data_soc = {
        "Tramo": ["Hasta $101.6M", "De $101.6M a $1.016M", "Más de $1.016M"],
        "Alícuota": ["25%", "30%", "35%"],
        "Fijo ($)": ["$0,00", "$25.419.893,82", "$299.954.747,02"]
    }
    st.table(pd.DataFrame(data_soc))

with t2:
    st.write("**Tope Cat K:** $94.805.682,90")
    st.caption("Ajustado a diciembre 2025.")

with t3:
    st.write("**Mínimo Enajenación Bienes Muebles:** $224.000,00")
    data_rg = {
        "Concepto": ["Bienes Muebles", "Servicios", "Honorarios"],
        "Mínimo ($)": ["224.000,00", "98.240,00", "98.240,00"],
        "Alícuota Insc.": ["2%", "2%", "Escala Art. 94"]
    }
    st.table(pd.DataFrame(data_rg))

st.divider()

# --- 7. SECCIÓN DE SEGUIMIENTO (AL FINAL) ---
st.subheader("📡 Radar de Menciones en Internet")
st.warning("Haga clic en los enlaces para buscar menciones nuevas detectadas en las últimas 24hs/semana.")

# Generamos links de búsqueda dinámica para seguimiento
def link_busqueda(query):
    return f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=nws&tbs=qdr:w"

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.info("### 🏢 UHY Macho")
    st.markdown(f"""
    * [Ver menciones en Noticias (última semana)]({link_busqueda('UHY Macho Argentina')})
    * [Ver menciones en Web general]({link_busqueda('UHY Macho & Asociados')})
    """)

with col_m2:
    st.info("### 👨‍💼 Roberto E. Macho")
    st.markdown(f"""
    * [Ver menciones en Noticias (última semana)]({link_busqueda('Roberto E. Macho contador')})
    * [Ver menciones en Web general]({link_busqueda('Roberto E. Macho UHY')})
    """)

with col_m3:
    st.info("### 👨‍⚖️ Tomás Merlos")
    st.markdown(f"""
    * [Ver menciones en Noticias (última semana)]({link_busqueda('Tomás Merlos UHY Macho')})
    * [Ver menciones en Web general]({link_busqueda('Tomás Merlos impuestos')})
    """)
