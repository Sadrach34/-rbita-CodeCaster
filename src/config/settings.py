"""
Configuración de la aplicación.
Constantes y parámetros que se usan en toda la aplicación.
"""


class AppConfig:
    """Configuración general de la aplicación"""
    
    # Información de la aplicación
    APP_NAME = "Orbita-CodeCaster"
    VERSION = "1.0.0"
    
    # Dimensiones de ventana
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    WINDOW_MIN_WIDTH = 600
    WINDOW_MIN_HEIGHT = 400
    
    # Fuentes
    FONT_FAMILY = "Arial"
    FONT_SIZE_TITLE = 16
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_SMALL = 8

class ColorConfig:
    """Configuración de colores de la aplicación"""
    
    COLOR_PRIMARY = "#007bff"
    COLOR_SUCCESS = "#28a745"
    COLOR_ERROR = "#dc3545"
    COLOR_WARNING = "#ffc107"

class EnvironmentConfig:
    """Configuración de entorno (desarrollo, producción, etc.)"""
    
    # Modo de desarrollo
    DEBUG = True
    
    # Base de datos (si se usa en el futuro)
    DATABASE_PATH = "data/app.db"
    
    # Logs
    LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
    LOG_FILE = "logs/app.log"


# Configuración activa (puede cambiar según el entorno)
active_config = AppConfig()
active_env = EnvironmentConfig()
