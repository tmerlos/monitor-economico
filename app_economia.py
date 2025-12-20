import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Monitor Fiscal ARCA - Pro", layout="wide")

# --- 1. DATOS DE MERCADO (DIVISAS) ---
@st.cache_data(ttl=600)
def obtener_pizarra():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        m = {d['nombre']: d['venta'] for d in res}
        return {
            "Oficial": m.get("Oficial", 1030.50),
            "Blue": m.get("Blue", 1485.00),
            "MEP": m.get("MEP", 1496.80),
            "CCL": m.get("Contado con Liquidación", 1555.00),
            "Tarjeta": m.get("Tarjeta", 1935.45)
        }
    except:
        return {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00, "Tarjeta": 1935.45}

pizarra = obtener_pizarra()

# --- 2. SIDEBAR (RESTAURADO) ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Auditoría")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    if st.button("🔄 Sincronizar Datos ARCA"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("### Configuración")
    st.checkbox("Mostrar Alertas Tempranas", value=True)
    st.checkbox("Modo Calculadora Fiscal", value=False)
    st.info("Valores oficiales según Ley 27.743 y Res. Grales. vigentes.")

# --- 3. ENCABEZADO CON BANDERA ---
col_flag, col_title = st.columns([1, 15])
with col_flag:
    st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_title:
    st.title("Monitor Económico e Impositivo Integral")

# --- 4. TIPOS DE CAMBIO ---
st.success(f"🏛️ **Referencia Dólar Oficial BCRA: ${pizarra['Oficial']:,.2f}**")
cols = st.columns(5)
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]:
        st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. NOTICIAS 6+6 CON LINKS ---
st.subheader("📰 Noticias y Alertas del Día")
ce, ci = st.columns(2)
with ce:
    st.markdown("**📈 Economía**")
    noticias_eco = [
        ("Subsidios: Crédito de USD 300M para energía", "https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/"),
        ("Desempleo: Baja al 6,6% en el tercer trimestre", "https://www.pagina12.com.ar/2025/12/19/aumenta-la-precariedad-y-baja-el-desempleo/"),
        ("Superávit: USD 2.498M de saldo comercial", "https://www.indec.gob.ar/"),
        ("Bonos: Exitosa licitación del Tesoro en USD", "https://www.argentina.gob.ar/noticias"),
        ("Campo: Proyectan cosecha récord 25/26", "https://www.lanacion.com.ar/economia/"),
        ("BCRA: Acumulación de reservas en Diciembre", "https://www.bloomberglinea.com/latinoamerica/argentina/")
    ]
    for t, l in noticias_eco: st.markdown(f"• [{t}]({l})")
with ci:
    st.markdown("**⚖️ Impositivas (ARCA)**")
    noticias_imp = [
        ("Umbrales: Precios de Transferencia a $1.500M", "https://aldiaargentina.microjuris.com/2025/12/16/legislacion-arca-se-actualizan-precios-de-transferencia/"),
        ("Monotributo: Vencimiento Cuota Diciembre 2025", "https://www.ambito.com/informacion-general/vencimiento-del-monotributo-diciembre-2025-arca-n6223081"),
        ("Senado: Tratamiento de Inocencia Fiscal", "https://chequeado.com/"),
        ("Vencimientos: Calendario de Enero 2026", "https://www.afip.gob.ar/vencimientos/"),
        ("Portal Tributario Municipal: Nueva plataforma", "https://www.argentina.gob.ar/noticias"),
        ("Pymes: Simplificación de Facturación", "https://www.afip.gob.ar/noticias/")
    ]
    for t, l in noticias_imp: st.markdown(f"• [{t}]({l})")

st.divider()

# --- 6. INFLACIÓN (AÑO COMPLETO) ---
st.subheader("📊 Inflación INDEC 2025 (Ene - Dic)")
df_inf = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic (Est)"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
})
df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 7. GANANCIAS SOCIEDADES (101.6M) ---
st.subheader("🏢 Ganancias: Sociedades")
data_soc = {
    "Tramo Ganancia Neta": ["Hasta $101.679.575,26", "De $101.679.575,26 a $1.016.795.752,60", "Más de $1.016.795.752,60"],
    "Alícuota": ["25%", "30%", "35%"],
    "Fijo ($)": ["$0,00", "$25.419.893,82", "$299.954.747,02"],
    "Sobre excedente de": ["$0,00", "$101.679.575,26", "$1.016.795.752,60"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 8. GANANCIAS PERSONAS HUMANAS (ART. 94) ---
st.subheader("👤 Ganancias: Personas Humanas (Escala Progresiva)")
data_ph = {
    "Ganancia Neta Imponible ($)": ["0 a 1.7M", "1.7M a 3.5M", "3.5M a 5.2M", "5.2M a 7.8M", "7.8M a 15.7M", "15.7M a 23.6M", "23.6M a 35.4M", "35.4M a 53.1M", "Más de 53.1M"],
    "Fijo ($)": ["0", "87.495", "244.986", "454.974", "848.702", "2.344.867", "4.156.015", "7.345.211", "12.837.714"],
    "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"]
}
st.table(pd.DataFrame(data_ph))

st.divider()

# --- 9. MONOTRIBUTO (94.8M) ---
st.subheader("⚖️ Monotributo: Escalas 2025")
df_mono = pd.DataFrame({
    "Cat.": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Anuales ($)": ["8.9M", "13.1M", "18.4M", "22.9M", "26.9M", "33.8M", "40.4M", "61.3M", "68.6M", "78.6M", "94.805.682,90"],
    "Cuota Mensual ($)": ["37k", "42k", "49k", "63k", "81k", "112k", "172k", "244k", "721k", "874k", "1.2M"]
})
st.table(df_mono)

st.divider()

# --- 10. RETENCIONES GANANCIAS RG 830 (NUEVO) ---
st.subheader("📋 Retenciones Ganancias: Res. Gral. 830")
st.caption("Valores y mínimos no sujetos a retención actualizados a Diciembre 2025.")
data_rg = {
    "Concepto de Pago": ["Bienes Muebles", "Locaciones de Servicios", "Honorarios Profesionales", "Alquileres"],
    "Mínimo No Sujeto ($)": ["327.200,00", "98.240,00", "98.240,00", "16.360,00"],
    "Alícuota Inscripto": ["2,0%", "2,0%", "Escala Art. 94 (Mín 3%)", "6,0%"],
    "Alícuota No Insc.": ["25,0%", "28,0%", "28,0%", "28,0%"]
}
st.table(pd.DataFrame(data_rg))
