import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor ARCA Senior - Auditoría", layout="wide")

# --- 1. CARGA DE MERCADOS (CORRECCIÓN DE ERROR DINÁMICO) ---
@st.cache_data(ttl=600)
def obtener_datos():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        # Convertimos a diccionario
        return {d['nombre']: d['venta'] for d in res}
    except:
        return {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00, "Tarjeta": 1935.45}

pizarra = obtener_datos()

# --- 2. SIDEBAR CON ÍNDICES CRÍTICOS (CAMBIO: EMPLEO) ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Control Senior")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    
    st.markdown("### 🔍 Índices Críticos")
    st.metric("Riesgo País", "785 bps", "-12")
    st.metric("Reservas Netas", "USD 31.2B", "+450M")
    st.metric("Tasa de Empleo", "44.6%", "+0.4%") # Nuevo índice solicitado
    st.metric("Índice CAC (Construc.)", "+4.2% mensual")
    st.metric("UVA (Valor Hoy)", "$1.245,60")
    
    st.divider()
    if st.button("🔄 Sincronizar Sistemas"):
        st.cache_data.clear()
        st.rerun()

# --- 3. ENCABEZADO CON BANDERA ---
col_flag, col_title = st.columns([1, 15])
with col_flag: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_title: st.title("Monitor Económico e Impositivo Integral")

# --- 4. TIPOS DE CAMBIO (SOLUCIÓN AL INDEXERROR) ---
# Creamos dinámicamente el número de columnas según la cantidad de dólares recibidos
cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: 
        st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. TASAS DE INTERÉS ---
st.subheader("🏦 Rendimientos y Tasas Financieras")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos Money Market")
    st.write("**Fima Premium:** 34.50% TNA")
    st.write("**Mercado Pago:** 32.10% TNA")
with t2:
    st.info("### 🏦 Bancos y Plazos")
    st.write("**Plazo Fijo:** 39.00% TNA")
    st.write("**Tasa Badlar:** 42.80% TNA")
with t3:
    st.warning("### 💳 Costo Financiero (C.F.T.)")
    st.write("**Préstamos Personales:** 78.00% avg")
    st.write("**Tarjeta de Crédito:** 112.00% avg")

st.divider()

# --- 6. NOTICIAS 6+6 ---
st.subheader("📰 Noticias y Alertas Clave")
ce, ci = st.columns(2)
with ce:
    st.markdown("**Economía**")
    noticias_e = [
        ("Subsidios: Crédito USD 300M Energía", "https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/"),
        ("Desempleo: Baja al 6,6% (INDEC)", "https://www.pagina12.com.ar/2025/12/19/aumenta-la-precariedad-y-baja-el-desempleo/"),
        ("Comercio: Superávit de USD 2.498M", "https://www.indec.gob.ar/"),
        ("Bonos: Licitación Tesoro", "https://www.argentina.gob.ar/noticias"),
        ("Campo: Proyección Cosecha 25/26", "https://www.lanacion.com.ar/economia/"),
        ("BCRA: Compra Reservas", "https://www.bcra.gob.ar/")
    ]
    for t, l in noticias_e: st.markdown(f"• [{t}]({l})")
with ci:
    st.markdown("**Impositivas (ARCA)**")
    noticias_i = [
        ("Umbrales: Precios Transferencia", "https://aldiaargentina.microjuris.com/2025/12/16/legislacion-arca-se-actualizan-precios-de-transferencia/"),
        ("Monotributo: Vencimiento Cuota", "https://www.ambito.com/informacion-general/vencimiento-del-monotributo-diciembre-2025-arca-n6223081"),
        ("Senado: Proyecto Inocencia Fiscal", "https://chequeado.com/"),
        ("Bienes Personales: Nuevas Escalas", "https://www.afip.gob.ar/ganancias-y-bienes-personales/"),
        ("Facturación: Simplificación PyME", "https://www.afip.gob.ar/noticias/"),
        ("Enero: Calendario 2026", "https://www.afip.gob.ar/vencimientos/")
    ]
    for t, l in noticias_i: st.markdown(f"• [{t}]({l})")

st.divider()

# --- 7. INFLACIÓN ---
st.subheader("📊 Historial de Inflación INDEC 2025")
df_inf = pd.DataFrame({
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre (Est)"],
    "IPC (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
})
df_inf['Acumulada (%)'] = ((1 + df_inf['IPC (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC (%)": "{:.1f}%", "Acumulada (%)": "{:.1f}%"}))

st.divider()

# --- 8. GANANCIAS SOCIEDADES (101.6M) ---
st.subheader("🏢 Ganancias: Personas Jurídicas (Sociedades)")

data_soc = {
    "Tramo Ganancia Neta": ["Hasta $101.679.575,26", "De $101.679.575,26 a $1.016.795.752,60", "Más de $1.016.795.752,60"],
    "Alícuota": ["25%", "30%", "35%"],
    "Monto Fijo ($)": ["$0,00", "$25.419.893,82", "$299.954.747,02"],
    "S/ Excedente de": ["$0,00", "$101.679.575,26", "$1.016.795.752,60"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 9. MONOTRIBUTO (TABLA COMPLETA) ---
st.subheader("⚖️ Monotributo: Escalas Vigentes 2025")
df_mono = pd.DataFrame({
    "Cat": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Anuales ($)": ["8.9M", "13.3M", "18.6M", "23.2M", "27.3M", "34.1M", "40.8M", "62.0M", "69.4M", "79.4M", "94.805.682,90"],
    "Cuota ($)": ["37k", "42k", "49k", "63k", "81k", "104k", "127k", "244k", "302k", "359k", "428k"]
})
st.table(df_mono)

st.divider()

# --- 10. RG 830: RETENCIONES (ENAJENACIÓN CORREGIDA $224k) ---
st.subheader("📋 Retenciones Ganancias: RG 830")
data_rg = {
    "Concepto": ["Enajenación Bienes Muebles", "Locaciones de Obra/Servicios", "Honorarios Profesionales", "Comisiones", "Alquileres"],
    "Mínimo No Sujeto ($)": ["224.000,00", "98.240,00", "98.240,00", "45.100,00", "16.360,00"],
    "Insc. (%)": ["2,0%", "2,0%", "Escala Art. 94", "3,0%", "6,0%"],
    "No Insc. (%)": ["25%", "28%", "28%", "28%", "28%"]
}
st.table(pd.DataFrame(data_rg))
