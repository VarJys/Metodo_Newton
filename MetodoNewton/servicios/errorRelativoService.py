
def calcular_error(x_actual, x_anterior):
    """
    Calcula el error relativo porcentual entre dos iteraciones.

    Parámetros:
    x_actual (float): Valor actual
    x_anterior (float): Valor anterior

    Retorna:
    float: Error relativo en porcentaje
    """
    return abs((x_actual - x_anterior)/x_actual)*100