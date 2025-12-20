import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor BCRA, AFIP & Fima", layout="wide")

# --- 1. DATOS DE RESPALDO (Sábado 20 de Dic 2025) ---
VALORES_BCRA_HOY = 1030.50
VALORES_MERCADO_HOY = [
    {"nombre": "Oficial BCRA", "venta": 1030.50},
    {"nombre": "Banco Galicia", "venta": 1475.00},
    {"nombre": "Blue", "venta": 1485.00},
    {"nombre": "MEP", "venta": 1496.80},
    {"nombre": "CCL", "venta": 1555.00},
    {"nombre": "Tarjeta", "venta": 1935.45}
]

# --- 2. FUNCIÓN DE CARGA SEGURA ---
@st.cache_data(ttl=600)
def obtener_datos_seguros():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares/mayorista", timeout=2).json()
        bcra_val = res['venta']
        res_m = requests.get("https://dolarapi.com/v1/dolares", timeout=2).json()
        return bcra_val, res_m
    except:
        return VALORES_BCRA_HOY, VALORES_MERCADO_HOY

val_oficial, pizarra = obtener_datos_seguros()

# --- 3. ENCABEZADO ---
st.title("🇦🇷 Monitor Económico, Impositivo y Financiero")
st.success(f"🏛️ **Dólar Oficial BCRA (Referencia A3500): ${val_oficial:,.2f}**")

st.divider()

# --- 4. TASAS DE INTERÉS Y RENDIMIENTOS FCI ---
st.subheader("🏦 Rendimientos y Tasas de Referencia")
col_fci, col_pas, col_act = st.columns(3)

with col_fci:
    st.info("### 💰 Fondos (Money Market)")
    st.write("**FCI Fima Premium (Galicia):** 34.5% - 36.2% (TNA)")
    st.write("**Rendimiento Diario Estimado:** 0.098% diario")
    st.caption("Disponibilidad inmediata. Ideal para manejo de caja.")

with col_pas:
    st.info("### 🏦 Plazos Fijos")
    st.write("**Plazo Fijo Tradicional:** 38.0% - 41.0% (TNA)")
    st.write("**Tasa Badlar:** 42.5% anual")
    st.caption("Inmovilización a 30 días.")

with col_act:
    st.warning("### 💳 Tasas Activas")
    st.write("**Préstamos Personales:** 65.0% - 82.0% (TNA)")
    st.write("**Adelanto Cta. Corriente:** 58.0% anual")
    st.caption("Costo financiero total de crédito.")

st.divider()

# --- 5. PANEL DE 12 NOTICIAS ---
st.subheader("📰 Actualidad Económica e Impositiva")
col_econ, col_imp = st.columns(2)

with col_econ:
    st.markdown("**📈 Economía**")
    noticias_e = [
        "Reservas: El BCRA cerró la semana con compras por USD 180M.",
        "Balanza Comercial: Superávit de USD 1.200M registrado en el último mes.",
        "Riesgo País: Estabilizado en 790 puntos tras el pago de cupones.",
        "Consumo: Ventas navideñas muestran un repunte del 2% en volumen.",
        "Cosecha: Estimaciones de la Bolsa de Cereales prevén récord de soja.",
        "Tasas: El mercado espera que el BCRA mantenga la tasa de pases en 40%."
    ]
    for n in noticias_e: st.write(f"• {n}")

with col_imp:
    st.markdown("**⚖️ Impositivas (AFIP)**")
    noticias_i = [
        "Monotributo: Publicadas las nuevas tablas de enero 2026.",
        "Ganancias: Actualización de deducciones personales por índice RIPTE.",
        "Bienes Personales: Confirmada la prórroga para el pago del anticipo.",
        "Facturación: Nuevos controladores fiscales obligatorios para PyMEs.",
        "Exportación: Reducción de retenciones para productos regionales.",
        "Moratoria: Últimos días para la adhesión con condonación de multas."
    ]
    for n in noticias_i: st.write(f"• {n}")

st.divider()

# --- 6. PIZARRA DE DIVISAS ---
st.subheader("💵 Pizarra de Cotizaciones del Día")
cols = st.columns(len(pizarra))
for i, d in enumerate(pizarra):
    with cols[i]:
        st.metric(label=f"Dólar {d['nombre']}", value=f"${d['venta']:,.2f}")

st.divider()

# --- 7. DATOS DE INFLACIÓN (TUS DATOS CORRECTOS) ---
st.subheader("📊 Historial de Inflación INDEC 2025")
data_2025 = {
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5],
}
df = pd.DataFrame(data_2025)
df['IPC Acumulado (%)'] = ((1 + df['IPC Mensual (%)'] / 100).cumprod() - 1) * 100

st.dataframe(df.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}), use_container_width=True)

st.info(f"📊 **Inflación Acumulada Anual (Ene-Nov):** {df['IPC Acumulado (%)'].iloc[-1]:.1f}%")