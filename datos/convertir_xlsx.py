"""Paso previo (una sola vez): Online Retail.xlsx -> datos.csv
Ambos programas (C++ y Python) leen datos.csv; ninguno lee el .xlsx directamente.
Requiere: pip install pandas openpyxl
Uso (desde la carpeta datos/):  python convertir_xlsx.py
"""
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
df = pd.read_excel(AQUI / "Online Retail.xlsx", usecols=["CustomerID"])
# Filas sin CustomerID (~135 000) se codifican como 0 para conservar las 541 909 filas
df["CustomerID"] = df["CustomerID"].fillna(0).astype("int64")
df.to_csv(AQUI / "datos.csv", index=False)
print(f"{len(df)} filas guardadas en {AQUI / 'datos.csv'}")
