"""Gráficos del experimento EXP-AED-002 (guardados como PNG)."""
import matplotlib
matplotlib.use("Agg")                      # sin ventana: solo guarda archivos
import matplotlib.pyplot as plt
import numpy as np

from tablas import ESCENARIOS, mediana

COLOR = {"lineal": "tab:red", "binaria": "tab:blue", "ordenamiento": "tab:green"}
ESTILO = {"C++": "-", "Python": "--"}
MARCA = {"C++": "o", "Python": "s"}


def _serie(df, lenguaje, algoritmo, escenario):
    f = df[(df.lenguaje == lenguaje) & (df.algoritmo == algoritmo) &
           (df.escenario == escenario)].sort_values("n")
    return f


def fig_comparaciones(df, ruta):
    """n vs. comparaciones (respuesta primaria). Son iguales en ambos lenguajes."""
    lang = df.lenguaje.iloc[0]
    fig, ejes = plt.subplots(2, 2, figsize=(10, 7), sharex=True)
    for ax, esc in zip(ejes.flat, ESCENARIOS):
        for alg in ("lineal", "binaria"):
            s = _serie(df, lang, alg, esc)
            ax.plot(s.n, s.comparaciones, marker="o", color=COLOR[alg], label=alg)
        n = np.array(sorted(df.n.unique()), dtype=float)
        ax.plot(n, n, ":", color="gray", label="referencia n")
        ax.plot(n, np.floor(np.log2(n)) + 1, "-.", color="gray", label="referencia ⌊log₂n⌋+1")
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(f"Escenario: {esc}")
        ax.grid(True, which="both", alpha=0.3)
    for ax in ejes[1]: ax.set_xlabel("n (tamaño de la muestra)")
    for ax in ejes[:, 0]: ax.set_ylabel("Comparaciones")
    ejes[0, 0].legend(fontsize=8)
    fig.suptitle("Comparaciones vs. n (escala log-log)")
    fig.tight_layout(); fig.savefig(ruta, dpi=150); plt.close(fig)


def fig_tiempo(df, ruta):
    """n vs. tiempo (respuesta secundaria): mediana y banda mín–máx."""
    fig, ejes = plt.subplots(2, 2, figsize=(10, 7), sharex=True)
    for ax, esc in zip(ejes.flat, ESCENARIOS):
        for lang in df.lenguaje.unique():
            for alg in ("lineal", "binaria"):
                s = _serie(df, lang, alg, esc)
                ax.plot(s.n, s.mediana_ns, ESTILO[lang], marker=MARCA[lang], ms=4,
                        color=COLOR[alg], label=f"{alg} ({lang})")
                ax.fill_between(s.n, np.maximum(s.min_ns, 1), s.max_ns, color=COLOR[alg], alpha=0.12)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(f"Escenario: {esc}")
        ax.grid(True, which="both", alpha=0.3)
    for ax in ejes[1]: ax.set_xlabel("n (tamaño de la muestra)")
    for ax in ejes[:, 0]: ax.set_ylabel("Tiempo por búsqueda (ns)")
    # Leyenda común fuera de los paneles (dentro tapaba las líneas del panel "inicio")
    handles, etiquetas = ejes[0, 0].get_legend_handles_labels()
    fig.legend(handles, etiquetas, loc="lower center", ncol=4, fontsize=9, frameon=False)
    fig.suptitle("Tiempo por búsqueda vs. n: mediana y banda mín–máx (log-log)")
    fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(ruta, dpi=150); plt.close(fig)


def fig_preparacion(df, ruta):
    """Costo de ordenar vs. costo de una búsqueda (peor caso)."""
    langs = list(df.lenguaje.unique())
    fig, ejes = plt.subplots(1, len(langs), figsize=(5.5 * len(langs), 4.5), squeeze=False)
    for ax, lang in zip(ejes[0], langs):
        for alg, esc, etq in (("ordenamiento", "-", "ordenar (preparación)"),
                              ("lineal", "ausente", "búsqueda lineal"),
                              ("binaria", "ausente", "búsqueda binaria")):
            s = _serie(df, lang, alg, esc)
            ax.plot(s.n, s.mediana_ns, marker="o", color=COLOR[alg], label=etq)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(lang); ax.set_xlabel("n"); ax.set_ylabel("Mediana de tiempo por operación (ns)")
        ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)
    fig.suptitle("Costo de preparación vs. costo de una consulta (peor caso)")
    fig.tight_layout(); fig.savefig(ruta, dpi=150); plt.close(fig)


def fig_amortizacion(df, n_ref, ruta):
    """Costo total para q consultas: lineal = q·t_lin ; binaria = t_orden + q·t_bin."""
    langs = list(df.lenguaje.unique())
    fig, ejes = plt.subplots(1, len(langs), figsize=(5.5 * len(langs), 4.5), squeeze=False)
    q = np.logspace(0, 6, 200)
    for ax, lang in zip(ejes[0], langs):
        ts = mediana(df, lang, "ordenamiento", "-", n_ref)
        tl = mediana(df, lang, "lineal", "ausente", n_ref)
        tb = mediana(df, lang, "binaria", "ausente", n_ref)
        ax.plot(q, q * tl, color=COLOR["lineal"], label="lineal: q·t_lineal")
        ax.plot(q, ts + q * tb, color=COLOR["binaria"], label="ordenar + binaria")
        if tl > tb:
            qs = ts / (tl - tb)
            ax.axvline(qs, color="gray", ls=":")
            ax.annotate(f"q* ≈ {qs:,.0f}".replace(",", " "), (qs, ts), textcoords="offset points",
                        xytext=(8, -14), fontsize=9)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(f"{lang}, n = {n_ref:,}".replace(",", " "))
        ax.set_xlabel("q (número de consultas)"); ax.set_ylabel("Costo total (ns)")
        ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)
    fig.suptitle("Amortización del ordenamiento (peor caso por consulta)")
    fig.tight_layout(); fig.savefig(ruta, dpi=150); plt.close(fig)
