#!/usr/bin/env python3
"""
Script principal para ejecutar todos los análisis del proyecto Orbita-CodeCaster.

Este script ejecuta:
1. Análisis de mosquitos
2. Análisis de cobertura del suelo
3. Modelo predictivo con Machine Learning
4. Generación de mapas interactivos

Uso: python scripts/analisis_completo.py
"""
import sys
from pathlib import Path

# Añadir directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.data_loader import DataLoader
from src.analisis_mosquitos import AnalizadorMosquitos
from src.analisis_cobertura import AnalizadorCobertura
from src.prediccion import PredictorMosquitos
import time


def print_banner():
    """Imprime el banner del proyecto."""
    banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║        🌍  ORBITA-CODECASTER - ANÁLISIS COMPLETO  🦟          ║
    ║                                                                ║
    ║   Análisis Geoespacial de Floraciones y Hábitats de Mosquitos ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_section(title):
    """Imprime un separador de sección."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def main():
    """Función principal del script."""
    start_time = time.time()
    
    print_banner()
    
    try:
        # =============================================
        # 1. CARGA DE DATOS
        # =============================================
        print_section("📂 FASE 1: CARGA DE DATOS")
        
        loader = DataLoader(data_dir="data/raw")
        loader.cargar_todos()
        loader.resumen_datos()
        
        # =============================================
        # 2. ANÁLISIS DE MOSQUITOS
        # =============================================
        print_section("🦟 FASE 2: ANÁLISIS DE MOSQUITOS")
        
        print("Ejecutando análisis de mosquitos...")
        analizador_mosquitos = AnalizadorMosquitos(loader.get_mosquitos())
        resultados_mosquitos = analizador_mosquitos.ejecutar_analisis_completo()
        
        # =============================================
        # 3. ANÁLISIS DE COBERTURA DEL SUELO
        # =============================================
        print_section("🌍 FASE 3: ANÁLISIS DE COBERTURA DEL SUELO")
        
        print("Ejecutando análisis de cobertura del suelo...")
        analizador_cobertura = AnalizadorCobertura(loader.get_imagery())
        resultados_cobertura = analizador_cobertura.ejecutar_analisis_completo()
        
        # =============================================
        # 4. MODELO PREDICTIVO
        # =============================================
        print_section("🤖 FASE 4: MODELO PREDICTIVO")
        
        print("Entrenando modelo predictivo con Machine Learning...")
        predictor = PredictorMosquitos(loader.get_imagery())
        resultados_prediccion = predictor.ejecutar_analisis_completo()
        
        # =============================================
        # 5. RELACIÓN ENTRE DATASETS
        # =============================================
        print_section("🔗 FASE 5: ANÁLISIS DE RELACIONES")
        
        print("Analizando relación entre mosquitos y cobertura del suelo...")
        analizar_relaciones(loader.get_mosquitos(), loader.get_imagery())
        
        # =============================================
        # RESUMEN FINAL
        # =============================================
        elapsed_time = time.time() - start_time
        
        print_section(" ANÁLISIS COMPLETO FINALIZADO")
        
        print(f"⏱️  Tiempo total de ejecución: {elapsed_time:.2f} segundos\n")
        
        print("📊 RESUMEN DE RESULTADOS:")
        print(f"   • {len(loader.get_mosquitos())} reportes de mosquitos analizados")
        print(f"   • {len(loader.get_imagery())} observaciones de cobertura analizadas")
        print(f"   • Modelo predictivo entrenado con {resultados_prediccion.get('test_score', 0):.2%} de precisión")
        
        print("\n📁 ARCHIVOS GENERADOS:")
        print("   Todos los resultados se encuentran en la carpeta 'data/output/':")
        print("   • Gráficos estadísticos (.png)")
        print("   • Mapas interactivos (.html)")
        print("   • Métricas del modelo predictivo")
        
        print("\n🎉 ¡Análisis completado exitosamente!")
        print("   Abre los archivos HTML en tu navegador para explorar los mapas.\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: No se encontró un archivo necesario")
        print(f"   Detalles: {e}")
        print(f"\n💡 Asegúrate de tener los archivos CSV en 'data/raw/'")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def analizar_relaciones(df_mosquitos, df_imagery):
    """
    Analiza la relación entre reportes de mosquitos y cobertura del suelo.
    
    Args:
        df_mosquitos: DataFrame de mosquitos
        df_imagery: DataFrame de imagery
    """
    print("\n🔍 Analizando relaciones entre datasets...")
    
    # Áreas con agua
    col_agua = 'ceoWaterLakePondedContainer'
    if col_agua in df_imagery.columns:
        areas_con_agua = df_imagery[df_imagery[col_agua] > 0]
        print(f"\n💧 Áreas con cuerpos de agua: {len(areas_con_agua)}")
        print(f"   ({len(areas_con_agua)/len(df_imagery)*100:.1f}% del total)")
    
    # Reportes de mosquitos
    print(f"\n🦟 Total de reportes de mosquitos: {len(df_mosquitos)}")
    
    # Análisis temporal
    if 'mes' in df_mosquitos.columns:
        meses_pico = df_mosquitos['mes'].value_counts().head(3)
        print(f"\n📅 Meses con más reportes:")
        meses_nombres = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 
                        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
        for mes, cantidad in meses_pico.items():
            nombre_mes = meses_nombres.get(mes, f'Mes {mes}')
            print(f"   • {nombre_mes}: {cantidad} reportes")
    
    # Correlación conceptual
    print(f"\n💡 INSIGHTS:")
    print(f"   • Las áreas con agua son hábitats potenciales para mosquitos")
    print(f"   • La vegetación puede proporcionar refugio y sombra")
    print(f"   • Las superficies impermeables pueden crear charcos de agua estancada")
    
    print("\n Análisis de relaciones completado\n")


if __name__ == "__main__":
    main()
