"""Carga de datos y construcción de la muestra reproducible."""
import csv
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(AQUI, "..", "datos", "datos.csv")
MASCARA_64 = (1 << 64) - 1


def cargar_claves():
    """Lee datos.csv (columna CustomerID) y construye una clave ÚNICA por fila:
         clave = CustomerID * 1 000 000 + número_de_fila

    Motivo: CustomerID tiene muy pocos valores distintos (~4 300). Con claves repetidas,
    la búsqueda lineal siempre hallaría la 1ª aparición y los escenarios "centro" y
    "final" no serían realmente centro ni final. Las filas sin CustomerID (~135 000)
    se codifican como 0 para conservar las 541 909 filas.
    """
    if not os.path.exists(RUTA_CSV):
        raise FileNotFoundError(
            f"No existe {os.path.normpath(RUTA_CSV)}. Ejecute antes datos/convertir_xlsx.py")
    with open(RUTA_CSV, newline="") as f:
        lector = csv.reader(f)
        next(lector)                                  # saltar encabezado
        return [int(fila[0]) * 1_000_000 + i for i, fila in enumerate(lector)]


def _splitmix64(z):
    """Mismo hash que en C++ (datos.hpp), para obtener el mismo orden."""
    z = (z + 0x9E3779B97F4A7C15) & MASCARA_64
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASCARA_64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASCARA_64
    return z ^ (z >> 31)


def mezclar_fija(claves, semilla=42):
    """Orden reproducible e idéntico al de C++: se ordena por hash(clave XOR semilla).
    (random.shuffle daría una permutación distinta a std::shuffle.)"""
    return sorted(claves, key=lambda k: (_splitmix64(k ^ semilla), k))


def tomar_muestra(todos, n):
    """Muestras anidadas: la de tamaño n es el prefijo de la misma permutación."""
    return todos[:n]
