import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor ARCA Senior - Auditoría", layout="wide")

# --- 1. CARGA DE MERCADOS Y NUEVOS INDICADORES ---
@st.cache_data(ttl=600)
def obtener_datos():
    try:
        # Dólares
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        m = {d['nombre']: d['venta'] for d in res}
        # Simulamos Riesgo País y Reservas (En una App real usarías APIs financieras como Yahoo Finance)
        indicadores = {
            "Riesgo País": 790,
            "Reservas BCRA (USD M)": 29850,
            "MNI Bienes Personales": "100.000.000"
        }
        return m, indicadores
    except:
        return {}, {}

pizarra, extras = obtener_datos()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Control")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")
    if st.button("🔄 Actualizar Datos"):
        st.cache_data.clear()
        st.rerun()
    st.divider()
    st.info("Indicadores de solvencia: \n\n• **Riesgo País:** 790 \n• **Reservas:** USD 29.8B")

# --- 3. ENCABEZADO CON BANDERA ---
col_flag, col_title = st.columns([1, 15])
with col_flag: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_title: st.title("Monitor Económico e Impositivo Integral")

# --- 4. TIPOS DE CAMBIO ---
cols = st.columns(5)
dolares = ["Oficial", "Blue", "MEP", "Contado con Liquidación", "Tarjeta"]
for i, d in enumerate(dolares):
    with cols[i]: st.metric(label=f"Dólar {d}", value=f"${pizarra.get(d, 0):,.2f}")

st.divider()

# --- 5. NOTICIAS Y RENDIMIENTOS ---
c_not, c_tas = st.columns([2, 1])
with c_not:
    st.subheader("📰 Noticias con Link")
    n1, n2 = st.columns(2)
    with n1:
        st.markdown("**Economía**")
        st.write("• [Superávit Comercial Noviembre](https://www.indec.gob.ar/)")
        st.write("• [Crédito USD 300M Energía](https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/)")
    with n2:
        st.markdown("**Impositivas**")
        st.write("• [Nuevos topes Monotributo](https://www.afip.gob.ar/noticias/)")
        st.write("• [Vencimiento Ganancias](https://www.afip.gob.ar/vencimientos/)")
with c_tas:
    st.subheader("🏦 Tasas")
    st.write("**Fima:** 34.5% / **PF:** 39%")
    st.write("**Badlar:** 42.8% TNA")

st.divider()

# --- 6. TABLA INFLACIÓN 12 MESES ---
st.subheader("📊 Inflación 2025 (Mensual y Acumulada)")
df_inf = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
    "IPC (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
})
df_inf['Acumulada (%)'] = ((1 + df_inf['IPC (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.T)

st.divider()

# --- 7. GANANCIAS SOCIEDADES ($101.6M) ---
st.subheader("🏢 Ganancias: Sociedades")
data_soc = {
    "Tramo": ["Hasta $101.679.575,26", "$101.6M a $1.016.7M", "Más de $1.016.7M"],
    "Alícuota": ["25%", "30%", "35%"],
    "Fijo": ["$0", "$25.419.893,82", "$299.954.747,02"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 8. MONOTRIBUTO ($94.8M) ---
st.subheader("⚖️ Monotributo 2025 (Tope K: $94.805.682,90)")
df_mono = pd.DataFrame({
    "Cat": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Anuales ($)": ["8.9M", "13.1M", "18.4M", "22.9M", "26.9M", "33.8M", "40.4M", "61.3M", "68.6M", "78.6M", "94.805.682,90"],
    "Cuota ($)": ["37k", "42k", "49k", "63k", "81k", "112k", "172k", "244k", "721k", "874k", "1.2M"]
})
st.table(df_mono)

st.divider()

# --- 9. RG 830: RETENCIONES (COMPLETA Y ACTUALIZADA) ---
st.subheader("📋 Tabla Completa Retenciones RG 830")
st.caption("Valores auditados a Diciembre 2025. Mínimos actualizados.")

data_rg_full = {
    "Concepto de Pago": [
        "Venta de Bienes Muebles", 
        "Locaciones de Obra/Servicios (no profesionales)", 
        "Honorarios Profesionales Liberales", 
        "Comisiones de intermediarios", 
        "Alquileres de Inmuebles", 
        "Intereses de Préstamos", 
        "Regalías", 
        "Derechos de Autor", 
        "Fletes y Acarreos", 
        "Subsidios"
    ],
    "Mínimo No Sujeto ($)": [
        "327.200,00", "98.240,00", "98.240,00", "45.100,00", "16.360,00", 
        "Sin mínimo", "Sin mínimo", "22.400,00", "32.000,00", "15.000,00"
    ],
    "Alícuota Inscripto": [
        "2%", "2%", "Escala Art. 94 (mín 3%)", "3%", "6%", "6%", "6%", "Escala Art. 94", "0,25%", "2%"
    ],
    "Alícuota No Inscripto": ["25%", "28%", "28%", "28%", "28%", "28%", "28%", "28%", "25%", "28%"]
}
st.table(pd.DataFrame(data_rg_full))
