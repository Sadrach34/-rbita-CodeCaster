# Analysis Modules - Technical Reference

Comprehensive technical documentation for the core analysis modules: `AnalizadorMosquitos` and `AnalizadorCobertura`.

## Table of Contents

1. [AnalizadorMosquitos](#analizadormosquitos)
2. [AnalizadorCobertura](#analizadorcobertura)
3. [Implementation Patterns](#implementation-patterns)
4. [Performance Characteristics](#performance-characteristics)

## AnalizadorMosquitos

### Class Overview

**Location:** `src/analisis_mosquitos.py`

**Purpose:** Statistical and geospatial analysis of mosquito habitat data from GLOBE Observer project.

**Inheritance:** None (standalone class)

**Dependencies:**

- pandas 1.5.0+
- matplotlib 3.6.0+
- seaborn 0.12.0+
- folium 0.14.0+
- folium.plugins (HeatMap, MarkerCluster)

### Class Definition

```python
class AnalizadorMosquitos:
    """
    Analyzes mosquito habitat mapper data.

    Performs statistical analysis, temporal pattern detection,
    geospatial mapping, and visualization generation.

    Attributes:
        df (pd.DataFrame): Input mosquito observation data
        resultados (dict): Accumulator for analysis results

    Thread Safety: Not thread-safe (modifies self.resultados)
    Memory: O(n) where n is number of observations
    """
```

### Constructor

```python
def __init__(self, df_mosquitos: pd.DataFrame) -> None:
    """
    Initialize mosquito analyzer.

    Args:
        df_mosquitos: DataFrame containing mosquito observations.
            Required columns:
                - mosquitohabitatmapperGenus: Mosquito genus (str)
                - mosquitohabitatmapperWaterSource: Water source type (str)
                - mosquitohabitatmapperMeasuredAt: ISO datetime (str)
                - mosquitohabitatmapperMeasurementLatitude: Latitude (float)
                - mosquitohabitatmapperMeasurementLongitude: Longitude (float)
            Optional columns:
                - mosquitohabitatmapperLarvaeCount: Number of larvae (int)
                - fecha: Parsed datetime (datetime64)
                - mes: Month number (int)
                - año: Year (int)

    Raises:
        None (graceful degradation if columns missing)

    Side Effects:
        - Initializes empty results dictionary
        - Stores reference to input DataFrame (not copied)

    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    self.df = df_mosquitos
    self.resultados = {}
```

### Methods

#### analizar_especies()

**Purpose:** Compute frequency distribution of mosquito genera.

**Algorithm:**

1. Count occurrences of each genus using `value_counts()`
2. Sort in descending order
3. Generate horizontal bar chart (top 10)
4. Save as PNG (300 DPI)

**Method Signature:**

```python
def analizar_especies(self) -> Optional[pd.Series]:
    """
    Analyze mosquito genus distribution.

    Returns:
        pd.Series: Genus counts indexed by genus name, sorted descending.
                  Returns None if required column missing.

    Side Effects:
        - Stores result in self.resultados['especies']
        - Saves PNG to 'data/output/especies_mosquitos.png'
        - Prints analysis results to stdout

    Performance:
        Time: O(n) for counting + O(k log k) for sorting (k unique genera)
        Space: O(k) for Series storage
        I/O: 1 file write (~500KB PNG)

    Error Handling:
        - Returns None if 'mosquitohabitatmapperGenus' column missing
        - Creates output directory if not exists
    """
```

**Visualization Specifications:**

```python
# Chart parameters
Figure size: (12, 6) inches
Chart type: Horizontal bar chart
Color scheme: 'darkred' (hex: #8B0000)
DPI: 300 (publication quality)
Title: 'Top 10 Especies de Mosquitos Reportadas'
X-axis: 'Especie'
Y-axis: 'Número de Reportes'
Rotation: 45° right-aligned
Layout: tight_layout() to prevent clipping
```

**Example Output:**

```
Genus               Count
Aedes                 150
Culex                  98
Anopheles              45
Psorophora             23
...
```

#### analizar_fuentes_agua()

**Purpose:** Analyze distribution of water source types.

**Method Signature:**

```python
def analizar_fuentes_agua(self) -> Optional[pd.DataFrame]:
    """
    Analyze water source type distribution.

    Returns:
        pd.DataFrame: Water source counts, top 15, sorted descending.
                     Returns None if column missing.

    Side Effects:
        - Stores result in self.resultados['fuentes_agua']
        - Saves PNG to 'data/output/fuentes_agua_mosquitos.png'

    Performance:
        Time: O(n) for counting
        Space: O(m) for m unique water sources
        I/O: 1 file write
    """
```

**Water Source Categories:**

- Standing water (puddles, ponds)
- Container (artificial, natural)
- Lake
- Stream/river
- Wetland
- Other

**Chart Specifications:**

- Type: Horizontal bar chart
- Color: 'steelblue'
- Size: (14, 7) inches
- Top 15 sources only

#### analizar_temporal()

**Purpose:** Detect temporal patterns (monthly distribution).

**Method Signature:**

```python
def analizar_temporal(self) -> Optional[pd.Series]:
    """
    Analyze temporal distribution of reports.

    Returns:
        pd.Series: Monthly counts indexed by month number (1-12).
                  Returns None if 'mes' column missing.

    Side Effects:
        - Stores result in self.resultados['reportes_mensuales']
        - Saves PNG to 'data/output/reportes_mensuales_mosquitos.png'

    Performance:
        Time: O(n) for grouping
        Space: O(12) for monthly aggregation

    Statistical Methods:
        - Frequency count by month
        - No seasonality decomposition (future enhancement)
    """
```

**Temporal Insights:**

- Identifies peak mosquito months
- Reveals seasonal patterns
- Supports public health planning

#### analizar_larvas()

**Purpose:** Analyze larvae presence/absence.

**Method Signature:**

```python
def analizar_larvas(self) -> Optional[dict]:
    """
    Analyze larvae observations.

    Returns:
        dict: {
            'con_larvas': int (count with larvae),
            'sin_larvas': int (count without larvae),
            'porcentaje_con_larvas': float (percentage)
        }
        Returns None if larvae column not found.

    Column Detection:
        Searches for columns containing 'larva' (case-insensitive).
        Uses first match found.

    Business Logic:
        - Larvae count > 0: Presence
        - Larvae count == 0: Absence
        - Null values: Treated as absence
    """
```

#### crear_mapa_calor()

**Purpose:** Generate density heatmap of mosquito observations.

**Method Signature:**

```python
def crear_mapa_calor(self, archivo: str = "data/output/mapa_calor_mosquitos.html")
    -> folium.Map:
    """
    Create heatmap visualization.

    Args:
        archivo: Output HTML file path

    Returns:
        folium.Map: Interactive map object with heatmap layer

    Algorithm:
        1. Extract lat/lon coordinates
        2. Filter invalid coordinates (0, null, out-of-bounds)
        3. Calculate map center (median lat/lon)
        4. Create folium.Map base
        5. Add HeatMap plugin layer
        6. Save to HTML

    Heatmap Parameters:
        radius=15: Pixel radius of influence
        blur=25: Gaussian blur amount
        max_zoom=13: Maximum zoom level
        gradient: Default (blue -> green -> yellow -> red)

    Performance:
        Time: O(n) for coordinate extraction + O(n²) for heatmap rendering
        Space: O(n) for coordinate storage
        I/O: 1 HTML write (~2-5MB depending on data)

    Coordinate Validation:
        - Latitude: -90 to +90
        - Longitude: -180 to +180
        - Non-zero (filters missing coordinates)
        - Non-null
    """
```

**Heatmap Visualization Details:**

```python
# Folium map configuration
tiles='OpenStreetMap'  # Base map
zoom_start=10          # Initial zoom level
control_scale=True     # Add scale bar

# HeatMap plugin configuration
HeatMap(
    data=[[lat, lon]],
    radius=15,           # Influence radius
    blur=25,             # Smoothing
    max_zoom=13,         # Stop clustering at zoom 13
    gradient={           # Color gradient (default)
        0.0: 'blue',
        0.5: 'lime',
        0.75: 'yellow',
        1.0: 'red'
    }
)
```

**Use Cases:**

- Identify mosquito hotspots
- Visualize geographic clustering
- Support targeted interventions

#### crear_mapa_marcadores()

**Purpose:** Create interactive map with individual observation markers.

**Method Signature:**

```python
def crear_mapa_marcadores(self,
                         archivo: str = "data/output/mapa_marcadores_mosquitos.html",
                         limite: int = 1000) -> folium.Map:
    """
    Create marker cluster map.

    Args:
        archivo: Output HTML path
        limite: Maximum markers to display (performance limit)

    Returns:
        folium.Map: Interactive map with MarkerCluster layer

    Algorithm:
        1. Sample observations if count > limite
        2. Create base map
        3. Initialize MarkerCluster
        4. For each observation:
            - Create popup with genus, water source, date
            - Add marker to cluster
        5. Add cluster to map
        6. Save HTML

    Marker Details:
        - Popup: HTML formatted with observation details
        - Icon: Default blue pin
        - Clustering: Automatic at zoom levels < 12

    Performance:
        Time: O(n) for marker creation (limited by 'limite')
        Space: O(n) for marker storage
        I/O: 1 HTML write

        Note: Large marker counts (>1000) significantly slow browser

    Sampling Strategy:
        If observations > limite:
            - Random sampling without replacement
            - Preserves statistical distribution
    """
```

**Popup HTML Template:**

```html
<div style="font-family: Arial; font-size: 12px;">
  <b>Género:</b> {genus}<br />
  <b>Fuente de agua:</b> {water_source}<br />
  <b>Fecha:</b> {date}<br />
  <b>Coordenadas:</b> ({lat}, {lon})
</div>
```

#### ejecutar_analisis_completo()

**Purpose:** Run all analysis methods in sequence.

**Method Signature:**

```python
def ejecutar_analisis_completo(self) -> dict:
    """
    Execute complete analysis pipeline.

    Returns:
        dict: Consolidated results from all analyses
            Keys:
                - 'especies': pd.Series
                - 'fuentes_agua': pd.DataFrame
                - 'reportes_mensuales': pd.Series
                - 'larvas': dict
                - 'mapa_calor': str (file path)
                - 'mapa_marcadores': str (file path)

    Execution Order:
        1. analizar_especies()
        2. analizar_fuentes_agua()
        3. analizar_temporal()
        4. analizar_larvas()
        5. crear_mapa_calor()
        6. crear_mapa_marcadores()

    Error Handling:
        - Each method handles missing columns independently
        - Continues execution even if one method fails
        - Missing results stored as None in output dict

    Side Effects:
        - Generates 4 PNG files
        - Generates 2 HTML files
        - Prints progress to stdout

    Performance:
        Time: Sum of individual method times (~30-60s typical)
        Space: O(n) peak memory usage
        I/O: 6 file writes (~10MB total)
    """
```

### Usage Example

```python
from src.analisis_mosquitos import AnalizadorMosquitos
from src.utils.data_loader import DataLoader

# Load data
loader = DataLoader("data/raw")
loader.cargar_todos()
df_mosquitos = loader.get_mosquitos()

# Initialize analyzer
analizador = AnalizadorMosquitos(df_mosquitos)

# Run specific analysis
especies = analizador.analizar_especies()
print(f"Most common genus: {especies.index[0]}")

# Or run complete pipeline
resultados = analizador.ejecutar_analisis_completo()

# Access results
print(f"Species analyzed: {len(resultados['especies'])}")
print(f"Heatmap saved: {resultados['mapa_calor']}")
```

## AnalizadorCobertura

### Class Overview

**Location:** `src/analisis_cobertura.py`

**Purpose:** Statistical analysis of land cover data from aerial imagery classification.

**Dependencies:**

- pandas 1.5.0+
- matplotlib 3.6.0+
- seaborn 0.12.0+
- numpy 1.23.0+

### Class Definition

```python
class AnalizadorCobertura:
    """
    Analyzes land cover imagery data.

    Performs statistical analysis of cover types (trees, grass, water,
    buildings, impervious surfaces) with visualization generation.

    Attributes:
        df (pd.DataFrame): Input imagery data
        resultados (dict): Analysis results accumulator
        columnas_cobertura (list): Expected column names
        nombres_cobertura (dict): Human-readable column labels
    """
```

### Constructor

```python
def __init__(self, df_imagery: pd.DataFrame) -> None:
    """
    Initialize land cover analyzer.

    Args:
        df_imagery: DataFrame with aerial imagery classification data.
            Expected columns:
                - ceoTREES_CANOPYCOVER: Tree canopy coverage (0-100%)
                - ceoBUSH_SCRUB: Bush/scrub coverage (0-100%)
                - ceoGRASS: Grass coverage (0-100%)
                - ceoBuilding: Building coverage (0-100%)
                - ceoImperviousSurface: Impervious surface (0-100%)
                - ceoWaterLakePondedContainer: Water bodies (0-100%)

    Side Effects:
        - Initializes column name mappings
        - Creates empty results dict
    """
    self.df = df_imagery
    self.resultados = {}

    self.columnas_cobertura = [
        'ceoTREES_CANOPYCOVER',
        'ceoBUSH_SCRUB',
        'ceoGRASS',
        'ceoBuilding',
        'ceoImperviousSurface',
        'ceoWaterLakePondedContainer'
    ]

    self.nombres_cobertura = {
        'ceoTREES_CANOPYCOVER': 'Árboles',
        'ceoBUSH_SCRUB': 'Arbustos',
        'ceoGRASS': 'Pasto',
        'ceoBuilding': 'Edificios',
        'ceoImperviousSurface': 'Superficies Impermeables',
        'ceoWaterLakePondedContainer': 'Agua'
    }
```

### Methods

#### analizar_promedios()

**Purpose:** Calculate mean coverage percentage for each land cover type.

**Method Signature:**

```python
def analizar_promedios(self) -> Optional[pd.Series]:
    """
    Compute average coverage percentages.

    Returns:
        pd.Series: Mean coverage for each type.
            Index: Column names
            Values: Percentages (0-100)

    Algorithm:
        1. Filter existing columns from expected list
        2. Compute column-wise mean using df[cols].mean()
        3. Generate bar chart with values labeled
        4. Save PNG

    Statistical Method:
        - Arithmetic mean (μ = Σx/n)
        - No weighted averaging
        - Ignores null values

    Visualization:
        - Bar chart with color-coded bars:
            Trees: forestgreen
            Shrubs: olive
            Grass: limegreen
            Buildings: gray
            Impervious: darkgray
            Water: steelblue
        - Values displayed on bars
        - 45° rotated labels

    Performance:
        Time: O(n × m) for n observations, m columns
        Space: O(m) for results
    """
```

#### analizar_distribucion()

**Purpose:** Generate histograms showing distribution of each cover type.

**Method Signature:**

```python
def analizar_distribucion(self) -> Optional[list]:
    """
    Visualize coverage distributions.

    Returns:
        list: Column names processed

    Algorithm:
        1. Create subplot grid (2 columns, ceil(n/2) rows)
        2. For each cover type:
            - Generate histogram (30 bins)
            - Compute mean and median
            - Plot vertical lines for mean (red) and median (green)
            - Add legend
        3. Hide unused subplots
        4. Save combined figure

    Statistical Metrics:
        - Mean: Central tendency
        - Median: Robust central tendency
        - Distribution shape: Skewness visible

    Chart Parameters:
        bins=30: Number of histogram bins
        alpha=0.7: Transparency
        edgecolor='black': Bar borders
        Color: steelblue

    Interpretation:
        - Right-skewed: Few high values (e.g., urban areas)
        - Left-skewed: Few low values (e.g., forests)
        - Bimodal: Distinct categories (e.g., water presence/absence)
    """
```

#### analizar_areas_con_agua()

**Purpose:** Extract and analyze areas containing water bodies.

**Method Signature:**

```python
def analizar_areas_con_agua(self) -> Optional[pd.DataFrame]:
    """
    Identify water-containing observations.

    Returns:
        pd.DataFrame: Subset of observations with water > 0

    Algorithm:
        1. Filter rows where ceoWaterLakePondedContainer > 0
        2. Extract relevant columns (lat, lon, water %, other covers)
        3. Generate scatter plot (water % vs. coordinates)
        4. Save results

    Use Cases:
        - Identify potential mosquito breeding sites
        - Map water body distribution
        - Correlate water with other land uses

    Performance:
        Time: O(n) for filtering
        Space: O(k) for k water observations (typically k << n)
    """
```

#### analizar_correlaciones()

**Purpose:** Compute Pearson correlation matrix for cover types.

**Method Signature:**

```python
def analizar_correlaciones(self) -> Optional[pd.DataFrame]:
    """
    Calculate correlation matrix.

    Returns:
        pd.DataFrame: Correlation matrix (m × m)
            Values: -1.0 to +1.0

    Algorithm:
        1. Select cover columns
        2. Compute pairwise Pearson correlation: ρ(X,Y) = cov(X,Y) / (σ_X × σ_Y)
        3. Generate heatmap with annotated values
        4. Save PNG

    Correlation Interpretation:
        +1.0: Perfect positive (when X increases, Y increases)
        0.0: No linear relationship
        -1.0: Perfect negative (when X increases, Y decreases)

    Heatmap Specifications:
        cmap='coolwarm': Blue (negative) to red (positive)
        annot=True: Display correlation values
        fmt='.2f': Two decimal places
        square=True: Square cells
        linewidths=0.5: Grid lines

    Common Patterns:
        - Trees vs. Buildings: Negative (urban/forest trade-off)
        - Grass vs. Trees: Positive (vegetated areas)
        - Water vs. Impervious: Negative (water in natural areas)

    Statistical Notes:
        - Assumes linear relationships
        - Sensitive to outliers
        - Does not imply causation
    """
```

#### analizar_vegetacion_urbano()

**Purpose:** Compare vegetation coverage vs. urban/built environment.

**Method Signature:**

```python
def analizar_vegetacion_urbano(self) -> Optional[dict]:
    """
    Compare natural vs. built environments.

    Returns:
        dict: {
            'vegetacion_total': float (trees + shrubs + grass %),
            'urbano_total': float (buildings + impervious %),
            'diferencia': float (vegetation - urban),
            'ratio': float (vegetation / urban)
        }

    Algorithm:
        1. Aggregate vegetation: trees + shrubs + grass
        2. Aggregate urban: buildings + impervious surfaces
        3. Compute summary statistics
        4. Generate comparative bar chart

    Aggregation Logic:
        vegetacion = mean(trees) + mean(shrubs) + mean(grass)
        urbano = mean(buildings) + mean(impervious)

    Interpretation:
        - Ratio > 1: More vegetation than urban
        - Ratio < 1: More urban than vegetation
        - Ratio ≈ 1: Balanced mixed use

    Use Cases:
        - Environmental health assessment
        - Urban planning metrics
        - Habitat quality indicators
    """
```

#### ejecutar_analisis_completo()

**Purpose:** Execute full analysis pipeline.

**Method Signature:**

```python
def ejecutar_analisis_completo(self) -> dict:
    """
    Run complete land cover analysis.

    Returns:
        dict: Consolidated results
            Keys:
                - 'promedios': pd.Series
                - 'areas_con_agua': pd.DataFrame
                - 'correlaciones': pd.DataFrame
                - 'vegetacion_urbano': dict

    Execution Order:
        1. analizar_promedios()
        2. analizar_distribucion()
        3. analizar_areas_con_agua()
        4. analizar_correlaciones()
        5. analizar_vegetacion_urbano()

    Side Effects:
        - Generates 4-5 PNG files
        - Prints results to stdout

    Performance:
        Time: ~20-40 seconds typical
        Space: O(n) peak
        I/O: 4-5 file writes (~5MB total)
    """
```

### Usage Example

```python
from src.analisis_cobertura import AnalizadorCobertura
from src.utils.data_loader import DataLoader

# Load data
loader = DataLoader("data/raw")
loader.cargar_todos()
df_imagery = loader.get_imagery()

# Initialize analyzer
analizador = AnalizadorCobertura(df_imagery)

# Run specific analysis
promedios = analizador.analizar_promedios()
print(f"Average tree coverage: {promedios['ceoTREES_CANOPYCOVER']:.1f}%")

# Check correlations
correlaciones = analizador.analizar_correlaciones()
corr_trees_water = correlaciones.loc['ceoTREES_CANOPYCOVER', 'ceoWaterLakePondedContainer']
print(f"Trees-Water correlation: {corr_trees_water:.2f}")

# Complete pipeline
resultados = analizador.ejecutar_analisis_completo()
```

## Implementation Patterns

### Common Design Patterns

Both analysis classes follow consistent design patterns:

#### 1. Method Structure Pattern

```python
def analizar_X(self):
    """Analysis method template."""

    # 1. Print section header
    print("=" * 60)
    print("SECTION TITLE")
    print("=" * 60)

    # 2. Validate required columns
    if required_column not in self.df.columns:
        print("⚠️  Column not found")
        return None

    # 3. Perform analysis
    result = self.df[columns].compute_something()

    # 4. Store in results dict
    self.resultados['key'] = result

    # 5. Print results
    print("\nResults:")
    print(result)

    # 6. Generate visualization
    plt.figure(figsize=(12, 6))
    # ... plotting code ...

    # 7. Save figure
    output_path = Path('data/output/filename.png')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Saved: {output_path}")
    plt.close()

    # 8. Return result
    return result
```

#### 2. Error Handling Pattern

```python
# Graceful degradation (no exceptions thrown)
if required_data not in available_data:
    print("⚠️  Warning message")
    return None

# Continue with partial results
# Other methods can still execute
```

#### 3. Output Standardization

All visualizations follow:

- DPI: 300 (publication quality)
- Layout: `tight_layout()` to prevent clipping
- Format: PNG with transparent background
- Naming: Descriptive filenames in `data/output/`

### Shared Utilities

Both classes use:

```python
# Matplotlib configuration
matplotlib.use('Agg')  # Non-interactive backend

# Path handling
from pathlib import Path
output_path = Path('data/output/file.png')
output_path.parent.mkdir(parents=True, exist_ok=True)

# Figure closing
plt.close()  # Free memory after saving
```

## Performance Characteristics

### Time Complexity

| Operation           | AnalizadorMosquitos | AnalizadorCobertura |
| ------------------- | ------------------- | ------------------- |
| Initialization      | O(1)                | O(1)                |
| Species analysis    | O(n log k)          | -                   |
| Temporal analysis   | O(n)                | -                   |
| Average calculation | -                   | O(n × m)            |
| Correlation matrix  | -                   | O(n × m²)           |
| Heatmap generation  | O(n²)               | -                   |
| Marker clustering   | O(n)                | -                   |
| Complete pipeline   | O(n²)               | O(n × m²)           |

Where:

- n = number of observations
- k = unique categories
- m = number of features (typically 6)

### Space Complexity

| Component                  | Space Usage            |
| -------------------------- | ---------------------- |
| Input DataFrame            | O(n × m)               |
| Results dictionary         | O(k)                   |
| Visualizations (in memory) | O(n) during generation |
| Saved files                | 0 (written to disk)    |

### Optimization Opportunities

1. **Marker Limiting:**

   ```python
   # Current: Sample if > 1000 markers
   # Improvement: Dynamic clustering threshold
   ```

2. **Caching:**

   ```python
   # Cache computed statistics
   @lru_cache(maxsize=128)
   def get_statistics(self):
       ...
   ```

3. **Parallel Processing:**

   ```python
   # Generate charts in parallel
   from multiprocessing import Pool
   with Pool(4) as pool:
       pool.map(generate_chart, analyses)
   ```

4. **Incremental Updates:**
   ```python
   # Avoid recomputing unchanged analyses
   if not self.resultados.get('especies_updated', False):
       self.analizar_especies()
   ```

### Memory Profiling

Typical memory usage for 10,000 observations:

```
Component                 Memory
---------------------------------
DataFrame (loaded)        ~5 MB
Analysis results          ~1 MB
Matplotlib figures        ~10 MB peak (released after save)
Folium maps              ~2 MB (HTML on disk)
---------------------------------
Peak memory usage        ~18 MB
```

For detailed implementation of prediction models, see [Prediction System](03_PREDICTION_SYSTEM.md).
