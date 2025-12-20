import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor Fiscal ARCA - Auditoría 2025", layout="wide")

# --- 1. DATOS DE MERCADO ---
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

# --- 2. SIDEBAR RESTAURADO ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Auditoría")
    st.write(f"📅 **Hoy:** {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    if st.button("🔄 Sincronizar Datos"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("### Indicadores Críticos")
    st.write("• Riesgo País: 785 bps")
    st.write("• Reservas Netas: USD 31.2B")

# --- 3. ENCABEZADO CON BANDERA ---
col_flag, col_title = st.columns([1, 15])
with col_flag: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_title: st.title("Monitor Económico e Impositivo Integral")

# --- 4. TIPOS DE CAMBIO ---
cols = st.columns(5)
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. TASAS DE INTERÉS (COMPLETAS) ---
st.subheader("🏦 Rendimientos y Tasas Financieras")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos Money Market")
    st.write("**Fima Premium:** 34.50% TNA")
    st.write("**Mercado Pago:** 32.10% TNA")
    st.write("**Personal Pay:** 33.40% TNA")
with t2:
    st.info("### 🏦 Bancos y Plazos")
    st.write("**Plazo Fijo:** 39.00% TNA")
    st.write("**Tasa Badlar:** 42.80% TNA")
    st.write("**Tasa TM20:** 41.20% TNA")
with t3:
    st.warning("### 💳 Costo Financiero (C.F.T.)")
    st.write("**Préstamos Personales:** 78.00% avg")
    st.write("**Adelantos Cuenta Cte:** 62.50% TNA")
    st.write("**Tarjeta de Crédito:** 112.00% avg")

st.divider()

# --- 6. NOTICIAS 6+6 ---
st.subheader("📰 Noticias con Link")
c_not_e, c_not_i = st.columns(2)
with c_not_e:
    st.markdown("**Economía**")
    noticias_e = [
        ("Subsidios: Crédito USD 300M Energía", "https://diarioelnorte.com.ar/el-gobierno-aprobo-un-prestamo-de-us-300-millones-para-reordenar-los-subsidios-energeticos/"),
        ("Desempleo: Baja al 6,6% (INDEC)", "https://www.pagina12.com.ar/2025/12/19/aumenta-la-precariedad-y-baja-el-desempleo/"),
        ("Comercio: Superávit de USD 2.498M", "https://www.indec.gob.ar/"),
        ("Bonos: Licitación Tesoro Diciembre", "https://www.argentina.gob.ar/noticias"),
        ("Campo: Proyección Cosecha 25/26", "https://www.lanacion.com.ar/economia/"),
        ("BCRA: Compra de Reservas Diarias", "https://www.bcra.gob.ar/")
    ]
    for t, l in noticias_e: st.markdown(f"• [{t}]({l})")
with c_not_i:
    st.markdown("**Impositivas (ARCA)**")
    noticias_i = [
        ("Umbrales: Precios de Transferencia", "https://aldiaargentina.microjuris.com/2025/12/16/legislacion-arca-se-actualizan-precios-de-transferencia/"),
        ("Monotributo: Vencimiento Cuota Dic", "https://www.ambito.com/informacion-general/vencimiento-del-monotributo-diciembre-2025-arca-n6223081"),
        ("Senado: Proyecto Inocencia Fiscal", "https://chequeado.com/"),
        ("Bienes Personales: Nuevas Escalas", "https://www.afip.gob.ar/ganancias-y-bienes-personales/"),
        ("Facturación: Simplificación PyME", "https://www.afip.gob.ar/noticias/"),
        ("Calendario: Vencimientos Enero 2026", "https://www.afip.gob.ar/vencimientos/")
    ]
    for t, l in noticias_i: st.markdown(f"• [{t}]({l})")

st.divider()

# --- 7. INFLACIÓN (FORMATO ORIGINAL) ---
st.subheader("📊 Historial de Inflación INDEC 2025")
df_inf = pd.DataFrame({
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre (Est)"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]
})
df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 8. GANANCIAS SOCIEDADES ($101.6M) Y PERSONAS HUMANAS ---
col_soc, col_ph = st.columns(2)
with col_soc:
    st.subheader("🏢 Ganancias: Sociedades")
    data_soc = {
        "Tramo Ganancia": ["Hasta $101.6M", "$101.6M a $1.016M", "Más de $1.016M"],
        "Alícuota": ["25%", "30%", "35%"],
        "Fijo ($)": ["$0", "$25.419.893,82", "$299.954.747,02"]
    }
    st.table(pd.DataFrame(data_soc))
with col_ph:
    st.subheader("👤 Ganancias: Personas Humanas")
    data_ph = {
        "Ganancia Imponible": ["0 a 1.7M", "1.7M a 3.5M", "3.5M a 7.8M", "Más de 53.1M"],
        "Fijo ($)": ["0", "87.495", "454.974", "12.837.714"],
        "Alícuota": ["5%", "9%", "15%", "35%"]
    }
    st.table(pd.DataFrame(data_ph))

st.divider()

# --- 9. MONOTRIBUTO (94.8M) ---
st.subheader("⚖️ Monotributo: Topes 2025")
df_mono = pd.DataFrame({
    "Cat": ["A", "D", "H", "K"],
    "Ingresos Anuales ($)": ["8.987.312,20", "23.211.504,10", "62.011.514,50", "94.805.682,90"],
    "Cuota Total ($)": ["37k", "63k", "244k", "1.2M"]
})
st.table(df_mono)

st.divider()

# --- 10. RETENCIONES RG 830 (AUDITADAS DICIEMBRE 2025) ---
st.subheader("📋 Retenciones Ganancias: Res. Gral. 830 (Tabla Final)")
st.caption("Valores y mínimos actualizados según índice de movilidad Ley 27.743.")
data_rg = {
    "Concepto de Pago": [
        "Enajenación Bienes Muebles", 
        "Locaciones de Obra/Servicios", 
        "Honorarios Prof. Liberales", 
        "Comisiones de Intermediarios", 
        "Alquileres Inmuebles", 
        "Intereses Préstamos/Mora"
    ],
    "Mínimo No Sujeto ($)": [
        "327.200,00", "98.240,00", "98.240,00", "45.100,00", "16.360,00", "Sin mínimo"
    ],
    "Alícuota Inscripto": [
        "2,0%", "2,0%", "Escala Art. 94 (mín 3%)", "3,0%", "6,0%", "6,0%"
    ],
    "Alícuota NO Inscripto": ["25%", "28%", "28%", "28%", "28%", "28%"]
}
st.table(pd.DataFrame(data_rg))
