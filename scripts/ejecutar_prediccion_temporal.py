#!/usr/bin/env python3
"""
Script para ejecutar la predicción temporal usando datos Sentinel-2.
Analiza series temporales y predice el estado futuro de la vegetación.

Uso: python scripts/ejecutar_prediccion_temporal.py
"""
import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.prediccion_temporal import PredictorTemporal


def main():
    """Ejecuta el análisis de predicción temporal."""
    print("=" * 80)
    print("  PREDICCIÓN TEMPORAL SENTINEL-2 - ZONA SONORA")
    print("=" * 80)
    print()
    print("📡 Este análisis:")
    print("   • Carga y procesa imágenes satelitales Sentinel-2")
    print("   • Analiza series temporales de índices de vegetación")
    print("   • Entrena modelos predictivos con Random Forest")
    print("   • Genera predicciones para 2 meses adelante")
    print("   • Crea visualizaciones y reportes completos")
    print()
    print("-" * 80)
    print()
    
    try:
        # Crear predictor
        predictor = PredictorTemporal(directorio_geojson="data/raw")
        
        # Ejecutar análisis completo
        resultados = predictor.ejecutar_analisis_completo(meses_adelante=2)
        
        if resultados:
            print("\n🎉 ¡Análisis completado exitosamente!")
            print("\n📂 Archivos generados en data/output/:")
            print("   • prediccion_series_temporales.png")
            print("   • prediccion_comparacion.png")
            print("   • reporte_prediccion_temporal_*.txt")
            print()
            
            # Mostrar resumen ejecutivo
            print("=" * 80)
            print("  RESUMEN EJECUTIVO DE PREDICCIÓN")
            print("=" * 80)
            
            for indice, pred in resultados.items():
                cambio = pred['cambio_porcentual']
                if cambio > 5:
                    tendencia = "📈 AUMENTO SIGNIFICATIVO"
                elif cambio < -5:
                    tendencia = "📉 DISMINUCIÓN SIGNIFICATIVA"
                else:
                    tendencia = "➡️ ESTABLE"
                
                print(f"\n{indice.replace('_', ' ').upper()}:")
                print(f"   {tendencia}")
                print(f"   Cambio esperado: {cambio:+.2f}%")
                print(f"   Confianza: {pred['confianza']:.1%}")
            
            print("\n" + "=" * 80)
            return 0
        else:
            print("\n❌ Error al generar predicciones")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
