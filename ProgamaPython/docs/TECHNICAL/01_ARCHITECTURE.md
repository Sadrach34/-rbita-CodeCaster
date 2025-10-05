# Technical Architecture

This document provides a comprehensive technical overview of the Orbita-CodeCaster system architecture, design patterns, and implementation details.

## Table of Contents

1. [System Overview](#system-overview)
2. [Architectural Patterns](#architectural-patterns)
3. [Component Architecture](#component-architecture)
4. [Data Flow](#data-flow)
5. [Module Dependencies](#module-dependencies)
6. [Design Decisions](#design-decisions)
7. [Performance Considerations](#performance-considerations)
8. [Scalability](#scalability)

## System Overview

### Core Architecture

Orbita-CodeCaster implements a **modular, pipeline-based architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   HTML     │  │    Maps    │  │   Charts   │            │
│  │  Reports   │  │  (Folium)  │  │ (Matplotlib)│           │
│  └────────────┘  └────────────┘  └────────────┘            │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                     Business Logic Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Analyzers   │  │  Predictors  │  │  Detectors   │     │
│  │              │  │              │  │              │     │
│  │ -Mosquito    │  │ -RF Model    │  │ -Blooms      │     │
│  │ -LandCover   │  │ -Temporal    │  │ -NDVI        │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                     Data Access Layer                        │
│  ┌──────────────────────────────────────────────────┐       │
│  │              DataLoader                           │       │
│  │  - CSV parsing                                    │       │
│  │  - GeoJSON handling                               │       │
│  │  - Data validation                                │       │
│  │  - Caching                                        │       │
│  └──────────────────────────────────────────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                     Data Storage Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │   CSV    │  │ GeoJSON  │  │  Output  │                  │
│  │  (raw)   │  │ (Sentinel)│  │  Files   │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Core Runtime:**

- **Python**: 3.8+ (target: 3.10-3.11 for optimal performance)
- **Backend**: Non-interactive (Agg) for server/headless deployment

**Data Processing:**

- **pandas** 1.5.0+: DataFrame operations, CSV I/O, time series
- **numpy** 1.23.0+: Numerical computations, array operations
- **geopandas** 0.11.0+ (optional): Advanced geospatial operations

**Machine Learning:**

- **scikit-learn** 1.2.0+:
  - `RandomForestClassifier`: Habitat prediction
  - `PolynomialFeatures`: Temporal trend fitting
  - `train_test_split`, `cross_val_score`: Model validation
  - Metrics: `accuracy_score`, `classification_report`, `r2_score`, `mean_squared_error`

**Visualization:**

- **matplotlib** 3.6.0+: Static plots (300 DPI publication quality)
- **seaborn** 0.12.0+: Statistical visualizations
- **folium** 0.14.0+: Interactive maps based on Leaflet.js
- **branca** 0.6.0+: HTML/CSS components for folium

**Geospatial:**

- **NASA GIBS API**: MODIS NDVI tile server
- **ESA Sentinel-2**: L2A atmospherically corrected imagery
- **EPSG:4326**: WGS84 coordinate reference system

## Architectural Patterns

### 1. Separation of Concerns

Each module has a single, well-defined responsibility:

**Data Layer** (`src/utils/data_loader.py`):

- Handles all file I/O operations
- Validates data schema
- Performs basic preprocessing (date parsing, type conversion)
- No business logic

**Analysis Layer** (`src/analisis_*.py`):

- Implements domain-specific algorithms
- Generates statistics and metrics
- No direct file I/O (uses DataLoader)
- Returns structured results (dicts, DataFrames)

**Prediction Layer** (`src/prediccion*.py`):

- Encapsulates ML models
- Training and prediction logic
- Model validation and metrics
- Independent of data source

**Presentation Layer** (`src/reporte_html.py`, `src/floraciones.py`):

- Creates visualizations
- Generates reports
- No data processing or analysis
- Consumes results from other layers

### 2. Dependency Injection

Classes accept dependencies through constructors:

```python
class AnalizadorMosquitos:
    def __init__(self, df_mosquitos: pd.DataFrame):
        """
        Args:
            df_mosquitos: Pre-loaded and validated DataFrame
        """
        self.df = df_mosquitos
```

**Benefits:**

- Easier testing (inject mock data)
- Flexibility (swap data sources)
- Clear dependencies

### 3. Factory Pattern

`DataLoader` acts as a factory for DataFrame creation:

```python
loader = DataLoader("data/raw")
loader.cargar_todos()

df_mosquitos = loader.get_mosquitos()
df_imagery = loader.get_imagery()
```

### 4. Pipeline Pattern

`main.py` implements an ETL (Extract, Transform, Load) pipeline:

```python
# Extract
loader = DataLoader()
loader.cargar_todos()

# Transform
analizador = AnalizadorMosquitos(loader.get_mosquitos())
resultados = analizador.ejecutar_analisis_completo()

# Load
generador.generar_reporte_html(resultados)
```

### 5. Stateless Design

Analysis classes maintain minimal state:

- Input DataFrames (immutable after init)
- Results dictionary (populated by methods)
- Configuration parameters

**No side effects** (methods don't modify input data).

## Component Architecture

### DataLoader (`src/utils/data_loader.py`)

**Responsibilities:**

- Load CSV files with error handling
- Parse and validate GeoJSON (Sentinel-2)
- Standardize column names
- Basic preprocessing (date parsing)
- Provide data summaries

**Key Methods:**

```python
class DataLoader:
    def cargar_todos() -> DataLoader:
        """Load all CSV files. Returns self for chaining."""

    def get_mosquitos() -> pd.DataFrame:
        """Return validated mosquito habitat data."""

    def get_imagery() -> pd.DataFrame:
        """Return aerial imagery classification data."""

    def get_landcover() -> pd.DataFrame:
        """Return land cover observation data."""

    def cargar_sentinel2(directorio: str) -> pd.DataFrame:
        """Load and parse Sentinel-2 GeoJSON files."""
```

**Error Handling:**

- `FileNotFoundError`: Graceful handling with warning messages
- Invalid data: Continues with partial dataset
- Schema validation: Checks required columns exist

### AnalizadorMosquitos (`src/analisis_mosquitos.py`)

**Purpose:** Statistical and geospatial analysis of mosquito habitat data.

**Core Algorithms:**

1. **Species Distribution Analysis**

   - Frequency counting with `value_counts()`
   - Visualization: Horizontal bar charts
   - Output: Ranked species list

2. **Water Source Analysis**

   - Categorical grouping
   - Percentage calculations
   - Pie chart generation

3. **Temporal Pattern Detection**

   - Time series aggregation by month/year
   - Trend identification
   - Line plot visualization

4. **Larvae Analysis**

   - Boolean filtering (larvae present/absent)
   - Contingency table generation
   - Statistical summary

5. **Heatmap Generation**

   - Folium HeatMap plugin
   - Gaussian kernel density estimation
   - Configurable radius and intensity

6. **Marker Clustering**
   - MarkerCluster plugin for performance
   - Popup information cards
   - Color-coded by attributes

**Method Signatures:**

```python
def analizar_especies(self) -> pd.Series:
    """Count mosquito genera frequencies."""

def analizar_fuentes_agua(self) -> pd.DataFrame:
    """Analyze water source distribution."""

def analizar_temporal(self) -> pd.DataFrame:
    """Detect temporal patterns (monthly/yearly)."""

def analizar_larvas(self) -> dict:
    """Analyze larvae presence/absence."""

def crear_mapa_calor(self, archivo: str) -> folium.Map:
    """Generate density heatmap."""

def crear_mapa_marcadores(self, archivo: str) -> folium.Map:
    """Create interactive marker map."""

def ejecutar_analisis_completo(self) -> dict:
    """Run all analyses. Returns structured results."""
```

### AnalizadorCobertura (`src/analisis_cobertura.py`)

**Purpose:** Land cover composition and correlation analysis.

**Core Algorithms:**

1. **Average Coverage Calculation**

   - Column-wise mean computation
   - Percentage conversion
   - Bar chart visualization

2. **Distribution Analysis**

   - Histogram generation
   - Kernel density estimation
   - Statistical moments (mean, std, skewness)

3. **Water Area Identification**

   - Threshold-based filtering (water > 0)
   - Geographic subset extraction
   - Scatter plot mapping

4. **Correlation Analysis**

   - Pearson correlation coefficient
   - Heatmap with color gradient
   - Annotation of values

5. **Vegetation vs. Urban Comparison**
   - Feature aggregation
   - Comparative bar charts
   - Percentage difference calculation

**Method Signatures:**

```python
def analizar_promedios(self) -> pd.Series:
    """Calculate average coverage percentages."""

def analizar_distribucion(self) -> None:
    """Generate distribution histograms."""

def analizar_areas_con_agua(self) -> pd.DataFrame:
    """Identify and extract water-containing areas."""

def analizar_correlaciones(self) -> pd.DataFrame:
    """Compute correlation matrix."""

def analizar_vegetacion_urbano(self) -> dict:
    """Compare vegetation vs. urban coverage."""

def ejecutar_analisis_completo(self) -> dict:
    """Run all analyses. Returns structured results."""
```

### PredictorMosquitos (`src/prediccion.py`)

**Purpose:** Machine learning-based habitat suitability prediction.

**Algorithm: Random Forest Classification**

**Model Configuration:**

```python
RandomForestClassifier(
    n_estimators=100,      # 100 decision trees
    random_state=42,        # Reproducibility
    max_depth=10,           # Prevent overfitting
    min_samples_split=5,    # Minimum samples to split node
    min_samples_leaf=2      # Minimum samples in leaf node
)
```

**Feature Engineering:**

- **Input features (X):**

  - `ceoTREES_CANOPYCOVER`: Tree density (0-100%)
  - `ceoBUSH_SCRUB`: Shrub coverage (0-100%)
  - `ceoGRASS`: Grass coverage (0-100%)
  - `ceoImperviousSurface`: Built environment (0-100%)

- **Target variable (y):**
  - Binary classification: `ceoWaterLakePondedContainer > 0`
  - 1 = Water present (mosquito habitat potential)
  - 0 = No water (low mosquito risk)

**Training Process:**

1. Data splitting: 70% train, 30% test (stratified)
2. Model fitting on training set
3. Prediction on test set
4. Validation: accuracy, precision, recall, F1-score
5. Feature importance extraction
6. Confusion matrix generation

**Validation Metrics:**

- **Accuracy**: Overall correctness
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **AUC-ROC**: Area under receiver operating characteristic curve

**Method Signatures:**

```python
def preparar_datos(self) -> tuple:
    """Feature selection and train/test split."""

def entrenar_modelo(self) -> None:
    """Train Random Forest classifier."""

def validar_modelo(self) -> dict:
    """Compute validation metrics."""

def obtener_importancia_features(self) -> pd.DataFrame:
    """Extract feature importance scores."""

def generar_visualizaciones(self) -> None:
    """Create confusion matrix and feature importance plots."""
```

### PredictorTemporal (`src/prediccion_temporal.py`)

**Purpose:** Time series forecasting using Sentinel-2 multispectral data.

**Algorithm: Polynomial Regression**

**Model Configuration:**

```python
PolynomialFeatures(degree=3)  # Cubic polynomial
LinearRegression()
```

**Data Processing:**

1. **Sentinel-2 GeoJSON Parsing:**

   - Extract acquisition dates from filenames
   - Parse properties dictionary
   - Extract surface classification percentages
   - Aggregate multiple images per date

2. **Feature Extraction:**

   - `verde` (vegetation): sum of `VEGE_*` classes
   - `agua`: sum of `AGUA` class
   - `urbano`: sum of `ARTIFICIAL_*` classes
   - `nieve`: `NIEVE_HIELO` class
   - `nubes`: `NUBES_*` classes

3. **Time Series Construction:**
   - Sort by date (chronological order)
   - Calculate day offsets from first observation
   - Create temporal index

**Prediction Process:**

1. **Model Training:**

   - Fit polynomial regression to historical data
   - Separate model for each variable
   - Store coefficients for interpretability

2. **Forecasting:**

   - Project 30, 60, and 90 days into future
   - Generate prediction intervals (±1 std dev)
   - Validate predictions against last observations

3. **Trend Analysis:**
   - Compute linear trend coefficient
   - Classify as "increasing", "decreasing", or "stable"
   - Calculate rate of change (% per day)

**Quality Metrics:**

- **R² (Coefficient of Determination)**: Model fit quality
- **RMSE (Root Mean Square Error)**: Prediction error magnitude
- **MAE (Mean Absolute Error)**: Average error
- **Residual Analysis**: Check for systematic bias

**Method Signatures:**

```python
def cargar_datos_sentinel2(directorio: str) -> pd.DataFrame:
    """Load and parse Sentinel-2 GeoJSON files."""

def preparar_datos(df: pd.DataFrame) -> tuple:
    """Feature engineering and temporal indexing."""

def entrenar_modelo(self, variable: str) -> None:
    """Train polynomial regression for variable."""

def predecir_futuro(self, dias_adelante: int) -> pd.DataFrame:
    """Generate forecasts for next N days."""

def analizar_tendencias(self) -> dict:
    """Compute trend statistics."""

def generar_visualizaciones(self) -> None:
    """Create time series plots with predictions."""

def calcular_metricas(self) -> dict:
    """Compute R², RMSE, and MAE."""
```

### GeneradorReporteHTML (`src/reporte_html.py`)

**Purpose:** Generate comprehensive HTML reports with embedded visualizations.

**Architecture:**

```
HTML Report Structure:
├── <!DOCTYPE html>
│   ├── <head>
│   │   ├── <meta> (charset, viewport)
│   │   ├── <title>
│   │   └── <style> (embedded CSS)
│   ├── <body>
│   │   ├── <header>
│   │   │   └── Title, date, summary
│   │   ├── <nav>
│   │   │   └── Table of contents
│   │   ├── <main>
│   │   │   ├── <section id="datos">
│   │   │   │   └── Data overview
│   │   │   ├── <section id="mosquitos">
│   │   │   │   ├── Analysis results
│   │   │   │   └── Embedded charts (base64)
│   │   │   ├── <section id="cobertura">
│   │   │   ├── <section id="prediccion">
│   │   │   ├── <section id="mapas">
│   │   │   │   └── Embedded folium maps
│   │   │   └── <section id="conclusiones">
│   │   └── <footer>
│   │       └── Metadata, timestamp
```

**CSS Framework:** Custom responsive design

- Mobile-first approach
- Breakpoints: 768px (tablet), 1024px (desktop)
- Flexbox layout
- Print-optimized styles

**Embedding Strategy:**

**Images:**

```python
import base64

with open(chart_path, 'rb') as f:
    img_data = base64.b64encode(f.read()).decode()
    html += f'<img src="data:image/png;base64,{img_data}" />'
```

**Maps:**

```python
with open(map_path, 'r') as f:
    map_html = f.read()
    # Extract <div> and <script> tags
    html += map_html
```

**Method Signatures:**

```python
def __init__(self, titulo: str, output_dir: str):
    """Initialize report generator."""

def agregar_seccion(self, titulo: str, contenido: str, nivel: int):
    """Add content section with heading."""

def agregar_imagen(self, ruta: str, descripcion: str):
    """Embed base64-encoded image."""

def agregar_mapa(self, ruta: str):
    """Embed folium map HTML."""

def agregar_tabla(self, df: pd.DataFrame, descripcion: str):
    """Convert DataFrame to HTML table."""

def generar(self, archivo_salida: str):
    """Write complete HTML to file."""
```

## Data Flow

### Complete Analysis Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ 1. INITIALIZATION                                            │
│    main.py execution                                         │
│    └─> Import modules                                        │
│    └─> Configure matplotlib backend                          │
│    └─> Create output directory                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. DATA LOADING                                              │
│    DataLoader.cargar_todos()                                 │
│    ├─> Read CSV files (mosquitos, landcover, imagery)       │
│    ├─> Parse GeoJSON (Sentinel-2)                           │
│    ├─> Validate schemas                                      │
│    └─> Preprocess (dates, types)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. MOSQUITO ANALYSIS                                         │
│    AnalizadorMosquitos(df_mosquitos)                         │
│    ├─> analizar_especies()                                  │
│    ├─> analizar_fuentes_agua()                              │
│    ├─> analizar_temporal()                                  │
│    ├─> analizar_larvas()                                    │
│    ├─> crear_mapa_calor()                                   │
│    └─> crear_mapa_marcadores()                              │
│    Output: PNG charts, HTML maps, result dict               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. LAND COVER ANALYSIS                                       │
│    AnalizadorCobertura(df_landcover)                         │
│    ├─> analizar_promedios()                                 │
│    ├─> analizar_distribucion()                              │
│    ├─> analizar_areas_con_agua()                            │
│    ├─> analizar_correlaciones()                             │
│    └─> analizar_vegetacion_urbano()                         │
│    Output: PNG charts, result dict                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. PREDICTION (ML)                                           │
│    PredictorMosquitos(df_imagery)                            │
│    ├─> preparar_datos()  [train/test split]                │
│    ├─> entrenar_modelo()  [RandomForest training]          │
│    ├─> validar_modelo()  [metrics computation]             │
│    └─> generar_visualizaciones()                            │
│    Output: PNG confusion matrix, feature importance          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. TEMPORAL PREDICTION                                       │
│    PredictorTemporal()                                       │
│    ├─> cargar_datos_sentinel2()                             │
│    ├─> preparar_datos()                                     │
│    ├─> entrenar_modelo(variable='verde')                    │
│    ├─> predecir_futuro(30, 60, 90 days)                    │
│    └─> generar_visualizaciones()                            │
│    Output: CSV predictions, PNG time series plots           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. BLOOM DETECTION                                           │
│    DetectorFloraciones()                                     │
│    └─> generar_mapa_ndvi()                                  │
│    Output: HTML map with NDVI overlay                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. REPORT GENERATION                                         │
│    GeneradorReporteHTML()                                    │
│    ├─> agregar_seccion() [for each analysis]               │
│    ├─> agregar_imagen() [embed charts]                     │
│    ├─> agregar_mapa() [embed maps]                         │
│    └─> generar() [write HTML file]                         │
│    Output: Complete HTML report                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Transformation Steps

**Raw CSV → Processed DataFrame:**

```python
# 1. Load
df = pd.read_csv('data.csv')

# 2. Parse dates
df['fecha'] = pd.to_datetime(df['measuredAt'])

# 3. Extract temporal features
df['mes'] = df['fecha'].dt.month
df['año'] = df['fecha'].dt.year
df['dia_año'] = df['fecha'].dt.dayofyear

# 4. Type conversion
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

# 5. Filtering
df = df.dropna(subset=['latitude', 'longitude'])
df = df[(df['latitude'] != 0) & (df['longitude'] != 0)]
```

**GeoJSON → Feature DataFrame:**

```python
# 1. Load GeoJSON
with open('S2A_*.geojson', 'r') as f:
    geojson = json.load(f)

# 2. Extract properties
props = geojson['features'][0]['properties']

# 3. Parse surface classification
clasificacion = json.loads(props['clasificacionSuperficie'])

# 4. Aggregate to DataFrame row
row = {
    'fecha': parse_date_from_filename(filename),
    'verde': sum(v for k, v in clasificacion.items() if 'VEGE' in k),
    'agua': clasificacion.get('AGUA', 0),
    ...
}

# 5. Append to DataFrame
df = pd.DataFrame([row])
```

## Module Dependencies

### Dependency Graph

```
main.py
├── src.utils.data_loader
├── src.analisis_mosquitos
│   ├── pandas
│   ├── matplotlib.pyplot
│   ├── seaborn
│   └── folium
├── src.analisis_cobertura
│   ├── pandas
│   ├── matplotlib.pyplot
│   └── seaborn
├── src.prediccion
│   ├── pandas
│   ├── sklearn.ensemble.RandomForestClassifier
│   ├── sklearn.model_selection.train_test_split
│   ├── sklearn.metrics
│   └── matplotlib.pyplot
├── src.prediccion_temporal
│   ├── pandas
│   ├── numpy
│   ├── sklearn.preprocessing.PolynomialFeatures
│   ├── sklearn.linear_model.LinearRegression
│   ├── sklearn.metrics
│   └── matplotlib.pyplot
├── src.floraciones
│   └── folium
└── src.reporte_html
    ├── base64
    └── datetime
```

### Import Strategy

**Lazy imports** where appropriate:

```python
# Eager (at module level)
import pandas as pd
import numpy as np

# Lazy (inside methods)
def crear_mapa_calor(self):
    from folium.plugins import HeatMap
    ...
```

**Benefits:**

- Faster startup time
- Reduced memory footprint
- Clear which features require which dependencies

## Design Decisions

### 1. Why Non-Interactive Backend?

**Decision:** Use `matplotlib.use('Agg')` before any pyplot imports.

**Rationale:**

- **Server deployment**: No X11/display required
- **Consistency**: Same behavior across environments
- **Performance**: Faster rendering without GUI overhead
- **CI/CD**: Works in automated pipelines

**Trade-off:** Cannot display plots interactively (but saves to file).

### 2. Why Not Database?

**Decision:** Store data as CSV/GeoJSON files, not in a database.

**Rationale:**

- **Simplicity**: No database setup required
- **Portability**: Files are easily shared
- **NASA format**: Data arrives as CSV/GeoJSON
- **Size**: Datasets are small enough for in-memory processing

**When to reconsider:** If dataset exceeds 1 million rows or concurrent users.

### 3. Why Random Forest for Classification?

**Decision:** Use Random Forest over simpler (logistic regression) or complex (neural network) models.

**Rationale:**

- **Non-linear relationships**: Captures complex patterns
- **Interpretability**: Feature importance is easily extracted
- **Robustness**: Handles missing data and outliers well
- **No hyperparameter tuning needed**: Works well with defaults
- **Fast training**: Efficient for our dataset size

**Trade-offs:**

- Larger model size than linear models
- Slower prediction than decision trees (but acceptable)

### 4. Why Polynomial Regression for Time Series?

**Decision:** Use polynomial regression rather than ARIMA, LSTM, or other time series models.

**Rationale:**

- **Simplicity**: Easy to understand and implement
- **Interpretability**: Coefficients have clear meaning
- **Small data**: Limited Sentinel-2 images (40-50), not enough for complex models
- **Smooth trends**: Vegetation changes are gradual, polynomial fits well

**Trade-offs:**

- Cannot capture seasonality as well as ARIMA
- No autoregressive component
- May overfit with high polynomial degree (mitigated with degree=3)

### 5. Why Embed Base64 Images in HTML?

**Decision:** Embed charts as base64 strings rather than linking external files.

**Rationale:**

- **Single file**: Report is self-contained, easily shared
- **No broken links**: Images cannot be accidentally deleted
- **Portability**: Works without web server

**Trade-offs:**

- Larger HTML file size
- Slightly slower browser loading (but acceptable for report size)

### 6. Why Stratified Train/Test Split?

**Decision:** Use stratified splitting in classification:

```python
train_test_split(X, y, test_size=0.3, stratify=y)
```

**Rationale:**

- **Balanced classes**: Ensures train and test have same class proportions
- **Prevents bias**: Important when classes are imbalanced
- **Better evaluation**: Test set is representative of full dataset

## Performance Considerations

### Memory Management

**Key Strategies:**

1. **Avoid unnecessary copies:**

   ```python
   # Bad
   df_copy = df.copy()
   df_copy['new_col'] = ...

   # Good
   df['new_col'] = ...
   ```

2. **Use categorical types:**

   ```python
   df['species'] = df['species'].astype('category')
   # Reduces memory by storing integers + lookup table
   ```

3. **Delete large objects:**

   ```python
   del large_dataframe
   import gc
   gc.collect()
   ```

4. **Chunk processing for very large files:**
   ```python
   chunks = pd.read_csv('large.csv', chunksize=10000)
   for chunk in chunks:
       process(chunk)
   ```

### Computational Complexity

**Bottlenecks:**

1. **Heatmap generation**: O(n²) for n points

   - **Mitigation**: Limit to 10,000 points, sample if needed

2. **Correlation matrix**: O(m²) for m features

   - **Mitigation**: Acceptable for small number of features (<20)

3. **Random Forest training**: O(n log n × trees × features)

   - **Mitigation**: 100 trees is reasonable, parallel training enabled

4. **Polynomial feature expansion**: O(n × degree^features)
   - **Mitigation**: Degree=3, only 1 feature at a time

### I/O Optimization

**File Reading:**

```python
# Specify dtypes to reduce memory
dtypes = {
    'plotid': 'int32',
    'latitude': 'float32',
    'longitude': 'float32',
    'species': 'category'
}
df = pd.read_csv('data.csv', dtype=dtypes)
```

**Caching:**

```python
# Cache processed data
if os.path.exists('processed.pkl'):
    df = pd.read_pickle('processed.pkl')
else:
    df = load_and_process()
    df.to_pickle('processed.pkl')
```

### Visualization Performance

**Matplotlib:**

- **DPI**: Use 300 DPI for print, 100 DPI for screen
- **Figure size**: Limit to 12x8 inches maximum
- **Close figures**: `plt.close()` after saving to free memory

**Folium:**

- **MarkerCluster**: Automatically clusters when zoomed out
- **Limit markers**: Cap at 10,000 markers per map
- **Tile caching**: Browser caches base map tiles

## Scalability

### Current Limitations

**Hardware:**

- **RAM**: Assumes entire dataset fits in memory (<8GB)
- **CPU**: Single-threaded for most operations (except Random Forest)
- **Storage**: Assumes local filesystem

**Data Size:**

- **CSV files**: <100MB each
- **Sentinel-2**: <100 images
- **Total data**: <2GB

### Scaling Strategies

**If data exceeds memory:**

1. **Chunked processing:**

   ```python
   for chunk in pd.read_csv('large.csv', chunksize=50000):
       results = process_chunk(chunk)
       save_results(results)
   ```

2. **Dask for parallel processing:**

   ```python
   import dask.dataframe as dd
   df = dd.read_csv('large.csv')
   result = df.groupby('species').count().compute()
   ```

3. **Database backend (PostgreSQL + PostGIS):**
   ```python
   engine = create_engine('postgresql://...')
   df = pd.read_sql('SELECT * FROM observations WHERE ...', engine)
   ```

**If compute is bottleneck:**

1. **Parallel processing:**

   ```python
   from multiprocessing import Pool
   with Pool(4) as pool:
       results = pool.map(process_file, file_list)
   ```

2. **GPU acceleration (for deep learning):**
   ```python
   # If switching to neural networks
   import tensorflow as tf
   with tf.device('/GPU:0'):
       model.fit(X, y)
   ```

**If need horizontal scaling:**

1. **API service:**

   - Convert to Flask/FastAPI REST API
   - Deploy behind load balancer
   - Stateless processing (no session data)

2. **Cloud batch processing:**
   - AWS Batch, Google Cloud Run
   - Containerize with Docker
   - Queue jobs with SQS/Pub-Sub

### Monitoring and Profiling

**Timing:**

```python
import time
start = time.time()
result = expensive_function()
print(f"Elapsed: {time.time() - start:.2f}s")
```

**Memory profiling:**

```python
from memory_profiler import profile

@profile
def analyze_data(df):
    ...
```

**Cython for critical loops:**
If pure Python is too slow, compile hot paths:

```python
# analysis.pyx
def compute_distances(double[:] lats, double[:] lons):
    cdef int i
    cdef double[:] dists = np.zeros(len(lats))
    for i in range(len(lats)):
        dists[i] = sqrt(lats[i]**2 + lons[i]**2)
    return dists
```

## Summary

Orbita-CodeCaster implements a **modular, pipeline-based architecture** with clear separation between data access, business logic, and presentation layers. Key design decisions favor **simplicity, interpretability, and portability** over complex distributed systems.

**Strengths:**

- Easy to understand and modify
- No external dependencies (databases, servers)
- Reproducible results
- Publication-quality outputs

**Areas for improvement:**

- Add database backend for larger datasets
- Implement caching for expensive operations
- Add parallel processing for multiple files
- Create REST API for programmatic access

For implementation details of specific modules, see:

- [Analysis Modules](02_ANALYSIS_MODULES.md)
- [Prediction System](03_PREDICTION_SYSTEM.md)
- [Data Structures](04_DATA_STRUCTURES.md)
- [API Reference](05_API_REFERENCE.md)
