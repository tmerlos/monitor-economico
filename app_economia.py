import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor ARCA & Radar Senior", layout="wide")

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
    st.metric("Nasdaq 100", "20.150,45", "▲ 1.1%")
    st.metric("Balanza Comercial", "USD +2.498M")
    st.metric("Tasa Desempleo", "6.6%")
    if st.button("🔄 Sincronizar"):
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

# --- 5. NOTICIAS Y ALERTAS (RESTAURADO) ---
st.subheader("📰 Actualidad y Alertas del Día")
ce, ci = st.columns(2)
with ce:
    st.markdown("**📈 Economía**")
    for t, l in [
        ("Subsidios: Crédito USD 300M para energía", "https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/"),
        ("Desempleo: Baja al 6,6% según INDEC", "https://www.pagina12.com.ar/2025/12/19/aumenta-la-precariedad-y-baja-el-desempleo/"),
        ("Comercio Exterior: Superávit Noviembre", "https://www.indec.gob.ar/"),
        ("BCRA: Compra sostenida de Reservas", "https://www.bcra.gob.ar/"),
        ("Inflación: Proyecciones cierre 2025", "https://www.ambito.com/economia"),
        ("Billetes: Circulación de nueva denominación", "https://www.lanacion.com.ar/economia/")
    ]:
        st.markdown(f"• [{t}]({l})")
with ci:
    st.markdown("**⚖️ Impositivas (ARCA)**")
    for t, l in [
        ("Umbrales: Precios Transferencia 2025", "https://aldiaargentina.microjuris.com/2025/12/16/legislacion-arca-se-actualizan-precios-de-transferencia/"),
        ("Vencimiento Monotributo Diciembre", "https://www.ambito.com/informacion-general/vencimiento-del-monotributo-diciembre-2025-arca-n6223081"),
        ("Bienes Personales: Nuevas escalas", "https://www.afip.gob.ar/ganancias-y-bienes-personales/"),
        ("Calendario Enero 2026: Vencimientos", "https://www.afip.gob.ar/vencimientos/"),
        ("Blanqueo: Prórrogas y novedades", "https://www.argentina.gob.ar/noticias"),
        ("Facturación Electrónica: Nuevos requisitos", "https://www.afip.gob.ar/noticias/")
    ]:
        st.markdown(f"• [{t}]({l})")

st.divider()

# --- 6. CUADROS DE IMPUESTOS (SET COMPLETO) ---
st.subheader("📊 Cuadros de Impuestos")
t_soc, t_mon, t_rg = st.tabs(["Ganancias Sociedades", "Monotributo 2025", "RG 830"])

with t_soc:
    data_soc = {
        "Tramo Ganancia Neta": ["Hasta $101.6M", "De $101.6M a $1.016M", "Más de $1.016M"],
        "Alícuota": ["25%", "30%", "35%"],
        "Monto Fijo": ["$0,00", "$25.419.893,82", "$299.954.747,02"]
    }
    st.table(pd.DataFrame(data_soc))

with t_mon:
    df_mono_full = pd.DataFrame({
        "Cat": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
        "Ingresos Anuales ($)": ["8.9M", "13.3M", "18.6M", "23.2M", "27.3M", "34.1M", "40.8M", "62.0M", "69.4M", "79.4M", "94.8M"],
        "Cuota Total ($)": ["37.085", "42.216", "49.435", "63.357", "81.412", "104.256", "127.108", "244.135", "302.510", "359.845", "428.100"]
    })
    st.table(df_mono_full)

with t_rg:
    data_rg_full = {
        "Concepto": ["Bienes Muebles", "Servicios", "Honorarios", "Alquileres", "Comisiones", "Fletes"],
        "Mínimo No Sujeto ($)": ["224.000", "98.240", "98.240", "16.360", "45.100", "32.000"],
        "Insc. (%)": ["2,0%", "2,0%", "Escala Art. 94", "6,0%", "3,0%", "0,25%"]
    }
    st.table(pd.DataFrame(data_rg_full))

st.divider()

# --- 7. RENDIMIENTOS E INFLACIÓN ---
st.subheader("📈 Rendimientos e Inflación")
tab_tasas, tab_inflacion = st.tabs(["🏦 Tasas de Interés", "📊 Inflación INDEC"])

with tab_tasas:
    t1, t2 = st.columns(2)
    with t1:
        st.info("### 💰 Fondos y Bancos")
        st.write("**Fima Premium (Santander):** 34.20% TNA")
        st.write("**Santander Plazo Fijo:** 39.00% TNA")
    with t2:
        st.warning("### 🏦 Referencias")
        st.write("**Tasa Badlar:** 42.80% TNA")
        st.write("**Tasa TM20:** 41.10% TNA")

with tab_inflacion:
    df_inf = pd.DataFrame({
        "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Dic (Est)"],
        "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
    })
    df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
    st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 8. RADAR DE SEGUIMIENTO (AL FINAL Y CONDICIONAL) ---
# Lógica: Solo muestra si hay novedades (Simulado en True para esta entrega)
novedades_detectadas = True 

if novedades_detectadas:
    st.subheader("📡 Radar de Alertas: Menciones Nuevas")
    def link_google(q): return f"https://www.google.com/search?q={q.replace(' ', '+')}&tbm=nws&tbs=qdr:w"
    
    ca, cb = st.columns(2)
    with ca:
        st.info("### 👤 Firma y Socios")
        st.markdown(f"• [Menciones: **UHY Macho Argentina**]({link_google('UHY Macho Argentina')})")
        st.markdown(f"• [Menciones: **Roberto E. Macho**]({link_google('Roberto E. Macho')})")
        st.markdown(f"• [Seguimiento: **Tomás Merlos**]({link_google('Tomás Merlos UHY')})")
    with cb:
        st.warning("### 🏢 Corporativo")
        st.markdown(f"• [Radar: **Novomatic Argentina**]({link_google('Novomatic Argentina')})")
        st.markdown(f"• [Radar: **Octavian Argentina**]({link_google('Octavian Argentina')})")
