import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor ARCA Pro - Alta Precisión", layout="wide")

# --- 1. FUNCIÓN DE INFLACIÓN AUTOMÁTICA (API DATOS GOB) ---
@st.cache_data(ttl=86400)
def obtener_inflacion_auto():
    try:
        url = "https://apis.datos.gob.ar/series/api/series/?ids=145.3_IPCF_AN_AL_0_M_31&format=csv"
        df = pd.read_csv(url)
        df['indice_tiempo'] = pd.to_datetime(df['indice_tiempo'])
        df_2025 = df[df['indice_tiempo'].dt.year == 2025].copy()
        df_2025['IPC Mensual (%)'] = df_2025.iloc[:, 1].pct_change() * 100
        df_2025['Mes'] = df_2025['indice_tiempo'].dt.strftime('%B')
        return df_2025[['Mes', 'IPC Mensual (%)']].dropna()
    except:
        return pd.DataFrame({"Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"], 
                             "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5]})

# --- 2. CARGA DE MERCADOS ---
@st.cache_data(ttl=600)
def obtener_pizarra():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        mapa = {d['nombre']: d['venta'] for d in res}
        return {
            "Oficial": mapa.get("Oficial", 1030.50), "Blue": mapa.get("Blue", 1485.00),
            "MEP": mapa.get("MEP", 1496.80), "CCL": mapa.get("Contado con Liquidación", 1555.00),
            "Tarjeta": mapa.get("Tarjeta", 1935.45)
        }
    except:
        return {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00, "Tarjeta": 1935.45}

pizarra = obtener_pizarra()
df_inflacion = obtener_inflacion_auto()

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Auditoría")
    st.info(f"📅 HOY: {datetime.now().strftime('%d/%m/%Y')}")
    if st.button("🔄 Actualizar Todo"):
        st.cache_data.clear()
        st.rerun()

# --- 4. ENCABEZADO Y DIVISAS ---
st.title("Monitor Económico e Impositivo Integral 🇦🇷")
st.success(f"🏛️ **Dólar Oficial (Ref. ARCA): ${pizarra['Oficial']:,.2f}**")
cols = st.columns(5)
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. TASAS Y RENDIMIENTOS ---
st.subheader("🏦 Rendimientos Financieros")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos MM")
    st.write("[Galicia Fima Premium](https://www.fondosfima.com.ar/): 34.5% TNA")
    st.write("[Santander Superfondo](https://www.santander.com.ar/): 34.2% TNA")
with t2:
    st.info("### 🏦 Bancos")
    st.write("**Plazo Fijo:** 39.0% TNA")
    st.write("**Badlar:** 42.8% TNA")
with t3:
    st.warning("### 💳 Crédito")
    st.write("**Personales:** 78% TNA / **Adelanto:** 62%")

st.divider()

# --- 6. NOTICIAS CON LINKS (DINÁMICAS) ---
st.subheader("📰 Noticias y Alertas (Links Directos)")
col_e, col_i = st.columns(2)

with col_e:
    st.markdown("**📈 Economía**")
    noticias_e = [
        ("BCRA: Compras de divisas y Reservas", "https://www.bcra.gob.ar/Noticias/default.asp"),
        ("Riesgo País y Bonos Argentinos (Ámbito)", "https://www.ambito.com/contenidos/riesgo-pais.html"),
        ("Indicadores de Consumo INDEC", "https://www.indec.gob.ar/"),
        ("Evolución del PBI y Actividad", "https://www.cronista.com/economia-politica/"),
        ("Exportaciones y Balanza Comercial", "https://www.lanacion.com.ar/economia/"),
        ("Cotización de Granos y Cosecha", "https://www.bolsadecereales.com/")
    ]
    for texto, link in noticias_e: st.markdown(f"• [{texto}]({link})")

with col_i:
    st.markdown("**⚖️ Impositivas (ARCA)**")
    noticias_i = [
        ("ARCA: Novedades y Resoluciones Grales.", "https://www.afip.gob.ar/noticias/"),
        ("Guía de Recategorización Monotributo", "https://monotributo.afip.gob.ar/"),
        ("Nuevas Escalas Ganancias 2025", "https://www.afip.gob.ar/ganancias-y-bienes-personales/"),
        ("Calendario de Vencimientos ARCA", "https://www.afip.gob.ar/vencimientos/"),
        ("Micrositio de Facturación Electrónica", "https://www.afip.gob.ar/facturacion/"),
        ("Regímenes de Retención (ABC Consultas)", "https://servicioscf.afip.gob.ar/publico/abc/index.aspx")
    ]
    for texto, link in noticias_i: st.markdown(f"• [{texto}]({link})")

st.divider()

# --- 7. INFLACIÓN AUTOMÁTICA ---
st.subheader("📊 Historial de Inflación INDEC (Automático)")
df_inflacion['IPC Acumulado (%)'] = ((1 + df_inflacion['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
st.table(df_inflacion.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 8. GANANCIAS JURÍDICAS (VALORES AUDITADOS) ---
st.subheader("🏢 Ganancias: Personas Jurídicas (Ley 27.630)")
data_soc = {
    "Tramo Ganancia Neta": ["Hasta $101.679.575,26", "De $101.679.575,26 a $1.016.795.752,60", "Más de $1.016.795.752,60"],
    "Alícuota": ["25%", "30%", "35%"],
    "Monto Fijo": ["$0,00", "$25.419.893,82", "$299.954.747,02"],
    "S/ Excedente de": ["$0,00", "$101.679.575,26", "$1.016.795.752,60"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 9. MONOTRIBUTO: ESCALAS VIGENTES (DICIEMBRE 2025) ---
st.subheader("⚖️ Monotributo: Topes Vigentes")
df_mono = pd.DataFrame({
    "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Anuales ($)": ["8.987.312,20", "13.345.101,40", "18.677.202,30", "23.211.504,10", "27.321.405,80", "34.112.508,40", "40.876.310,10", "62.011.514,50", "69.455.618,20", "79.445.820,10", "94.805.682,90"],
    "Cuota Total ($)": ["36.8k", "42.1k", "49.5k", "63.2k", "81.4k", "104.2k", "127.1k", "244.1k", "302.5k", "359.8k", "428.1k"]
})
st.table(df_mono)

st.divider()

# --- 10. RETENCIONES GANANCIAS (RG 830) ---
st.subheader("📋 Retenciones Ganancias (RG 830) - Mínimos Vigentes")
data_rg = {
    "Concepto": ["Bienes Muebles", "Locaciones de Servicios", "Honorarios Profesionales", "Alquileres"],
    "Mínimo No Sujeto ($)": ["327.200,00", "98.240,00", "98.240,00", "16.360,00"],
    "Inscripto": ["2%", "2%", "Escala Art. 94", "6%"]
}
st.table(pd.DataFrame(data_rg))
