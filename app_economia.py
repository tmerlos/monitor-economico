# -*- coding: utf-8 -*-
import os
import re
import json
import datetime as dt
from typing import List, Dict, Any, Optional

import requests
import pandas as pd
from bs4 import BeautifulSoup

# --------------------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------------------

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

TODAY = dt.date.today()

def safe_get(url: str, params: Optional[dict] = None, headers: Optional[dict] = None, timeout: int = 30) -> requests.Response:
    resp = requests.get(url, params=params or {}, headers=headers or HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp

def parse_table_to_df(soup: BeautifulSoup, table_selector: str) -> pd.DataFrame:
    table = soup.select_one(table_selector)
    if table is None:
        return pd.DataFrame()
    rows = []
    headers = [th.get_text(strip=True) for th in table.select("thead th")] or [th.get_text(strip=True) for th in table.select("tr th")]
    for tr in table.select("tbody tr"):
        rows.append([td.get_text(strip=True) for td in tr.select("td")])
    df = pd.DataFrame(rows, columns=headers if headers else None)
    return df

# --------------------------------------------------------------------------------------
# 1) Inflación mensual y acumulada (IPC INDEC)
# --------------------------------------------------------------------------------------
# Fuentes de apoyo periodístico y compilaciones públicas que reflejan el IPC y acumulados.

def get_inflacion_mensual_2025() -> pd.DataFrame:
    """
    Obtiene inflación mensual y acumulada 2025 desde una compilación pública.
    Retorna DataFrame con columnas: Mes, Inflación mensual (%), Inflación acumulada (%).
    """
    url = "https://calcularsueldo.com.ar/inflacion/inflacion-argentina-2025"
    resp = safe_get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    # La página incluye una tabla 'Inflación INDEC por mes 2025'
    tables = soup.find_all("table")
    if not tables:
        return pd.DataFrame()
    # Intento identificar la tabla por título cercano
    df = pd.read_html(str(tables[0]))[0]
    # Normaliza nombres
    df.columns = [c.strip() for c in df.columns]
    # Renombra si corresponde
    rename_map = {
        "Mes / Año": "Mes",
        "Inflación mensual": "Inflación mensual (%)",
        "Inflación acumulada": "Inflación acumulada (%)"
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    return df

def get_inflacion_noticias_contexto() -> Dict[str, Any]:
    """Devuelve últimos titulares y datos de contexto (IPC de noviembre, acumulados, interanual)."""
    news = []
    for url in [
        "https://www.iprofesional.com/economia/419097-inflacion-indec-2025-argentina-evolucion-mes-a-mes",
        "https://tn.com.ar/economia/2025/12/11/inflacion-2025-los-datos-del-indec-mes-a-mes/"
    ]:
        try:
            resp = safe_get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.find("title").get_text(strip=True)
            news.append({"title": title, "url": url})
        except Exception:
            pass
    return {"fuentes": news}

# --------------------------------------------------------------------------------------
# 2) Tipos de cambio del día (oficial, blue, MEP, CCL, tarjeta, cripto)
# --------------------------------------------------------------------------------------

def get_tipos_de_cambio_del_dia() -> Dict[str, Any]:
    """
    Obtiene cotizaciones del día de TN (oficial BNA, blue, MEP, CCL, tarjeta, cripto).
    """
    url = "https://tn.com.ar/economia/2025/12/20/dolar-oficial-hoy-y-dolar-blue-a-cuanto-cotizan-este-sabado-20-de-diciembre/"
    resp = safe_get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    def extract(label: str) -> Optional[float]:
        m = re.search(rf"{label}\s*(Compra|)\s*\$?\s*([\d\.,]+)", text)
        if not m:
            return None
        value = m.group(2).replace(".", "").replace(",", ".")
        try:
            return float(value)
        except Exception:
            return None

    data = {
        "oficial_bna_compra": extract("Dólar oficial Compra"),
        "oficial_bna_venta": extract("Dólar oficial Venta"),
        "blue_compra": extract("Dólar blue Compra"),
        "blue_venta": extract("Dólar blue Venta"),
        "dolar_tarjeta": extract("Dólar tarjeta"),
    }

    # MEP / CCL / Cripto (valores mencionados en la nota)
    def extract_inline(label: str) -> Optional[float]:
        m = re.search(rf"{label}\s*\$?\s*([\d\.,]+)", text)
        if not m:
            return None
        value = m.group(1).replace(".", "").replace(",", ".")
        try:
            return float(value)
        except Exception:
            return None

    data.update({
        "mep": extract_inline("Dólar MEP"),
        "ccl": extract_inline("Dólar CCL"),
        "cripto": extract_inline("Dólar cripto"),
        "fecha": str(TODAY)
    })
    return data

# --------------------------------------------------------------------------------------
# 3) Dólar oficial al final de cada mes (BNA histórico)
# --------------------------------------------------------------------------------------

def get_dolar_oficial_fin_de_mes_2025() -> pd.DataFrame:
    """
    Descarga valores diarios del dólar BNA en 2025 desde un sitio con histórico
    y calcula el último valor de cada mes (venta).
    """
    url = "https://www.cotizacion-dolar.com.ar/dolar-historico-bna-2025.php"
    resp = safe_get(url)
    # La página permite seleccionar fechas; usaremos pandas.read_html para extraer tablas listadas
    dfs = pd.read_html(resp.text)
    # Algunas implementaciones listan varias tablas; intentamos consolidar por columnas esperadas
    all_df = []
    for df in dfs:
        cols = [c.lower() for c in df.columns]
        if any("fecha" in c for c in cols) and any("venta" in c for c in cols):
            all_df.append(df)
    if not all_df:
        return pd.DataFrame()
    hist = pd.concat(all_df, ignore_index=True)
    # Normaliza columnas
    hist.columns = [str(c).strip() for c in hist.columns]
    fecha_col = [c for c in hist.columns if "Fecha" in c][0]
    venta_col = [c for c in hist.columns if "Venta" in c][0]
    hist[fecha_col] = pd.to_datetime(hist[fecha_col], dayfirst=True, errors="coerce")
    hist = hist.dropna(subset=[fecha_col])
    hist["Mes"] = hist[fecha_col].dt.to_period("M").astype(str)
    # Tomar último día de cada mes
    idx = hist.groupby("Mes")[fecha_col].idxmax()
    fin_mes = hist.loc[idx, [fecha_col, "Mes", venta_col]].sort_values(fecha_col)
    fin_mes = fin_mes.rename(columns={venta_col: "Dólar oficial BNA (venta)"})
    return fin_mes.reset_index(drop=True)

# --------------------------------------------------------------------------------------
# 4) Noticias: 6 económicas y 6 impositivas del día
# --------------------------------------------------------------------------------------

def scrape_latest_news_from_portal(url: str, limit: int = 6) -> List[Dict[str, str]]:
    resp = safe_get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    items = []
    for a in soup.select("a"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if href and title and len(title) > 35 and href.startswith("http"):
            items.append({"title": title, "url": href})
        if len(items) >= limit:
            break
    return items

def get_noticias_economicas_y_impositivas(limit: int = 6) -> Dict[str, List[Dict[str, str]]]:
    economicas = scrape_latest_news_from_portal("https://www.infobae.com/economia/", limit=limit)
    # Fuentes impositivas (cambios tributarios y reforma laboral con impacto fiscal)
    impositivas = []
    for url in [
        "https://www.infobae.com/economia/2025/12/10/el-gobierno-prepara-un-proyecto-con-cambios-en-cuatro-impuestos-clave-cuales-son-y-por-que-se-adelanto/",
        "https://tn.com.ar/economia/2025/12/15/reforma-laboral-los-cambios-en-impuestos-condicionan-el-plan-fiscal-del-gobierno-y-tensan-la-meta-con-el-fmi/",
        "https://www.elliberal.com.ar/nota/66659/2025/12/ganancias-iva-e-impuestos-internos-todos-los-cambios-tributarios-que-impulsa-la-reforma-laboral"
    ]:
        try:
            resp = safe_get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.find("title").get_text(strip=True)
            impositivas.append({"title": title, "url": url})
        except Exception:
            pass
    # Si faltan noticias impositivas, completa con titulares económicos relacionados
    if len(impositivas) < limit:
        extra = scrape_latest_news_from_portal("https://www.infobae.com/economia/", limit=(limit - len(impositivas)))
        impositivas.extend(extra)
    return {"economicas": economicas[:limit], "impositivas": impositivas[:limit]}

# --------------------------------------------------------------------------------------
# 5) Tabla actual de retenciones RG 830 (ARCA)
# --------------------------------------------------------------------------------------

def get_rg_830_retenciones() -> pd.DataFrame:
    """
    Obtiene la tabla vigente de retenciones del régimen de la RG 830, según la biblioteca de ARCA.
    Nota: el documento puede estar en PDF/HTML; aquí se intenta extraer tablas HTML si están disponibles.
    """
    url = "https://biblioteca.afip.gob.ar/dcp/REAG09005740_2025_07_30"  # Sitio ARCA (AFIP biblioteca)
    resp = safe_get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    # Buscar tablas en el documento
    tables = soup.find_all("table")
    if not tables:
        # Si no hay tablas HTML, intenta detectar enlaces a PDF
        links = [a.get("href") for a in soup.select("a") if a.get("href", "").lower().endswith(".pdf")]
        if links:
            return pd.DataFrame({"Mensaje": ["La tabla principal está en PDF. Descargue y procese el PDF: " + links[0]]})
        return pd.DataFrame({"Mensaje": ["No se encontró tabla HTML en la página de la RG 830."]})
    # Tomar la primera tabla reconocible
    df = pd.read_html(str(tables[0]))[0]
    df.columns = [str(c).strip() for c in df.columns]
    return df

# --------------------------------------------------------------------------------------
# 6) Última tabla del Impuesto a las Ganancias para empresas (Personas jurídicas, ARCA)
# --------------------------------------------------------------------------------------

def get_ganancias_empresas_escala() -> pd.DataFrame:
    """
    Extrae la escala vigente para ejercicios iniciados a partir del 1/1/2025 del sitio de ARCA.
    """
    url = "https://www.arca.gob.ar/gananciasYBienes/ganancias/personas-juridicas/determinacion/escala.asp"
    resp = safe_get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    # Buscar bloque/tabla asociado a "Para ejercicios fiscales iniciados a partir del 1º de enero de 2025"
    text = soup.get_text("\n", strip=True)
    # Extraer tablas HTML
    tables = soup.find_all("table")
    dfs = [pd.read_html(str(t))[0] for t in tables] if tables else []
    if not dfs:
        return pd.DataFrame({"Mensaje": ["No se encontró la tabla de la escala en HTML."]})
    # Seleccionar la tabla que contenga columnas de tramos/alícuotas
    candidates = []
    for df in dfs:
        cols_lower = [str(c).lower() for c in df.columns]
        if any("ganancia" in c for c in cols_lower) or any("alícuota" in c for c in cols_lower) or any("impuesto" in c for c in cols_lower):
            candidates.append(df)
    if candidates:
        df = candidates[0]
    else:
        df = dfs[0]
    df.columns = [str(c).strip() for c in df.columns]
    return df

# --------------------------------------------------------------------------------------
# Runner principal
# --------------------------------------------------------------------------------------

def main() -> Dict[str, Any]:
    out: Dict[str, Any] = {}

    # Inflación
    out["inflacion_2025"] = get_inflacion_mensual_2025().to_dict(orient="records")
    out["inflacion_contexto_fuentes"] = get_inflacion_noticias_contexto()

    # Tipos de cambio del día
    out["tipos_de_cambio_hoy"] = get_tipos_de_cambio_del_dia()

    # Dólar oficial fin de mes 2025
    fin_mes = get_dolar_oficial_fin_de_mes_2025()
    out["dolar_oficial_fin_de_mes_2025"] = fin_mes.to_dict(orient="records")

    # Noticias
    noticias = get_noticias_economicas_y_impositivas(limit=6)
    out["noticias_economicas"] = noticias["economicas"]
    out["noticias_impositivas"] = noticias["impositivas"]

    # RG 830 retenciones
    rg830 = get_rg_830_retenciones()
    out["rg830_retenciones"] = rg830.to_dict(orient="records")

    # Ganancias empresas (escala)
    escala = get_ganancias_empresas_escala()
    out["ganancias_empresas_escala"] = escala.to_dict(orient="records")

    return out

if __name__ == "__main__":
    data = main()
    print(json.dumps(data, ensure_ascii=False, indent=2))
