#pragma once
// Lectura de datos.csv y construcción de la muestra reproducible.
#include <algorithm>
#include <fstream>
#include <cstdint>
#include <utility>
#include <stdexcept>
#include <string>
#include <vector>
using std::pair;
using std::string;
using std::vector;

// Lee la columna CustomerID y construye una clave ÚNICA por fila:
//     clave = CustomerID * 1 000 000 + número_de_fila
// Motivo: CustomerID tiene muy pocos valores distintos (~4 300). Con claves repetidas,
// la búsqueda lineal siempre hallaría la 1ª aparición y los escenarios "centro" y
// "final" no serían realmente centro ni final. Con clave única, la posición es exacta.
inline vector<long long> leerClaves(const string& ruta) {
    std::ifstream f(ruta);
    if (!f) throw std::runtime_error("No se pudo abrir " + ruta + " (¿ejecutó convertir_xlsx.py?)");
    string linea;
    std::getline(f, linea);                       // saltar encabezado
    vector<long long> claves;
    long long fila = 0;
    while (std::getline(f, linea)) {
        if (linea.empty()) continue;
        long long cliente = std::stoll(linea);
        claves.push_back(cliente * 1'000'000 + fila);
        ++fila;
    }
    return claves;
}

// splitmix64: función hash determinista y fácil de replicar en Python.
inline uint64_t splitmix64(uint64_t z) {
    z += 0x9E3779B97F4A7C15ULL;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

// "Mezcla" reproducible: ordena las claves por hash(clave XOR semilla).
// Se usa un hash propio (y no std::shuffle) para que Python obtenga EXACTAMENTE
// el mismo orden: random.shuffle y std::shuffle producen permutaciones distintas.
// La muestra de tamaño n es el prefijo de esta permutación (muestras anidadas).
inline void mezclarFija(vector<long long>& v, uint64_t semilla = 42) {
    vector<pair<uint64_t, long long>> tmp;
    tmp.reserve(v.size());
    for (long long k : v) tmp.push_back({splitmix64(static_cast<uint64_t>(k) ^ semilla), k});
    std::sort(tmp.begin(), tmp.end());
    for (size_t i = 0; i < v.size(); ++i) v[i] = tmp[i].second;
}

inline vector<long long> tomarMuestra(const vector<long long>& todos, size_t n) {
    return vector<long long>(todos.begin(), todos.begin() + n);
}
