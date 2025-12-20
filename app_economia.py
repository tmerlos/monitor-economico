import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor ARCA Senior - Datos Completos", layout="wide")

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

# --- 5. CUADROS DE IMPUESTOS (SET COMPLETO) ---
st.subheader("📊 Cuadros de Impuestos")
t_soc, t_mon, t_rg = st.tabs(["Ganancias Sociedades", "Monotributo 2025 (Completo)", "RG 830 (Completo)"])

with t_soc:
    st.write("**Escala Progresiva Ley 27.630**")
    
    data_soc = {
        "Tramo Ganancia Neta": ["Hasta $101.679.575,26", "De $101.679.575,26 a $1.016.795.752,60", "Más de $1.016.795.752,60"],
        "Alícuota": ["25%", "30%", "35%"],
        "Monto Fijo": ["$0,00", "$25.419.893,82", "$299.954.747,02"],
        "Sobre Excedente de": ["$0,00", "$101.679.575,26", "$1.016.795.752,60"]
    }
    st.table(pd.DataFrame(data_soc))

with t_mon:
    st.write("**Escala de Categorías Vigentes - Diciembre 2025**")
    df_mono_full = pd.DataFrame({
        "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
        "Ingresos Brutos Anuales ($)": [
            "8.987.312,20", "13.345.101,40", "18.677.202,30", "23.211.504,10", "27.321.405,80", 
            "34.112.508,40", "40.876.310,10", "62.011.514,50", "69.455.618,20", "79.445.820,10", "94.805.682,90"
        ],
        "Cuota Total Mensual ($)": ["37.085", "42.216", "49.435", "63.357", "81.412", "104.256", "127.108", "244.135", "302.510", "359.845", "428.100"]
    })
    st.table(df_mono_full)

with t_rg:
    st.write("**Anexo II - Régimen de Retención General (RG 830)**")
    
    data_rg_full = {
        "Concepto": [
            "Enajenación de Bienes Muebles", 
            "Locaciones de Obra/Servicios (No Profesionales)", 
            "Honorarios Profesionales Liberales", 
            "Alquileres de Inmuebles", 
            "Comisiones y Consignaciones", 
            "Intereses por Préstamos", 
            "Derechos de Autor", 
            "Fletes y Acarreos", 
            "Subsidios y Ayudas del Estado"
        ],
        "Mínimo No Sujeto ($)": [
            "224.000,00", "98.240,00", "98.240,00", "16.360,00", "45.100,00", 
            "Sin Mínimo", "22.400,00", "32.000,00", "15.000,00"
        ],
        "Alícuota Inscripto": ["2,0%", "2,0%", "Escala Art. 94 (Mín 3%)", "6,0%", "3,0%", "6,0%", "Escala Art. 94", "0,25%", "2,0%"],
        "Alícuota No Insc.": ["25%", "28%", "28%", "28%", "28%", "28%", "28%", "25%", "28%"]
    }
    st.table(pd.DataFrame(data_rg_full))

st.divider()

# --- 6. RENDIMIENTOS E INFLACIÓN ---
st.subheader("📈 Rendimientos e Inflación")
tab_tasas, tab_inflacion = st.tabs(["🏦 Tasas de Interés", "📊 Inflación INDEC"])

with tab_tasas:
    t1, t2 = st.columns(2)
    with t1:
        st.info("### 💰 Fondos y Bancos")
        st.write("**Fima Premium (Santander):** 34.20% TNA")
        st.write("**Santander Plazo Fijo:** 39.00% TNA")
        st.write("**Galicia Money Market:** 34.50% TNA")
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

# --- 7. RADAR DE SEGUIMIENTO (CONDICIONAL) ---
# Simulación de detección
novedades = {"UHY": True, "Roberto": True, "Empresas": True}

if any(novedades.values()):
    st.subheader("📡 Radar de Alertas: Menciones Nuevas")
    def link(q): return f"https://www.google.com/search?q={q.replace(' ', '+')}&tbm=nws&tbs=qdr:w"
    
    ca, cb = st.columns(2)
    with ca:
        st.info("### 👤 Firma y Socios")
        st.markdown(f"• [Menciones: **UHY Macho Argentina**]({link('UHY Macho Argentina')})")
        st.markdown(f"• [Menciones: **Roberto E. Macho**]({link('Roberto E. Macho')})")
        st.markdown(f"• [Menciones: **Tomás Merlos**]({link('Tomás Merlos UHY')})")
    with cb:
        st.warning("### 🏢 Corporativo")
        st.markdown(f"• [Radar: **Novomatic Argentina**]({link('Novomatic Argentina')})")
        st.markdown(f"• [Radar: **Octavian Argentina**]({link('Octavian Argentina')})")
else:
    st.empty()
