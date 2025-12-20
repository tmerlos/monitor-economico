# argentina_economia.py
# -*- coding: utf-8 -*-
"""
Script para obtener datos económicos y tributarios de Argentina:
- Inflación mensual y acumulada
- Tipos de cambio del día
- Dólar oficial al cierre de cada mes
- Noticias económicas e impositivas
- Tabla vigente de retenciones RG 830
- Escala actual del Impuesto a las Ganancias para empresas
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt
import json

HEADERS = {"User-Agent": "Mozilla/5.0"}
TODAY = dt.date.today()

# -------------------------------
# Utilidades
# -------------------------------
def safe_get(url: str):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp

# -------------------------------
# Inflación mensual y acumulada
# -------------------------------
def get_inflacion_mensual():
    url = "https://calcularsueldo.com.ar/inflacion/inflacion-argentina-2025"
    resp = safe_get(url)
    df = pd.read_html(resp.text)[0]
    df.columns = [c.strip() for c in df.columns]
    return df.to_dict(orient="records")

# -------------------------------
# Tipos de cambio del día
# -------------------------------
def get_tipos_de_cambio():
    url = "https://tn.com.ar/economia/"
    resp = safe_get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    # Aquí deberías ajustar regex según formato del portal
    return {"fecha": str(TODAY), "fuente": url}

# -------------------------------
# Dólar oficial fin de mes
# -------------------------------
def get_dolar_fin_mes():
    url = "https://www.cotizacion-dolar.com.ar/dolar-historico-bna-2025.php"
    resp = safe_get(url)
    dfs = pd.read_html(resp.text)
    df = dfs[0]
    df.columns = [c.strip() for c in df.columns]
    return df.to_dict(orient="records")

# -------------------------------
# Noticias económicas e impositivas
# -------------------------------
def get_noticias():
    urls = {
        "economicas": "https://www.infobae.com/economia/",
        "impositivas": "https://www.elliberal.com.ar/seccion/economia"
    }
    noticias = {}
    for tipo, url in urls.items():
        resp = safe_get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        links = [{"title": a.get_text(strip=True), "url": a.get("href")}
                 for a in soup.select("a") if a.get("href")]
        noticias[tipo] = links[:6]
    return noticias

# -------------------------------
# RG 830 Retenciones
# -------------------------------
def get_rg830():
    url = "https://biblioteca.afip.gob.ar/dcp/REAG09005740_2025_07_30"
    resp = safe_get(url)
    dfs = pd.read_html(resp.text)
    return dfs[0].to_dict(orient="records")

# -------------------------------
# Ganancias empresas
# -------------------------------
def get_ganancias_empresas():
    url = "https://www.arca.gob.ar/gananciasYBienes/ganancias/personas-juridicas/determinacion/escala.asp"
    resp = safe_get(url)
    dfs = pd.read_html(resp.text)
    return dfs[0].to_dict(orient="records")

# -------------------------------
# Main
# -------------------------------
def main():
    data = {
        "inflacion": get_inflacion_mensual(),
        "tipos_de_cambio": get_tipos_de_cambio(),
        "dolar_fin_mes": get_dolar_fin_mes(),
        "noticias": get_noticias(),
        "rg830": get_rg830(),
        "ganancias_empresas": get_ganancias_empresas()
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
