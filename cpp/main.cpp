// EXP-AED-002: búsqueda lineal vs. binaria sobre CustomerID (Online Retail).
// Compilar (CON optimización, obligatorio para un benchmark serio) y ejecutar
// DESDE LA CARPETA cpp/ (las rutas son relativas a ella):
//     g++ -std=c++20 -O2 main.cpp -o experimento
//     ./experimento            (en PowerShell: .\experimento)
// Anote en el informe el compilador, su versión y las banderas usadas.
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <random>
#include <filesystem>
#include <fstream>
#include <string>
#include <vector>
#include "busqueda.hpp"
#include "datos.hpp"
#include "medicion.hpp"
using namespace std;

const vector<size_t> TAMANOS = {100, 1000, 10000, 100000, 500000};
const int REPETICIONES  = 30;
const int CALENTAMIENTO = 3;          // bloques de calentamiento (no se registran)

const string RUTA_DATOS = "../datos/datos.csv";
const string DIR_SALIDA = "../resultados/";

struct Algoritmo {
    string nombre;
    bool   requiereOrden;
    int  (*contada)(const vector<long long>&, long long, long long&);
    int  (*rapida)(const vector<long long>&, long long);
};

int main() {
    // ---- 1. Carga (FUERA de toda medición) ----
    vector<long long> todos = leerClaves(RUTA_DATOS);
    mezclarFija(todos);
    cout << "Filas cargadas: " << todos.size() << "\n";

    filesystem::create_directories(DIR_SALIDA);
    ofstream crudo(DIR_SALIDA + "resultados_crudos_cpp.csv");
    ofstream resumen(DIR_SALIDA + "resultados_resumen_cpp.csv");
    crudo   << fixed << setprecision(2);
    resumen << fixed << setprecision(2);
    crudo   << "lenguaje,n,algoritmo,escenario,repeticion,comparaciones,tiempo_ns,llamadas_bloque\n";
    resumen << "lenguaje,n,algoritmo,escenario,comparaciones,promedio_ns,mediana_ns,min_ns,max_ns,llamadas_bloque\n";

    const vector<Algoritmo> algoritmos = {
        {"lineal",  false, busquedaLineal,  busquedaLinealRapida},
        {"binaria", true,  busquedaBinaria, busquedaBinariaRapida},
    };

    for (size_t n : TAMANOS) {
        if (n > todos.size()) {
            cout << "n=" << n << " omitido (solo hay " << todos.size() << " filas)\n";
            continue;
        }
        // ---- 2. Misma muestra para ambos algoritmos ----
        vector<long long> desordenada = tomarMuestra(todos, n);

        // ---- 3. Costo de preparación: ordenar (medido aparte) ----
        // Para n pequeño se ordenan K copias seguidas (copias preparadas FUERA del cronómetro).
        long long Ks = max<long long>(1, 100000 / static_cast<long long>(n));
        vector<long long> ordenada;
        vector<double> tOrden;
        for (int r = 0; r < REPETICIONES; ++r) {
            vector<vector<long long>> copias(Ks, desordenada);
            // Cada copia con un orden distinto (fuera del cronómetro): si todas fueran idénticas,
            // el predictor de saltos "aprendería" la secuencia y subestimaría el costo de ordenar.
            for (long long i = 1; i < Ks; ++i) {
                mt19937 g(static_cast<unsigned>(r * Ks + i));
                shuffle(copias[i].begin(), copias[i].end(), g);
            }
            long long total = medirNs([&] { for (auto& c : copias) sort(c.begin(), c.end()); });
            tOrden.push_back(static_cast<double>(total) / Ks);
            if (r == 0) ordenada = copias[0];
        }
        for (int r = 0; r < REPETICIONES; ++r)
            crudo << "C++," << n << ",ordenamiento,-," << r + 1 << ",0," << tOrden[r] << "," << Ks << "\n";
        Resumen ro = resumir(tOrden);
        resumen << "C++," << n << ",ordenamiento,-,0," << ro.promedio << "," << ro.mediana
                << "," << ro.minimo << "," << ro.maximo << "," << Ks << "\n";

        // ---- 4. Claves objetivo (las mismas para ambos algoritmos) ----
        const vector<pair<string, long long>> escenarios = {
            {"inicio",  desordenada[0]},
            {"centro",  desordenada[n / 2]},
            {"final",   desordenada[n - 1]},
            {"ausente", -1},                     // las claves reales son >= 0
        };

        for (const auto& alg : algoritmos) {
            const vector<long long>& datos = alg.requiereOrden ? ordenada : desordenada;
            for (const auto& esc_x : escenarios) {
                const string& esc = esc_x.first;
                const long long clave = esc_x.second;

                // Comparaciones (una vez: es determinista) y verificación de correctitud
                long long ops = 0;
                int pos = alg.contada(datos, clave, ops);
                bool existe = (esc != "ausente");
                if (existe ? (pos < 0 || datos[pos] != clave) : (pos != -1)) {
                    cerr << "ERROR de correctitud: " << alg.nombre << " n=" << n << " " << esc << "\n";
                    return 1;
                }

                // Una llamada a la versión SIN contador; noOptimizar evita que el
                // compilador la elimine o la saque fuera del bucle.
                auto llamada = [&] {
                    long long x = clave;
                    noOptimizar(x);
                    long long r = alg.rapida(datos, x);
                    noOptimizar(r);
                };
                long long K = calibrarK(llamada);
                auto bloque = [&] { for (long long i = 0; i < K; ++i) llamada(); };

                for (int w = 0; w < CALENTAMIENTO; ++w) bloque();
                vector<double> tiempos;
                for (int r = 0; r < REPETICIONES; ++r) {
                    double t = static_cast<double>(medirNs(bloque)) / K;   // ns por búsqueda
                    tiempos.push_back(t);
                    crudo << "C++," << n << "," << alg.nombre << "," << esc << ","
                          << r + 1 << "," << ops << "," << t << "," << K << "\n";
                }
                Resumen s = resumir(tiempos);
                resumen << "C++," << n << "," << alg.nombre << "," << esc << "," << ops << ","
                        << s.promedio << "," << s.mediana << "," << s.minimo << "," << s.maximo
                        << "," << K << "\n";
            }
        }
        cout << "n=" << n << " listo\n";
    }
    cout << "Generados en " << DIR_SALIDA << ": resultados_crudos_cpp.csv y resultados_resumen_cpp.csv\n";
    return 0;
}
