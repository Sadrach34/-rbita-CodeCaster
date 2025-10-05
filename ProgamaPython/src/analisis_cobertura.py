"""
Módulo de análisis de cobertura del suelo.
Analiza datos de land cover e imagery con visualizaciones.
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path


class AnalizadorCobertura:
    """Analiza datos de cobertura del suelo."""
    
    def __init__(self, df_imagery):
        """
        Inicializa el analizador.
        
        Args:
            df_imagery: DataFrame con datos de imagery
        """
        self.df = df_imagery
        self.resultados = {}
        
        # Definir columnas de cobertura
        self.columnas_cobertura = [
            'ceoTREES_CANOPYCOVER',
            'ceoBUSH_SCRUB',
            'ceoGRASS',
            'ceoBuilding',
            'ceoImperviousSurface',
            'ceoWaterLakePondedContainer'
        ]
        
        # Nombres legibles
        self.nombres_cobertura = {
            'ceoTREES_CANOPYCOVER': 'Árboles',
            'ceoBUSH_SCRUB': 'Arbustos',
            'ceoGRASS': 'Pasto',
            'ceoBuilding': 'Edificios',
            'ceoImperviousSurface': 'Superficies Impermeables',
            'ceoWaterLakePondedContainer': 'Agua'
        }
    
    def analizar_promedios(self):
        """Analiza los promedios de cobertura por tipo."""
        print("=" * 60)
        print("🌍 ANÁLISIS DE COBERTURA DEL SUELO")
        print("=" * 60)
        
        # Filtrar columnas que existen
        columnas_existentes = [col for col in self.columnas_cobertura if col in self.df.columns]
        
        if not columnas_existentes:
            print("⚠️  No se encontraron columnas de cobertura")
            return None
        
        # Calcular promedios
        promedios = self.df[columnas_existentes].mean()
        self.resultados['promedios'] = promedios
        
        print("\nPromedio de cobertura del suelo (%):")
        for col, valor in promedios.items():
            nombre = self.nombres_cobertura.get(col, col)
            print(f"   {nombre}: {valor:.2f}%")
        
        # Crear gráfico
        plt.figure(figsize=(12, 6))
        nombres = [self.nombres_cobertura.get(col, col) for col in promedios.index]
        
        bars = plt.bar(range(len(promedios)), promedios.values, 
                      color=['forestgreen', 'olive', 'limegreen', 'gray', 'darkgray', 'steelblue'])
        
        plt.title('Promedio de Cobertura del Suelo (%)', fontsize=14, fontweight='bold')
        plt.xlabel('Tipo de Cobertura')
        plt.ylabel('Porcentaje Promedio')
        plt.xticks(range(len(promedios)), nombres, rotation=45, ha='right')
        
        # Agregar valores en las barras
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Guardar
        output_path = Path('data/output/promedio_cobertura_suelo.png')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n Gráfico guardado: {output_path}")
        plt.close()
        
        return promedios
    
    def analizar_distribucion(self):
        """Analiza la distribución de cada tipo de cobertura."""
        print("\n" + "=" * 60)
        print("📊 DISTRIBUCIÓN DE COBERTURA")
        print("=" * 60)
        
        columnas_existentes = [col for col in self.columnas_cobertura if col in self.df.columns]
        
        if not columnas_existentes:
            print("⚠️  No se encontraron columnas de cobertura")
            return None
        
        # Crear subplots
        n_cols = len(columnas_existentes)
        n_rows = (n_cols + 1) // 2
        
        fig, axes = plt.subplots(n_rows, 2, figsize=(14, n_rows * 4))
        axes = axes.flatten() if n_rows > 1 else [axes]
        
        for i, col in enumerate(columnas_existentes):
            ax = axes[i]
            nombre = self.nombres_cobertura.get(col, col)
            
            # Histograma
            self.df[col].hist(bins=30, ax=ax, color='steelblue', edgecolor='black', alpha=0.7)
            ax.set_title(f'Distribución: {nombre}', fontweight='bold')
            ax.set_xlabel('Porcentaje de Cobertura')
            ax.set_ylabel('Frecuencia')
            
            # Estadísticas
            media = self.df[col].mean()
            mediana = self.df[col].median()
            ax.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media: {media:.1f}%')
            ax.axvline(mediana, color='green', linestyle='--', linewidth=2, label=f'Mediana: {mediana:.1f}%')
            ax.legend()
        
        # Ocultar ejes extras
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')
        
        plt.tight_layout()
        
        # Guardar
        output_path = Path('data/output/distribucion_cobertura.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f" Gráfico de distribución guardado: {output_path}")
        plt.close()
        
        return columnas_existentes
    
    def analizar_areas_con_agua(self):
        """Analiza específicamente las áreas con cuerpos de agua."""
        print("\n" + "=" * 60)
        print("💧 ANÁLISIS DE ÁREAS CON AGUA")
        print("=" * 60)
        
        col_agua = 'ceoWaterLakePondedContainer'
        
        if col_agua not in self.df.columns:
            print("⚠️  Columna de agua no encontrada")
            return None
        
        # Filtrar áreas con agua
        areas_con_agua = self.df[self.df[col_agua] > 0]
        total_areas = len(self.df)
        areas_agua = len(areas_con_agua)
        porcentaje = (areas_agua / total_areas) * 100
        
        self.resultados['areas_con_agua'] = areas_agua
        self.resultados['porcentaje_agua'] = porcentaje
        
        print(f"\nTotal de áreas analizadas: {total_areas}")
        print(f"Áreas con agua: {areas_agua}")
        print(f"Porcentaje: {porcentaje:.2f}%")
        
        if areas_agua > 0:
            print(f"\nPromedio de cobertura de agua (en áreas con agua): {areas_con_agua[col_agua].mean():.2f}%")
            print(f"Máximo de cobertura de agua: {areas_con_agua[col_agua].max():.2f}%")
        
        # Gráfico de pie
        plt.figure(figsize=(10, 8))
        labels = ['Sin agua', 'Con agua']
        sizes = [total_areas - areas_agua, areas_agua]
        colors = ['lightcoral', 'lightblue']
        explode = (0, 0.1)
        
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Proporción de Áreas con Presencia de Agua', fontsize=14, fontweight='bold')
        plt.axis('equal')
        
        # Guardar
        output_path = Path('data/output/areas_con_agua.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n Gráfico guardado: {output_path}")
        plt.close()
        
        return areas_con_agua
    
    def analizar_correlaciones(self):
        """Analiza las correlaciones entre diferentes tipos de cobertura."""
        print("\n" + "=" * 60)
        print("🔗 ANÁLISIS DE CORRELACIONES")
        print("=" * 60)
        
        columnas_existentes = [col for col in self.columnas_cobertura if col in self.df.columns]
        
        if len(columnas_existentes) < 2:
            print("⚠️  No hay suficientes columnas para análisis de correlación")
            return None
        
        # Calcular matriz de correlación
        correlaciones = self.df[columnas_existentes].corr()
        self.resultados['correlaciones'] = correlaciones
        
        print("\nMatriz de correlación:")
        print(correlaciones)
        
        # Crear heatmap
        plt.figure(figsize=(12, 10))
        nombres = [self.nombres_cobertura.get(col, col) for col in columnas_existentes]
        
        sns.heatmap(correlaciones, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, linewidths=1,
                   xticklabels=nombres, yticklabels=nombres,
                   cbar_kws={'label': 'Coeficiente de Correlación'})
        
        plt.title('Correlaciones entre Tipos de Cobertura del Suelo', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        # Guardar
        output_path = Path('data/output/correlaciones_cobertura.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n Heatmap de correlación guardado: {output_path}")
        plt.close()
        
        return correlaciones
    
    def analizar_vegetacion_urbano(self):
        """Compara áreas de vegetación vs áreas urbanas."""
        print("\n" + "=" * 60)
        print("🌳 VEGETACIÓN VS URBANO")
        print("=" * 60)
        
        col_arboles = 'ceoTREES_CANOPYCOVER'
        col_edificios = 'ceoBuilding'
        col_impermeable = 'ceoImperviousSurface'
        
        columnas_necesarias = [col_arboles, col_edificios, col_impermeable]
        columnas_existentes = [col for col in columnas_necesarias if col in self.df.columns]
        
        if len(columnas_existentes) < 2:
            print("⚠️  No hay suficientes datos para este análisis")
            return None
        
        # Calcular índices
        if col_arboles in self.df.columns:
            vegetacion_promedio = self.df[col_arboles].mean()
        else:
            vegetacion_promedio = 0
        
        if col_edificios in self.df.columns and col_impermeable in self.df.columns:
            urbano_promedio = (self.df[col_edificios] + self.df[col_impermeable]).mean()
        elif col_edificios in self.df.columns:
            urbano_promedio = self.df[col_edificios].mean()
        elif col_impermeable in self.df.columns:
            urbano_promedio = self.df[col_impermeable].mean()
        else:
            urbano_promedio = 0
        
        print(f"\nÍndice de vegetación promedio: {vegetacion_promedio:.2f}%")
        print(f"Índice urbano promedio: {urbano_promedio:.2f}%")
        
        # Gráfico comparativo
        plt.figure(figsize=(10, 6))
        categorias = ['Vegetación\n(Árboles)', 'Desarrollo Urbano\n(Edificios + Impermeables)']
        valores = [vegetacion_promedio, urbano_promedio]
        colores = ['forestgreen', 'dimgray']
        
        bars = plt.bar(categorias, valores, color=colores, width=0.6)
        plt.title('Comparación: Vegetación vs Desarrollo Urbano', 
                 fontsize=14, fontweight='bold')
        plt.ylabel('Porcentaje Promedio de Cobertura')
        
        # Agregar valores
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{valor:.1f}%',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        plt.ylim(0, max(valores) * 1.2)
        plt.tight_layout()
        
        # Guardar
        output_path = Path('data/output/vegetacion_vs_urbano.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n Gráfico comparativo guardado: {output_path}")
        plt.close()
        
        return {'vegetacion': vegetacion_promedio, 'urbano': urbano_promedio}
    
    def resumen_completo(self):
        """Genera un resumen completo del análisis."""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE COBERTURA DEL SUELO")
        print("=" * 60)
        
        print(f"\n📈 ESTADÍSTICAS GENERALES:")
        print(f"   Total de observaciones: {len(self.df)}")
        
        if self.resultados.get('promedios') is not None:
            print(f"\n🌍 PROMEDIOS DE COBERTURA:")
            for col, valor in self.resultados['promedios'].items():
                nombre = self.nombres_cobertura.get(col, col)
                print(f"   {nombre}: {valor:.2f}%")
        
        if self.resultados.get('areas_con_agua'):
            print(f"\n💧 ÁREAS CON AGUA:")
            print(f"   Total: {self.resultados['areas_con_agua']}")
            print(f"   Porcentaje: {self.resultados['porcentaje_agua']:.2f}%")
        
        print("\n" + "=" * 60)
    
    def ejecutar_analisis_completo(self):
        """Ejecuta todos los análisis disponibles."""
        print("\n🚀 INICIANDO ANÁLISIS COMPLETO DE COBERTURA DEL SUELO\n")
        
        self.analizar_promedios()
        self.analizar_distribucion()
        self.analizar_areas_con_agua()
        self.analizar_correlaciones()
        self.analizar_vegetacion_urbano()
        self.resumen_completo()
        
        print("\n ANÁLISIS DE COBERTURA COMPLETO FINALIZADO")
        print("📁 Revisa la carpeta 'data/output/' para ver los resultados\n")
        
        return self.resultados


if __name__ == "__main__":
    # Ejemplo de uso
    from utils.data_loader import DataLoader
    
    loader = DataLoader()
    loader.cargar_todos()
    
    analizador = AnalizadorCobertura(loader.get_imagery())
    analizador.ejecutar_analisis_completo()
