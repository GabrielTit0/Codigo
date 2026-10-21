"""Genera tablas y gráficos a partir de los CSV de resumen de C++ y Python.

Lee de resultados/:
    resultados_resumen_cpp.csv       (salida del programa en C++)
    resultados_resumen_python.csv    (salida del programa en Python)
y escribe tablas y figuras en resultados/analisis/.
Ejecutar:  python analizar.py   (desde cualquier carpeta)
Requiere:  pip install -r ../requirements.txt
Si falta uno de los archivos, se analiza solo el otro.
"""
import os

import pandas as pd

import graficos
import tablas

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR_RESULTADOS = os.path.normpath(os.path.join(AQUI, "..", "resultados"))
ENTRADAS = [os.path.join(DIR_RESULTADOS, f)
            for f in ("resultados_resumen_cpp.csv", "resultados_resumen_python.csv")]
SALIDA = os.path.join(DIR_RESULTADOS, "analisis")
N_REF = 100_000          # tamaño usado para la tabla de indicadores de la guía


def main():
    existentes = [f for f in ENTRADAS if os.path.exists(f)]
    if not existentes:
        raise SystemExit("No se encontró ningún CSV de resumen en esta carpeta.")
    for f in ENTRADAS:
        print(("Usando   " if f in existentes else "Falta    ") + os.path.basename(f))
    df = pd.concat([pd.read_csv(f) for f in existentes], ignore_index=True)
    os.makedirs(SALIDA, exist_ok=True)
    n_ref = N_REF if N_REF in df.n.values else int(df.n.max())

    # ---- Tablas (CSV para hoja de cálculo + Markdown para el informe) ----
    t_peor = tablas.tabla_peor_caso(df)
    t_ind = tablas.tabla_indicadores(df, n_ref)
    t_amo = tablas.tabla_amortizacion(df)
    for nombre, t in (("tabla_peor_caso", t_peor), ("tabla_indicadores", t_ind),
                      ("tabla_amortizacion", t_amo)):
        t.to_csv(f"{SALIDA}/{nombre}.csv", index=False)
        with open(f"{SALIDA}/{nombre}.md", "w", encoding="utf-8") as f:
            f.write(tablas.a_markdown(t))
    df.to_csv(f"{SALIDA}/resumen_completo.csv", index=False)

    # ---- Gráficos ----
    graficos.fig_comparaciones(df, f"{SALIDA}/fig1_comparaciones.png")
    graficos.fig_tiempo(df, f"{SALIDA}/fig2_tiempo.png")
    graficos.fig_preparacion(df, f"{SALIDA}/fig3_preparacion.png")
    graficos.fig_amortizacion(df, n_ref, f"{SALIDA}/fig4_amortizacion.png")

    print(f"\nArchivos generados en '{SALIDA}/':")
    for nombre in sorted(os.listdir(SALIDA)):
        print("  ", nombre)
    print("\nIndicadores (n =", n_ref, "):\n")
    print(tablas.a_markdown(t_ind))


if __name__ == "__main__":
    main()
