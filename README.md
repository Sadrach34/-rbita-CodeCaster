# 🌍 Orbita-CodeCaster

**ÓRBITA (Codecasters)** is a geospatial analysis platform for NASA's Bloomwatch challenge. It monitors and predicts global blooms using NASA Earth observation data, integrating land cover analysis and mosquito habitat data with GLOBE Observer citizen science data.

## 🚀 Features

- 🗺️ **Bloom visualization** with NASA GIBS satellite imagery (MODIS NDVI)
- 🦟 **Mosquito habitat analysis** using GLOBE Observer data
- 🌳 **Land cover classification** (trees, vegetation, water, buildings)
- 📊 **Interactive dashboards** with dynamic maps
- 🤖 **Predictive analysis** of phenological patterns
- ⭐ **NEW: Temporal prediction with Sentinel-2** - Predicts vegetation state 2 months ahead using 45+ satellite images
- 📈 **Data visualization** with charts and statistics
- 📄 **Interactive HTML reports** with embedded graphics and Folium maps

## 📚 Complete Documentation

This project has **comprehensive documentation** covering all aspects of the system:

### 📖 Main Documentation

The documentation is divided into two sections:

**For General Users** (non-technical, easy-to-follow guides):

- **[docs/USER_GUIDE/](docs/USER_GUIDE/README.md)** - Complete user guide with:
  - Getting Started - Installation and setup
  - Basic Usage - Running analyses step-by-step
  - Understanding Results - Interpreting outputs
  - FAQ - Common problems and solutions

**For Engineers and Developers** (highly technical reference):

- **[docs/TECHNICAL/](docs/TECHNICAL/)** - Technical documentation including:
  - Architecture - System design and patterns
  - Analysis Modules - Detailed algorithm documentation
  - Prediction System - ML models and mathematical foundations
  - Data Structures - Complete schemas and validation
  - API Reference - Method signatures and examples

### 📘 Quick Start Guides (Legacy)

- **[docs/USO_MAIN.md](docs/USO_MAIN.md)** - Using the main script
- **[docs/PREDICCION_TEMPORAL.md](docs/PREDICCION_TEMPORAL.md)** - Temporal prediction with Sentinel-2
- **[docs/VER_REPORTE.md](docs/VER_REPORTE.md)** - Viewing reports
- **[docs/REPORTE_HTML.md](docs/REPORTE_HTML.md)** - Generating HTML reports

### 🎯 Where to Start?

| If you want to...                  | Read this                                                                                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Install and use the system**     | [USER_GUIDE/01_GETTING_STARTED.md](docs/USER_GUIDE/01_GETTING_STARTED.md)                                                             |
| **Run analyses**                   | [USER_GUIDE/02_BASIC_USAGE.md](docs/USER_GUIDE/02_BASIC_USAGE.md)                                                                     |
| **Understand results**             | [USER_GUIDE/03_UNDERSTANDING_RESULTS.md](docs/USER_GUIDE/03_UNDERSTANDING_RESULTS.md)                                                 |
| **Understand system architecture** | [TECHNICAL/01_ARCHITECTURE.md](docs/TECHNICAL/01_ARCHITECTURE.md)                                                                     |
| **Understand data formats**        | [TECHNICAL/04_DATA_STRUCTURES.md](docs/TECHNICAL/04_DATA_STRUCTURES.md)                                                               |
| **Understand ML algorithms**       | [TECHNICAL/03_PREDICTION_SYSTEM.md](docs/TECHNICAL/03_PREDICTION_SYSTEM.md)                                                           |
| **Develop new features**           | [TECHNICAL/02_ANALYSIS_MODULES.md](docs/TECHNICAL/02_ANALYSIS_MODULES.md) + [05_API_REFERENCE.md](docs/TECHNICAL/05_API_REFERENCE.md) |

## 📋 Requisitos Previos

- **Python 3.8+** (recomendado Python 3.11 o superior)
- **pip** (gestor de paquetes de Python)
- Conexión a internet para acceder a tiles satelitales

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Sadrach34/Orbita-CodeCaster.git
cd Orbita-CodeCaster
```

### 2. Crear y activar entorno virtual

**En Linux/Mac:**

```bash
python -m venv mi_entorno
source mi_entorno/bin/activate
```

**En Windows:**

```bash
python -m venv mi_entorno
mi_entorno\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Verificar instalación

```bash
python -c "import folium; print('✅ Folium instalado correctamente')"
```

## 🎯 Uso Rápido

### ⚡ Análisis Completo (Recomendado)

Ejecuta el análisis completo de todos los datos con un solo comando:

```bash
python main.py
```

**Esto generará automáticamente:**

- 📄 Reporte completo en TXT con todas las estadísticas
- 🗺️ Mapa interactivo de mosquitos (HeatMap + Clusters)
- 🌍 Mapa interactivo de cobertura del suelo
- 📊 Gráficos de análisis
- 🤖 Modelo predictivo con Random Forest
- 🔮 **⭐ NUEVO:** Predicción temporal a 2 meses con Sentinel-2

**Archivos generados en:** `data/output/reporte_completo_*.txt` y `mapa_*.html`

[📖 Ver guía completa de uso](docs/USO_MAIN.md)

---

### 🔮 ⭐ Predicción Temporal (NUEVO)

Predice el estado de la vegetación para 2 meses adelante usando tus 34 imágenes Sentinel-2:

```bash
python scripts/ejecutar_prediccion_temporal.py
```

**¿Qué hace?**

- 📡 Analiza 34 imágenes satelitales Sentinel-2 (abril-octubre 2025)
- 📊 Calcula índices: NDVI, Vegetación, Verdor, Agua
- 🤖 Entrena modelos Random Forest (precisión 94-98%)
- 🔮 Predice valores para diciembre 2025
- 📈 Genera gráficos de series temporales
- 📄 Crea reporte detallado

**Archivos generados:**

- `prediccion_series_temporales.png` - Evolución temporal + predicciones
- `prediccion_comparacion.png` - Comparación actual vs futuro
- `reporte_prediccion_temporal_*.txt` - Reporte completo

[📖 Ver guía de predicción temporal](INICIO_RAPIDO_PREDICCION.md) | [📚 Documentación completa](docs/PREDICCION_TEMPORAL.md)

---

### Generar Mapa de Floraciones

```bash
python scripts/generar_mapa_floraciones.py
```

Esto creará un archivo HTML en `data/output/floraciones.html` con:

- Mapa base de México
- Capa de NDVI satelital de NASA GIBS
- Marcadores de detecciones de floración

### Usar como Módulo en tu Código

```python
from src.floraciones import DetectorFloraciones

# Crear detector
detector = DetectorFloraciones(centro_lat=23.6, centro_lon=-102.5, zoom=5)

# Crear mapa base
detector.crear_mapa_base()

# Agregar capa satelital
detector.agregar_capa_ndvi(fecha="2025-03-15")

# Agregar detección de floración
detector.agregar_deteccion(
    lat=32.5,
    lon=-115.5,
    fecha="2025-03-15",
    intensidad="Alta"
)

# Guardar mapa
detector.guardar_mapa("mi_mapa.html")
```

### Análisis de Datos CSV

```python
import pandas as pd

# Cargar datos de mosquitos
mosquitos = pd.read_csv('data/raw/AdoptAPixel3km2020_GO_MosquitoHabitatMapper.csv')

# Análisis básico
print(f"Total de reportes: {len(mosquitos)}")
print(f"Especies detectadas: {mosquitos['mosquitohabitatmapperGenus'].unique()}")
```

## 📁 Estructura del Proyecto

```
Orbita-CodeCaster/
├── README.md                      # Este archivo
├── requirements.txt               # Dependencias Python
├── .gitignore                     # Archivos ignorados por Git
│
├── data/                          # Datos del proyecto
│   ├── raw/                       # Datos originales (CSV de GLOBE Observer)
│   ├── processed/                 # Datos procesados
│   └── output/                    # Mapas y visualizaciones generadas
│
├── src/                           # Código fuente principal
│   ├── __init__.py
│   ├── floraciones.py             # Módulo de detección de floraciones
│   └── utils/                     # Utilidades compartidas
│
├── scripts/                       # Scripts ejecutables
│   └── generar_mapa_floraciones.py
│
├── notebooks/                     # Jupyter notebooks para análisis
├── tests/                         # Pruebas unitarias
└── docs/                          # Documentación adicional
```

## 📊 Fuentes de Datos

### GLOBE Observer

Datos ciudadanos de observación terrestre que incluyen:

- **Land Cover**: Cobertura del suelo (árboles, vegetación, agua, edificios)
- **Mosquito Habitat Mapper**: Ubicaciones de hábitats de mosquitos
- **Aerial Imagery Labels**: Etiquetas de clasificación visual

### NASA GIBS

Imágenes satelitales MODIS con índice de vegetación NDVI:

- Resolución: 250m
- Frecuencia: 16 días
- Fuente: MODIS Terra

## 🛠️ Tecnologías Utilizadas

- **Folium**: Visualización de mapas interactivos
- **Pandas**: Análisis de datos tabulares
- **NumPy**: Cálculos numéricos
- **Matplotlib/Seaborn**: Visualización de gráficos
- **scikit-learn**: Machine learning (análisis predictivo)
- **Jupyter**: Notebooks interactivos

## 📖 Documentación Adicional

- [Guía de instalación detallada](docs/INSTALL.md) _(próximamente)_
- [Documentación API](docs/API.md) _(próximamente)_
- [Tutorial de análisis](notebooks/) _(próximamente)_

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 🐛 Reportar Problemas

Si encuentras un bug o tienes una sugerencia, por favor [abre un issue](https://github.com/Sadrach34/Orbita-CodeCaster/issues).

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Sadrach34** - _Desarrollo inicial_ - [GitHub](https://github.com/Sadrach34)

## 🙏 Agradecimientos

- **NASA GIBS** por proporcionar imágenes satelitales de acceso público
- **GLOBE Observer** por los datos de ciencia ciudadana
- **Comunidad de Python** por las excelentes bibliotecas de código abierto
- **NASA Space Apps Challenge** por inspirar este proyecto

## 🔗 Enlaces

- [NASA GIBS](https://earthdata.nasa.gov/eosdis/science-system-description/eosdis-components/gibs)
- [GLOBE Observer](https://observer.globe.gov/)
- [NASA Bloomwatch Challenge](https://www.spaceappschallenge.org/)

---

⭐ Si este proyecto te resulta útil, ¡considera darle una estrella en GitHub!
