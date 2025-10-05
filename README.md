# 🌍 Orbita-CodeCaster

**ÓRBITA (Codecasters)** es una plataforma de análisis geoespacial para el desafío NASA Bloomwatch. Monitorea y predice floraciones globales usando datos de observación terrestre de la NASA, integrando análisis de cobertura del suelo y hábitats de mosquitos con datos ciudadanos de GLOBE Observer.

## 🚀 Características

- 🗺️ **Visualización de floraciones** con imágenes satelitales NASA GIBS (MODIS NDVI)
- 🦟 **Análisis de hábitats de mosquitos** usando datos de GLOBE Observer
- 🌳 **Clasificación de cobertura del suelo** (árboles, vegetación, agua, edificios)
- 📊 **Dashboards interactivos** con mapas dinámicos
- 🤖 **Análisis predictivo** de patrones fenológicos
- 📈 **Visualización de datos** con gráficos y estadísticas

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

**Archivos generados en:** `data/output/reporte_completo_*.txt` y `mapa_*.html`

[📖 Ver guía completa de uso](docs/USO_MAIN.md)

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
