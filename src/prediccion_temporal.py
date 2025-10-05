"""Módulo de predicción temporal usando datos satelitales Sentinel-2."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'


class PredictorTemporal:
    """Predictor temporal usando datos satelitales Sentinel-2."""
    
    def __init__(self, directorio_geojson="data/raw"):
        self.directorio = Path(directorio_geojson)
        self.datos_temporales = []
        self.df_temporal = None
        self.modelos = {}
        self.predicciones = {}
        self.figuras = []
    
    def cargar_datos_geojson(self):
        """Carga y procesa todos los archivos GeoJSON."""
        print("=" * 70)
        print("�� CARGANDO DATOS SATELITALES SENTINEL-2")
        print("=" * 70)
        
        archivos = sorted(self.directorio.glob("S2*_L2A.geojson"))
        
        if not archivos:
            print("⚠️  No se encontraron archivos GeoJSON")
            return False
        
        print(f"\n📁 Encontrados {len(archivos)} archivos GeoJSON")
        
        for archivo in archivos:
            try:
                with open(archivo, 'r') as f:
                    geojson = json.load(f)
                
                properties = geojson.get('properties', {})
                fecha_str = properties.get('datetime', '')
                if fecha_str:
                    fecha = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
                else:
                    continue
                
                datos = {
                    'fecha': fecha,
                    'cloud_cover': properties.get('eo:cloud_cover', 0),
                    'vegetation_pct': properties.get('s2:vegetation_percentage', 0),
                    'not_vegetated_pct': properties.get('s2:not_vegetated_percentage', 0),
                    'water_pct': properties.get('s2:water_percentage', 0),
                    'snow_ice_pct': properties.get('s2:snow_ice_percentage', 0),
                    'unclassified_pct': properties.get('s2:unclassified_percentage', 0),
                    'archivo': archivo.name
                }
                
                self.datos_temporales.append(datos)
                
            except Exception as e:
                print(f"⚠️  Error procesando {archivo.name}: {e}")
        
        self.df_temporal = pd.DataFrame(self.datos_temporales)
        self.df_temporal = self.df_temporal.sort_values('fecha').reset_index(drop=True)
        
        fecha_inicio = self.df_temporal['fecha'].min()
        self.df_temporal['dias_desde_inicio'] = (
            self.df_temporal['fecha'] - fecha_inicio
        ).dt.total_seconds() / 86400
        
        print(f"\n✅ Datos cargados exitosamente")
        print(f"   Periodo: {self.df_temporal['fecha'].min().date()} a {self.df_temporal['fecha'].max().date()}")
        print(f"   Total de observaciones: {len(self.df_temporal)}")
        
        return True
    
    def calcular_estadisticas(self):
        """Calcula estadísticas descriptivas de los datos."""
        print("\n" + "=" * 70)
        print("📊 ESTADÍSTICAS DESCRIPTIVAS")
        print("=" * 70)
        
        estadisticas = self.df_temporal[[
            'cloud_cover', 'vegetation_pct', 'not_vegetated_pct', 
            'water_pct', 'snow_ice_pct'
        ]].describe()
        
        print("\n", estadisticas.round(2))
        return estadisticas
    
    def visualizar_series_temporales(self):
        """Visualiza las series temporales de las métricas principales."""
        print("\n" + "=" * 70)
        print("📈 GENERANDO VISUALIZACIONES DE SERIES TEMPORALES")
        print("=" * 70)
        
        fig, axes = plt.subplots(3, 2, figsize=(16, 12))
        fig.suptitle('Series Temporales - Análisis Sentinel-2', 
                    fontsize=18, fontweight='bold', y=0.995)
        
        metricas = [
            ('vegetation_pct', 'Vegetación (%)', 'green', '🌿'),
            ('not_vegetated_pct', 'No Vegetado (%)', 'brown', '🏜️'),
            ('water_pct', 'Agua (%)', 'blue', '💧'),
            ('cloud_cover', 'Cobertura de Nubes (%)', 'gray', '☁️'),
            ('snow_ice_pct', 'Nieve/Hielo (%)', 'cyan', '❄️'),
            ('unclassified_pct', 'Sin Clasificar (%)', 'orange', '❓')
        ]
        
        for idx, (metrica, titulo, color, emoji) in enumerate(metricas):
            ax = axes[idx // 2, idx % 2]
            
            ax.plot(self.df_temporal['fecha'], self.df_temporal[metrica], 
                   marker='o', linestyle='-', color=color, linewidth=2, 
                   markersize=6, alpha=0.7, label='Observado')
            
            z = np.polyfit(self.df_temporal['dias_desde_inicio'], 
                          self.df_temporal[metrica], 1)
            p = np.poly1d(z)
            ax.plot(self.df_temporal['fecha'], 
                   p(self.df_temporal['dias_desde_inicio']),
                   linestyle='--', color='red', linewidth=2, 
                   alpha=0.6, label='Tendencia')
            
            ax.set_title(f'{emoji} {titulo}', fontsize=13, fontweight='bold', pad=10)
            ax.set_xlabel('Fecha', fontsize=10)
            ax.set_ylabel('Porcentaje (%)', fontsize=10)
            ax.legend(loc='best', fontsize=9)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        output_path = Path('data/output/series_temporales.png')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"✅ Gráfico guardado: {output_path}")
        
        self.figuras.append(('series_temporales', fig))
        return fig
    
    def entrenar_modelos_prediccion(self, meses_adelante=2):
        """Entrena modelos de predicción para cada métrica."""
        print("\n" + "=" * 70)
        print(f"🤖 ENTRENANDO MODELOS DE PREDICCIÓN ({meses_adelante} MESES ADELANTE)")
        print("=" * 70)
        
        metricas = ['vegetation_pct', 'not_vegetated_pct', 'water_pct', 
                   'cloud_cover', 'snow_ice_pct']
        
        X = self.df_temporal[['dias_desde_inicio']].values
        
        for metrica in metricas:
            y = self.df_temporal[metrica].values
            
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)
            
            modelo = LinearRegression()
            modelo.fit(X_poly, y)
            
            y_pred = modelo.predict(X_poly)
            r2 = r2_score(y, y_pred)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            
            self.modelos[metrica] = {
                'modelo': modelo,
                'poly': poly,
                'r2': r2,
                'rmse': rmse
            }
            
            print(f"\n📊 {metrica}:")
            print(f"   R² Score: {r2:.4f}")
            print(f"   RMSE: {rmse:.4f}")
        
        fecha_final = self.df_temporal['fecha'].max()
        dias_final = self.df_temporal['dias_desde_inicio'].max()
        
        dias_futuros = np.arange(
            dias_final + 5, 
            dias_final + (meses_adelante * 30), 
            5
        )
        
        fechas_futuras = [
            fecha_final + timedelta(days=float(d - dias_final)) 
            for d in dias_futuros
        ]
        
        predicciones_futuras = {'fecha': fechas_futuras}
        
        for metrica in metricas:
            X_futuro = dias_futuros.reshape(-1, 1)
            X_futuro_poly = self.modelos[metrica]['poly'].transform(X_futuro)
            pred = self.modelos[metrica]['modelo'].predict(X_futuro_poly)
            pred = np.clip(pred, 0, 100)
            predicciones_futuras[metrica] = pred
        
        self.predicciones = pd.DataFrame(predicciones_futuras)
        
        print(f"\n✅ Modelos entrenados y predicciones generadas")
        print(f"   Predicciones hasta: {fechas_futuras[-1].date()}")
        
        return True
    
    def visualizar_predicciones(self):
        """Visualiza las predicciones junto con los datos históricos."""
        print("\n" + "=" * 70)
        print("🔮 GENERANDO VISUALIZACIONES DE PREDICCIONES")
        print("=" * 70)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('Predicciones Temporales - Próximos 2 Meses', 
                    fontsize=18, fontweight='bold', y=0.995)
        
        metricas = [
            ('vegetation_pct', 'Vegetación (%)', 'green', '🌿'),
            ('water_pct', 'Agua (%)', 'blue', '💧'),
            ('cloud_cover', 'Cobertura de Nubes (%)', 'gray', '☁️'),
            ('not_vegetated_pct', 'No Vegetado (%)', 'brown', '🏜️')
        ]
        
        for idx, (metrica, titulo, color, emoji) in enumerate(metricas):
            ax = axes[idx // 2, idx % 2]
            
            ax.plot(self.df_temporal['fecha'], self.df_temporal[metrica],
                   marker='o', linestyle='-', color=color, linewidth=2,
                   markersize=6, alpha=0.7, label='Datos Históricos')
            
            ax.plot(self.predicciones['fecha'], self.predicciones[metrica],
                   marker='s', linestyle='--', color='red', linewidth=2,
                   markersize=5, alpha=0.8, label='Predicción')
            
            pred_values = self.predicciones[metrica].values
            ax.fill_between(self.predicciones['fecha'],
                           np.clip(pred_values - 10, 0, 100),
                           np.clip(pred_values + 10, 0, 100),
                           color='red', alpha=0.2, label='Intervalo de Confianza')
            
            fecha_division = self.df_temporal['fecha'].max()
            ax.axvline(x=fecha_division, color='black', linestyle=':',
                      linewidth=2, alpha=0.5, label='Fecha Actual')
            
            ax.set_title(f'{emoji} {titulo}', fontsize=13, fontweight='bold', pad=10)
            ax.set_xlabel('Fecha', fontsize=10)
            ax.set_ylabel('Porcentaje (%)', fontsize=10)
            ax.legend(loc='best', fontsize=8)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.tick_params(axis='x', rotation=45)
            
            r2 = self.modelos[metrica]['r2']
            ax.text(0.02, 0.98, f'R² = {r2:.3f}', 
                   transform=ax.transAxes, fontsize=9,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        output_path = Path('data/output/predicciones_temporales.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"✅ Gráfico guardado: {output_path}")
        
        self.figuras.append(('predicciones', fig))
        return fig
    
    def analisis_cambios(self):
        """Analiza los cambios esperados en las próximas semanas."""
        print("\n" + "=" * 70)
        print("📊 ANÁLISIS DE CAMBIOS ESPERADOS")
        print("=" * 70)
        
        ultimo_historico = self.df_temporal.iloc[-1]
        ultima_prediccion = self.predicciones.iloc[-1]
        
        cambios = {}
        metricas = ['vegetation_pct', 'water_pct', 'cloud_cover', 'not_vegetated_pct']
        
        print("\n📈 Cambios esperados desde hoy hasta dentro de 2 meses:\n")
        
        for metrica in metricas:
            valor_actual = ultimo_historico[metrica]
            valor_futuro = ultima_prediccion[metrica]
            cambio = valor_futuro - valor_actual
            cambio_pct = (cambio / valor_actual * 100) if valor_actual != 0 else 0
            
            cambios[metrica] = {
                'actual': valor_actual,
                'futuro': valor_futuro,
                'cambio': cambio,
                'cambio_pct': cambio_pct
            }
            
            flecha = "📈" if cambio > 0 else "📉" if cambio < 0 else "➡️"
            print(f"{flecha} {metrica}:")
            print(f"   Actual: {valor_actual:.2f}%")
            print(f"   Predicción: {valor_futuro:.2f}%")
            print(f"   Cambio: {cambio:+.2f}% ({cambio_pct:+.1f}%)\n")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        nombres = [m.replace('_pct', '').replace('_', ' ').title() for m in metricas]
        cambios_valores = [cambios[m]['cambio'] for m in metricas]
        colores = ['green' if c > 0 else 'red' if c < 0 else 'gray' 
                  for c in cambios_valores]
        
        bars = ax.bar(nombres, cambios_valores, color=colores, alpha=0.7, edgecolor='black')
        
        for bar, valor in zip(bars, cambios_valores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{valor:+.1f}%',
                   ha='center', va='bottom' if valor > 0 else 'top',
                   fontsize=11, fontweight='bold')
        
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.set_title('Cambios Esperados en los Próximos 2 Meses', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Cambio (%)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Métrica', fontsize=12, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        output_path = Path('data/output/analisis_cambios.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"✅ Gráfico guardado: {output_path}")
        
        self.figuras.append(('cambios', fig))
        return cambios, fig
    
    def generar_reporte_resumen(self):
        """Genera un resumen del análisis."""
        print("\n" + "=" * 70)
        print("📋 RESUMEN DEL ANÁLISIS PREDICTIVO")
        print("=" * 70)
        
        fecha_inicio = self.df_temporal['fecha'].min().date()
        fecha_fin = self.df_temporal['fecha'].max().date()
        fecha_prediccion = self.predicciones['fecha'].iloc[-1].date()
        
        print(f"\n🗓️  Periodo Analizado: {fecha_inicio} a {fecha_fin}")
        print(f"🔮 Predicción hasta: {fecha_prediccion}")
        print(f"📊 Total de observaciones: {len(self.df_temporal)}")
        print(f"🎯 Modelos entrenados: {len(self.modelos)}")
        
        print("\n📈 Precisión de los Modelos (R²):")
        for metrica, info in self.modelos.items():
            calidad = "Excelente" if info['r2'] > 0.9 else "Bueno" if info['r2'] > 0.7 else "Aceptable"
            print(f"   • {metrica}: {info['r2']:.4f} ({calidad})")
        
        output_csv = Path('data/output/predicciones_futuras.csv')
        self.predicciones.to_csv(output_csv, index=False)
        print(f"\n✅ Predicciones guardadas en: {output_csv}")
        
        return {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'fecha_prediccion': fecha_prediccion,
            'n_observaciones': len(self.df_temporal),
            'modelos': self.modelos
        }
    
    def ejecutar_analisis_completo(self, meses_adelante=2):
        """Ejecuta el análisis completo de predicción temporal."""
        print("\n" + "🚀" * 35)
        print("🛰️  ANÁLISIS PREDICTIVO TEMPORAL - SENTINEL-2")
        print("🚀" * 35)
        
        if not self.cargar_datos_geojson():
            print("\n❌ Error: No se pudieron cargar los datos")
            return None
        
        self.calcular_estadisticas()
        self.visualizar_series_temporales()
        self.entrenar_modelos_prediccion(meses_adelante)
        self.visualizar_predicciones()
        self.analisis_cambios()
        resumen = self.generar_reporte_resumen()
        
        print("\n" + "✅" * 35)
        print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("✅" * 35)
        print("\n📁 Revisa la carpeta 'data/output/' para ver todos los resultados\n")
        
        return resumen


if __name__ == "__main__":
    predictor = PredictorTemporal()
    predictor.ejecutar_analisis_completo(meses_adelante=2)
