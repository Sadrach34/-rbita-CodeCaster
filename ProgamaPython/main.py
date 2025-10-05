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

# Configure matplotlib to use non-interactive backend before any other imports
import matplotlib
matplotlib.use('Agg')

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.data_loader import DataLoader
from src.analisis_mosquitos import AnalizadorMosquitos
from src.analisis_cobertura import AnalizadorCobertura
from src.prediccion import PredictorMosquitos
from src.prediccion_temporal import PredictorTemporal
from src.reporte_html import GeneradorReporteHTML
import folium
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd
import matplotlib.pyplot as plt


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
        
        # Eliminar archivos anteriores
        self._limpiar_archivos_anteriores()
    
    def _limpiar_archivos_anteriores(self):
        """Elimina todos los archivos del output excepto .gitkeep."""
        print("\n Limpiando directorio de salida...")
        
        archivos_eliminados = 0
        
        # Listar todos los archivos en output
        for archivo in self.output_dir.iterdir():
            # No eliminar .gitkeep ni directorios
            if archivo.name == '.gitkeep' or archivo.is_dir():
                continue
            
            try:
                archivo.unlink()
                archivos_eliminados += 1
            except Exception as e:
                print(f"No se pudo eliminar {archivo.name}: {e}")
        
        if archivos_eliminados > 0:
            print(f"Eliminados {archivos_eliminados} archivos anteriores")
            print()  # Línea en blanco para separar
        
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
        self.log(f"Reporte guardado: {archivo}")
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
        
        self.log(f"Mapa de mosquitos guardado: {archivo_html}")
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
            self.log("⚠️No se encontraron columnas de coordenadas en imagery", "WARNING")
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
        
        self.log(f"Mapa de cobertura guardado: {archivo_html}")
        self.reporte_txt.append(f"\n🌍 Mapa de cobertura: {archivo_html}\n")
        self.reporte_txt.append(f"   Áreas con agua detectadas: {len(areas_agua)}\n")
        
        return archivo_html
    
    def crear_mapa_plantas(self, df_landcover):
        """
        Crea un mapa interactivo con datos de plantas y cobertura terrestre.
        
        Args:
            df_landcover: DataFrame con datos de cobertura terrestre (LandCover)
        
        Returns:
            Ruta del archivo HTML generado
        """
        self.separador("GENERANDO MAPA DE PLANTAS Y VEGETACIÓN")
        
        # Filtrar coordenadas válidas
        df_coords = df_landcover[[
            'landcoversMeasurementLatitude',
            'landcoversMeasurementLongitude',
            'landcoversMucDescription',
            'landcoversLeavesOnTrees',
            'landcoversDryGround',
            'landcoversMuddy',
            'landcoversStandingWater',
            'landcoversMeasuredAt',
            'landcoversFieldNotes'
        ]].dropna(subset=[
            'landcoversMeasurementLatitude',
            'landcoversMeasurementLongitude'
        ])
        
        self.log(f"Procesando {len(df_coords)} observaciones de cobertura terrestre")
        
        # Calcular centro del mapa
        centro_lat = df_coords['landcoversMeasurementLatitude'].mean()
        centro_lon = df_coords['landcoversMeasurementLongitude'].mean()
        
        # Crear mapa base con diferentes tiles
        mapa = folium.Map(
            location=[centro_lat, centro_lon],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Agregar tiles satelitales
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Vista Satélite',
            overlay=False,
            control=True
        ).add_to(mapa)
        
        # Definir colores según tipo de vegetación
        colores_vegetacion = {
            'Trees': '#228B22',  # Verde bosque
            'Shrubs': '#90EE90',  # Verde claro
            'Herbaceous': '#7CFC00',  # Verde lima
            'Urban': '#808080',  # Gris
            'Barren': '#D2B48C',  # Marrón claro
            'Water': '#4169E1',  # Azul
            'Other': '#DDA0DD'  # Púrpura claro
        }
        
        # Crear grupos de capas para diferentes tipos de vegetación
        grupos_capas = {}
        for tipo in colores_vegetacion.keys():
            grupos_capas[tipo] = folium.FeatureGroup(name=f'🌿 {tipo}')
        
        # Agregar marcadores por cada observación
        for idx, row in df_coords.iterrows():
            descripcion = str(row.get('landcoversMucDescription', 'Desconocido'))
            
            # Determinar tipo de vegetación
            tipo_veg = 'Other'
            for tipo in colores_vegetacion.keys():
                if tipo.lower() in descripcion.lower():
                    tipo_veg = tipo
                    break
            
            color = colores_vegetacion[tipo_veg]
            
            # Iconos según características
            if row.get('landcoversLeavesOnTrees', False):
                icon = 'tree'
                icon_color = 'green'
            elif row.get('landcoversStandingWater', False):
                icon = 'tint'
                icon_color = 'blue'
            elif 'urban' in descripcion.lower():
                icon = 'building'
                icon_color = 'gray'
            else:
                icon = 'leaf'
                icon_color = 'lightgreen'
            
            # Crear popup informativo
            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px; width: 280px;">
                <h4 style="margin: 0 0 10px 0; color: #2E7D32;">🌿 Observación de Vegetación</h4>
                <p><b>Tipo de cobertura:</b> {descripcion}</p>
                <p><b>Características:</b></p>
                <ul style="margin: 5px 0; padding-left: 20px;">
                    <li>Hojas en árboles: {'✓ Sí' if row.get('landcoversLeavesOnTrees', False) else '✗ No'}</li>
                    <li>Suelo seco: {'✓ Sí' if row.get('landcoversDryGround', False) else '✗ No'}</li>
                    <li>Suelo fangoso: {'✓ Sí' if row.get('landcoversMuddy', False) else '✗ No'}</li>
                    <li>Agua estancada: {'✓ Sí' if row.get('landcoversStandingWater', False) else '✗ No'}</li>
                </ul>
                <p><b>Fecha:</b> {row.get('landcoversMeasuredAt', 'N/A')}</p>
                <p><b>Notas:</b> {str(row.get('landcoversFieldNotes', 'Sin notas'))[:100]}</p>
                <p style="font-size: 10px; color: #666;">
                   <b>Coordenadas:</b><br>
                   Lat: {row['landcoversMeasurementLatitude']:.5f}<br>
                   Lon: {row['landcoversMeasurementLongitude']:.5f}
                </p>
            </div>
            """
            
            # Crear marcador
            marker = folium.CircleMarker(
                location=[
                    row['landcoversMeasurementLatitude'],
                    row['landcoversMeasurementLongitude']
                ],
                radius=8,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{descripcion}",
                color=color,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            )
            
            # Agregar al grupo correspondiente
            marker.add_to(grupos_capas[tipo_veg])
        
        # Agregar todos los grupos al mapa
        for grupo in grupos_capas.values():
            grupo.add_to(mapa)
        
        # Crear mapa de calor para densidad de vegetación
        heat_data = [[
            row['landcoversMeasurementLatitude'],
            row['landcoversMeasurementLongitude']
        ] for idx, row in df_coords.iterrows()]
        
        heat_group = folium.FeatureGroup(name='Mapa de Calor - Densidad')
        HeatMap(
            heat_data,
            radius=15,
            blur=20,
            max_zoom=10,
            gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'}
        ).add_to(heat_group)
        heat_group.add_to(mapa)
        
        # Agregar leyenda personalizada
        leyenda_html = """
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; 
                    width: 220px; height: auto; 
                    background-color: white; 
                    border:2px solid #2E7D32; 
                    z-index:9999; 
                    font-size:12px;
                    padding: 12px;
                    border-radius: 8px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.3);">
            <h4 style="margin: 0 0 10px 0; color: #2E7D32; border-bottom: 2px solid #2E7D32; padding-bottom: 5px;">
                🌿 Tipos de Vegetación
            </h4>
            <p style="margin: 5px 0;"><span style="color:#228B22;">●</span> Árboles (Trees)</p>
            <p style="margin: 5px 0;"><span style="color:#90EE90;">●</span> Arbustos (Shrubs)</p>
            <p style="margin: 5px 0;"><span style="color:#7CFC00;">●</span> Herbáceas (Grass)</p>
            <p style="margin: 5px 0;"><span style="color:#808080;">●</span> Urbano</p>
            <p style="margin: 5px 0;"><span style="color:#D2B48C;">●</span> Tierra desnuda</p>
            <p style="margin: 5px 0;"><span style="color:#4169E1;">●</span> Agua</p>
            <p style="margin: 5px 0;"><span style="color:#DDA0DD;">●</span> Otros</p>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(leyenda_html))
        
        # Agregar control de capas
        folium.LayerControl(collapsed=False).add_to(mapa)
        
        # Agregar título al mapa
        titulo_html = """
        <div style="position: fixed; 
                    top: 10px; left: 50px; 
                    width: 400px; height: 60px; 
                    background-color: rgba(255, 255, 255, 0.9); 
                    border:2px solid #2E7D32;
                    border-radius: 8px;
                    z-index:9999; 
                    font-size:16px;
                    padding: 10px;
                    text-align: center;">
            <h3 style="margin: 0; color: #2E7D32;">🌍 Mapa de Cobertura Vegetal</h3>
            <p style="margin: 5px 0; font-size: 12px; color: #666;">
                Datos GLOBE Observer - Análisis de Plantas
            </p>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(titulo_html))
        
        # Guardar mapa
        archivo_html = self.output_dir / f"mapa_plantas_{self.timestamp}.html"
        mapa.save(str(archivo_html))

        self.log(f"Mapa de plantas guardado: {archivo_html}")
        self.reporte_txt.append(f"Mapa de plantas y vegetación: {archivo_html}\n")
        self.reporte_txt.append(f"   Centro del mapa: ({centro_lat:.4f}, {centro_lon:.4f})\n")
        self.reporte_txt.append(f"   Total de observaciones: {len(df_coords)}\n")
        
        # Estadísticas por tipo
        for tipo, grupo in grupos_capas.items():
            count = len([layer for layer in grupo._children.values()])
            if count > 0:
                self.reporte_txt.append(f"   - {tipo}: {count} puntos\n")
        
        return archivo_html
    
    def crear_mapa_unificado(self, df_mosquitos, df_imagery, df_landcover):
        """
        Crea un mapa con todos los datos: mosquitos, cobertura y plantas.
        
        Args:
            df_mosquitos: DataFrame con datos de mosquitos
            df_imagery: DataFrame con datos de imagery
            df_landcover: DataFrame con datos de cobertura terrestre
        
        Returns:
            Ruta del archivo HTML generado
        """
        self.separador("GENERANDO MAPA")
        
        # Calcular centro global basado en todos los datos
        todas_lats = []
        todas_lons = []
        
        # Coordenadas de mosquitos
        df_mosq = df_mosquitos[[
            'mosquitohabitatmapperMeasurementLatitude',
            'mosquitohabitatmapperMeasurementLongitude',
            'mosquitohabitatmapperGenus',
            'mosquitohabitatmapperWaterSource',
            'mosquitohabitatmapperMeasuredAt'
        ]].dropna(subset=['mosquitohabitatmapperMeasurementLatitude',
                          'mosquitohabitatmapperMeasurementLongitude'])
        todas_lats.extend(df_mosq['mosquitohabitatmapperMeasurementLatitude'].tolist())
        todas_lons.extend(df_mosq['mosquitohabitatmapperMeasurementLongitude'].tolist())
        
        # Coordenadas de imagery
        if 'LATITUDE' in df_imagery.columns and 'LONGITUDE' in df_imagery.columns:
            df_img = df_imagery[['LATITUDE', 'LONGITUDE']].dropna()
            todas_lats.extend(df_img['LATITUDE'].tolist())
            todas_lons.extend(df_img['LONGITUDE'].tolist())
        
        # Coordenadas de landcover
        df_land = df_landcover[[
            'landcoversMeasurementLatitude',
            'landcoversMeasurementLongitude',
            'landcoversMucDescription',
            'landcoversLeavesOnTrees',
            'landcoversStandingWater'
        ]].dropna(subset=['landcoversMeasurementLatitude',
                          'landcoversMeasurementLongitude'])
        todas_lats.extend(df_land['landcoversMeasurementLatitude'].tolist())
        todas_lons.extend(df_land['landcoversMeasurementLongitude'].tolist())
        
        centro_lat = sum(todas_lats) / len(todas_lats)
        centro_lon = sum(todas_lons) / len(todas_lons)

        self.log(f"Centro del mapa: ({centro_lat:.4f}, {centro_lon:.4f})")

        # Crear mapa base
        mapa = folium.Map(
            location=[centro_lat, centro_lon],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Agregar tiles adicionales
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='🛰️ Vista Satélite',
            overlay=False,
            control=True
        ).add_to(mapa)
        
        # ==================== CAPA 1: MOSQUITOS ====================
        self.log("Agregando capa de mosquitos...")
        grupo_mosquitos = folium.FeatureGroup(name='🦟 Mosquitos', show=True)
        
        colores_especies = {
            'Aedes': 'red',
            'Culex': 'orange',
            'Anopheles': 'darkred',
            'Other': 'blue'
        }
        
        for idx, row in df_mosq.iterrows():
            especie = str(row.get('mosquitohabitatmapperGenus', 'Desconocida'))
            color = colores_especies.get(especie, 'gray')
            
            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px; width: 200px;">
                <h4 style="margin: 0 0 10px 0; color: #d32f2f;">🦟 Reporte de Mosquito</h4>
                <p><b>Especie:</b> {especie}</p>
                <p><b>Fuente de agua:</b> {str(row.get('mosquitohabitatmapperWaterSource', 'N/A'))}</p>
                <p><b>Fecha:</b> {str(row.get('mosquitohabitatmapperMeasuredAt', 'N/A'))}</p>
            </div>
            """
            
            folium.CircleMarker(
                location=[row['mosquitohabitatmapperMeasurementLatitude'],
                         row['mosquitohabitatmapperMeasurementLongitude']],
                radius=6,
                popup=folium.Popup(popup_html, max_width=220),
                tooltip=f"Mosquito: {especie}",
                color=color,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(grupo_mosquitos)
        
        grupo_mosquitos.add_to(mapa)
        
        # Mapa de calor de mosquitos
        heat_mosquitos = folium.FeatureGroup(name='🔥 Calor - Mosquitos', show=False)
        heat_data_mosq = [[row['mosquitohabitatmapperMeasurementLatitude'],
                          row['mosquitohabitatmapperMeasurementLongitude']]
                         for idx, row in df_mosq.iterrows()]
        HeatMap(heat_data_mosq, radius=15, blur=25, max_zoom=13,
                gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'}
        ).add_to(heat_mosquitos)
        heat_mosquitos.add_to(mapa)
        
        # ==================== CAPA 2: COBERTURA DEL SUELO ====================
        self.log("Agregando capa de cobertura del suelo...")
        grupo_cobertura = folium.FeatureGroup(name='🌍 Cobertura del Suelo', show=False)
        
        if 'LATITUDE' in df_imagery.columns and 'LONGITUDE' in df_imagery.columns:
            df_img_agua = df_img.merge(
                df_imagery[['LATITUDE', 'LONGITUDE', 'ceoWaterLakePondedContainer']], 
                on=['LATITUDE', 'LONGITUDE']
            ).dropna()
            
            areas_agua = df_img_agua[df_img_agua['ceoWaterLakePondedContainer'] > 0]
            
            for idx, row in areas_agua.iterrows():
                folium.CircleMarker(
                    location=[row['LATITUDE'], row['LONGITUDE']],
                    radius=5,
                    popup=f"Agua: {row['ceoWaterLakePondedContainer']:.1f}%",
                    tooltip=f"Agua: {row['ceoWaterLakePondedContainer']:.1f}%",
                    color='blue',
                    fillColor='cyan',
                    fillOpacity=0.6,
                    weight=1
                ).add_to(grupo_cobertura)
        
        grupo_cobertura.add_to(mapa)
        
        # ==================== CAPA 3: PLANTAS Y VEGETACIÓN ====================
        self.log("Agregando capa de plantas y vegetación...")
        
        colores_vegetacion = {
            'Trees': '#228B22',
            'Shrubs': '#90EE90',
            'Herbaceous': '#7CFC00',
            'Urban': '#808080',
            'Barren': '#D2B48C',
            'Water': '#4169E1',
            'Other': '#DDA0DD'
        }
        
        # Crear grupos de plantas
        grupos_plantas = {}
        for tipo in colores_vegetacion.keys():
            grupos_plantas[tipo] = folium.FeatureGroup(name=f'🌿 Plantas - {tipo}', show=False)
        
        # Contador para verificar qué grupos tienen datos
        contadores = {tipo: 0 for tipo in colores_vegetacion.keys()}
        
        for idx, row in df_land.iterrows():
            descripcion = str(row.get('landcoversMucDescription', 'Desconocido'))
            
            # Determinar tipo de vegetación
            tipo_veg = 'Other'
            for tipo in ['Trees', 'Shrubs', 'Herbaceous', 'Urban', 'Barren', 'Water']:
                if tipo.lower() in descripcion.lower():
                    tipo_veg = tipo
                    break
            
            color = colores_vegetacion[tipo_veg]
            contadores[tipo_veg] += 1
            
            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px; width: 250px;">
                <h4 style="margin: 0 0 10px 0; color: #2E7D32;">🌿 Vegetación</h4>
                <p><b>Tipo:</b> {descripcion}</p>
                <p><b>Hojas en árboles:</b> {'✓' if row.get('landcoversLeavesOnTrees', False) else '✗'}</p>
                <p><b>Agua estancada:</b> {'✓' if row.get('landcoversStandingWater', False) else '✗'}</p>
            </div>
            """
            
            marker = folium.CircleMarker(
                location=[row['landcoversMeasurementLatitude'],
                         row['landcoversMeasurementLongitude']],
                radius=7,
                popup=folium.Popup(popup_html, max_width=270),
                tooltip=descripcion,
                color=color,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            )
            
            # Agregar marcador al grupo correspondiente
            marker.add_to(grupos_plantas[tipo_veg])
        
        # Solo agregar grupos que tengan marcadores
        for tipo, grupo in grupos_plantas.items():
            if contadores[tipo] > 0:
                grupo.add_to(mapa)
                self.log(f"  - {tipo}: {contadores[tipo]} puntos")
        
        # Mapa de calor de vegetación
        heat_plantas = folium.FeatureGroup(name='🔥 Calor - Vegetación', show=False)
        heat_data_plants = [[row['landcoversMeasurementLatitude'],
                            row['landcoversMeasurementLongitude']]
                           for idx, row in df_land.iterrows()]
        HeatMap(heat_data_plants, radius=12, blur=18, max_zoom=10,
                gradient={0.2: 'green', 0.4: 'lightgreen', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'}
        ).add_to(heat_plantas)
        heat_plantas.add_to(mapa)
        
        # ==================== LEYENDA Y CONTROLES ====================
        
        # Leyenda completa
        leyenda_html = """
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; 
                    width: 240px; max-height: 500px;
                    overflow-y: auto;
                    background-color: white; 
                    border:3px solid #1976D2; 
                    z-index:9999; 
                    font-size:11px;
                    padding: 12px;
                    border-radius: 8px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.3);">
            <h4 style="margin: 0 0 10px 0; color: #1976D2; border-bottom: 2px solid #1976D2; padding-bottom: 5px;">
                📊 Leyenda del Mapa
            </h4>
            
            <h5 style="margin: 10px 0 5px 0; color: #d32f2f;">🦟 Mosquitos</h5>
            <p style="margin: 3px 0;"><span style="color:red;">●</span> Aedes</p>
            <p style="margin: 3px 0;"><span style="color:orange;">●</span> Culex</p>
            <p style="margin: 3px 0;"><span style="color:darkred;">●</span> Anopheles</p>
            
            <h5 style="margin: 10px 0 5px 0; color: #1976D2;">🌍 Cobertura</h5>
            <p style="margin: 3px 0;"><span style="color:cyan;">●</span> Áreas con agua</p>
            
            <h5 style="margin: 10px 0 5px 0; color: #2E7D32;">🌿 Vegetación</h5>
            <p style="margin: 3px 0;"><span style="color:#228B22;">●</span> Árboles</p>
            <p style="margin: 3px 0;"><span style="color:#90EE90;">●</span> Arbustos</p>
            <p style="margin: 3px 0;"><span style="color:#7CFC00;">●</span> Herbáceas</p>
            <p style="margin: 3px 0;"><span style="color:#808080;">●</span> Urbano</p>
            <p style="margin: 3px 0;"><span style="color:#D2B48C;">●</span> Tierra desnuda</p>
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(leyenda_html))
        
        # Título con botón al reporte
        titulo_html = """

<div style="position: fixed;
            top: 20px; 
            left: 50%;
            transform: translateX(-50%);
            width: 480px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 12px;
            z-index: 9999;
            font-size: 14px;
            padding: 16px 20px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);">
    <h3 style="margin: 0; 
               color: white; 
               font-size: 18px;
               font-weight: 600;
               text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
        🌍 Mapa Unificado - Orbita CodeCaster
    </h3>
    <p style="margin: 8px 0 0 0; 
              font-size: 12px; 
              color: rgba(255,255,255,0.95);
              font-weight: 500;">
        Mosquitos 🦟 | Cobertura del Suelo 🌍 | Vegetación 🌿
    </p>
    <p style="margin: 4px 0 0 0; 
              font-size: 10px; 
              color: rgba(255,255,255,0.8);">
        Usa el control de capas para mostrar/ocultar datos
    </p>
</div>
        """
        mapa.get_root().html.add_child(folium.Element(titulo_html))
        
        # Control de capas
        folium.LayerControl(collapsed=False, position='topright').add_to(mapa)
        
        # Guardar mapa como mapa.html (archivo principal)
        archivo_html = self.output_dir / "mapa.html"
        mapa.save(str(archivo_html))
        
        self.log(f" Mapa guardado: {archivo_html}")
        self.reporte_txt.append(f"\n Mapa interactivo: {archivo_html}\n")
        self.reporte_txt.append(f"   Centro: ({centro_lat:.4f}, {centro_lon:.4f})\n")
        self.reporte_txt.append(f"   📊 Capas incluidas:\n")
        self.reporte_txt.append(f"      - Mosquitos: {len(df_mosq)} puntos\n")
        self.reporte_txt.append(f"      - Cobertura: {len(df_img) if 'df_img' in locals() else 0} puntos\n")
        self.reporte_txt.append(f"      - Vegetación: {len(df_land)} puntos\n")
        self.reporte_txt.append(f"      - Mapas de calor: 2 capas\n")
        
        return archivo_html


def main():
    """Función principal que ejecuta todos los análisis."""
    print("\n" + "=" * 80)
    print("ORBITA-CODECASTER - ANÁLISIS COMPLETO")
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
        df_landcover = loader.get_landcover()

        generador.log(f"Datos de mosquitos: {len(df_mosquitos)} registros")
        generador.log(f"Datos de imagery: {len(df_imagery)} registros")
        generador.log(f"Datos de cobertura terrestre (plantas): {len(df_landcover)} registros")

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
            
            generador.log(f"Modelo entrenado con precisión: {precision:.2%}")
        except Exception as e:
            generador.log(f"⚠️ Error en modelo predictivo: {str(e)}", "WARNING")
        
        # 4B. PREDICCIÓN TEMPORAL (NUEVO)
        generador.separador("4B. PREDICCIÓN TEMPORAL A 2 MESES")
        predictor_temporal = None
        resumen_prediccion = None
        
        try:
            predictor_temporal = PredictorTemporal(directorio_geojson="data/raw")
            resumen_prediccion = predictor_temporal.ejecutar_analisis_completo(meses_adelante=2)
            
            if resumen_prediccion:
                generador.reporte_txt.append("\n PREDICCIÓN TEMPORAL (2 MESES):\n")
                generador.reporte_txt.append("-" * 80 + "\n")
                generador.reporte_txt.append(f"   Periodo analizado: {resumen_prediccion['fecha_inicio']} a {resumen_prediccion['fecha_fin']}\n")
                generador.reporte_txt.append(f"   Predicción hasta: {resumen_prediccion['fecha_prediccion']}\n")
                generador.reporte_txt.append(f"   Observaciones: {resumen_prediccion['n_observaciones']}\n")
                
                generador.reporte_txt.append("\n   Precisión de modelos:\n")
                for metrica, info in resumen_prediccion['modelos'].items():
                    calidad = "Excelente" if info['r2'] > 0.9 else "Bueno" if info['r2'] > 0.7 else "Aceptable"
                    generador.reporte_txt.append(f"      • {metrica}: R² = {info['r2']:.4f} ({calidad})\n")
                
                generador.log(" Predicción temporal completada")
            else:
                generador.log(" No se pudieron generar predicciones temporales", "WARNING")
                
        except Exception as e:
            generador.log(f" Error en predicción temporal: {str(e)}", "WARNING")
            import traceback
            traceback.print_exc()
        
        # 5. GENERAR MAPA
        generador.separador("5. GENERANDO MAPA")
        
        # Solo generar el mapa (los 3 en 1)
        mapa_unificado = generador.crear_mapa_unificado(df_mosquitos, df_imagery, df_landcover)
        
        # 6. GENERAR REPORTE HTML INTERACTIVO
        generador.separador("6. GENERANDO REPORTE HTML INTERACTIVO")
        reporte_html_path = None
        
        if predictor_temporal and resumen_prediccion:
            try:
                generador.log("Creando reporte HTML con todas las visualizaciones...")
                
                reporte_html = GeneradorReporteHTML("Reporte Completo - Orbita CodeCaster")
                
                # Agregar métricas principales
                reporte_html.agregar_metrica(
                    "Archivos GeoJSON",
                    str(resumen_prediccion['n_observaciones']),
                    "Imágenes Sentinel-2 procesadas",
                    "📁"
                )
                
                reporte_html.agregar_metrica(
                    "Reportes de Mosquitos",
                    str(len(df_mosquitos)),
                    "Observaciones de campo",
                    "🦟"
                )
                
                reporte_html.agregar_metrica(
                    "Periodo Analizado",
                    f"{resumen_prediccion['fecha_inicio']} a {resumen_prediccion['fecha_fin']}",
                    "Rango de fechas",
                    "📅"
                )
                
                # Calcular R² promedio
                r2_promedio = sum(m['r2'] for m in resumen_prediccion['modelos'].values()) / len(resumen_prediccion['modelos'])
                reporte_html.agregar_metrica(
                    "Precisión Promedio",
                    f"{r2_promedio:.1%}",
                    "R² de modelos predictivos",
                    "🎯"
                )
                
                # Agregar sección de resumen
                reporte_html.agregar_seccion(
                    "📋 Resumen Ejecutivo",
                    f"""
                    Este reporte integra el análisis completo del proyecto Orbita-CodeCaster, incluyendo:
                    <br><br>
                    <b>🦟 Análisis de Mosquitos:</b> {len(df_mosquitos)} reportes de campo analizados
                    <br>
                    <b>🌍 Cobertura del Suelo:</b> {len(df_imagery)} observaciones de cobertura
                    <br>
                    <b>🌿 Vegetación:</b> {len(df_landcover)} puntos de cobertura terrestre
                    <br>
                    <b>🔮 Predicción Temporal:</b> Proyecciones hasta {resumen_prediccion['fecha_prediccion']}
                    <br><br>
                    Los modelos predictivos analizan datos satelitales Sentinel-2 para anticipar cambios
                    en vegetación, agua y cobertura terrestre en los próximos 2 meses.
                    """,
                    "texto"
                )
                
                # Agregar información de modelos
                modelos_info = []
                for metrica, info in resumen_prediccion['modelos'].items():
                    calidad = "Excelente" if info['r2'] > 0.9 else "Bueno" if info['r2'] > 0.7 else "Aceptable"
                    modelos_info.append(
                        f"✓ <b>{metrica.replace('_', ' ').title()}</b>: R² = {info['r2']:.4f} ({calidad}) | RMSE = {info['rmse']:.4f}"
                    )
                
                reporte_html.agregar_seccion(
                    "🤖 Modelos Predictivos",
                    modelos_info,
                    "lista"
                )
                
                # Agregar gráficos generados
                generador.log("Agregando visualizaciones al reporte HTML...")
                
                for nombre, fig in predictor_temporal.figuras:
                    if nombre == 'series_temporales':
                        reporte_html.agregar_grafico(
                            fig,
                            "Series Temporales Históricas",
                            "Análisis de series temporales de todas las métricas espectrales observadas."
                        )
                    elif nombre == 'predicciones':
                        reporte_html.agregar_grafico(
                            fig,
                            "Predicciones Temporales a 2 Meses",
                            "Predicciones futuras basadas en modelos polinomiales con intervalo de confianza del ±10%."
                        )
                    elif nombre == 'cambios':
                        reporte_html.agregar_grafico(
                            fig,
                            "Análisis de Cambios Esperados",
                            "Cambios proyectados en las métricas principales para los próximos 2 meses."
                        )
                    
                    plt.close(fig)
                
                # Agregar conclusiones
                ultimo_hist = predictor_temporal.df_temporal.iloc[-1]
                ultima_pred = predictor_temporal.predicciones.iloc[-1]
                
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
                        • Se analizaron {len(df_mosquitos)} reportes de mosquitos en la zona<br>
                        • Precisión promedio de modelos: {r2_promedio:.1%}<br>
                        • Se recomienda monitoreo continuo para validar predicciones
                    </div>
                </div>
                """
                
                reporte_html.agregar_seccion(
                    " Conclusiones y Recomendaciones",
                    conclusiones,
                    "texto"
                )
                
                # Generar archivo HTML
                reporte_html_path = reporte_html.generar_html(
                    str(generador.output_dir / "reporte.html")
                )
                
                generador.log(f" Reporte HTML generado: reporte.html")
                
            except Exception as e:
                generador.log(f"⚠️  Error generando reporte HTML: {str(e)}", "WARNING")
                import traceback
                traceback.print_exc()
        else:
            generador.log("⚠️  No se generó reporte HTML (predicción temporal no disponible)", "WARNING")
        
        # 7. GUARDAR REPORTE FINAL TXT
        generador.separador("7. GUARDANDO REPORTE FINAL TXT")
        
        generador.reporte_txt.append("\n" + "=" * 80 + "\n")
        generador.reporte_txt.append("  📋 RESUMEN FINAL\n")
        generador.reporte_txt.append("=" * 80 + "\n")
        generador.reporte_txt.append(f"\n Análisis completado exitosamente\n")
        generador.reporte_txt.append(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        generador.reporte_txt.append(f"\n📁 Archivos generados:\n")
        generador.reporte_txt.append(f"   - 🌟 Mapa Central: mapa.html\n")
        if reporte_html_path:
            generador.reporte_txt.append(f"   - 🌐 Reporte HTML: reporte.html\n")
        generador.reporte_txt.append(f"   - 📊 Gráficos: Ver carpeta {generador.output_dir}/\n")
        
        archivo_reporte = generador.guardar_reporte_txt()
        
        # MENSAJE FINAL
        print("\n" + "=" * 80)
        print(" ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        print(f"\n Todos los archivos se guardaron en: {generador.output_dir}/")
        print(f"\n Reporte TXT: {archivo_reporte}")
        
        print(f"\n ARCHIVO CENTRAL - MAPA INTERACTIVO:")
        print(f"   {mapa_unificado}")
        print(f"   Este es tu punto de entrada principal")
        print(f"   Comando para abrir:")
        print(f"   xdg-open {mapa_unificado}")
        
        if reporte_html_path:
            print(f"\n REPORTE COMPLETO:")
            print(f"   {reporte_html_path}")
            print(f"   Accesible desde el botón en mapa.html")
            print(f"   • Visualizaciones embebidas de alta calidad")
            print(f"   • Gráficos de series temporales y predicciones")
            print(f"   • Métricas y conclusiones automáticas")
        
        print(f"\n� ARCHIVOS ADICIONALES:")
        print(f"   • Series temporales (series_temporales.png)")
        print(f"   • Predicciones futuras (predicciones_temporales.png)")
        print(f"   • Análisis de cambios (analisis_cambios.png)")
        print(f"   • Datos CSV (predicciones_futuras.csv)")
        
        print("\n TIPS:")
        print("   • Abre mapa.html en tu navegador - es tu archivo principal")
        print("   • Usa el botón 'Ver Reporte Completo' para estadísticas detalladas")
        print("   • Los archivos HTML son autocontenidos - compártelos por email")
        print("   • Usa Ctrl+P en el navegador para exportar a PDF")
        print("=" * 80 + "\n")
        
    except Exception as e:
        generador.log(f"❌ ERROR CRÍTICO: {str(e)}", "ERROR")
        generador.guardar_reporte_txt()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
