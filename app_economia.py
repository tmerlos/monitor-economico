import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor ARCA Pro", layout="wide")

# --- 1. CARGA DINÁMICA DE MERCADOS ---
@st.cache_data(ttl=600)
def obtener_mercados():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        # Convertimos la lista en un diccionario para acceso directo
        mapa = {d['nombre']: d['venta'] for d in res}
        return {
            "Oficial": mapa.get("Oficial", 1030.50),
            "Blue": mapa.get("Blue", 1485.00),
            "MEP": mapa.get("MEP", 1496.80),
            "CCL": mapa.get("Contado con Liquidación", 1555.00),
            "Tarjeta": mapa.get("Tarjeta", 1935.45)
        }
    except:
        return {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00, "Tarjeta": 1935.45}

pizarra = obtener_mercados()

# --- 2. SIDEBAR PRO ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel de Auditoría")
    st.markdown("### Período Fiscal 2025")
    st.write("**Base Legal:** Ley 27.743")
    if st.button("🔄 Sincronizar con ARCA/BCRA"):
        st.cache_data.clear()
        st.rerun()

# --- 3. ENCABEZADO ---
col_f1, col_f2 = st.columns([1, 15])
with col_f1: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col_f2: st.title("Monitor Económico e Impositivo Integral")
st.success(f"🏛️ **Dólar Oficial (Ref. ARCA): ${pizarra['Oficial']:,.2f}**")

# --- 4. PIZARRA DE COTIZACIONES ---
cols = st.columns(5)
for i, (nombre, valor) in enumerate(pizarra.items()):
    with cols[i]:
        st.metric(label=f"Dólar {nombre}", value=f"${valor:,.2f}")

st.divider()

# --- 5. TASAS Y RENDIMIENTOS ---
st.subheader("🏦 Rendimientos Financieros Actuales")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("### 💰 Fondos Money Market")
    st.write("**Fima Premium (Galicia):** 34.50% TNA")
    st.write("**Superfondo Ahorro (Santander):** 34.20% TNA")
with t2:
    st.info("### 🏦 Plazos Fijos")
    st.write("**TNA Minorista (Bancos):** 39.0% - 41.5%")
    st.write("**Tasa Badlar:** 42.85%")
with t3:
    st.warning("### 💳 Crédito y Financiación")
    st.write("**Personales:** 78% TNA / **Adelanto:** 62%")

st.divider()

# --- 6. PANEL DE ACTUALIDAD (6+6) ---
st.subheader("📰 Actualidad y Novedades")
col_not_e, col_not_i = st.columns(2)
with col_not_e:
    st.markdown("**📈 Economía**")
    noticias_e = ["Reservas: El BCRA compró USD 180M.", "Riesgo País: Bajó a 790 puntos.", "Superávit: Saldo comercial positivo.", "Consumo: Repunte estacional de ventas.", "Cosecha: Estimación récord de soja.", "Inflación: Desaceleración confirmada."]
    for n in noticias_e: st.write(f"• {n}")
with col_not_i:
    st.markdown("**⚖️ Impositivas (ARCA)**")
    noticias_i = ["Monotributo: Recategorización Enero 2026.", "Ganancias: Publicadas escalas Art. 94.", "Bienes Personales: Nuevos mínimos exentos.", "Facturación: Límites de identificación 2025.", "Retenciones: Ajuste de mínimos RG 830.", "Moratoria: Útimos días para adhesión."]
    for n in noticias_i: st.write(f"• {n}")

st.divider()

# --- 7. TABLA DE INFLACIÓN (IPC) ---
st.subheader("📊 Historial de Inflación INDEC 2025")
df_inf = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5]
})
df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 8. MONOTRIBUTO 2025/2026 (TABLA LEY 27.743) ---
st.subheader("⚖️ Monotributo: Escalas Vigentes")
st.caption("Valores unificados para Servicios y Bienes - ARCA.")
df_mono = pd.DataFrame({
    "Cat.": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Brutos Anuales ($)": ["6.45M", "9.45M", "13.25M", "16.45M", "19.35M", "24.25M", "29.0M", "44.0M", "49.25M", "56.4M", "68.0M"],
    "Cuota Total Srv/Bienes ($)": ["26.600", "30.280", "35.458", "45.443", "58.519", "74.825", "91.419", "175.091", "217.120", "258.150", "307.130"]
})
st.table(df_mono)

st.divider()

# --- 9. GANANCIAS SOCIEDADES (PERSONAS JURÍDICAS) ---
st.subheader("🏢 Impuesto a las Ganancias: Sociedades")
st.write("Escala Progresiva Período 2025 (Ajustada por IPC):")
data_soc = {
    "Ganancia Neta Imponible Acumulada": ["Hasta $51.048.708", "De $51.048.708 a $510.487.085", "Más de $510.487.085"],
    "Alícuota": ["25%", "30%", "35%"],
    "Paga Fijo": ["$0", "$12.762.177", "$150.593.690"],
    "Más % s/ excedente de": ["$0", "$51.048.708", "$510.487.085"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 10. GANANCIAS PERSONAS HUMANAS (ART. 94) ---
st.subheader("👤 Impuesto a las Ganancias: Personas Humanas")
st.caption("Escala Progresiva Anualizada 2025 (Valores definitivos Ley 27.743)")

data_ph = {
    "Ganancia Neta Imponible ($)": ["0 - 1.2M", "1.2M - 2.4M", "2.4M - 4.8M", "4.8M - 9.6M", "9.6M - 19.2M", "19.2M - 38.4M", "38.4M - 76.8M", "76.8M - 153.6M", "Más de 153.6M"],
    "Monto Fijo ($)": ["0", "60.000", "168.000", "456.000", "1.176.000", "3.000.000", "7.416.000", "17.784.000", "41.592.000"],
    "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"]
}
st.table(pd.DataFrame(data_ph))

st.divider()

# --- 11. RETENCIONES GANANCIAS (RG 830) ---
st.subheader("📋 Retenciones Ganancias RG 830")
data_rg = {
    "Concepto": ["Bienes Muebles", "Locaciones de Servicios", "Honorarios Profesionales", "Alquileres"],
    "Mínimo No Sujeto ($)": ["224.000", "67.170", "67.170", "11.200"],
    "Inscripto (%)": ["2%", "2%", "Escala Art. 94 (mín 3%)", "6%"]
}
st.table(pd.DataFrame(data_rg))
