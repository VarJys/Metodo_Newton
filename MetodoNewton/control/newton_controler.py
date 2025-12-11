import sys
import os
from datetime import datetime  # ← FALTABA ESTE IMPORT

# AGREGAR LA RUTA BASE DEL PROYECTO
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import flask as f
import metodo.metodoNewton as mt
import servicios.graficarServices as gr

# IMPORTAR FUNCIONES DEL HISTORIAL
from servicios.historialService import guardar_historial, cargar_historial

# Obtener la ruta base del proyecto de manera dinámica
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'interfaz', 'templates')
static_dir = os.path.join(base_dir, 'interfaz', 'static')

app = f.Flask(
    __name__, 
    template_folder=template_dir,
    static_folder=static_dir
)

@app.route('/')
def index():
    return f.render_template('index.html')

@app.route('/Calcular', methods=['POST'])
def interfaz_newton():
    try:
        data = f.request.json
        
        funcion = data.get('funcion')
        x0 = float(data.get('valorInicial'))  # ← ERA 'valorInicial', NO 'xi'
        tolerancia = float(data.get('tolerancia'))
        
        # ---- 1. EJECUTAR MÉTODO DE NEWTON ----
        raiz, iteraciones, errores = mt.newton_raphson(funcion, x0, tolerancia)
        
        # ---- 2. PREPARAR TABLA PARA LA VISTA ----
        datos_tabla = []
        for i in range(len(iteraciones)):
            val_error = errores[i] if i < len(errores) else 0
            datos_tabla.append({
                'iteracion': i + 1,
                'x': round(iteraciones[i], 8),
                'fx': 0,  # tu método no devuelve f(x)
                'error': round(val_error, 8)
            })
        
        # ---- 3. GENERAR GRÁFICA (retorna base64) ----
        valor_raiz_json = round(raiz, 8) if raiz is not None else "No converge"
        if(valor_raiz_json!="No converge"):
            img_base64 = gr.graficar(funcion, iteraciones, raiz, x0)  # ← CAMBIÉ nombre_grafica por img_base64
        else:
            img_base64=None
        
        
        # ---- 4. GUARDAR HISTORIAL ----
        guardar_historial({
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'funcion': funcion,
            'xi': x0,  # ← CORREGIDO: era 'xi' indefinido
            'tolerancia': tolerancia,
            'resultado': valor_raiz_json,  # ← CORREGIDO: era 'raiz' sin formato
            'num_iteraciones': len(iteraciones),
            'grafica_base64': img_base64  # ← CORREGIDO: nombre correcto
        })
        
        # ---- 5. RESPUESTA JSON ----
        return f.jsonify({
            'raiz': valor_raiz_json,
            'iteraciones': datos_tabla,
            'errores': [round(e, 8) for e in errores],
            'img': img_base64  # ← CORREGIDO: retornar base64
        })
    
    except Exception as e:
        return f.jsonify({'error': str(e)}), 400

@app.route('/historial')
def ver_historial():
    historial = cargar_historial()
    # Invertir para mostrar los más recientes primero
    historial.reverse()
    return f.render_template('historial.html', historial=historial)

@app.route('/limpiar-historial', methods=['POST'])
def limpiar_historial():
    """Endpoint para limpiar el historial"""
    import json
    ruta_historial = os.path.join(BASE_DIR, "historial.json")
    try:
        with open(ruta_historial, "w", encoding="utf-8") as f:
            json.dump([], f)
        return f.jsonify({"success": True})
    except Exception as e:
        return f.jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)