#!/usr/bin/env python3
"""
MAIN.PY - Análisis completo del proyecto Orbita-CodeCaster
==========================================================
Este script ejecuta todos los análisis y genera:
- Mapas interactivos HTML
- Reportes en formato TXT
- Visualizaciones guardadas como imágenes

Uso: python main.py
"""
import sys
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.data_loader import DataLoader
from src.analisis_mosquitos import AnalizadorMosquitos
from src.analisis_cobertura import AnalizadorCobertura
from src.prediccion import PredictorMosquitos
import folium
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd


class GeneradorReportes:
    """Genera todos los reportes y mapas del proyecto."""
    
    def __init__(self, output_dir="data/output"):
        """
        Inicializa el generador de reportes.
        
        Args:
            output_dir: Directorio donde guardar los resultados
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.reporte_txt = []
        
    def log(self, mensaje, nivel="INFO"):
        """Agrega un mensaje al reporte."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        linea = f"[{timestamp}] {nivel}: {mensaje}"
        print(linea)
        self.reporte_txt.append(linea + "\n")
    
    def separador(self, titulo=""):
        """Agrega un separador visual al reporte."""
        linea = "\n" + "=" * 80 + "\n"
        if titulo:
            linea += f"  {titulo}\n"
            linea += "=" * 80 + "\n"
        self.reporte_txt.append(linea)
        print(linea.strip())
    
    def guardar_reporte_txt(self):
        """Guarda el reporte en archivo TXT."""
        archivo = self.output_dir / f"reporte_completo_{self.timestamp}.txt"
        with open(archivo, 'w', encoding='utf-8') as f:
            f.writelines(self.reporte_txt)
        self.log(f"✅ Reporte guardado: {archivo}")
        return archivo
    
    def crear_mapa_mosquitos(self, df_mosquitos):
        """
        Crea un mapa interactivo con reportes de mosquitos.
        
        Args:
            df_mosquitos: DataFrame con datos de mosquitos
        
        Returns:
            Ruta del archivo HTML generado
        """
        self.separador("GENERANDO MAPA DE MOSQUITOS")
        
        # Filtrar coordenadas válidas
        df_coords = df_mosquitos[[
            'mosquitohabitatmapperMeasurementLatitude',
            'mosquitohabitatmapperMeasurementLongitude',
            'mosquitohabitatmapperGenus',
            'mosquitohabitatmapperWaterSource',
            'mosquitohabitatmapperMeasuredAt'
        ]].dropna(subset=[
            'mosquitohabitatmapperMeasurementLatitude',
            'mosquitohabitatmapperMeasurementLongitude'
        ])
        
        self.log(f"Procesando {len(df_coords)} reportes con coordenadas válidas")
        
        # Calcular centro del mapa
        centro_lat = df_coords['mosquitohabitatmapperMeasurementLatitude'].mean()
        centro_lon = df_coords['mosquitohabitatmapperMeasurementLongitude'].mean()
        
        # Crear mapa base
        mapa = folium.Map(
            location=[centro_lat, centro_lon],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Agregar capa de calor
        heat_data = [[
            row['mosquitohabitatmapperMeasurementLatitude'],
            row['mosquitohabitatmapperMeasurementLongitude']
        ] for idx, row in df_coords.iterrows()]
        
        HeatMap(
            heat_data,
            name='Mapa de Calor',
            radius=15,
            blur=25,
            max_zoom=13
        ).add_to(mapa)
        
        # Agregar cluster de marcadores
        marker_cluster = MarkerCluster(name='Reportes Individuales').add_to(mapa)
        
        # Colores por especie
        colores_especies = {
            'Aedes': 'red',
            'Culex': 'orange',
            'Anopheles': 'darkred',
            'Other': 'blue'
        }
        
        for idx, row in df_coords.iterrows():
            especie = row.get('mosquitohabitatmapperGenus', 'Desconocida')
            color = colores_especies.get(especie, 'gray')
            
            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px; width: 200px;">
                <h4 style="margin: 0 0 10px 0; color: #333;">🦟 Reporte de Mosquito</h4>
                <p><b>Especie:</b> {especie}</p>
                <p><b>Fuente de agua:</b> {row.get('mosquitohabitatmapperWaterSource', 'N/A')}</p>
                <p><b>Fecha:</b> {row.get('mosquitohabitatmapperMeasuredAt', 'N/A')}</p>
                <p><b>Coordenadas:</b><br>
                   Lat: {row['mosquitohabitatmapperMeasurementLatitude']:.4f}<br>
                   Lon: {row['mosquitohabitatmapperMeasurementLongitude']:.4f}
                </p>
            </div>
            """
            
            folium.Marker(
                location=[
                    row['mosquitohabitatmapperMeasurementLatitude'],
                    row['mosquitohabitatmapperMeasurementLongitude']
                ],
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.Icon(color=color, icon='bug', prefix='fa')
            ).add_to(marker_cluster)
        
        # Agregar leyenda
        leyenda_html = """
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; 
                    width: 200px; height: auto; 
                    background-color: white; 
                    border:2px solid grey; 
                    z-index:9999; 
                    font-size:14px;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);">
            <h4 style="margin: 0 0 10px 0;">🦟 Especies</h4>
            <p><i class="fa fa-circle" style="color:red"></i> Aedes</p>
            <p><i class="fa fa-circle" style="color:orange"></i> Culex</p>
            <p><i class="fa fa-circle" style="color:darkred"></i> Anopheles</p>
            <p><i class="fa fa-circle" style="color:gray"></i> Otras</p>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(leyenda_html))
        
        # Agregar control de capas
        folium.LayerControl().add_to(mapa)
        
        # Guardar mapa
        archivo_html = self.output_dir / f"mapa_mosquitos_{self.timestamp}.html"
        mapa.save(str(archivo_html))
        
        self.log(f"✅ Mapa de mosquitos guardado: {archivo_html}")
        self.reporte_txt.append(f"\n📍 Mapa interactivo: {archivo_html}\n")
        self.reporte_txt.append(f"   Centro del mapa: ({centro_lat:.4f}, {centro_lon:.4f})\n")
        self.reporte_txt.append(f"   Total de puntos: {len(df_coords)}\n")
        
        return archivo_html
    
    def crear_mapa_cobertura(self, df_imagery):
        """
        Crea un mapa con análisis de cobertura del suelo.
        
        Args:
            df_imagery: DataFrame con datos de imagery
        
        Returns:
            Ruta del archivo HTML generado
        """
        self.separador("GENERANDO MAPA DE COBERTURA DEL SUELO")
        
        # Filtrar datos con coordenadas
        if 'LONGITUDE' in df_imagery.columns and 'LATITUDE' in df_imagery.columns:
            df_coords = df_imagery[['LATITUDE', 'LONGITUDE', 
                                    'ceoWaterLakePondedContainer']].dropna()
        else:
            self.log("⚠️  No se encontraron columnas de coordenadas en imagery", "WARNING")
            return None
        
        self.log(f"Procesando {len(df_coords)} observaciones de cobertura")
        
        # Calcular centro
        centro_lat = df_coords['LATITUDE'].mean()
        centro_lon = df_coords['LONGITUDE'].mean()
        
        # Crear mapa
        mapa = folium.Map(
            location=[centro_lat, centro_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Agregar marcadores para áreas con agua
        areas_agua = df_coords[df_coords['ceoWaterLakePondedContainer'] > 0]
        
        for idx, row in areas_agua.iterrows():
            folium.CircleMarker(
                location=[row['LATITUDE'], row['LONGITUDE']],
                radius=5,
                popup=f"Agua: {row['ceoWaterLakePondedContainer']:.1f}%",
                color='blue',
                fill=True,
                fillColor='cyan',
                fillOpacity=0.6
            ).add_to(mapa)
        
        # Guardar
        archivo_html = self.output_dir / f"mapa_cobertura_{self.timestamp}.html"
        mapa.save(str(archivo_html))
        
        self.log(f"✅ Mapa de cobertura guardado: {archivo_html}")
        self.reporte_txt.append(f"\n🌍 Mapa de cobertura: {archivo_html}\n")
        self.reporte_txt.append(f"   Áreas con agua detectadas: {len(areas_agua)}\n")
        
        return archivo_html


def main():
    """Función principal que ejecuta todos los análisis."""
    print("\n" + "=" * 80)
    print("  🌍 ORBITA-CODECASTER - ANÁLISIS COMPLETO")
    print("=" * 80 + "\n")
    
    # Inicializar generador de reportes
    generador = GeneradorReportes()
    generador.separador("INICIANDO ANÁLISIS")
    
    try:
        # 1. CARGAR DATOS
        generador.separador("1. CARGANDO DATOS")
        loader = DataLoader()
        loader.cargar_todos()
        
        # Obtener dataframes
        df_mosquitos = loader.get_mosquitos()
        df_imagery = loader.get_imagery()
        
        generador.log(f"✅ Datos de mosquitos: {len(df_mosquitos)} registros")
        generador.log(f"✅ Datos de imagery: {len(df_imagery)} registros")
        
        # 2. ANÁLISIS DE MOSQUITOS
        generador.separador("2. ANÁLISIS DE MOSQUITOS")
        analizador_mosquitos = AnalizadorMosquitos(df_mosquitos)
        
        # Estadísticas
        generador.reporte_txt.append("\n📊 ESTADÍSTICAS DE MOSQUITOS:\n")
        generador.reporte_txt.append("-" * 80 + "\n")
        
        especies = df_mosquitos['mosquitohabitatmapperGenus'].value_counts()
        generador.reporte_txt.append("\n🦟 Especies reportadas:\n")
        for especie, count in especies.items():
            generador.reporte_txt.append(f"   - {especie}: {count} reportes\n")
        
        fuentes = df_mosquitos['mosquitohabitatmapperWaterSource'].value_counts().head(10)
        generador.reporte_txt.append("\n💧 Fuentes de agua más comunes:\n")
        for fuente, count in fuentes.items():
            generador.reporte_txt.append(f"   - {fuente}: {count} reportes\n")
        
        # Análisis temporal
        generador.log("Analizando datos temporales...")
        reportes_mes = df_mosquitos['mes'].value_counts().sort_index()
        generador.reporte_txt.append("\n📅 Reportes por mes:\n")
        for mes, count in reportes_mes.items():
            generador.reporte_txt.append(f"   Mes {mes}: {count} reportes\n")
        
        # 3. ANÁLISIS DE COBERTURA
        generador.separador("3. ANÁLISIS DE COBERTURA DEL SUELO")
        analizador_cobertura = AnalizadorCobertura(df_imagery)
        
        # Ejecutar análisis de promedios (imprime directamente)
        analizador_cobertura.analizar_promedios()
        
        # Capturar resultados si están disponibles
        if hasattr(analizador_cobertura, 'resultados') and analizador_cobertura.resultados:
            generador.reporte_txt.append("\n🌳 PROMEDIOS DE COBERTURA DEL SUELO:\n")
            generador.reporte_txt.append("-" * 80 + "\n")
            if 'promedios' in analizador_cobertura.resultados:
                for tipo, valor in analizador_cobertura.resultados['promedios'].items():
                    generador.reporte_txt.append(f"   {tipo}: {valor:.2f}%\n")
        
        generador.log("Análisis de cobertura completado")
        
        # 4. MODELO PREDICTIVO
        generador.separador("4. MODELO PREDICTIVO")
        try:
            modelo_pred = PredictorMosquitos(df_imagery)
            modelo_pred.preparar_datos()
            precision = modelo_pred.entrenar_modelo()
            
            generador.reporte_txt.append("\n🤖 MODELO PREDICTIVO:\n")
            generador.reporte_txt.append("-" * 80 + "\n")
            generador.reporte_txt.append(f"   Precisión del modelo: {precision:.2%}\n")
            generador.reporte_txt.append(f"   Algoritmo: Random Forest\n")
            generador.reporte_txt.append(f"   Variable objetivo: Presencia de agua\n")
            
            generador.log(f"✅ Modelo entrenado con precisión: {precision:.2%}")
        except Exception as e:
            generador.log(f"⚠️  Error en modelo predictivo: {str(e)}", "WARNING")
        
        # 5. GENERAR MAPAS
        generador.separador("5. GENERANDO MAPAS INTERACTIVOS")
        
        # Mapa de mosquitos
        mapa_mosquitos = generador.crear_mapa_mosquitos(df_mosquitos)
        
        # Mapa de cobertura
        mapa_cobertura = generador.crear_mapa_cobertura(df_imagery)
        
        # 6. GUARDAR REPORTE FINAL
        generador.separador("6. GUARDANDO REPORTE FINAL")
        
        generador.reporte_txt.append("\n" + "=" * 80 + "\n")
        generador.reporte_txt.append("  📋 RESUMEN FINAL\n")
        generador.reporte_txt.append("=" * 80 + "\n")
        generador.reporte_txt.append(f"\n✅ Análisis completado exitosamente\n")
        generador.reporte_txt.append(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        generador.reporte_txt.append(f"\n📁 Archivos generados:\n")
        generador.reporte_txt.append(f"   - Mapa de mosquitos: {mapa_mosquitos.name}\n")
        if mapa_cobertura:
            generador.reporte_txt.append(f"   - Mapa de cobertura: {mapa_cobertura.name}\n")
        generador.reporte_txt.append(f"   - Gráficos: Ver carpeta {generador.output_dir}/\n")
        
        archivo_reporte = generador.guardar_reporte_txt()
        
        # MENSAJE FINAL
        print("\n" + "=" * 80)
        print("  ✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        print(f"\n📁 Todos los archivos se guardaron en: {generador.output_dir}/")
        print(f"\n📄 Reporte completo: {archivo_reporte}")
        print(f"🗺️  Mapa de mosquitos: {mapa_mosquitos}")
        if mapa_cobertura:
            print(f"🌍 Mapa de cobertura: {mapa_cobertura}")
        print("\n🌐 Abre los archivos HTML en tu navegador para ver los mapas interactivos")
        print("=" * 80 + "\n")
        
    except Exception as e:
        generador.log(f"❌ ERROR CRÍTICO: {str(e)}", "ERROR")
        generador.guardar_reporte_txt()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
