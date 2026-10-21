#pragma once
// Cronómetro por BLOQUES y estadísticos.
// Problema: el reloj de algunos sistemas (p. ej. Windows) avanza en pasos de ~100 ns, y una
// búsqueda binaria dura decenas de ns. Solución: cronometrar K llamadas seguidas y dividir
// entre K, con K elegido para que el bloque dure >= ~200 000 ns (error de reloj < 0,1 %).
#include <algorithm>
#include <chrono>
#include <numeric>
#include <vector>
using std::vector;

using Reloj = std::chrono::steady_clock;

// Ejecuta f() y devuelve su duración TOTAL en nanosegundos.
template <class F>
long long medirNs(F&& f) {
    auto t0 = Reloj::now();
    f();
    auto t1 = Reloj::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
}

// Impide que el compilador elimine o saque fuera del bucle una llamada "pura".
template <class T>
inline void noOptimizar(T& v) {
#if defined(__GNUC__) || defined(__clang__)
    asm volatile("" : "+r"(v) : : "memory");
#else
    volatile T copia = v;
    v = copia;
#endif
}

// Busca K (potencia de 2) tal que K llamadas a f() duren al menos objetivoNs.
template <class F>
long long calibrarK(F&& f, long long objetivoNs = 200000, long long maxK = 1LL << 22) {
    long long K = 1;
    while (K < maxK && medirNs([&] { for (long long i = 0; i < K; ++i) f(); }) < objetivoNs)
        K *= 2;
    return K;
}

struct Resumen { double promedio, mediana, minimo, maximo; };

inline Resumen resumir(vector<double> v) {   // copia: se ordena localmente
    std::sort(v.begin(), v.end());
    double prom = std::accumulate(v.begin(), v.end(), 0.0) / v.size();
    size_t m = v.size();
    double med = (m % 2) ? v[m / 2] : (v[m / 2 - 1] + v[m / 2]) / 2.0;
    return {prom, med, v.front(), v.back()};
}
