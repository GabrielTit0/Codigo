"""Construcción de tablas a partir de los resúmenes de C++ y Python."""
import math

import numpy as np
import pandas as pd

ESCENARIOS = ["inicio", "centro", "final", "ausente"]


def mediana(df, lenguaje, algoritmo, escenario, n):
    """Mediana de tiempo (ns) de una combinación; NaN si no existe."""
    f = df[(df.lenguaje == lenguaje) & (df.algoritmo == algoritmo) &
           (df.escenario == escenario) & (df.n == n)]
    return f.mediana_ns.iloc[0] if len(f) else np.nan


def comparaciones(df, lenguaje, algoritmo, escenario, n):
    f = df[(df.lenguaje == lenguaje) & (df.algoritmo == algoritmo) &
           (df.escenario == escenario) & (df.n == n)]
    return f.comparaciones.iloc[0] if len(f) else np.nan


def pendiente_loglog(df, lenguaje, algoritmo, escenario, columna):
    """Pendiente de log(columna) vs log(n): ~1 = crecimiento lineal, ~0 = casi constante
    o logarítmico (log n crece mucho más lento que cualquier potencia de n)."""
    f = df[(df.lenguaje == lenguaje) & (df.algoritmo == algoritmo) & (df.escenario == escenario)]
    f = f.sort_values("n")
    return np.polyfit(np.log(f.n), np.log(f[columna]), 1)[0]


def fmt(v, decimales=0):
    """Número con separador de miles en espacio (100 000)."""
    if pd.isna(v):
        return "-"
    if decimales == 0 and abs(v) < 100 and v != round(v):
        decimales = 1                       # tiempos pequeños (decenas de ns): un decimal
    return f"{v:,.{decimales}f}".replace(",", " ")


def a_markdown(tabla):
    """DataFrame -> tabla Markdown (sin depender de 'tabulate')."""
    cols = [str(c) for c in tabla.columns]
    lineas = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, fila in tabla.iterrows():
        lineas.append("| " + " | ".join(str(v) for v in fila) + " |")
    return "\n".join(lineas) + "\n"


# ---------------------------------------------------------------------------
def tabla_peor_caso(df):
    """Comparaciones y mediana de tiempo, escenario 'ausente' (peor caso), por n."""
    filas = []
    for lang in df.lenguaje.unique():
        for n in sorted(df.n.unique()):
            filas.append({
                "Lenguaje": lang, "n": fmt(n),
                "Comp. lineal": fmt(comparaciones(df, lang, "lineal", "ausente", n)),
                "Comp. binaria": fmt(comparaciones(df, lang, "binaria", "ausente", n)),
                "Mediana lineal (ns)": fmt(mediana(df, lang, "lineal", "ausente", n)),
                "Mediana binaria (ns)": fmt(mediana(df, lang, "binaria", "ausente", n)),
                "Ordenar (ns)": fmt(mediana(df, lang, "ordenamiento", "-", n)),
            })
    return pd.DataFrame(filas)


def tabla_indicadores(df, n_ref):
    """Tabla 'Indicador | Lineal | Binaria | Interpretación' de la guía (sección 13)."""
    filas = []
    for lang in df.lenguaje.unique():
        cl = comparaciones(df, lang, "lineal", "ausente", n_ref)
        cb = comparaciones(df, lang, "binaria", "ausente", n_ref)
        tl = mediana(df, lang, "lineal", "ausente", n_ref)
        tb = mediana(df, lang, "binaria", "ausente", n_ref)
        ts = mediana(df, lang, "ordenamiento", "-", n_ref)
        pl = pendiente_loglog(df, lang, "lineal", "ausente", "mediana_ns")
        pb = pendiente_loglog(df, lang, "binaria", "ausente", "mediana_ns")
        filas += [
            {"Lenguaje": lang, "Indicador": f"Comparaciones, n={fmt(n_ref)} (ausente)",
             "Lineal": fmt(cl), "Binaria": fmt(cb),
             "Interpretación": f"La binaria hace {cl / cb:,.0f} veces menos comparaciones".replace(",", " ")},
            {"Lenguaje": lang, "Indicador": "Mediana de tiempo (ns)",
             "Lineal": fmt(tl), "Binaria": fmt(tb),
             "Interpretación": f"Cociente de tiempos: {tl / tb:,.0f}x".replace(",", " ")},
            {"Lenguaje": lang, "Indicador": "Crecimiento observado (pendiente log-log del tiempo)",
             "Lineal": f"{pl:.2f}", "Binaria": f"{pb:.2f}",
             "Interpretación": "~1 = lineal; ~0 = crece muy lento (logarítmico)"},
            {"Lenguaje": lang, "Indicador": "Costo de preparación (ns)",
             "Lineal": "0", "Binaria": fmt(ts),
             "Interpretación": f"Ordenar equivale a ~{ts / tl:.1f} búsquedas lineales"},
        ]
    return pd.DataFrame(filas)


def tabla_amortizacion(df):
    """Desafío avanzado: q* = consultas a partir de las cuales ordenar + binaria
    supera a la lineal.   lineal: q*t_lin   |   binaria: t_orden + q*t_bin   (peor caso)."""
    filas = []
    for lang in df.lenguaje.unique():
        for n in sorted(df.n.unique()):
            ts = mediana(df, lang, "ordenamiento", "-", n)
            tl = mediana(df, lang, "lineal", "ausente", n)
            tb = mediana(df, lang, "binaria", "ausente", n)
            qstar = math.ceil(ts / (tl - tb)) if tl > tb else None
            filas.append({"Lenguaje": lang, "n": fmt(n), "Ordenar (ns)": fmt(ts),
                          "Lineal por consulta (ns)": fmt(tl), "Binaria por consulta (ns)": fmt(tb),
                          "q* (consultas para amortizar)": fmt(qstar) if qstar else "nunca"})
    return pd.DataFrame(filas)
