#!/usr/bin/env python3
"""
Script para generar un reporte HTML completo con predicciones temporales.
Ejecutar: python scripts/generar_reporte_html.py
"""
import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.prediccion_temporal import PredictorTemporal
from src.reporte_html import GeneradorReporteHTML
import matplotlib.pyplot as plt


def generar_reporte_completo():
    """Genera un reporte HTML completo con todas las visualizaciones y predicciones."""
    
    print("\n" + "=" * 80)
    print("🌍 GENERADOR DE REPORTE HTML - PREDICCIÓN TEMPORAL SENTINEL-2")
    print("=" * 80 + "\n")
    
    # Paso 1: Ejecutar análisis predictivo
    print("📊 Paso 1: Ejecutando análisis predictivo temporal...")
    predictor = PredictorTemporal()
    resumen = predictor.ejecutar_analisis_completo(meses_adelante=2)
    
    if not resumen:
        print("\n❌ Error: No se pudo completar el análisis predictivo")
        return None
    
    # Paso 2: Crear generador de reporte HTML
    print("\n" + "=" * 80)
    print("📝 Paso 2: Generando reporte HTML interactivo...")
    print("=" * 80 + "\n")
    
    reporte = GeneradorReporteHTML("Reporte de Predicción Temporal - Sentinel-2")
    
    # Agregar métricas principales
    reporte.agregar_metrica(
        "Archivos Procesados",
        str(resumen['n_observaciones']),
        "Imágenes Sentinel-2 analizadas",
        "📁"
    )
    
    reporte.agregar_metrica(
        "Periodo Analizado",
        f"{resumen['fecha_inicio']} a {resumen['fecha_fin']}",
        "Rango de fechas de observaciones",
        "📅"
    )
    
    reporte.agregar_metrica(
        "Predicción hasta",
        str(resumen['fecha_prediccion']),
        "Fecha final de las predicciones",
        "🔮"
    )
    
    # Calcular R² promedio
    r2_promedio = sum(m['r2'] for m in resumen['modelos'].values()) / len(resumen['modelos'])
    reporte.agregar_metrica(
        "Precisión Promedio",
        f"{r2_promedio:.1%}",
        "R² de los modelos predictivos",
        "🎯"
    )
    
    # Agregar sección de resumen ejecutivo
    reporte.agregar_seccion(
        "📋 Resumen Ejecutivo",
        f"""
        Este reporte presenta el análisis de predicción temporal para una zona en Sonora, México, 
        utilizando datos satelitales Sentinel-2. Se analizaron {resumen['n_observaciones']} imágenes 
        desde {resumen['fecha_inicio']} hasta {resumen['fecha_fin']}, generando predicciones 
        hasta {resumen['fecha_prediccion']}.
        <br><br>
        Los modelos predictivos desarrollados analizan la evolución temporal de métricas clave como 
        vegetación, cobertura de nubes, agua y áreas no vegetadas, permitiendo anticipar cambios 
        en la zona durante los próximos 2 meses.
        """,
        "texto"
    )
    
    # Agregar información de los modelos
    modelos_info = []
    for metrica, info in resumen['modelos'].items():
        calidad = "Excelente" if info['r2'] > 0.9 else "Bueno" if info['r2'] > 0.7 else "Aceptable"
        modelos_info.append(
            f"✓ <b>{metrica.replace('_', ' ').title()}</b>: R² = {info['r2']:.4f} ({calidad}) | RMSE = {info['rmse']:.4f}"
        )
    
    reporte.agregar_seccion(
        "🤖 Modelos Predictivos",
        modelos_info,
        "lista"
    )
    
    # Agregar gráficos generados
    print("📊 Agregando visualizaciones al reporte...")
    
    for nombre, fig in predictor.figuras:
        if nombre == 'series_temporales':
            reporte.agregar_grafico(
                fig,
                "Series Temporales Históricas",
                "Análisis de las series temporales de todas las métricas espectrales observadas en el periodo de estudio."
            )
        elif nombre == 'predicciones':
            reporte.agregar_grafico(
                fig,
                "Predicciones Temporales",
                "Predicciones para los próximos 2 meses basadas en modelos polinomiales de grado 2, con intervalo de confianza del ±10%."
            )
        elif nombre == 'cambios':
            reporte.agregar_grafico(
                fig,
                "Análisis de Cambios Esperados",
                "Cambios esperados en las métricas principales desde la fecha actual hasta dentro de 2 meses."
            )
        
        plt.close(fig)
    
    # Agregar tabla de predicciones
    print("📋 Agregando tabla de predicciones...")
    
    # Tomar las primeras y últimas 5 predicciones
    df_pred = predictor.predicciones.copy()
    df_pred['fecha'] = df_pred['fecha'].dt.strftime('%Y-%m-%d')
    
    tabla_datos = df_pred[['fecha', 'vegetation_pct', 'water_pct', 'cloud_cover']].head(10).to_dict('records')
    
    # Renombrar columnas para la tabla
    tabla_datos_formateada = []
    for fila in tabla_datos:
        tabla_datos_formateada.append({
            'Fecha': fila['fecha'],
            'Vegetación (%)': f"{fila['vegetation_pct']:.2f}",
            'Agua (%)': f"{fila['water_pct']:.2f}",
            'Nubes (%)': f"{fila['cloud_cover']:.2f}"
        })
    
    reporte.agregar_seccion(
        "📊 Tabla de Predicciones (Primeros 10 días)",
        tabla_datos_formateada,
        "tabla"
    )
    
    # Agregar conclusiones
    ultimo_hist = predictor.df_temporal.iloc[-1]
    ultima_pred = predictor.predicciones.iloc[-1]
    
    cambio_veg = ultima_pred['vegetation_pct'] - ultimo_hist['vegetation_pct']
    cambio_agua = ultima_pred['water_pct'] - ultimo_hist['water_pct']
    
    tendencia_veg = "aumentará" if cambio_veg > 0 else "disminuirá"
    tendencia_agua = "aumentará" if cambio_agua > 0 else "disminuirá"
    
    conclusiones = f"""
    <div class="alerta info">
        <span style="font-size: 2em;">ℹ️</span>
        <div>
            <strong>Conclusiones Principales:</strong><br>
            • La vegetación {tendencia_veg} aproximadamente {abs(cambio_veg):.1f}% en los próximos 2 meses<br>
            • La presencia de agua {tendencia_agua} alrededor de {abs(cambio_agua):.3f}%<br>
            • Los modelos predictivos muestran una precisión promedio del {r2_promedio:.1%}<br>
            • Se recomienda monitoreo continuo para validar las predicciones
        </div>
    </div>
    """
    
    reporte.agregar_seccion(
        "🎯 Conclusiones",
        conclusiones,
        "texto"
    )
    
    # Generar archivo HTML
    print("\n" + "=" * 80)
    print("💾 Generando archivo HTML final...")
    print("=" * 80 + "\n")
    
    ruta_html = reporte.generar_html("data/output/reporte_prediccion_temporal.html")
    
    print("\n" + "✅" * 40)
    print("✅ REPORTE HTML GENERADO EXITOSAMENTE")
    print("✅" * 40)
    print(f"\n📄 Archivo generado: {ruta_html}")
    print(f"🌐 Abre el archivo en tu navegador para ver el reporte interactivo")
    print(f"\n💡 Comando para abrir:")
    print(f"   xdg-open {ruta_html}  # Linux")
    print(f"   open {ruta_html}      # macOS")
    print(f"   start {ruta_html}     # Windows\n")
    
    return ruta_html


if __name__ == "__main__":
    try:
        generar_reporte_completo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
