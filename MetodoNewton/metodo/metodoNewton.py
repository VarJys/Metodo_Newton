
import servicios.evaluarFuncionService as ev
import servicios.derivadaService as d
import servicios.errorRelativoService as e


def newton_raphson(funcion, x0, tolerancia=0.001, max_iter=50):
    """
    Aplica el método de Newton-Raphson para encontrar la raíz de una función.

    Parámetros:
    funcion (str): Función como string
    x0 (float): Valor inicial
    tolerancia (float): Criterio de convergencia
    max_iter (int): Número máximo de iteraciones

    Retorna:
    tuple: (raíz aproximada, lista de iteraciones, lista de errores)
    """
    deriv = d.obtener_derivada(funcion)
    iteraciones = []
    errores = []
    raiz = x0

    for i in range(max_iter):
        fx, fpx = ev.evaluar_funcion(funcion, deriv, raiz)
        if fx is None or fpx is None or fpx == 0:
            return None, iteraciones, errores
        x1 = raiz - fx/fpx  # formula del metodo
        error = e.calcular_error(x1, raiz)
        iteraciones.append(x1)
        errores.append(error)
        if error < tolerancia:
            return x1, iteraciones, errores
        raiz = x1

    return raiz, iteraciones, errores
