"""Cronómetro por BLOQUES y estadísticos.

Problema: el reloj de algunos sistemas (p. ej. Windows) avanza en pasos de ~100 ns y una
búsqueda binaria dura cientos o pocos miles de ns. Solución: cronometrar K llamadas seguidas
y dividir entre K, con K elegido para que el bloque dure >= ~200 000 ns (error de reloj < 0,1 %).
Nota: el bucle `for _ in range(k)` añade unos pocos ns por llamada (sobrecarga constante, igual
para ambos algoritmos); es despreciable frente a búsquedas de cientos de ns o más.
"""
import statistics
from time import perf_counter_ns


def tiempo_bloque(f, a, x, k):
    """Duración TOTAL (ns) de k llamadas seguidas a f(a, x)."""
    t0 = perf_counter_ns()
    for _ in range(k):
        f(a, x)
    return perf_counter_ns() - t0


def calibrar_k(f, a, x, objetivo_ns=200_000, max_k=1 << 20):
    """Menor potencia de 2 tal que k llamadas duren al menos objetivo_ns."""
    k = 1
    while k < max_k and tiempo_bloque(f, a, x, k) < objetivo_ns:
        k *= 2
    return k


def resumir(tiempos):
    return {
        "promedio": statistics.mean(tiempos),
        "mediana": statistics.median(tiempos),
        "minimo": min(tiempos),
        "maximo": max(tiempos),
    }
