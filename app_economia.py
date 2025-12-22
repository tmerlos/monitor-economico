import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Monitor Estratégico UHY 2025", layout="wide")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #004B39; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    [data-testid="stSidebar"] .stButton button { color: #004B39 !important; background-color: #FFFFFF !important; }
    [data-testid="stSidebar"] a { color: #80ffdb !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CARGA DE DATOS ---
@st.cache_data(ttl=600)
def obtener_datos():
    try:
        res = requests.get("https://dolarapi.com/v1/dolares", timeout=5).json()
        pizarra = {d['nombre']: d['venta'] for d in res}
    except:
        pizarra = {"Oficial": 1030.50, "Blue": 1485.00, "MEP": 1496.80, "CCL": 1555.00}
    
    try:
        lat, lon = -34.6037, -58.3816
        url_w = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation_probability"
        res_w = requests.get(url_w, timeout=3).json()
        temp = res_w['current_weather']['temperature']
        prob = res_w['hourly']['precipitation_probability'][datetime.now().hour]
        clima = f"{temp}°C - CABA (Lluvia: {prob}%)"
    except:
        clima = "27°C - CABA (Lluvia: --%)"
        
    return pizarra, clima

pizarra, clima_actual = obtener_datos()

# --- 3. SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo_uhy.png", use_container_width=True)
    except:
        st.image("https://www.uhy.com/themes/custom/uhy_theme/logo.svg", use_container_width=True)
    
    st.markdown(f"### 🌡️ {clima_actual}")
    st.markdown(f"📅 **{datetime.now().strftime('%d/%m/%Y')}**")
    st.divider()
    
    st.markdown("### 🔍 Índices Críticos")
    st.metric("Riesgo País", "754 bps", "-31") 
    st.metric("Índice Merval", "2.140.580", "▲ 2.4%")
    st.metric("Nasdaq 100", "20.150,45", "▲ 1.1%")
    st.metric("Tasa Desempleo", "6.6%")
    
    st.divider()
    st.markdown("### 📉 Dólar Futuro")
    st.metric("Junio 2026", "$1.410,20", "+1.8%")
    st.metric("Diciembre 2026", "$1.645,50", "+2.1%")
    st.caption("Fuente: [Matba Rofex](https://www.matbarofex.com.ar/)")
    
    st.divider()
    if st.button("🔄 Actualizar Todo"):
        st.cache_data.clear()
        st.rerun()

# --- 4. ENCABEZADO ---
st.title("Monitor Económico e Impositivo Integral")
st.markdown("**Powered by UHY Macho & Asociados**")
st.markdown("---")

cols = st.columns(len(pizarra))
for i, (n, v) in enumerate(pizarra.items()):
    with cols[i]:
        st.metric(label=f"Dólar {n}", value=f"${v:,.2f}")

st.divider()

# --- 5. ACTUALIDAD ---
st.subheader("📰 Centro de Novedades y Alertas")
t_eco, t_imp, t_bo = st.tabs(["📈 Noticias Económicas (6)", "⚖️ Noticias Impositivas (6)", "📜 Boletín Oficial"])

with t_eco:
    c1, c2 = st.columns(2)
    eco_list = [
        ("Dólar Blue: $1.485 sostenida", "https://www.ambito.com"),
        ("Reservas BCRA: u$s 42.413M", "https://www.bcra.gob.ar"),
        ("Caputo: Preadjudicación hidroeléctricas", "https://www.cronista.com"),
        ("Brecha Cambiaria: MEP en 3,1%", "https://www.infobae.com"),
        ("Informalidad: 70% sin registro", "https://www.lanacion.com.ar"),
        ("Agenda USA: Demoras en acuerdos", "https://www.clarin.com")
    ]
    for i, (t, l) in enumerate(eco_list):
        with (c1 if i < 3 else c2): st.markdown(f"• [{t}]({l})")

with t_imp:
    c3, c4 = st.columns(2)
    imp_list = [
        ("Inocencia Fiscal: Nuevo piso evasión", "https://www.ambito.com"),
        ("Bienes Personales: Mínimo $384,7M", "https://www.afip.gob.ar"),
        ("Moratoria CABA: Hasta 9 enero", "https://www.agip.gob.ar"),
        ("Retenciones: Baja Soja y Trigo", "https://www.infocampo.com.ar"),
        ("ARCA: Topes Impuesto PAIS", "https://servicioscf.afip.gob.ar"),
        ("Ley Tarifaria 2026: Escalas Prov.", "https://www.boletinoficial.gob.ar")
    ]
    for i, (t, l) in enumerate(imp_list):
        with (c3 if i < 3 else c4): st.markdown(f"• [{t}]({l})")

with t_bo:
    with st.container(border=True):
        st.info("🔎 **Publicaciones del Día en Boletín Oficial**")
        st.markdown("🔴 **RG 5612/2025:** Actualización de retenciones por movilidad y viáticos.")
        st.markdown("🔴 **RG 5613/2025:** Modificación de plazos para regímenes informativos.")
        st.markdown("---")
        st.link_button("Ir al Boletín Oficial (1ra Sección)", "https://www.boletinoficial.gob.ar/seccion/primera")

st.divider()

# --- 6. INDICADORES ---
st.subheader("📊 Indicadores Financieros")
tab_tasas, tab_inflacion = st.tabs(["🏦 Tasas y Fondos", "📊 Inflación (Tabla Completa)"])

with tab_tasas:
    c_act, c_pas = st.columns(2)
    with c_act:
        st.error("#### Tasas Activas (Costo)")
        st.write("• **Adelanto Cta Cte:** 62.00% TNA")
        st.write("• **Descuento Cheques:** 48.00% TNA")
        st.write("• **Tarjetas (Ley):** 122.00% TNA")
    with c_pas:
        st.success("#### Tasas Pasivas (Rendimiento)")
        st.write("• **Fima Ahorro Pesos (Galicia):** 28.21% TNA")
        st.write("• **Santander Super Ahorro $:** 19.23% TNA")
        st.write("• **Plazo Fijo Minorista:** 39.00% TNA")
        st.write("• **Tasa Badlar:** 42.80% TNA")

with tab_inflacion:
    st.markdown("**Evolución del Índice de Precios al Consumidor (2025)**")
    df_inf = pd.DataFrame({
        "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre (Est)"],
        "IPC Mensual (%)": [2.20, 2.40, 3.70, 2.80, 1.50, 1.60, 1.90, 1.90, 2.10, 2.30, 2.50, 2.30]
    })
    df_inf['IPC Acumulado (%)'] = ((1 + df_inf['IPC Mensual (%)'] / 100).cumprod() - 1) * 100
    st.table(df_inf.style.format({"IPC Mensual (%)": "{:.2f}%", "IPC Acumulado (%)": "{:.2f}%"}))

st.divider()

# --- 7. TABLAS DE IMPUESTOS Y CALCULADORA ---
st.subheader("⚖️ Tablas de Liquidación Completas (Auditadas)")
t_ph, t_bbpp, t_deduc, t_soc, t_mon, t_rg, t_calc = st.tabs(["Ganancias PH", "Bienes Personales", "Deducciones", "Sociedades", "Monotributo", "RG 830", "🧮 Calculadora"])

with t_ph:
    st.markdown("#### Escala Art. 94 LIG - Período Fiscal 2025 (Completa)")
    df_ph = pd.DataFrame({
        "Ganancia Neta Imponible Acum. ($)": ["0 a 1.636.568,36", "1.636.568,36 a 3.273.136,72", "3.273.136,72 a 4.909.705,08", "4.909.705,08 a 7.364.557,62", "7.364.557,62 a 14.729.115,24", "14.729.115,24 a 22.093.672,86", "22.093.672,86 a 33.140.509,29", "33.140.509,29 a 49.667.273,02", "Más de 49.667.273,02"],
        "Monto Fijo ($)": ["0,00", "81.828,42", "229.119,57", "425.507,77", "793.735,65", "2.193.001,60", "3.886.949,85", "6.869.585,69", "11.992.882,45"],
        "Alícuota %": ["5%", "9%", "12%", "15%", "19%", "23%", "27%", "31%", "35%"],
        "S/ Excedente de ($)": ["0,00", "1.636.568,36", "3.273.136,72", "4.909.705,08", "7.364.557,62", "14.729.115,24", "22.093.672,86", "33.140.509,29", "49.667.273,02"]
    })
    st.table(df_ph)

with t_bbpp:
    st.markdown("#### Bienes Personales 2025")
    st.write("**Mínimo No Imponible:** $384.728.044,56 | **Casa Habitación:** $1.346.548.155,99")
    df_bbpp = pd.DataFrame({
        "Valor Total de Bienes que exceda el MNI ($)": ["0 a 52.664.283,73", "52.664.283,73 a 114.105.948,16", "Más de 114.105.948,16"],
        "Pagarán ($)": ["0,00", "263.321,42", "724.133,90"],
        "Más el %": ["0,50%", "0,75%", "1,00%"],
        "Sobre el excedente de ($)": ["0,00", "52.664.283,73", "114.105.948,16"]
    })
    st.table(df_bbpp)

with t_deduc:
    st.markdown("#### Deducciones Personales Art. 30")
    df_ded = pd.DataFrame({
        "Concepto": ["Ganancia No Imponible (a)", "Cónyuge (b)", "Hijo menor 18 (b)", "Hijo Incapacitado (b)", "Ded. Especial Autónoma (c)", "Ded. Especial Empleado (c)"],
        "Monto Anual 2025 ($)": ["4.093.923,60", "3.858.913,56", "1.946.069,52", "3.892.139,04", "8.187.847,20", "19.650.833,28"]
    })
    st.table(df_ded)

with t_soc:
    st.markdown("#### Ganancias Sociedades")
    df_soc = pd.DataFrame({
        "Tramo Ganancia Neta ($)": ["0 a 101.679.575,26", "101.679.575,26 a 1.016.795.752,60", "Más de 1.016.795.752,60"],
        "Alícuota": ["25%", "30%", "35%"],
        "Monto Fijo ($)": ["0,00", "25.419.893,82", "299.954.747,02"]
    })
    st.table(df_soc)

with t_mon:
    st.markdown("#### Monotributo Dic 2025 (Valores Completos)")
    df_mono_full = pd.DataFrame({
        "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
        "Ingresos Brutos Anuales ($)": [
            "8.987.312,20", "13.345.101,40", "18.677.202,30", "23.211.504,10", "27.321.405,80", 
            "34.112.508,40", "40.876.310,10", "62.011.514,50", "69.455.618,20", "79.445.820,10", "94.805.682,90"
        ],
        "Cuota Total Mensual ($)": [
            "37.085,00", "42.216,00", "49.435,00", "63.357,00", "81.412,00", 
            "104.256,00", "127.108,00", "244.135,00", "302.510,00", "359.845,00", "428.100,00"
        ]
    })
    st.table(df_mono_full)

with t_rg:
    st.markdown("#### RG 830 - Retenciones")
    data_rg_full = {
        "Concepto": ["Bienes Muebles", "Obras/Servicios", "Honorarios", "Alquileres", "Comisiones", "Fletes"],
        "Mínimo No Sujeto ($)": ["224.000", "98.240", "98.240", "16.360", "45.100", "32.000"],
        "Insc. (%)": ["2,0%", "2,0%", "Escala", "6,0%", "3,0%", "0,25%"]
    }
    st.table(pd.DataFrame(data_rg_full))

with t_calc:
    st.markdown("### 🧮 Calculadora de Impuesto a las Ganancias (Detallada)")
    st.info("Ingrese los sueldos brutos de cada mes. El sistema calculará automáticamente los aportes topeados mes a mes y el impuesto acumulado.")

    meses = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
    
    # 1. Selector de Mes de Cálculo
    mes_sel = st.selectbox("📅 Seleccione Mes de Liquidación", list(meses.keys()), index=11, format_func=lambda x: meses[x])

    # 2. Grilla de Carga de Sueldos
    sueldos_mensuales = {}
    sac_junio = 0.0
    sac_diciembre = 0.0
    
    with st.expander("📝 Carga de Sueldos Brutos Mensuales", expanded=True):
        col_grilla = st.columns(4)
        for i in range(1, 13):
            with col_grilla[(i-1)%4]:
                # Si el mes es mayor al seleccionado, deshabilitar o dejar en 0 (visual)
                disabled = i > mes_sel
                val = st.number_input(f"{meses[i]}", min_value=0.0, step=10000.0, key=f"s_{i}", disabled=disabled, value=0.0)
                sueldos_mensuales[i] = val
        
        st.markdown("---")
        st.markdown("**Carga de SAC (Aguinaldo)**")
        c_sac1, c_sac2 = st.columns(2)
        with c_sac1:
            sac_junio = st.number_input("SAC 1er Semestre (Junio)", min_value=0.0, step=10000.0, disabled=(mes_sel < 6))
        with c_sac2:
            sac_diciembre = st.number_input("SAC 2do Semestre (Diciembre)", min_value=0.0, step=10000.0, disabled=(mes_sel < 12))

    # --- LÓGICA DE CÁLCULO ACUMULADA ---
    def calcular_acumulados_real(mes_corte, sueldos_dict, sac_jun, sac_dic):
        bruto_total = 0.0
        aportes_total = 0.0
        
        # Valor Tope Diciembre 2025 fijo
        valor_tope_diciembre = 3731212.01
        
        # Iterar mes a mes hasta el mes de corte
        for m in range(1, mes_corte + 1):
            s_mes = sueldos_dict.get(m, 0.0)
            
            # 1. Base Tope del mes m (ajustado por inflación inversa)
            base_tope_m = valor_tope_diciembre / (1.035**(12 - m))
            
            # 2. Aportes Sueldo
            base_calc = min(s_mes, base_tope_m)
            aporte_mes = base_calc * 0.17
            
            bruto_total += s_mes
            aportes_total += aporte_mes
            
            # 3. SAC y Aportes SAC
            if m == 6:
                bruto_total += sac_jun
                # Tope SAC es 50% del tope mensual
                base_sac_jun = min(sac_jun, base_tope_m / 2)
                aportes_total += base_sac_jun * 0.17
            
            if m == 12:
                bruto_total += sac_dic
                base_sac_dic = min(sac_dic, base_tope_m / 2)
                aportes_total += base_sac_dic * 0.17
        
        # 4. Deducciones
        mni = 4093923.60
        ded_esp = 19650833.28
        ded_total_acum = ((mni + ded_esp) / 12) * mes_corte
        
        # 5. Neto
        neto = max(0, bruto_total - ded_total_acum - aportes_total)
        
        # 6. Escala
        escala = [
            {"d": 0, "h": 1636568.36, "f": 0, "p": 5, "exc": 0},
            {"d": 1636568.36, "h": 3273136.72, "f": 81828.42, "p": 9, "exc": 1636568.36},
            {"d": 3273136.72, "h": 4909705.08, "f": 229119.57, "p": 12, "exc": 3273136.72},
            {"d": 4909705.08, "h": 7364557.62, "f": 425507.77, "p": 15, "exc": 4909705.08},
            {"d": 7364557.62, "h": 14729115.24, "f": 793735.65, "p": 19, "exc": 7364557.62},
            {"d": 14729115.24, "h": 22093672.86, "f": 2193001.60, "p": 23, "exc": 14729115.24},
            {"d": 22093672.86, "h": 33140509.29, "f": 3886949.85, "p": 27, "exc": 22093672.86},
            {"d": 33140509.29, "h": 49667273.02, "f": 6869585.69, "p": 31, "exc": 33140509.29},
            {"d": 49667273.02, "h": float('inf'), "f": 11992882.45, "p": 35, "exc": 49667273.02},
        ]
        
        tramo_obj = next((t for t in escala if t["d"] <= neto < t["h"]), None)
        imp = 0.0
        if tramo_obj:
            imp = tramo_obj["f"] + ((neto - tramo_obj["exc"]) * (tramo_obj["p"] / 100))
            
        # Base máxima del mes seleccionado (para visualización)
        base_max_sel = valor_tope_diciembre / (1.035**(12 - mes_corte))
        
        return imp, bruto_total, aportes_total, ded_total_acum, neto, tramo_obj, base_max_sel

    # Ejecución
    imp_actual, br_acum, ap_acum, de_acum, nt_suj, tramo_act, tope_act = calcular_acumulados_real(mes_sel, sueldos_mensuales, sac_junio, sac_diciembre)
    
    imp_anterior = 0.0
    if mes_sel > 1:
        # Calcular hasta el mes anterior para sacar la diferencia
        imp_anterior, _, _, _, _, _, _ = calcular_acumulados_real(mes_sel - 1, sueldos_mensuales, sac_junio, sac_diciembre)
    
    retencion_mes = imp_actual - imp_anterior

    st.markdown("---")
    
    with st.container(border=True):
        st.markdown(f"### 📉 Resultado Acumulado a {meses[mes_sel]}")
        
        c_res1, c_res2, c_res3, c_res4 = st.columns(4)
        c_res1.metric("Bruto Acumulado", f"${br_acum:,.2f}")
        c_res2.metric("Aportes (17%)", f"-${ap_acum:,.2f}")
        c_res3.metric("Deducciones (MNI+Esp)", f"-${de_acum:,.2f}")
        c_res4.metric("Neto Sujeto a Impuesto", f"${nt_suj:,.2f}")
        
        st.divider()

        # BASE MAXIMA
        st.write(f"ℹ️ **Base Imponible Máxima para Aportes ({meses[mes_sel]} 2025):** ${tope_act:,.2f}")
        st.markdown("") 

        if tramo_act:
            st.write(f"**Ubicación en Escala:** Tramo de ${tramo_act['d']:,.2f} a ${tramo_act['h'] if tramo_act['h']!=float('inf') else '...':,.2f}")
            st.write(f"**Monto Fijo:** ${tramo_act['f']:,.2f} + **{tramo_act['p']}%** sobre excedente de ${tramo_act['exc']:,.2f}")
        
        st.divider()
        
        c_imp1, c_imp2 = st.columns(2)
        c_imp1.metric("Impuesto Acum. Mes Anterior", f"${imp_anterior:,.2f}")
        c_imp2.metric(f"Impuesto del Mes ({meses[mes_sel]})", f"${retencion_mes:,.2f}")
        
        st.error(f"### Total Impuesto Determinado (Acumulado): ${imp_actual:,.2f}")

st.divider()

# --- 8. NOVEDADES ---
c_usa, c_prov = st.columns(2)

with c_usa:
    with st.container(border=True):
        st.subheader("🇺🇸 Tax Update (Dec 2025)")
        st.markdown("**📍 Estados Unidos**")
        st.info("""
        **IRS Enforcement on Form 1099-K**
        * The IRS confirmed the **$600 threshold** for Form 1099-K is effective for 2025 returns.
        * **Impact:** Third-party settlement organizations must report gross payments > $600.
        * **Action:** Reconcile US-source income for LLCs.
        * **Deadline:** Check filings before Jan 2026.
        """)

with c_prov:
    with st.container(border=True):
        st.subheader("Novedades Provinciales (Dic 2025)")
        st.markdown("**📍 Provincia de Santa Fe**")
        st.success("""
        * **Ley Impositiva 2026:** Aprobada. Tope aumento inmobiliario 140%.
        * **IIBB:** Alícuota reducida (2.5%) para PyMEs industriales.
        """)
        st.markdown("**📍 Provincia de Tucumán**")
        st.warning("""
        * **Moratoria:** Prórroga hasta el 30/12/2025 (Dto. 3584/3). 
        * **Sellos:** Exención para contratos de alquiler de vivienda.
        """)
