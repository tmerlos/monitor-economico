import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Monitor ARCA Profesional", layout="wide")

# --- 1. CARGA DE DATOS DE MERCADO ---
@st.cache_data(ttl=600)
def obtener_pizarra():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=3).json()
        datos = {d['nombre']: d['venta'] for d in res}
        return {
            "Oficial": datos.get("Oficial", 1030.5),
            "Blue": datos.get("Blue", 1485.0),
            "MEP": datos.get("MEP", 1496.8),
            "CCL": datos.get("Contado con Liquidación", 1555.0),
            "Tarjeta": datos.get("Tarjeta", 1935.45)
        }
    except:
        return {"Oficial": 1030.5, "Blue": 1485.0, "MEP": 1496.8, "CCL": 1555.0, "Tarjeta": 1935.45}

pizarra = obtener_pizarra()
Dólar oficial fin de mes
# -------------------------------
def get_dolar_fin_mes():
    url = "https://www.cotizacion-dolar.com.ar/dolar-historico-bna-2025.php"
    resp = safe_get(url)
    dfs = pd.read_html(resp.text)
    df = dfs[0]
    df.columns = [c.strip() for c in df.columns]
    return df.to_dict(orient="records")



# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.title("Panel ARCA")
    st.markdown("### Período Fiscal 2025")
    if st.button("🔄 Sincronizar Todo"):
        st.cache_data.clear()
        st.rerun()

# --- 3. ENCABEZADO ---
col1, col2 = st.columns([1, 12])
with col1: st.image("https://flagcdn.com/w80/ar.png", width=70)
with col2: st.title("Monitor Económico e Impositivo Integral")
st.success(f"🏛️ **Dólar Oficial (Referencia ARCA): ${pizarra['Oficial']:,.2f}**")

# --- 4. COTIZACIONES ---
cols = st.columns(5)
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]: st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. RENDIMIENTOS FINANCIEROS ---
st.subheader("🏦 Tasas y Rendimientos")
c1, c2, c3 = st.columns(3)
with c1:
    st.info("### 💰 Fondos Money Market")
    st.write("**Fima Premium (Galicia):** 34.50% TNA")
    st.write("**Superfondo Ahorro (Santander):** 34.20% TNA")
with c2:
    st.info("### 🏦 Plazos Fijos")
    st.write("**TNA Minorista (Bancos):** 39.0%")
    st.write("**Tasa Badlar:** 42.1%")
with c3:
    st.warning("### 💳 Crédito y Financiación")
    st.write("**Préstamos Personales:** 78% TNA")
    st.write("**Adelanto Cta Cte:** 62% TNA")

st.divider()

# --- 6. PANEL DE 12 NOTICIAS (REINCORPORADO) ---
st.subheader("📰 Actualidad del Día")
col_not_e, col_not_i = st.columns(2)
with col_not_e:
    st.markdown("**📈 Economía**")
    for n in ["Reservas: Compras por USD 180M.", "Superávit Comercial: USD 1.200M.", "Riesgo País: 790 puntos.", "Consumo: Suba del 2% en el mes.", "Cosecha: Récord proyectado de soja.", "Tasas: BCRA mantiene política estable."]:
        st.write(f"• {n}")
with col_not_i:
    st.markdown("**⚖️ Impositivas (ARCA)**")
    for n in ["Monotributo: Recategorización Enero.", "Ganancias: Publicación RIPTE anual.", "Bienes Personales: Nuevos beneficios.", "Factura Electrónica: Nuevos límites.", "Retenciones: Baja en expo servicios.", "Moratoria: Fecha límite próxima."]:
        st.write(f"• {n}")

st.divider()

# --- 7. INFLACIÓN ---
st.subheader("📊 Historial de Inflación INDEC 2025")
df_inf = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"],
    "IPC Mensual (%)": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5]
})
df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
st.table(df_inf.style.format({"IPC Mensual (%)": "{:.1f}%", "IPC Acumulado (%)": "{:.1f}%"}))

st.divider()

# --- 8. MONOTRIBUTO: ESCALAS LEY 27.743 ---
st.subheader("⚖️ Monotributo: Topes Vigentes 2025/2026")
df_mono = pd.DataFrame({
    "Cat.": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    "Ingresos Anuales ($)": ["6.450.000", "9.450.000", "13.250.000", "16.450.000", "19.350.000", "24.250.000", "29.000.000", "44.000.000", "49.250.000", "56.400.000", "68.000.000"],
    "Cuota Total Bienes/Srv ($)": ["26.600", "30.280", "35.458", "45.443", "58.519", "74.825", "91.419", "175.091", "217.120", "258.150", "307.130"]
})
st.table(df_mono)

st.divider()

# --- 9. GANANCIAS SOCIEDADES ---
st.subheader("🏢 Ganancias: Personas Jurídicas (ARCA)")
data_soc = {
    "Ganancia Neta Imponible Acumulada": ["Hasta $51.048.708", "$51.048.708 a $510.487.085", "Más de $510.487.085"],
    "Alícuota": ["25%", "30%", "35%"],
    "Monto Fijo": ["$0", "$12.762.177", "$150.593.690"],
    "S/ Excedente de": ["$0", "$51.048.708", "$510.487.085"]
}
st.table(pd.DataFrame(data_soc))

st.divider()

# --- 10. GANANCIAS PERSONAS HUMANAS ---
st.subheader("👤 Ganancias: Personas Humanas (Art. 94)")
data_ph = {
    "Ganancia Neta Imponible ($)": ["0 - 1.2M", "1.2M - 2.4M", "2.4M - 4.8M", "4.8M - 9.6M", "9.6M - 19.2M", "19.2M - 38.4M", "38.4M - 76.8M", "76.8M - 153.6M", "Más de 153.6M"],
    "Fijo ($)": ["0", "60.000", "168.000", "456.000", "1.176.000", "3.000.000", "7.416.000", "17.784.000", "41.592.000"],
    "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"]
}
st.table(pd.DataFrame(data_ph))

st.divider()

# --- 11. RETENCIONES RG 830 ---
st.subheader("📋 Retenciones Ganancias (RG 830)")
data_rg = {
    "Concepto": ["Bienes Muebles", "Servicios", "Honorarios", "Alquileres"],
    "Mínimo No Sujeto ($)": ["224.000", "67.170", "67.170", "11.200"],
    "Alícuota Inscriptos": ["2%", "2%", "Escala Art. 94", "6%"]
}
st.table(pd.DataFrame(data_rg))

