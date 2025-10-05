#!/usr/bin/env python3
"""
Script para generar mapas de floraciones.
Uso: python scripts/generar_mapa_floraciones.py
"""
import sys
from pathlib import Path

# Añadir directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.floraciones import generar_mapa_rapido


def main():
    """Función principal del script."""
    print("🌸 Generando mapa de floraciones...")
    
    # Detecciones de ejemplo (en producción, estas vendrían de análisis de datos)
    detecciones = [
        {"lat": 32.5, "lon": -115.5, "fecha": "2025-03-15", "intensidad": "Alta"},
        {"lat": 20.7, "lon": -103.3, "fecha": "2025-03-18", "intensidad": "Media"},
        {"lat": 28.6, "lon": -106.1, "fecha": "2025-03-20", "intensidad": "Alta"},
    ]
    
    # Generar mapa
    ruta = generar_mapa_rapido(detecciones)
    print(f"🗺️  Abre el archivo en tu navegador: {ruta}")


if __name__ == "__main__":
    main()
