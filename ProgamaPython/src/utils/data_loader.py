"""
Utilidades para cargar y procesar datos CSV del proyecto.
"""
import pandas as pd
from pathlib import Path


class DataLoader:
    """Carga y gestiona los datos del proyecto."""
    
    def __init__(self, data_dir="data/raw"):
        """
        Inicializa el cargador de datos.
        
        Args:
            data_dir: Directorio donde están los archivos CSV
        """
        self.data_dir = Path(data_dir)
        self.landcover = None
        self.mosquitos = None
        self.imagery = None
    
    def cargar_todos(self):
        """Carga todos los archivos CSV."""
        print("📂 Cargando datos...")
        
        try:
            self.landcover = pd.read_csv(
                self.data_dir / 'AdoptAPixel3km2020_GO_LandCover.csv'
            )
            print(f"✅ LandCover cargado: {len(self.landcover)} registros")
        except FileNotFoundError:
            print("⚠️  Archivo LandCover no encontrado")
            self.landcover = None
        
        try:
            self.mosquitos = pd.read_csv(
                self.data_dir / 'AdoptAPixel3km2020_GO_MosquitoHabitatMapper.csv'
            )
            # Procesar fechas
            self.mosquitos['fecha'] = pd.to_datetime(
                self.mosquitos['mosquitohabitatmapperMeasuredAt']
            )
            self.mosquitos['mes'] = self.mosquitos['fecha'].dt.month
            self.mosquitos['año'] = self.mosquitos['fecha'].dt.year
            print(f"✅ Mosquitos cargado: {len(self.mosquitos)} registros")
        except FileNotFoundError:
            print("⚠️  Archivo Mosquitos no encontrado")
            self.mosquitos = None
        
        try:
            self.imagery = pd.read_csv(
                self.data_dir / 'AdoptAPixel3km2020_100m_aerialImageryLabels.csv'
            )
            print(f"✅ Imagery cargado: {len(self.imagery)} registros")
        except FileNotFoundError:
            print("⚠️  Archivo Imagery no encontrado")
            self.imagery = None
        
        print("\n✅ Datos cargados correctamente\n")
        return self
    
    def get_mosquitos(self):
        """Retorna el DataFrame de mosquitos."""
        if self.mosquitos is None:
            raise ValueError("Datos de mosquitos no cargados. Ejecuta cargar_todos() primero.")
        return self.mosquitos
    
    def get_imagery(self):
        """Retorna el DataFrame de imagery."""
        if self.imagery is None:
            raise ValueError("Datos de imagery no cargados. Ejecuta cargar_todos() primero.")
        return self.imagery
    
    def get_landcover(self):
        """Retorna el DataFrame de landcover."""
        if self.landcover is None:
            raise ValueError("Datos de landcover no cargados. Ejecuta cargar_todos() primero.")
        return self.landcover
    
    def resumen_datos(self):
        """Imprime un resumen de los datos cargados."""
        print("=" * 60)
        print("📊 RESUMEN DE DATOS")
        print("=" * 60)
        
        if self.mosquitos is not None:
            print(f"\n🦟 MOSQUITOS:")
            print(f"   Total de reportes: {len(self.mosquitos)}")
            print(f"   Rango de fechas: {self.mosquitos['fecha'].min()} a {self.mosquitos['fecha'].max()}")
            if 'mosquitohabitatmapperGenus' in self.mosquitos.columns:
                especies_unicas = self.mosquitos['mosquitohabitatmapperGenus'].nunique()
                print(f"   Especies únicas reportadas: {especies_unicas}")
        
        if self.imagery is not None:
            print(f"\n🌍 IMAGERY:")
            print(f"   Total de observaciones: {len(self.imagery)}")
            if 'ceoPLOTID' in self.imagery.columns:
                plots_unicos = self.imagery['ceoPLOTID'].nunique()
                print(f"   Parcelas únicas: {plots_unicos}")
        
        if self.landcover is not None:
            print(f"\n🌳 LAND COVER:")
            print(f"   Total de observaciones: {len(self.landcover)}")
        
        print("\n" + "=" * 60 + "\n")


def cargar_datos_rapido():
    """
    Función de conveniencia para cargar todos los datos rápidamente.
    
    Returns:
        DataLoader con todos los datos cargados
    """
    loader = DataLoader()
    loader.cargar_todos()
    loader.resumen_datos()
    return loader
