"""
Módulo de análisis de datos de mosquitos.
Incluye estadísticas, visualizaciones y mapas de calor.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap, MarkerCluster
from pathlib import Path


class AnalizadorMosquitos:
    """Analiza datos de reportes de mosquitos."""
    
    def __init__(self, df_mosquitos):
        """
        Inicializa el analizador.
        
        Args:
            df_mosquitos: DataFrame con datos de mosquitos
        """
        self.df = df_mosquitos
        self.resultados = {}
    
    def analizar_especies(self):
        """Analiza las especies de mosquitos reportadas."""
        print("=" * 60)
        print("🦟 ANÁLISIS DE ESPECIES DE MOSQUITOS")
        print("=" * 60)
        
        if 'mosquitohabitatmapperGenus' not in self.df.columns:
            print("⚠️  Columna de especies no encontrada")
            return None
        
        especies = self.df['mosquitohabitatmapperGenus'].value_counts()
        self.resultados['especies'] = especies
        
        print("\nEspecies de mosquitos reportadas:")
        print(especies)
        
        # Crear gráfico
        plt.figure(figsize=(12, 6))
        especies.head(10).plot(kind='bar', color='darkred')
        plt.title('Top 10 Especies de Mosquitos Reportadas', fontsize=14, fontweight='bold')
        plt.xlabel('Especie')
        plt.ylabel('Número de Reportes')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Guardar
        output_path = Path('data/output/especies_mosquitos.png')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✅ Gráfico guardado: {output_path}")
        plt.close()
        
        return especies
    
    def analizar_fuentes_agua(self):
        """Analiza las fuentes de agua donde se encuentran mosquitos."""
        print("\n" + "=" * 60)
        print("💧 ANÁLISIS DE FUENTES DE AGUA")
        print("=" * 60)
        
        if 'mosquitohabitatmapperWaterSource' not in self.df.columns:
            print("⚠️  Columna de fuentes de agua no encontrada")
            return None
        
        fuentes = self.df['mosquitohabitatmapperWaterSource'].value_counts().head(15)
        self.resultados['fuentes_agua'] = fuentes
        
        print("\nFuentes de agua más comunes:")
        print(fuentes)
        
        # Crear gráfico
        plt.figure(figsize=(14, 7))
        fuentes.plot(kind='barh', color='steelblue')
        plt.title('Top 15 Fuentes de Agua para Mosquitos', fontsize=14, fontweight='bold')
        plt.xlabel('Número de Reportes')
        plt.ylabel('Tipo de Fuente')
        plt.tight_layout()
        
        # Guardar
        output_path = Path('data/output/fuentes_agua_mosquitos.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✅ Gráfico guardado: {output_path}")
        plt.close()
        
        return fuentes
    
    def analizar_temporal(self):
        """Analiza la distribución temporal de los reportes."""
        print("\n" + "=" * 60)
        print("📅 ANÁLISIS TEMPORAL")
        print("=" * 60)
        
        if 'mes' not in self.df.columns:
            print("⚠️  Columna de mes no encontrada")
            return None
        
        reportes_mensuales = self.df['mes'].value_counts().sort_index()
        self.resultados['reportes_mensuales'] = reportes_mensuales
        
        print("\nReportes por mes:")
        print(reportes_mensuales)
        
        # Crear gráfico
        meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        plt.figure(figsize=(12, 6))
        ax = reportes_mensuales.plot(kind='bar', color='forestgreen')
        plt.title('Reportes de Mosquitos por Mes (2020)', fontsize=14, fontweight='bold')
        plt.xlabel('Mes')
        plt.ylabel('Número de Reportes')
        
        # Personalizar etiquetas del eje x
        if len(reportes_mensuales) <= 12:
            labels = [meses_nombres[int(i)-1] if i <= 12 else str(i) 
                     for i in reportes_mensuales.index]
            ax.set_xticklabels(labels, rotation=45)
        
        plt.tight_layout()
        
        # Guardar
        output_path = Path('data/output/reportes_mensuales_mosquitos.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✅ Gráfico guardado: {output_path}")
        plt.close()
        
        return reportes_mensuales
    
    def analizar_larvas(self):
        """Analiza los reportes con presencia de larvas."""
        print("\n" + "=" * 60)
        print("🐛 ANÁLISIS DE LARVAS")
        print("=" * 60)
        
        # Buscar columna de larvas (puede tener diferentes nombres)
        columnas_larvas = [col for col in self.df.columns if 'larva' in col.lower()]
        
        if not columnas_larvas:
            print("⚠️  Columna de larvas no encontrada")
            return None
        
        columna_larvas = columnas_larvas[0]
        con_larvas = self.df[self.df[columna_larvas] > 0]
        
        print(f"\nTotal de reportes: {len(self.df)}")
        print(f"Reportes con larvas: {len(con_larvas)}")
        print(f"Porcentaje con larvas: {len(con_larvas)/len(self.df)*100:.2f}%")
        
        self.resultados['con_larvas'] = len(con_larvas)
        self.resultados['porcentaje_larvas'] = len(con_larvas)/len(self.df)*100
        
        return con_larvas
    
    def crear_mapa_calor(self, output='data/output/mapa_calor_mosquitos.html'):
        """
        Crea un mapa de calor de reportes de mosquitos.
        
        Args:
            output: Ruta del archivo HTML de salida
        """
        print("\n" + "=" * 60)
        print("🗺️  CREANDO MAPA DE CALOR")
        print("=" * 60)
        
        # Verificar columnas de coordenadas
        lat_col = 'mosquitohabitatmapperMeasurementLatitude'
        lon_col = 'mosquitohabitatmapperMeasurementLongitude'
        
        if lat_col not in self.df.columns or lon_col not in self.df.columns:
            print("⚠️  Columnas de coordenadas no encontradas")
            return None
        
        # Limpiar datos
        df_coords = self.df[[lat_col, lon_col]].dropna()
        
        if len(df_coords) == 0:
            print("⚠️  No hay coordenadas válidas")
            return None
        
        print(f"Puntos válidos: {len(df_coords)}")
        
        # Calcular centro del mapa
        centro_lat = df_coords[lat_col].mean()
        centro_lon = df_coords[lon_col].mean()
        
        print(f"Centro del mapa: ({centro_lat:.4f}, {centro_lon:.4f})")
        
        # Crear mapa base
        mapa = folium.Map(
            location=[centro_lat, centro_lon],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Preparar datos para mapa de calor
        heat_data = [[row[lat_col], row[lon_col]] for _, row in df_coords.iterrows()]
        
        # Agregar capa de calor
        HeatMap(
            heat_data,
            name='Mapa de Calor',
            min_opacity=0.3,
            max_zoom=13,
            radius=15,
            blur=25,
            gradient={0.4: 'blue', 0.6: 'lime', 0.8: 'orange', 1.0: 'red'}
        ).add_to(mapa)
        
        # Control de capas
        folium.LayerControl().add_to(mapa)
        
        # Guardar
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        mapa.save(output_path)
        
        print(f"\n✅ Mapa de calor guardado: {output_path}")
        
        return mapa
    
    def crear_mapa_marcadores(self, max_markers=500, output='data/output/mapa_marcadores_mosquitos.html'):
        """
        Crea un mapa con marcadores agrupados.
        
        Args:
            max_markers: Número máximo de marcadores a mostrar
            output: Ruta del archivo HTML de salida
        """
        print("\n" + "=" * 60)
        print("📍 CREANDO MAPA CON MARCADORES")
        print("=" * 60)
        
        # Verificar columnas
        lat_col = 'mosquitohabitatmapperMeasurementLatitude'
        lon_col = 'mosquitohabitatmapperMeasurementLongitude'
        
        if lat_col not in self.df.columns or lon_col not in self.df.columns:
            print("⚠️  Columnas de coordenadas no encontradas")
            return None
        
        # Limpiar y limitar datos
        df_sample = self.df.dropna(subset=[lat_col, lon_col]).head(max_markers)
        
        print(f"Mostrando {len(df_sample)} marcadores")
        
        # Calcular centro
        centro_lat = df_sample[lat_col].mean()
        centro_lon = df_sample[lon_col].mean()
        
        # Crear mapa
        mapa = folium.Map(
            location=[centro_lat, centro_lon],
            zoom_start=4,
            tiles='CartoDB positron'
        )
        
        # Agregar cluster de marcadores
        marker_cluster = MarkerCluster(name='Reportes de Mosquitos').add_to(mapa)
        
        # Agregar marcadores
        for idx, row in df_sample.iterrows():
            popup_text = f"""
            <b>Reporte #{idx}</b><br>
            <b>Especie:</b> {row.get('mosquitohabitatmapperGenus', 'N/A')}<br>
            <b>Fuente:</b> {row.get('mosquitohabitatmapperWaterSource', 'N/A')}<br>
            <b>Fecha:</b> {row.get('fecha', 'N/A')}
            """
            
            folium.Marker(
                location=[row[lat_col], row[lon_col]],
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color='red', icon='bug', prefix='fa')
            ).add_to(marker_cluster)
        
        # Control de capas
        folium.LayerControl().add_to(mapa)
        
        # Guardar
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        mapa.save(output_path)
        
        print(f"✅ Mapa con marcadores guardado: {output_path}")
        
        return mapa
    
    def resumen_completo(self):
        """Genera un resumen completo del análisis."""
        print("\n" + "=" * 60)
        print("📊 RESUMEN ESTADÍSTICO COMPLETO")
        print("=" * 60)
        
        print(f"\n📈 ESTADÍSTICAS GENERALES:")
        print(f"   Total de reportes: {len(self.df)}")
        print(f"   Rango de fechas: {self.df['fecha'].min()} a {self.df['fecha'].max()}")
        
        if 'mosquitohabitatmapperGenus' in self.df.columns:
            especies_unicas = self.df['mosquitohabitatmapperGenus'].nunique()
            print(f"   Especies únicas: {especies_unicas}")
        
        if 'mosquitohabitatmapperWaterSource' in self.df.columns:
            fuentes_unicas = self.df['mosquitohabitatmapperWaterSource'].nunique()
            print(f"   Tipos de fuentes de agua: {fuentes_unicas}")
        
        if self.resultados.get('con_larvas'):
            print(f"\n🐛 LARVAS:")
            print(f"   Reportes con larvas: {self.resultados['con_larvas']}")
            print(f"   Porcentaje: {self.resultados['porcentaje_larvas']:.2f}%")
        
        print("\n" + "=" * 60)
    
    def ejecutar_analisis_completo(self):
        """Ejecuta todos los análisis disponibles."""
        print("\n🚀 INICIANDO ANÁLISIS COMPLETO DE MOSQUITOS\n")
        
        self.analizar_especies()
        self.analizar_fuentes_agua()
        self.analizar_temporal()
        self.analizar_larvas()
        self.crear_mapa_calor()
        self.crear_mapa_marcadores()
        self.resumen_completo()
        
        print("\n✅ ANÁLISIS COMPLETO FINALIZADO")
        print("📁 Revisa la carpeta 'data/output/' para ver los resultados\n")
        
        return self.resultados


if __name__ == "__main__":
    # Ejemplo de uso
    from utils.data_loader import DataLoader
    
    loader = DataLoader()
    loader.cargar_todos()
    
    analizador = AnalizadorMosquitos(loader.get_mosquitos())
    analizador.ejecutar_analisis_completo()
