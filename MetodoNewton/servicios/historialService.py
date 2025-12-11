import sys
import os
import json
from datetime import datetime

# Agregar ruta base del proyecto al sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ruta del archivo historial.json en la raíz del proyecto
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_historial = os.path.join(base_dir, "historial.json")

def cargar_historial():
    """Carga el historial desde el archivo JSON."""
    if not os.path.exists(ruta_historial):
        return []
    
    try:
        with open(ruta_historial, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def guardar_historial(registro):
    """Agrega un registro al archivo historial.json."""
    historial = cargar_historial()
    registro["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historial.append(registro)
    
    with open(ruta_historial, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)