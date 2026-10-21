# Análisis teórico previo — Fase B

## 1. Tamaño de entrada y operación dominante

### ¿Qué representa `n`?

En este problema, `n` representa la cantidad de elementos de la colección sobre la cual se realiza la búsqueda. Por ejemplo, si se construye una muestra con 100 000 valores de `CustomerID`, entonces:

$$
n=100\,000
$$

El valor de `n` no representa el número total de columnas, transacciones consultadas ni repeticiones del experimento. Representa únicamente el número de claves disponibles en la estructura que recibe el algoritmo. Para comparar correctamente ambos algoritmos, la búsqueda lineal y la binaria deben utilizar la misma cantidad de elementos y las mismas claves, con la diferencia de que la búsqueda binaria trabaja sobre una copia ordenada. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

### Operación dominante

La operación dominante será la comparación entre un elemento de la colección y la clave buscada. En la búsqueda lineal, se cuenta la comparación:

```python
valor == x
```

En la búsqueda binaria, se cuenta principalmente la evaluación de:

```python
a[medio] == x
```

y, cuando la igualdad es falsa, también la comparación que decide si se continúa hacia la izquierda o hacia la derecha:

```python
a[medio] < x
```

Sin embargo, el código base de la guía incrementa `ops` una vez por cada elemento revisado en la búsqueda lineal o por cada posición intermedia examinada en la búsqueda binaria. Por ello, en el experimento `ops` representa una unidad de trabajo comparable, denominada aquí **iteración de búsqueda**. El conteo de operaciones es más adecuado que el tiempo aislado para estudiar la complejidad, porque el tiempo depende adicionalmente del lenguaje, el hardware, la memoria y el sistema operativo. [Guía de práctica; Black, 2020; Cormen et al., 2022]

## 2. Búsqueda lineal

### Conteo de operaciones en el peor caso y función `T(n)`

La búsqueda lineal recorre los elementos desde la primera posición hasta encontrar el objetivo. En el peor caso, el objetivo está en la última posición o no pertenece a la colección. En ambas situaciones se revisan los `n` elementos.

Por tanto, si se cuenta una operación por cada elemento revisado:

$$
T_{\text{lineal}}(n)=n
$$

En el código de la guía, esto se observa en:

```python
for i, valor in enumerate(a):
    ops += 1
    if valor == x:
        return i, ops
```

Cuando la clave está ausente, el ciclo se ejecuta exactamente `n` veces. Cuando la clave está en la última posición, también se ejecuta `n` veces. Si se contabilizaran además el incremento del índice, la condición del ciclo y otras operaciones auxiliares, la función tendría la forma:

$$
T(n)=an+b
$$

donde `a > 0` y `b` son constantes independientes de `n`. Esta expresión sigue teniendo crecimiento lineal. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

### Cota superior `O(n)`

Para demostrar que:

$$
T(n)\in O(n)
$$

se requiere encontrar constantes positivas `c` y `n_0` tales que:

$$
T(n)\leq c\,n
$$

para todo `n >= n_0`.

Usando el modelo simplificado del contador de operaciones:

$$
T(n)=n
$$

se puede escoger:

$$
c=1,\qquad n_0=1
$$

Entonces:

$$
T(n)=n\leq 1\cdot n
$$

para todo `n >= 1`. Por consiguiente:

$$
T(n)\in O(n)
$$

Si se utilizara una función más completa `T(n)=an+b`, también existirían constantes `c` y `n_0` adecuadas. Por ejemplo, para `n >= b/a`, se puede escoger una constante `c` suficientemente grande para que `an+b <= cn`. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

### Cota inferior `Ω(n)`

Para demostrar que:

$$
T(n)\in \Omega(n)
$$

se requiere que existan constantes positivas `c` y `n_0` tales que:

$$
T(n)\geq c\,n
$$

para todo `n >= n_0`.

En el peor caso de la búsqueda lineal:

$$
T(n)=n
$$

Por tanto, se puede escoger:

$$
c=1,\qquad n_0=1
$$

y se cumple:

$$
T(n)=n\geq 1\cdot n
$$

Así:

$$
T(n)\in \Omega(n)
$$

Esta afirmación describe una cota inferior para el escenario analizado, pero no significa que todas las búsquedas lineales necesiten `n` comparaciones. Si el objetivo aparece en la primera posición, solamente se realiza una comparación. [Guía de práctica; Cormen et al., 2022; Black, 2020]

### Cota ajustada `Θ(n)`

Como en el peor caso se cumplen simultáneamente:

$$
T(n)\in O(n)
$$

y:

$$
T(n)\in \Omega(n)
$$

se concluye que:

$$
T(n)\in \Theta(n)
$$

La búsqueda lineal tiene, por tanto, crecimiento lineal en el peor caso. Para la versión simplificada `T(n)=n`, se pueden usar las mismas constantes:

$$
c_1=1,\qquad c_2=1,\qquad n_0=1
$$

y se cumple:

$$
c_1n\leq T(n)\leq c_2n
$$

Es decir:

$$
1\cdot n\leq n\leq1\cdot n
$$

La notación `Θ(n)` expresa que el número de operaciones crece proporcionalmente a `n`, ignorando factores constantes y términos de orden inferior. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

### Mejor caso

El mejor caso ocurre cuando el objetivo se encuentra en la primera posición. El algoritmo realiza una sola comparación:

$$
T_{\text{mejor}}(n)=1
$$

Por tanto:

$$
T_{\text{mejor}}(n)\in O(1),\qquad
T_{\text{mejor}}(n)\in \Omega(1),\qquad
T_{\text{mejor}}(n)\in \Theta(1)
$$

Aunque la colección aumente, el algoritmo termina inmediatamente si la clave buscada permanece en la primera posición. [Guía de práctica; Cormen et al., 2022; Black, 2020]

### Peor caso

El peor caso ocurre cuando:

- El objetivo se encuentra en la última posición; o
- El objetivo no está presente.

En ambos casos se inspeccionan los `n` elementos:

$$
T_{\text{peor}}(n)=n
$$

Por ello:

$$
T_{\text{peor}}(n)\in \Theta(n)
$$

Este es el escenario más importante para estudiar la escalabilidad de la búsqueda lineal, porque cada incremento de `n` puede producir un incremento proporcional en el número de comparaciones. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

### Caso promedio y supuestos probabilísticos

Para calcular un promedio es necesario especificar una distribución de entradas. Si se supone que el objetivo está presente y tiene la misma probabilidad de encontrarse en cualquiera de las `n` posiciones, el número esperado de comparaciones es:

$$
E[T(n)]
=
\frac{1+2+3+\cdots+n}{n}
$$

Como:

$$
1+2+\cdots+n=\frac{n(n+1)}{2}
$$

se obtiene:

$$
E[T(n)]
=
\frac{n+1}{2}
$$

Por tanto:

$$
E[T(n)]\in\Theta(n)
$$

Este resultado requiere suponer que todas las posiciones son igualmente probables. Si la búsqueda puede ser infructuosa, también debe declararse la probabilidad de que la clave esté ausente. Por ejemplo, si la clave está ausente con probabilidad `p` y, cuando está presente, se distribuye uniformemente, entonces:

$$
E[T(n)]
=
 p\,n+(1-p)\frac{n+1}{2}
$$

Mientras `p` sea una constante independiente de `n`, el crecimiento promedio continúa siendo:

$$
\Theta(n)
$$

Sin estos supuestos, no es correcto presentar un único promedio teórico universal. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

## 3. Búsqueda binaria

### Recurrencia del peor caso

La búsqueda binaria requiere que la colección esté ordenada. En cada iteración se examina el elemento central y se descarta aproximadamente la mitad de los elementos restantes.

Sea `B(n)` el número máximo de iteraciones para una colección de `n` elementos. Después de examinar el elemento central, el mayor subproblema restante tiene aproximadamente:

$$
\left\lceil\frac{n-1}{2}\right\rceil
$$

elementos. Por tanto, una recurrencia adecuada para el peor caso es:

$$
B(n)
=
B\left(\left\lceil\frac{n-1}{2}\right\rceil\right)+1
$$

con condición inicial:

$$
B(0)=0
$$

De manera simplificada, también puede escribirse como:

$$
B(n)=B\left(\frac{n}{2}\right)+1
$$

La recurrencia muestra que el problema se reduce a la mitad en cada paso, a diferencia de la búsqueda lineal, que elimina solamente un elemento por iteración. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

### Solución de la recurrencia

Aplicando expansión sucesiva:

$$
B(n)=B\left(\frac{n}{2}\right)+1
$$

$$
B(n)=B\left(\frac{n}{4}\right)+2
$$

$$
B(n)=B\left(\frac{n}{8}\right)+3
$$

Después de `k` pasos:

$$
B(n)=B\left(\frac{n}{2^k}\right)+k
$$

El proceso termina cuando:

$$
\frac{n}{2^k}\leq1
$$

Esto ocurre cuando:

$$
2^k\geq n
$$

Por lo tanto:

$$
k\geq\log_2 n
$$

La solución asintótica es:

$$
B(n)\in\Theta(\log n)
$$

La base del logaritmo no modifica la clasificación asintótica, porque cambiar de base solo introduce un factor constante. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

### Por qué la división a la mitad produce crecimiento logarítmico

Cada comparación de la búsqueda binaria reduce el intervalo de búsqueda aproximadamente a la mitad. Después de una iteración queda aproximadamente `n/2` elementos; después de dos, `n/4`; después de tres, `n/8`; y después de `k` iteraciones:

$$
\frac{n}{2^k}
$$

Cuando el tamaño restante llega a uno, se cumple:

$$
\frac{n}{2^k}\leq1
$$

La cantidad de divisiones entre dos necesarias para transformar `n` en un valor constante es proporcional a `log_2 n`. Por ello, duplicar el tamaño de entrada incrementa el número de iteraciones aproximadamente en una unidad, mientras que en la búsqueda lineal duplicar `n` puede duplicar el número de comparaciones. [Guía de práctica; Cormen et al., 2022; Black, 2020]

### Número máximo de comparaciones para el código de la guía

El código de la guía es:

```python
def busqueda_binaria(a, x):
    izq, der, ops = 0, len(a)-1, 0
    while izq <= der:
        medio = izq + (der-izq)//2
        ops += 1
        if a[medio] == x:
            return medio, ops
        if a[medio] < x:
            izq = medio + 1
        else:
            der = medio - 1
    return -1, ops
```

En este código, `ops` se incrementa una vez por cada posición central evaluada. Por ello, `ops` cuenta iteraciones o elementos centrales examinados, no todas las comparaciones booleanas ejecutadas dentro de la iteración.

Para el código exacto, el número máximo de iteraciones en el peor caso es:

$$
B_{\max}(n)=\lfloor\log_2 n\rfloor+1
$$

para `n >= 1`.

Por ejemplo:

| `n` | Máximo de iteraciones según el código |
|---:|---:|
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 3 |
| 5 | 3 |
| 8 | 4 |
| 16 | 5 |

Por tanto, entre las dos expresiones propuestas, la respuesta exacta para este contador es:

$$
\boxed{\lfloor\log_2 n\rfloor+1}
$$

No es exactamente `ceil(log_2 n)`. La diferencia aparece especialmente cuando `n` es una potencia de dos. Por ejemplo, para `n=4`:

$$
\lceil\log_2 4\rceil=2
$$

pero el código puede necesitar tres iteraciones en el peor caso:

$$
\lfloor\log_2 4\rfloor+1=3
$$

También puede expresarse de forma equivalente como:

$$
B_{\max}(n)=\lceil\log_2(n+1)\rceil
$$

para `n >= 1`. Si se contaran individualmente la comparación de igualdad y la comparación de orden, el número total de comparaciones primitivas sería distinto; la fórmula anterior corresponde específicamente al contador `ops` de la guía. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

## 4. Cotas asintóticas frente a casos

### ¿Por qué `Ω` no es sinónimo automático de “mejor caso”?

`Ω` describe una cota inferior asintótica de una función de costo. No identifica por sí sola el escenario mejor, promedio o peor. El significado depende de la función que se esté analizando.

Por ejemplo, para la búsqueda lineal en el peor caso:

$$
T_{\text{peor}}(n)=n
$$

y se cumple:

$$
T_{\text{peor}}(n)\in\Omega(n)
$$

Sin embargo, este resultado pertenece al peor caso, no al mejor caso.

Por otro lado, para el mejor caso de la misma búsqueda:

$$
T_{\text{mejor}}(n)=1
$$

y se cumple:

$$
T_{\text{mejor}}(n)\in\Omega(1)
$$

Así, `Ω` significa “crece al menos tan rápido como”, bajo la función y el escenario especificados. La expresión “mejor caso” describe una selección de entradas; la notación `Ω` describe una relación asintótica entre funciones. Son conceptos diferentes. [Guía de práctica; Cormen et al., 2022; Black, 2020]

Un ejemplo adicional es la búsqueda binaria. En el peor caso:

$$
T_{\text{peor}}(n)\in\Omega(\log n)
$$

mientras que en el mejor caso:

$$
T_{\text{mejor}}(n)\in\Omega(1)
$$

Por tanto, no sería correcto afirmar simplemente que “`Ω` representa el mejor caso”. Lo correcto es indicar qué función se está acotando, sobre qué conjunto de entradas y en qué escenario. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

## 5. Predicciones

### Predicción para `n` frente a comparaciones

Para la búsqueda lineal se espera una relación aproximadamente lineal entre `n` y el número de comparaciones:

$$
C_{\text{lineal}}(n)\approx n
$$

Las diferencias entre escenarios serán evidentes:

- **Inicio:** aproximadamente 1 comparación.
- **Centro:** aproximadamente `n/2` comparaciones.
- **Final:** aproximadamente `n` comparaciones.
- **Ausente:** exactamente `n` comparaciones.

En el escenario promedio, suponiendo que el objetivo está uniformemente distribuido entre las posiciones, se espera aproximadamente:

$$
\frac{n+1}{2}
$$

comparaciones.

Para la búsqueda binaria se espera un crecimiento logarítmico:

$$
C_{\text{binaria}}(n)\approx \lfloor\log_2 n\rfloor+1
$$

La diferencia entre los escenarios debería ser mucho menor que en la búsqueda lineal, aunque el objetivo puede encontrarse inmediatamente en el centro o requerir varias iteraciones si se encuentra en otra posición o está ausente. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

Por ejemplo, tomando el peor caso aproximado:

| `n` | Búsqueda lineal | Búsqueda binaria |
|---:|---:|---:|
| 100 | 100 | 7 |
| 1 000 | 1 000 | 10 |
| 10 000 | 10 000 | 14 |
| 100 000 | 100 000 | 17 |
| 500 000 | 500 000 | 19 |

Los valores de la búsqueda binaria corresponden a:

$$
\lfloor\log_2 n\rfloor+1
$$

y se presentan como predicción del contador `ops`. Los resultados reales pueden ser menores en escenarios favorables. [Guía de práctica; Cormen et al., 2022; Black, 2020]

### Predicción para `n` frente a tiempo

El tiempo de la búsqueda lineal debería aumentar aproximadamente de forma lineal con `n`, especialmente en los escenarios final y ausente. El tiempo de la búsqueda binaria debería aumentar mucho más lentamente, debido a su crecimiento logarítmico.

Sin embargo, las curvas de tiempo no necesariamente serán perfectamente lineales o logarítmicas. Pueden observarse variaciones debido a:

- Resolución del cronómetro.
- Interrupciones del sistema operativo.
- Estado de la caché.
- Gestión de memoria.
- Calentamiento del entorno de ejecución.
- Optimización del compilador.
- Sobrecarga del intérprete de Python.
- Costo de realizar una llamada de función.
- Acceso a memoria y representación de los datos.

Por esta razón, la cantidad de comparaciones debe utilizarse como evidencia principal de complejidad, mientras que el tiempo debe interpretarse como una medida del comportamiento observado en una configuración concreta. [Guía de práctica; Black, 2020; Cormen et al., 2022]

Además, para la búsqueda binaria debe separarse el costo de ordenar la colección. El costo total puede representarse como:

$$
T_{\text{total}}=
T_{\text{ordenamiento}}+
q\cdot T_{\text{búsqueda binaria}}
$$

donde `q` es el número de consultas. Si se realiza una sola consulta, el ordenamiento puede hacer que la solución completa sea menos conveniente. Si se realizan muchas consultas, el costo de ordenar puede amortizarse y la búsqueda binaria puede resultar más eficiente en el costo total. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

### Diferencias esperadas entre Python y C++

Se espera que C++ presente tiempos menores que Python en esta configuración concreta, especialmente cuando `n` es grande y se ejecutan muchas operaciones. C++ se compila normalmente a código nativo, mientras que Python introduce sobrecarga del intérprete, de los objetos dinámicos, de la iteración y de la llamada a funciones.

Sin embargo, esta predicción no significa que C++ tenga una mejor complejidad asintótica. Si ambos programas implementan correctamente la misma búsqueda, ambos deben presentar las mismas clases de complejidad:

$$
\text{Búsqueda lineal: }\Theta(n)
$$

$$
\text{Búsqueda binaria: }\Theta(\log n)
$$

La diferencia esperada entre lenguajes corresponde principalmente a constantes de ejecución y características de implementación. [Guía de práctica; Python Software Foundation, 2026; cppreference.com, 2026]

También se espera que la diferencia temporal entre Python y C++ pueda ser menos clara para tamaños pequeños. Cuando una búsqueda tarda un tiempo cercano a la resolución del cronómetro, la sobrecarga de medición puede ser comparable al costo de la operación. Por eso deben analizarse medianas, repeticiones y tendencias generales, en lugar de interpretar una medición individual como resultado definitivo. [Guía de práctica; Python Software Foundation, 2026; cppreference.com, 2026]

En conclusión, la predicción principal es que el número de comparaciones mostrará con claridad la ventaja de escalabilidad de la búsqueda binaria frente a la búsqueda lineal. Los tiempos deberían seguir una tendencia semejante, pero estarán afectados por factores de implementación y del entorno experimental. La comparación entre Python y C++ debe limitarse a la máquina, versiones, compiladores, configuraciones y código utilizados, sin afirmar que un lenguaje es universalmente mejor que el otro. [Guía de práctica; Cormen et al., 2022; Skiena, 2020]

## Referencias utilizadas

Black, P. E. (2020). *DADS: The on-line dictionary of algorithms and data structures*. National Institute of Standards and Technology. https://www.nist.gov/publications/dads-line-dictionary-algorithms-and-data-structures

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press. https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/

cppreference.com. (2026). *Date and time utilities*. https://en.cppreference.com/w/cpp/chrono

Python Software Foundation. (2026). *time — Time access and conversions*. Python documentation. https://docs.python.org/3/library/time.html

Skiena, S. S. (2020). *The algorithm design manual* (3rd ed.). Springer. https://link.springer.com/book/10.1007/978-3-030-54256-7
