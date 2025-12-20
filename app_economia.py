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
