"""Algoritmos de búsqueda (código base de la guía).

Cada uno tiene dos versiones:
  - "contada": cuenta comparaciones (respuesta primaria). NO se usa para cronometrar.
  - "rapida" : sin contador (respuesta secundaria: tiempo), para no medir la sobrecarga de `ops`.
"""


# ---------- Versiones con contador ----------
def busqueda_lineal(a, x):
    ops = 0
    for i, valor in enumerate(a):
        ops += 1
        if valor == x:
            return i, ops
    return -1, ops


def busqueda_binaria(a, x):
    izq, der, ops = 0, len(a) - 1, 0
    while izq <= der:
        medio = izq + (der - izq) // 2
        ops += 1
        if a[medio] == x:
            return medio, ops
        if a[medio] < x:
            izq = medio + 1
        else:
            der = medio - 1
    return -1, ops


# ---------- Versiones sin contador (para medir tiempo) ----------
def busqueda_lineal_rapida(a, x):
    for i, valor in enumerate(a):
        if valor == x:
            return i
    return -1


def busqueda_binaria_rapida(a, x):
    izq, der = 0, len(a) - 1
    while izq <= der:
        medio = izq + (der - izq) // 2
        if a[medio] == x:
            return medio
        if a[medio] < x:
            izq = medio + 1
        else:
            der = medio - 1
    return -1
