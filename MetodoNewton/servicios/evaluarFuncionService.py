import traduccion.traduccion as tr
import sympy as sp


def evaluar_funcion(funcion, derivada, valor):
    x = sp.Symbol('x')

    f = tr.traducir_expresion(funcion)
    fprima = tr.traducir_expresion(derivada)

    try:
        return float(f.subs(x, valor)), float(fprima.subs(x, valor))
    except Exception as e:
        print("Error:", e)
        return None, None
