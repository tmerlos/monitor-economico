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

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Control")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    
    st.markdown("### 🔍 Índices Críticos")
    st.metric("Riesgo País", "754 bps", "-31") 
    st.metric("Índice Merval", "2.140.580", "▲ 2.4%")
    st.metric("Balanza Comercial", "USD +2.498M", "Superávit")
    st.metric("Tasa Desempleo", "6.6%", "Estable")
    
    if st.button("🔄 Actualizar Sistemas"):
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

# --- 5. RADAR DE SEGUIMIENTO (ALERTAS DINÁMICAS) ---
st.subheader("📡 Radar de Menciones y Alertas Corporativas")
st.caption("Se muestran accesos directos a las menciones detectadas en las últimas 24hs/semana.")

def link_alerta(query):
    return f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=nws&tbs=qdr:w"

# Bloque de Firma y Socios
with st.expander("👤 Seguimiento: UHY Macho, Roberto Macho y Tomás Merlos", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"🔍 [Menciones UHY Macho]({link_alerta('UHY Macho Argentina')})")
    with c2: st.markdown(f"🔍 [Menciones Roberto E. Macho]({link_alerta('Roberto E. Macho')})")
    with c3: st.markdown(f"🔍 [Menciones Tomás Merlos]({link_alerta('Tomás Merlos UHY')})")

# Bloque de Empresas (Novomatic / Octavian)
with st.expander("🏢 Seguimiento Corporativo: Novomatic & Octavian", expanded=True):
    ca, cb = st.columns(2)
    with ca: st.markdown(f"🚨 [Alertas Novomatic Argentina]({link_alerta('Novomatic Argentina')})")
    with cb: st.markdown(f"🚨 [Alertas Octavian Argentina]({link_alerta('Octavian Argentina')})")

st.divider()

# --- 6. NOTICIAS 6+6 ---
st.subheader("📰 Actualidad del Día")
ce, ci = st.columns(2)
with ce:
    st.markdown("**Economía**")
    for t, l in [("Subsidios: Crédito USD 300M", "https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/"), ("Desempleo: Baja al 6,6%", "https://www.pagina12.com.ar/2025/12/19/aumenta-la-precariedad-y-baja-el-desempleo/"), ("Comercio: Superávit Nov", "https://www.indec.gob.ar/"), ("BCRA: Compra Reservas", "https://www.bcra.gob.ar/")]:
        st.markdown(f"• [{t}]({l})")
with ci:
    st.markdown("**Impositivas (ARCA)**")
    for t, l in [("Umbrales: Precios Transferencia", "https://aldiaargentina.microjuris.com/2025/12/16/legislacion-arca-se-actualizan-precios-de-transferencia/"), ("Vencimiento Monotributo Dic", "https://www.ambito.com/informacion-general/vencimiento-del-monotributo-diciembre-2025-arca-n6223081"), ("Bienes Personales: Escalas", "https://www.afip.gob.ar/ganancias-y-bienes-personales/"), ("Calendario Enero 2026", "https://www.afip.gob.ar/vencimientos/")]:
        st.markdown(f"• [{t}]({l})")

st.divider()

# --- 7. CUADROS DE IMPUESTOS (TÍTULO ACTUALIZADO) ---
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
    st.caption("Ajustado por IPC a Diciembre 2025.")

with t_rg:
    data_rg = {
        "Concepto": ["Bienes Muebles", "Servicios", "Honorarios"],
        "Mínimo ($)": ["224.000,00", "98.240,00", "98.240,00"],
        "Alícuota Insc.": ["2%", "2%", "Escala Art. 94"]
    }
    st.table(pd.DataFrame(data_rg))

st.divider()

# --- 8. INFLACIÓN ---
st.subheader("📊 Historial de Inflación INDEC 2025")
df_inf = pd.DataFrame({
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre (Est)"],
    "IPC (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
})
df_inf['Acumulada (%)'] = ((1 + df_inf['IPC (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC (%)": "{:.1f}%", "Acumulada (%)": "{:.1f}%"}))
