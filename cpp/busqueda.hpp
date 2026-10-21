#pragma once
// Algoritmos de búsqueda. Cada uno tiene dos versiones:
//  - "contada": cuenta comparaciones (respuesta primaria). NO se usa para cronometrar.
//  - "rapida" : sin contador (respuesta secundaria: tiempo), para no añadir sobrecarga.
#include <vector>
using std::vector;

// ---------- Versiones con contador (código base de la guía) ----------
inline int busquedaLineal(const vector<long long>& a, long long x, long long& ops) {
    ops = 0;
    for (size_t i = 0; i < a.size(); ++i) {
        ++ops;
        if (a[i] == x) return static_cast<int>(i);
    }
    return -1;
}

inline int busquedaBinaria(const vector<long long>& a, long long x, long long& ops) {
    int izq = 0, der = static_cast<int>(a.size()) - 1;
    ops = 0;
    while (izq <= der) {
        int medio = izq + (der - izq) / 2;
        ++ops;
        if (a[medio] == x) return medio;
        if (a[medio] < x) izq = medio + 1;
        else der = medio - 1;
    }
    return -1;
}

// ---------- Versiones sin contador (para medir tiempo) ----------
inline int busquedaLinealRapida(const vector<long long>& a, long long x) {
    for (size_t i = 0; i < a.size(); ++i)
        if (a[i] == x) return static_cast<int>(i);
    return -1;
}

inline int busquedaBinariaRapida(const vector<long long>& a, long long x) {
    int izq = 0, der = static_cast<int>(a.size()) - 1;
    while (izq <= der) {
        int medio = izq + (der - izq) / 2;
        if (a[medio] == x) return medio;
        if (a[medio] < x) izq = medio + 1;
        else der = medio - 1;
    }
    return -1;
}
