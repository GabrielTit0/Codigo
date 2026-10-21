| Lenguaje | Indicador | Lineal | Binaria | Interpretación |
|---|---|---|---|---|
| C++ | Comparaciones, n=100 000 (ausente) | 100 000 | 16 | La binaria hace 6 250 veces menos comparaciones |
| C++ | Mediana de tiempo (ns) | 31 388 | 17.1 | Cociente de tiempos: 1 837x |
| C++ | Crecimiento observado (pendiente log-log del tiempo) | 0.97 | 0.14 | ~1 = lineal; ~0 = crece muy lento (logarítmico) |
| C++ | Costo de preparación (ns) | 0 | 6 310 600 | Ordenar equivale a ~201.1 búsquedas lineales |
| Python | Comparaciones, n=100 000 (ausente) | 100 000 | 16 | La binaria hace 6 250 veces menos comparaciones |
| Python | Mediana de tiempo (ns) | 6 049 800 | 1 494 | Cociente de tiempos: 4 049x |
| Python | Crecimiento observado (pendiente log-log del tiempo) | 1.16 | 0.12 | ~1 = lineal; ~0 = crece muy lento (logarítmico) |
| Python | Costo de preparación (ns) | 0 | 28 809 000 | Ordenar equivale a ~4.8 búsquedas lineales |
