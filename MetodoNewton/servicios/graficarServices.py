import base64
import io
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sympy as sp
import traduccion.traduccion as tr

matplotlib.use('Agg')


def graficar(funcion, iteraciones, raiz, x0):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    todos_valores = [x0] + iteraciones
    iteraciones_nums = list(range(len(todos_valores)))

    ax1.plot(iteraciones_nums, todos_valores, 'b-o', linewidth=2.5, markersize=8,
             markerfacecolor='blue', markeredgecolor='darkblue', markeredgewidth=1)

    for i, valor in enumerate(todos_valores):
        if not iteraciones:
            max_valor = valor + 1
            min_valor = valor - 1
        else:
            max_valor = max(todos_valores)
            min_valor = min(todos_valores)

        rango = max_valor - min_valor
        rango = 1 if rango == 0 else rango

        if valor > (min_valor + rango * 0.7):
            xytext = (0, -25)
            va = 'top'
        else:
            xytext = (0, 15)
            va = 'bottom'

        ax1.annotate(f'{valor:.6f}', (i, valor), textcoords="offset points", xytext=xytext,
                     ha='center', va=va, fontsize=10,
                     bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))

    if raiz is not None:
        ax1.axhline(y=raiz, color='green', linestyle='--', alpha=0.7, linewidth=1.5,
                    label=f'Raíz ≈ {raiz:.6f}')
    else:
        ax1.plot([], [], ' ', label='Raíz no encontrada')

    ax1.set_xlabel('Iteración', fontsize=12)
    ax1.set_ylabel('Valor de x', fontsize=12)
    ax1.set_title('Convergencia de las Aproximaciones',
                  fontsize=14, fontweight='bold', pad=30)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xticks(iteraciones_nums)

    if todos_valores:
        y_min = min(todos_valores)
        y_max = max(todos_valores)
        rango_y = y_max - y_min
        if rango_y == 0:
            rango_y = 1
        ax1.set_ylim(y_min - rango_y * 0.1, y_max + rango_y * 0.2)

    try:
        f = sp.lambdify(
            sp.Symbol('x'), tr.traducir_expresion(funcion), 'numpy')

        puntos_referencia = iteraciones + [raiz] if raiz is not None else iteraciones + [x0]

        margen = 2
        x_min = min(puntos_referencia) - margen
        x_max = max(puntos_referencia) + margen

        x_vals = np.linspace(x_min, x_max, 400)
        y_vals = f(x_vals)

        ax2.plot(x_vals, y_vals, 'b-', linewidth=2, label=f"f(x) = {funcion}")
        ax2.axhline(0, color="black", linewidth=1)

        if raiz is not None:
            ax2.scatter(raiz, f(raiz), color="green", s=150, marker='*',
                        label=f"Raíz ≈ {raiz:.6f}", zorder=5)

        vals_evaluar = [f(xi) for xi in iteraciones] + [0]
        ymin = min(vals_evaluar) - 1
        ymax = max(vals_evaluar) + 1
        ax2.set_ylim(ymin, ymax)

    except Exception as e:
        print(f"Error graficando función: {e}")
        ax2.text(0.5, 0.5, "Error al graficar función", ha='center')

    ax2.set_xlabel('x', fontsize=12)
    ax2.set_ylabel('f(x)', fontsize=12)
    ax2.set_title(f'Función: f(x) = {funcion}',
                  fontsize=14, fontweight='bold', pad=20)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout(pad=2.0)
    img_memory = io.BytesIO()
    plt.savefig(img_memory, format='png')
    img_memory.seek(0)
    plt.close()

    img_base64 = base64.b64encode(img_memory.getvalue()).decode('utf-8')
    return img_base64
