import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor Económico Real 2025", layout="wide")

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
def obtener_datos():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares/mayorista", timeout=2).json()
        bcra_val = res['venta']
        res_m = requests.get("https://dolarapi.com/v1/dolares", timeout=2).json()
        # Filtrar solo los que queremos mostrar en la pizarra principal
        nombres_interes = ["Oficial", "Blue", "MEP", "CCL", "Tarjeta"]
        pizarra_filtrada = [d for d in res_m if d['nombre'] in nombres_interes]
        return bcra_val, pizarra_filtrada
    except:
        return VALORES_BCRA_HOY, VALORES_MERCADO_HOY

val_oficial, pizarra = obtener_datos()

# --- 3. ENCABEZADO Y ALERTA OFICIAL ---
st.title("🇦🇷 Monitor Económico, Impositivo y Financiero")
st.success(f"🏛️ **Dólar Oficial BCRA (Referencia A3500): ${val_oficial:,.2f}**")

st.divider()

# --- 4. PIZARRA DE COTIZACIONES (AHORA ARRIBA) ---
st.subheader("💵 Pizarra de Cotizaciones del Día")
cols_piz = st.columns(len(pizarra))
for i, d in enumerate(pizarra):
    with cols_piz[i]:
        st.metric(label=f"Dólar {d['nombre']}", value=f"${d.get('venta', 0):,.2f}")

st.divider()

# --- 5. TASAS DE INTERÉS Y FONDOS FIMA ---
st.subheader("🏦 Rendimientos y Tasas de Referencia")
c1, c2, c3 = st.columns(3)
with c1:
    st.info("### 💰 Fondos (Fima)")
    st.write("**Fima Premium (Galicia):** 34.5% - 36.2% (TNA)")
    st.caption("Disponibilidad inmediata.")
with c2:
    st.info("### 🏦 Plazos Fijos")
    st.write("**TNA Promedio:** 38.0% - 41.0%")
    st.caption("Inmovilizado 30 días.")
with c3:
    st.warning("### 💳 Tasas Activas")
    st.write("**Préstamos Personales:** 65.0% - 82.0%")
    st.write("**Adelanto Cta Cte:** 58.0%")

st.divider()

# --- 6. PANEL DE 12 NOTICIAS ---
st.subheader("📰 Actualidad Económica e Impositiva")
col_e, col_i = st.columns(2)
with col_e:
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
with col_i:
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

# --- 7. HISTORIAL INFLACIÓN (DATOS EXACTOS) ---
st.subheader("📊 Historial de Inflación INDEC 2025")
df = pd.DataFrame({
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5],
})
df['IPC Acumulado (%)'] = ((1 + df['IPC Mensual (%)'] / 100).cumprod() - 1) * 100

st.dataframe(df.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}), use_container_width=True)

st.info(f"📊 **Inflación Acumulada Anual (Ene-Nov):** {df['IPC Acumulado (%)'].iloc[-1]:.1f}%")
