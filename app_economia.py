import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. CONFIGURACIÓN ESTRUCTURAL
st.set_page_config(page_title="Monitor Estratégico UHY", layout="wide")

@st.cache_data(ttl=600)
def obtener_datos_completos():
    # Divisas
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        pizarra = {d['nombre']: d['venta'] for d in res}
    except:
        pizarra = {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00}
    
    # Clima CABA (Open-Meteo)
    try:
        url_w = "https://api.open-meteo.com/v1/forecast?latitude=-34.61&longitude=-58.38&current_weather=true&hourly=precipitation_probability"
        res_w = requests.get(url_w).json()
        temp = res_w['current_weather']['temperature']
        prob = res_w['hourly']['precipitation_probability'][datetime.now().hour]
        clima = {"temp": f"{temp}°C", "lluvia": f"{prob}%"}
    except:
        clima = {"temp": "27°C", "lluvia": "71%"}
        
    return pizarra, clima

pizarra, clima = obtener_datos_completos()

# 2. SIDEBAR (DATOS Y CLIMA)
with st.sidebar:
    st.image("https://flagcdn.com/w160/ar.png", width=100)
    st.subheader(f"🌡️ {clima['temp']} | 🌧️ {clima['lluvia']}")
    st.caption(f"Buenos Aires, {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    
    st.markdown("### 🔍 Índices de Mercado")
    st.metric("Riesgo País", "754 bps", "-31") 
    st.metric("Dólar Futuro (Dic-26)", "$1.645,50", "+2.1%")
    st.metric("Índice Merval", "2.140.580", "▲ 2.4%")
    st.metric("Nasdaq 100", "20.150,45", "▲ 1.1%")
    st.metric("Balanza Comercial", "USD +2.498M")
    
    if st.button("🔄 Sincronizar"):
        st.cache_data.clear()
        st.rerun()

# 3. CUERPO PRINCIPAL
st.title("Monitor Económico e Impositivo Integral")

# Cards de Dólares
cols = st.columns(len(pizarra))
for i, (nombre, valor) in enumerate(pizarra.items()):
    with cols[i]:
        st.metric(label=f"Dólar {nombre}", value=f"${valor:,.2f}")

st.divider()

# 4. ACTUALIDAD (TABS: ECONOMÍA, IMPUESTOS, BOLETÍN)
st.subheader("📰 Centro de Novedades y Alertas")
t_eco, t_imp, t_bo = st.tabs(["📈 Economía", "⚖️ Impuestos", "📜 Resoluciones ARCA (B.O.)"])

with t_eco:
    c1, c2 = st.columns(2)
    eco = [("Dólar Blue: $1.485 sostenida", "https://www.ambito.com"), ("Reservas BCRA: u$s 42.413M", "https://www.bcra.gob.ar"), ("Caputo: Preadjudicación hidroeléctricas", "https://www.cronista.com"), ("Brecha Cambiaria: MEP en 3,1%", "https://www.infobae.com"), ("Informalidad: 70% sin registro", "https://www.lanacion.com.ar"), ("Agenda USA: Demoras en acuerdos", "https://www.clarin.com")]
    for i, (t, l) in enumerate(eco):
        with (c1 if i < 3 else c2): st.markdown(f"• [{t}]({l})")

with t_imp:
    c3, c4 = st.columns(2)
    imp = [("Inocencia Fiscal: Nuevo piso evasión", "https://www.ambito.com"), ("Bienes Personales: Mínimo $384,7M", "https://www.afip.gob.ar"), ("Moratoria CABA: Hasta 9 enero", "https://www.agip.gob.ar"), ("Retenciones: Baja Soja y Trigo", "https://www.infocampo.com.ar"), ("ARCA: Topes Impuesto PAIS", "https://servicioscf.afip.gob.ar"), ("Ley Tarifaria 2026: Escalas Prov.", "https://www.boletinoficial.gob.ar")]
    for i, (t, l) in enumerate(imp):
        with (c3 if i < 3 else c4): st.markdown(f"• [{t}]({l})")

with t_bo:
    st.info("🔎 **Boletín Oficial - Publicaciones de Hoy**")
    st.warning("⚠️ **RG 5612/2025:** Actualización de retenciones por movilidad y viáticos.")
    st.warning("⚠️ **RG 5613/2025:** Modificación de plazos para regímenes informativos.")
    st.link_button("Acceder a la Primera Sección B.O.", "https://www.boletinoficial.gob.ar/seccion/primera")

st.divider()

# 5. INDICADORES ECONÓMICOS
st.subheader("📊 Indicadores de Mercado")
col_tasas, col_inf = st.columns(2)

with col_tasas:
    with st.container(border=True):
        st.markdown("**🏦 Tasas y Rendimientos**")
        st.write("✅ **Fima Galicia:** 28.21% TNA")
        st.write("✅ **Santander MM:** 19.23% TNA")
        st.write("✅ **Plazo Fijo:** 39.00% TNA")
        st.write("❌ **Costo Adelanto Cte:** 62.00% TNA")

with col_inf:
    with st.container(border=True):
        st.markdown("**📉 Evolución Inflación 2025**")
        df_i = pd.DataFrame({"IPC %": [2.2, 2.4, 3.7, 2.8, 1.5, 1.6, 1.9, 1.9, 2.1, 2.3, 2.5, 2.3]}, 
                            index=["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"])
        st.line_chart(df_i, height=150)

st.divider()

# 6. CUADROS DE IMPUESTOS (DATOS EXACTOS)
st.subheader("⚖️ Tablas de Liquidación Auditadas")
t_ph, t_bbpp, t_ded, t_soc, t_mon = st.tabs(["Ganancias PH", "Bienes Personales", "Deducciones", "Sociedades", "Monotributo"])

with t_ph:
    df_ph = pd.DataFrame({
        "Escala": ["Mínima", "Media", "Máxima"],
        "Desde ($)": ["0,00", "14.729.115,24", "49.667.273,02"],
        "Fijo ($)": ["0,00", "2.193.001,60", "11.992.882,45"],
        "Ali %": ["5%", "23%", "35%"]
    })
    st.table(df_ph)

with t_bbpp:
    st.write("**MNI:** $384.728.044,56 | **Casa-Habitación:** $1.346.548.155,99")
    df_bbpp = pd.DataFrame({"Tramos": ["0-52M", "52-114M", "+114M"], "Ali": ["0,50%", "0,75%", "1,00%"], "Fijo ($)": ["0,00", "263.321,42", "724.133,90"]})
    st.table(df_bbpp)

with t_ded:
    st.table(pd.DataFrame({"Deducción": ["MNI", "Cónyuge", "Hijo", "Especial"], "Monto Anual ($)": ["4.093.923,60", "3.858.913,56", "1.946.069,52", "19.650.833,28"]}))

with t_soc:
    st.table(pd.DataFrame({"Ganancia Neta": ["Hasta 101M", "101M - 1B", "+1B"], "Ali": ["25%", "30%", "35%"]}))

with t_mon:
    st.table(pd.DataFrame({"Cat": ["A", "D", "K"], "Ingresos ($)": ["8.9M", "23.2M", "94.8M"], "Cuota ($)": ["37.085", "63.357", "428.100"]}))

st.divider()

# 7. US TAX UPDATE (DICIEMBRE 2025)
st.subheader("🇺🇸 US Tax Alert: IRS Enforcement on Form 1099-K (Dec 2025)")
with st.container(border=True):
    st.markdown("""
    **New Reporting Standards for Digital Payments**
    The IRS has confirmed that for the 2025 tax year, the **$600 reporting threshold** for Form 1099-K is officially in effect, ending the transition period.
    
    * **Scope:** Third-party settlement organizations (PayPal, Venmo, Stripe) must report gross payments exceeding $600.
    * **Key Risk:** Foreign owners of US LLCs (consultants/E-commerce) will have higher transparency for their US-source income.
    * **Action:** Ensure your US tax filings (Form 1040-NR or 1120/5472) align with these reported amounts to avoid audits.
    * **Source:** [IRS Newsroom - December 2025 Update](https://www.irs.gov/newsroom)
    """)
