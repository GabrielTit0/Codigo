"""EXP-AED-002: búsqueda lineal vs. binaria sobre CustomerID (Online Retail).
Ejecutar:  python main.py          (desde cualquier carpeta)
Requiere:  datos/datos.csv (generado con datos/convertir_xlsx.py). No necesita pandas.
Anote en el informe la versión de Python (python --version) y el sistema operativo.
"""
import csv
import os
import random
from time import perf_counter_ns

from busqueda import (busqueda_binaria, busqueda_binaria_rapida,
                      busqueda_lineal, busqueda_lineal_rapida)
from datos import cargar_claves, mezclar_fija, tomar_muestra
from medicion import calibrar_k, resumir, tiempo_bloque

TAMANOS = [100, 1_000, 10_000, 100_000, 500_000]
REPETICIONES = 30
CALENTAMIENTO = 3          # bloques de calentamiento (no se registran)
DIR_SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados")

# nombre, ¿requiere datos ordenados?, versión con contador, versión rápida
ALGORITMOS = [
    ("lineal", False, busqueda_lineal, busqueda_lineal_rapida),
    ("binaria", True, busqueda_binaria, busqueda_binaria_rapida),
]


def main():
    # ---- 1. Carga (FUERA de toda medición) ----
    todos = mezclar_fija(cargar_claves())
    print(f"Filas cargadas: {len(todos)}")

    os.makedirs(DIR_SALIDA, exist_ok=True)
    crudo = open(os.path.join(DIR_SALIDA, "resultados_crudos_python.csv"), "w", newline="")
    resumen = open(os.path.join(DIR_SALIDA, "resultados_resumen_python.csv"), "w", newline="")
    w_crudo, w_res = csv.writer(crudo, lineterminator="\n"), csv.writer(resumen, lineterminator="\n")
    w_crudo.writerow(["lenguaje", "n", "algoritmo", "escenario", "repeticion",
                      "comparaciones", "tiempo_ns", "llamadas_bloque"])
    w_res.writerow(["lenguaje", "n", "algoritmo", "escenario", "comparaciones",
                    "promedio_ns", "mediana_ns", "min_ns", "max_ns", "llamadas_bloque"])

    for n in TAMANOS:
        if n > len(todos):
            print(f"n={n} omitido (solo hay {len(todos)} filas)")
            continue

        # ---- 2. Misma muestra para ambos algoritmos ----
        desordenada = tomar_muestra(todos, n)

        # ---- 3. Costo de preparación: ordenar (medido aparte) ----
        # Para n pequeño se ordenan K copias seguidas (copias preparadas FUERA del cronómetro).
        k_orden = max(1, 100_000 // n)
        t_orden = []
        for r in range(REPETICIONES):
            copias = [list(desordenada) for _ in range(k_orden)]
            # Cada copia con un orden distinto (fuera del cronómetro): si todas fueran idénticas,
            # el predictor de saltos "aprendería" la secuencia y subestimaría el costo de ordenar.
            for i in range(1, k_orden):
                random.Random(r * k_orden + i).shuffle(copias[i])
            t0 = perf_counter_ns()
            for c in copias:
                c.sort()
            t1 = perf_counter_ns()
            t_orden.append((t1 - t0) / k_orden)
            if r == 0:
                ordenada = copias[0]
            w_crudo.writerow(["Python", n, "ordenamiento", "-", r + 1, 0, f"{t_orden[-1]:.2f}", k_orden])
        s = resumir(t_orden)
        w_res.writerow(["Python", n, "ordenamiento", "-", 0, f"{s['promedio']:.2f}", f"{s['mediana']:.2f}",
                        f"{s['minimo']:.2f}", f"{s['maximo']:.2f}", k_orden])

        # ---- 4. Claves objetivo (las mismas para ambos algoritmos y para C++) ----
        escenarios = [
            ("inicio", desordenada[0]),
            ("centro", desordenada[n // 2]),
            ("final", desordenada[n - 1]),
            ("ausente", -1),                    # las claves reales son >= 0
        ]

        for nombre, requiere_orden, contada, rapida in ALGORITMOS:
            datos = ordenada if requiere_orden else desordenada
            for esc, x in escenarios:
                # Comparaciones (una vez: es determinista) y verificación de correctitud
                pos, ops = contada(datos, x)
                if esc != "ausente":
                    assert pos >= 0 and datos[pos] == x, f"ERROR {nombre} n={n} {esc}"
                else:
                    assert pos == -1, f"ERROR {nombre} n={n} {esc}"

                # Calibrar el tamaño del bloque, calentar y cronometrar bloques
                k = calibrar_k(rapida, datos, x)
                for _ in range(CALENTAMIENTO):
                    tiempo_bloque(rapida, datos, x, k)
                tiempos = []
                for r in range(REPETICIONES):
                    t = tiempo_bloque(rapida, datos, x, k) / k          # ns por búsqueda
                    tiempos.append(t)
                    w_crudo.writerow(["Python", n, nombre, esc, r + 1, ops, f"{t:.2f}", k])
                s = resumir(tiempos)
                w_res.writerow(["Python", n, nombre, esc, ops, f"{s['promedio']:.2f}", f"{s['mediana']:.2f}",
                                f"{s['minimo']:.2f}", f"{s['maximo']:.2f}", k])
        print(f"n={n} listo")

    crudo.close()
    resumen.close()
    print("Generados en resultados/: resultados_crudos_python.csv y resultados_resumen_python.csv")


if __name__ == "__main__":
    main()
