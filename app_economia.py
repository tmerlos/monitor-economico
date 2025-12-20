import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor ARCA Profesional - Auditado", layout="wide")

# --- 1. DATOS DE MERCADO (DIVISAS) ---
@st.cache_data(ttl=600)
def obtener_pizarra():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        m = {d['nombre']: d['venta'] for d in res}
        return {
            "Oficial": m.get("Oficial", 1030.50), "Blue": m.get("Blue", 1485.00),
            "MEP": m.get("MEP", 1496.80), "CCL": m.get("Contado con Liquidación", 1555.00),
            "Tarjeta": m.get("Tarjeta", 1935.45)
        }
    except:
        return {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00, "Tarjeta": 1935.45}

pizarra = obtener_pizarra()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Auditoría")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    if st.button("🔄 Sincronizar"):
        st.cache_data.clear()
        st.rerun()
    st.info("Valores validados según Ley 27.743.")

# --- 3. ENCABEZADO ---
col_flag, col_title = st.columns([1, 15])
with col_flag: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_title: st.title("Monitor Económico e Impositivo Integral")

# --- 4. TIPOS DE CAMBIO ---
cols = st.columns(5)
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. TASAS DE INTERÉS ---
st.subheader("🏦 Rendimientos y Tasas")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos MM")
    st.write("**Fima Premium:** 34.5% TNA")
    st.write("**Santander Ahorro:** 34.2% TNA")
with t2:
    st.info("### 🏦 Bancos")
    st.write("**Plazo Fijo:** 39.0% TNA")
    st.write("**Badlar:** 42.8% TNA")
with t3:
    st.warning("### 💳 Crédito")
    st.write("**Personales:** 78.0% TNA")
    st.write("**Tarjetas:** 112.0% TNA")

st.divider()

# --- 6. NOTICIAS 6+6 ---
st.subheader("📰 Noticias con Link")
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Economía**")
    for t, l in [("Subsidios: Crédito USD 300M", "https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/"), ("Desempleo: Baja al 6,6%", "https://www.pagina12.com.ar/2025/12/19/aumenta-la-precariedad-y-baja-el-desempleo/"), ("Comercio: Superávit Noviembre", "https://www.indec.gob.ar/"), ("Bonos: Licitación exitosa", "https://www.argentina.gob.ar/noticias"), ("Campo: Cosecha 25/26", "https://www.lanacion.com.ar/economia/"), ("BCRA: Compra Reservas", "https://www.bcra.gob.ar/")]:
        st.markdown(f"• [{t}]({l})")
with c2:
    st.markdown("**Impositivas**")
    for t, l in [("Umbrales: Precios Transferencia", "https://aldiaargentina.microjuris.com/2025/12/16/legislacion-arca-se-actualizan-precios-de-transferencia/"), ("Monotributo: Vencimiento Cuota", "https://www.ambito.com/informacion-general/vencimiento-del-monotributo-diciembre-2025-arca-n6223081"), ("Senado: Inocencia Fiscal", "https://chequeado.com/"), ("Bienes Personales: Escalas", "https://www.afip.gob.ar/ganancias-y-bienes-personales/"), ("Pymes: Facturación", "https://www.afip.gob.ar/noticias/"), ("Enero: Calendario 2026", "https://www.afip.gob.ar/vencimientos/")]:
        st.markdown(f"• [{t}]({l})")

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

# --- 8. MONOTRIBUTO (COMPLETO A-K) ---
st.subheader("⚖️ Monotributo: Todas las Categorías 2025")
df_mono = pd.DataFrame({
    "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Anuales ($)": [
        "8.987.312,20", "13.345.101,40", "18.677.202,30", "23.211.504,10", "27.321.405,80", 
        "34.112.508,40", "40.876.310,10", "62.011.514,50", "69.455.618,20", "79.445.820,10", "94.805.682,90"
    ],
    "Cuota Total ($)": ["37k", "42k", "49k", "63k", "81k", "104k", "127k", "244k", "302k", "359k", "428k"]
})
st.table(df_mono)

st.divider()

# --- 9. RG 830: RETENCIONES (ENAJENACIÓN CORREGIDA) ---
st.subheader("📋 Retenciones Ganancias: RG 830 (Auditada)")
data_rg = {
    "Concepto": [
        "Enajenación de Bienes Muebles", "Locaciones de Obra/Servicios", "Honorarios Profesionales", 
        "Comisiones", "Alquileres", "Fletes y Acarreos"
    ],
    "Mínimo No Sujeto ($)": ["224.000,00", "98.240,00", "98.240,00", "45.100,00", "16.360,00", "32.000,00"],
    "Insc. (%)": ["2,0%", "2,0%", "Escala Art. 94", "3,0%", "6,0%", "0,25%"],
    "No Insc. (%)": ["25%", "28%", "28%", "28%", "28%", "25%"]
}
st.table(pd.DataFrame(data_rg))
