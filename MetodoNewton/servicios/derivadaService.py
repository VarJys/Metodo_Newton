# Librerías necesarias para cálculos simbólicos, numéricos, visualización e interfaces
import traduccion.traduccion as tr
import sympy as sp


def obtener_derivada(funcion):
    """
    Obtiene la derivada  de una función dada como string.

    Parámetros:
    funcion (str): Función en formato string, por ejemplo 'x**3 - x - 2'

    Retorna:
    sympy.Expr: Derivada simbólica de la función
    """
    x = sp.Symbol('x')  # define la variable que vas a usar.
    # convierte el string en función simbólica usando x
    f = tr.traducir_expresion(funcion)
    return sp.diff(f, x)
