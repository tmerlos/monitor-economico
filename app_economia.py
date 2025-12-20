import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor Económico", layout="wide")

# --- 1. VALORES DE RESPALDO (Sábado 20 de Dic 2025) ---
VALORES_BACKUP = {
    "Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80,
    "CCL": 1555.00, "Tarjeta": 1935.45, "Cripto": 1541.00
}

# --- 2. FUNCIÓN DE CARGA ---
@st.cache_data(ttl=600)
def obtener_pizarra():
    datos = VALORES_BACKUP.copy()
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=3).json()
        for d in res:
            nombre = d['nombre']
            if nombre == "Oficial": datos["Oficial"] = d['venta']
            elif nombre == "Blue": datos["Blue"] = d['venta']
            elif nombre == "MEP": datos["MEP"] = d['venta']
            elif nombre == "Contado con Liquidación": datos["CCL"] = d['venta']
            elif nombre == "Tarjeta": datos["Tarjeta"] = d['venta']
            elif nombre == "Cripto": datos["Cripto"] = d['venta']
    except: pass
    return datos

pizarra = obtener_pizarra()

# --- 3. BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Configuración")
    periodo = st.radio("Ver datos de:", ["2025 (Histórico)", "2026 (Proyectado)"])
    
    st.divider()
    if st.button("🔄 Refrescar Dólares"):
        st.cache_data.clear()
        st.rerun()
    
    st.info("Monitor Económico v2.0\nActualizado: Dic 2025")

# --- 4. ENCABEZADO ---
col_tit1, col_tit2 = st.columns([1, 15])
with col_tit1:
    st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_tit2:
    st.title("Monitor Económico e Impositivo Integral")

st.success(f"🏛️ **Dólar Oficial BCRA: ${pizarra['Oficial']:,.2f}**")
st.divider()

# --- 5. PIZARRA DE COTIZACIONES ---
st.subheader("💵 Tipos de Cambio del Día")
cols = st.columns(6)
nombres = ["Blue", "MEP", "CCL", "Tarjeta", "Cripto", "Oficial"]
for i, n in enumerate(nombres):
    with cols[i]:
        st.metric(label=f"Dólar {n}", value=f"${pizarra[n]:,.2f}")

st.divider()

# --- 6. PANEL DE 12 NOTICIAS ---
st.subheader("📰 Actualidad Económica e Impositiva")
col_e, col_i = st.columns(2)
with col_e:
    st.markdown("**📈 Economía**")
    for n in ["Reservas: Compras por USD 180M.", "Superávit Comercial: USD 1.200M.", "Riesgo País: 790 puntos.", "Consumo: Suba del 2%.", "Cosecha: Récord de soja.", "Tasas: BCRA estable en 40%."]:
        st.write(f"• {n}")
with col_i:
    st.markdown("**⚖️ Impositivas (AFIP)**")
    for n in ["Monotributo: Nuevas tablas 2026.", "Ganancias: Ajuste RIPTE.", "Bienes Personales: Prorroga anticipo.", "Facturación: Nuevos controladores.", "Exportación: Baja de retenciones.", "Moratoria: Últimos días."]:
        st.write(f"• {n}")

st.divider()

# --- 7. HISTORIAL INFLACIÓN (AHORA ANTES QUE RETENCIONES) ---
if periodo == "2025 (Histórico)":
    st.subheader("📊 Historial de Inflación INDEC 2025")
    df_inf = pd.DataFrame({
        "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre"],
        "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5],
    })
    df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
    st.dataframe(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}), use_container_width=True)
    st.info(f"📊 **Inflación Acumulada Anual (Ene-Nov):** {df_inf['IPC Acumulado (%)'].iloc[-1]:.1f}%")
else:
    st.subheader("🔮 Proyección Inflación 2026 (REM)")
    st.warning("Estimaciones basadas en el Relevamiento de Expectativas de Mercado.")
    st.write("• Enero: 2.0% (P)")
    st.write("• Febrero: 1.8% (P)")
    st.write("• Marzo: 2.1% (P)")

st.divider()

# --- 8. RENDIMIENTOS FCI Y TASAS ---
st.subheader("🏦 Rendimientos y Tasas Financieras")
c1, c2, c3 = st.columns(3)
with c1:
    st.info("### 💰 Fondos Money Market")
    st.write("**Fima Premium (Galicia):** 34.5% TNA")
    st.write("**Superfondo Ahorro (Santander):** 34.2% TNA")
with c2:
    st.info("### 🏦 Plazos Fijos")
    st.write("**TNA Promedio Bancos:** 38.0% - 41.0%")
with c3:
    st.warning("### 💳 Tasas Activas")
    st.write("**Préstamos Personales:** 65% - 82% TNA")

st.divider()

# --- 9. TABLA DE RETENCIONES RG 830 ---
st.subheader("⚖️ Régimen de Retención Ganancias - RG 830")
data_rg830 = {
    "Concepto de Pago": ["Bienes Muebles", "Locaciones de Servicios", "Comisiones", "Honorarios Prof.", "Alquileres Inmuebles", "Intereses Préstamos"],
    "Mínimo No Sujeto ($)": ["224.000", "67.000", "31.000", "67.000", "11.200", "Sin mínimo"],
    "Alícuota Inscriptos (%)": ["2%", "2%", "3%", "Escala Art. 94", "6%", "6%"]
}
st.table(pd.DataFrame(data_rg830))
