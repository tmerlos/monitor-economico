import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor ARCA - UHY Macho & Asociados", layout="wide")

# --- 1. CARGA DE MERCADOS (Sincronizado) ---
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
    st.title("Panel de Control Senior")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    
    st.markdown("### 🔍 Índices Críticos")
    st.metric("Riesgo País", "754 bps", "-31", delta_color="normal") 
    st.metric("Índice Merval", "2.140.580", "▲ 2.4%", delta_color="normal")
    st.metric("Balanza Comercial", "USD +2.498M", "Superávit")
    st.metric("Tasa Desempleo", "6.6%", "Estable")
    st.metric("Reservas Netas", "USD 31.2B", "+450M")
    
    st.divider()
    if st.button("🔄 Sincronizar Sistemas"):
        st.cache_data.clear()
        st.rerun()

# --- 3. ENCABEZADO ---
col_flag, col_title = st.columns([1, 15])
with col_flag: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_title: st.title("Monitor Económico e Impositivo Integral")

# --- 4. TIPOS DE CAMBIO DINÁMICOS ---
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

# --- 6. INFLACIÓN (AÑO COMPLETO) ---
st.subheader("📊 Historial de Inflación INDEC 2025")
df_inf = pd.DataFrame({
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre (Est)"],
    "IPC (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
})
df_inf['Acumulada (%)'] = ((1 + df_inf['IPC (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC (%)": "{:.1f}%", "Acumulada (%)": "{:.1f}%"}))

st.divider()

# --- 7. CUADROS IMPOSITIVOS ---
st.subheader("📊 Tablas Técnicas de Auditoría")
tab1, tab2, tab3 = st.tabs(["Ganancias Sociedades", "Monotributo 2025", "RG 830"])

with tab1:
    st.markdown("**Escala Ley 27.630 - Ejercicios Dic 2025**")
    
    data_soc = {
        "Tramo Ganancia Neta": ["Hasta $101.679.575,26", "De $101.679.575,26 a $1.016.795.752,60", "Más de $1.016.795.752,60"],
        "Alícuota": ["25%", "30%", "35%"],
        "Monto Fijo ($)": ["$0,00", "$25.419.893,82", "$299.954.747,02"]
    }
    st.table(pd.DataFrame(data_soc))

with tab2:
    st.write("**Topes por Categoría**")
    df_mono = pd.DataFrame({
        "Cat": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K (Tope)"],
        "Ingresos Anuales ($)": ["8.9M", "13.3M", "18.6M", "23.2M", "27.3M", "34.1M", "40.8M", "62.0M", "69.4M", "79.4M", "94.805.682,90"],
        "Cuota Total Mensual ($)": ["37k", "42k", "49k", "63k", "81k", "104k", "127k", "244k", "302k", "359k", "428k"]
    })
    st.table(df_mono)

with tab3:
    st.markdown("**Retenciones Auditadas**")
    data_rg = {
        "Concepto": ["Enajenación Bienes Muebles", "Locaciones/Servicios", "Honorarios Profesionales", "Alquileres"],
        "Mínimo No Sujeto ($)": ["224.000,00", "98.240,00", "98.240,00", "16.360,00"],
        "Alícuota Insc. (%)": ["2,0%", "2,0%", "Escala Art. 94", "6,0%"]
    }
    st.table(pd.DataFrame(data_rg))

st.divider()

# --- 8. PANEL DE LIDERAZGO (AL FINAL) ---
st.subheader("🌐 Liderazgo Institucional - UHY Macho & Asociados")
uhy_col1, uhy_col2, uhy_col3 = st.columns(3)

with uhy_col1:
    st.info("### 🏢 La Firma")
    st.markdown("""
    **UHY Macho & Asociados** Miembro independiente de **UHY International**.  
    Red global con más de 340 oficinas en 100 países.  
    [Sitio Web](https://www.uhymacho.com/)
    """)

with uhy_col2:
    st.info("### 👨‍💼 Roberto E. Macho")
    st.markdown("""
    **Socio Principal** Liderazgo en consultoría de alta complejidad y auditoría externa.  
    Referente en gestión de firmas profesionales y estrategia corporativa.
    """)

with uhy_col3:
    st.info("### 👨‍⚖️ Tomás Merlos")
    st.markdown("""
    **Socio Tax & Legal** Especialista en planificación fiscal nacional e internacional.  
    Experto en el marco normativo de ARCA y reformas tributarias.
    """)
