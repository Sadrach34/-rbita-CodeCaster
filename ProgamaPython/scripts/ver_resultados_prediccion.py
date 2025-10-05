#!/usr/bin/env python3
"""
Script para visualizar rápidamente los resultados de la predicción temporal.
Muestra un resumen ejecutivo en terminal.
"""
import sys
from pathlib import Path
from datetime import datetime


def encontrar_ultimo_reporte():
    """Encuentra el reporte más reciente."""
    output_dir = Path("data/output")
    reportes = list(output_dir.glob("reporte_prediccion_temporal_*.txt"))
    
    if not reportes:
        return None
    
    # Ordenar por fecha de modificación
    reportes.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return reportes[0]


def mostrar_reporte():
    """Muestra el contenido del reporte más reciente."""
    reporte = encontrar_ultimo_reporte()
    
    if not reporte:
        print("❌ No se encontró ningún reporte de predicción temporal.")
        print("💡 Ejecuta primero: python scripts/ejecutar_prediccion_temporal.py")
        return 1
    
    print("=" * 80)
    print("📊 RESUMEN DE PREDICCIÓN TEMPORAL")
    print("=" * 80)
    print(f"\n📄 Archivo: {reporte.name}")
    print(f"📅 Generado: {datetime.fromtimestamp(reporte.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📏 Tamaño: {reporte.stat().st_size} bytes")
    print("\n" + "-" * 80)
    print("\n📝 CONTENIDO DEL REPORTE:\n")
    
    with open(reporte, 'r', encoding='utf-8') as f:
        contenido = f.read()
        print(contenido)
    
    print("\n" + "=" * 80)
    print("📊 ARCHIVOS DE VISUALIZACIÓN")
    print("=" * 80)
    
    output_dir = Path("data/output")
    
    # Buscar imágenes
    img_series = output_dir / "prediccion_series_temporales.png"
    img_comp = output_dir / "prediccion_comparacion.png"
    
    if img_series.exists():
        print(f"\n Series temporales: {img_series}")
        print(f"   Tamaño: {img_series.stat().st_size / 1024:.1f} KB")
    
    if img_comp.exists():
        print(f"\n Comparación: {img_comp}")
        print(f"   Tamaño: {img_comp.stat().st_size / 1024:.1f} KB")
    
    print("\n" + "=" * 80)
    print("💡 CÓMO VER LAS IMÁGENES:")
    print("=" * 80)
    print("\nEn VSCode:")
    print(f"   code {img_series}")
    
    print("\nEn terminal:")
    print(f"   xdg-open {img_series}  # Linux")
    print(f"   open {img_series}      # Mac")
    print(f"   start {img_series}     # Windows")
    
    print("\n" + "=" * 80)
    
    return 0


def main():
    """Función principal."""
    try:
        return mostrar_reporte()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
