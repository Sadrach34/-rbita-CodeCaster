"""
Módulo para detección y visualización de floraciones usando datos satelitales.
"""
import folium
import datetime
from pathlib import Path


class DetectorFloraciones:
    """Detecta y visualiza floraciones usando imágenes satelitales NDVI."""
    
    def __init__(self, centro_lat=23.6345, centro_lon=-102.5528, zoom=5):
        """
        Inicializa el detector de floraciones.
        
        Args:
            centro_lat: Latitud del centro del mapa
            centro_lon: Longitud del centro del mapa
            zoom: Nivel de zoom inicial
        """
        self.centro_lat = centro_lat
        self.centro_lon = centro_lon
        self.zoom = zoom
        self.mapa = None
        self.detecciones = []
    
    def crear_mapa_base(self):
        """Crea el mapa base con CartoDB Positron."""
        self.mapa = folium.Map(
            location=[self.centro_lat, self.centro_lon],
            zoom_start=self.zoom,
            tiles="CartoDB positron"
        )
        return self.mapa
    
    def agregar_capa_ndvi(self, fecha=None):
        """
        Agrega capa de NDVI de NASA GIBS.
        
        Args:
            fecha: Fecha en formato YYYY-MM-DD (por defecto hoy)
        """
        if fecha is None:
            fecha = datetime.date.today().strftime("%Y-%m-%d")
        
        gibs_layer = folium.raster_layers.TileLayer(
            tiles=f"https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MOD13A1_NDVI_16Day/default/{fecha}/250m/{{z}}/{{y}}/{{x}}.jpg",
            attr="NASA GIBS",
            name="MODIS NDVI (16-day)",
            overlay=True,
            control=True,
            fmt="image/jpeg"
        )
        gibs_layer.add_to(self.mapa)
    
    def agregar_deteccion(self, lat, lon, fecha, intensidad="Media"):
        """
        Agrega una detección de floración al mapa.
        
        Args:
            lat: Latitud
            lon: Longitud
            fecha: Fecha de detección
            intensidad: Nivel de intensidad (Alta/Media/Baja)
        """
        deteccion = {
            "lat": lat,
            "lon": lon,
            "fecha": fecha,
            "intensidad": intensidad
        }
        self.detecciones.append(deteccion)
        
        color = {
            "Alta": "red",
            "Media": "orange",
            "Baja": "green"
        }.get(intensidad, "blue")
        
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>Floración detectada</b><br>Fecha: {fecha}<br>Intensidad: {intensidad}",
            icon=folium.Icon(color=color, icon="leaf")
        ).add_to(self.mapa)
    
    def guardar_mapa(self, ruta_salida="data/output/floraciones.html"):
        """
        Guarda el mapa como archivo HTML.
        
        Args:
            ruta_salida: Ruta donde guardar el archivo
        """
        # Crear directorio si no existe
        Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
        
        # Añadir control de capas
        folium.LayerControl().add_to(self.mapa)
        
        # Guardar
        self.mapa.save(ruta_salida)
        print(f"✅ Mapa generado: {ruta_salida}")
        return ruta_salida


def generar_mapa_rapido(detecciones=None, salida="data/output/floraciones.html"):
    """
    Genera un mapa rápido con detecciones de floración.
    
    Args:
        detecciones: Lista de diccionarios con lat, lon, fecha, intensidad
        salida: Ruta del archivo de salida
    
    Returns:
        Ruta del archivo generado
    """
    detector = DetectorFloraciones()
    detector.crear_mapa_base()
    detector.agregar_capa_ndvi()
    
    if detecciones is None:
        detecciones = [
            {"lat": 32.5, "lon": -115.5, "fecha": "2025-03-15", "intensidad": "Alta"},
            {"lat": 20.7, "lon": -103.3, "fecha": "2025-03-18", "intensidad": "Media"},
            {"lat": 28.6, "lon": -106.1, "fecha": "2025-03-20", "intensidad": "Alta"},
        ]
    
    for d in detecciones:
        detector.agregar_deteccion(d["lat"], d["lon"], d["fecha"], d["intensidad"])
    
    return detector.guardar_mapa(salida)


if __name__ == "__main__":
    # Ejemplo de uso directo
    print("🌸 Generando mapa de floraciones...")
    ruta = generar_mapa_rapido()
    print(f"🗺️  Abre el archivo: {ruta}")
