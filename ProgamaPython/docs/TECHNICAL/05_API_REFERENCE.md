# API Reference - Complete Method Signatures

Complete technical reference for all public APIs, classes, and functions.

## Table of Contents

1. [Data Loading](#data-loading)
2. [Analysis Modules](#analysis-modules)
3. [Prediction Modules](#prediction-modules)
4. [Utility Functions](#utility-functions)
5. [Quick Reference](#quick-reference)

## Data Loading

### Class: DataLoader

**Module:** `src.data_loader`

**Purpose:** Load and parse CSV and GeoJSON data files

#### Constructor

```python
def __init__(self) -> None:
    """
    Initialize DataLoader.

    Initializes empty containers for three data types:
    - df_mosquitos: Mosquito habitat observations
    - df_imagery: Aerial imagery land cover labels
    - df_temporal: Sentinel-2 time series

    Raises:
        None

    Example:
        >>> loader = DataLoader()
    """
```

#### cargar_datos_mosquitos

```python
def cargar_datos_mosquitos(
    self,
    ruta: str = 'data/raw/AdoptAPixel3km2020_GO_MosquitoHabitatMapper.csv'
) -> pd.DataFrame:
    """
    Load GLOBE Observer mosquito habitat mapper data.

    Loads CSV file, parses dates, extracts temporal features.

    Args:
        ruta (str): Path to mosquito CSV file.
            Default: 'data/raw/AdoptAPixel3km2020_GO_MosquitoHabitatMapper.csv'

    Returns:
        pd.DataFrame: Mosquito observations with columns:
            - All original CSV columns
            - fecha (datetime64[ns]): Parsed observation timestamp
            - mes (int64): Month (1-12)
            - año (int64): Year (e.g., 2020)

    Raises:
        FileNotFoundError: If CSV file does not exist at `ruta`
        pd.errors.EmptyDataError: If CSV file is empty
        pd.errors.ParserError: If CSV format is invalid

    Processing Steps:
        1. Read CSV with UTF-8 encoding
        2. Parse 'mosquitohabitatmapperMeasuredAt' to datetime
        3. Extract month and year columns
        4. Store in self.df_mosquitos

    Example:
        >>> loader = DataLoader()
        >>> df = loader.cargar_datos_mosquitos()
        >>> print(df.shape)
        (1234, 28)
        >>> print(df['fecha'].dtype)
        datetime64[ns]
    """
```

#### cargar_datos_imagery

```python
def cargar_datos_imagery(
    self,
    ruta: str = 'data/raw/AdoptAPixel3km2020_100m_aerialImageryLabels.csv'
) -> pd.DataFrame:
    """
    Load Collect Earth Online aerial imagery labels.

    Loads CSV file with land cover classification percentages.

    Args:
        ruta (str): Path to imagery CSV file.
            Default: 'data/raw/AdoptAPixel3km2020_100m_aerialImageryLabels.csv'

    Returns:
        pd.DataFrame: Imagery data with columns:
            - ceoPLOTID (int64): Plot identifier
            - ceoLON, ceoLAT (float64): Coordinates
            - ceoTREES_CANOPYCOVER (float64): Tree coverage (%)
            - ceoBUSH_SCRUB (float64): Bush/scrub coverage (%)
            - ceoGRASS (float64): Grass coverage (%)
            - ceoBuilding (float64): Building coverage (%)
            - ceoImperviousSurface (float64): Impervious surface (%)
            - ceoWaterLakePondedContainer (float64): Water bodies (%)
            - ceoSampleGeometry (object): WKT geometry

    Raises:
        FileNotFoundError: If CSV file does not exist
        pd.errors.EmptyDataError: If CSV is empty

    Processing Steps:
        1. Read CSV with UTF-8 encoding
        2. Store in self.df_imagery

    Example:
        >>> loader = DataLoader()
        >>> df = loader.cargar_datos_imagery()
        >>> print(df.columns.tolist())
        ['ceoPLOTID', 'ceoLON', 'ceoLAT', ...]
    """
```

#### cargar_datos_temporales

```python
def cargar_datos_temporales(
    self,
    directorio: str = 'data/raw',
    patron: str = 'S2*_T12RWU_*.geojson'
) -> pd.DataFrame:
    """
    Load Sentinel-2 time series data from GeoJSON files.

    Scans directory for GeoJSON files matching pattern, parses each file,
    extracts surface classification percentages, sorts by date.

    Args:
        directorio (str): Directory containing GeoJSON files.
            Default: 'data/raw'
        patron (str): Glob pattern for file matching.
            Default: 'S2*_T12RWU_*.geojson'
            Matches: S2A and S2B satellites, tile T12RWU

    Returns:
        pd.DataFrame: Time series data with columns:
            - fecha (datetime64[ns]): Acquisition timestamp
            - cloud_cover (float64): Cloud percentage (0-100)
            - vegetation_pct (float64): Vegetation percentage
            - not_vegetated_pct (float64): Non-vegetated percentage
            - water_pct (float64): Water percentage
            - snow_ice_pct (float64): Snow/ice percentage
            - unclassified_pct (float64): Unclassified percentage
            - archivo (object): Source filename
            - dias_desde_inicio (float64): Days since first observation

        Sorted by 'fecha' in ascending order.

    Raises:
        FileNotFoundError: If no files match pattern in directorio
        json.JSONDecodeError: If GeoJSON file is malformed
        KeyError: If required properties missing in GeoJSON

    Processing Steps:
        1. Find all files matching glob pattern
        2. For each file:
            a. Parse JSON
            b. Extract 'properties' dict
            c. Parse 'datetime' field
            d. Extract s2:* percentage fields
        3. Concatenate into single DataFrame
        4. Sort by fecha
        5. Calculate dias_desde_inicio (delta from min date)
        6. Store in self.df_temporal

    Example:
        >>> loader = DataLoader()
        >>> df = loader.cargar_datos_temporales()
        >>> print(df.shape)
        (87, 8)
        >>> print(df['fecha'].min(), df['fecha'].max())
        2025-04-15 00:00:00 2025-10-02 00:00:00
    """
```

## Analysis Modules

### Class: AnalizadorMosquitos

**Module:** `src.analisis_mosquitos`

**Purpose:** Analyze mosquito habitat observations

#### Constructor

```python
def __init__(self, df_mosquitos: pd.DataFrame) -> None:
    """
    Initialize mosquito analyzer.

    Args:
        df_mosquitos (pd.DataFrame): Mosquito observations from DataLoader.
            Required columns:
                - mosquitohabitatmapperGenus (object)
                - mosquitohabitatmapperWaterSource (object)
                - mosquitohabitatmapperLarvaeCount (float64)
                - mes (int64)
                - mosquitohabitatmapperMeasurementLatitude (float64)
                - mosquitohabitatmapperMeasurementLongitude (float64)

    Raises:
        TypeError: If df_mosquitos is not a pandas DataFrame
        ValueError: If required columns are missing

    Attributes:
        df (pd.DataFrame): Stored input DataFrame
        resultados (dict): Empty dict, populated by analysis methods

    Example:
        >>> analizador = AnalizadorMosquitos(df_mosquitos)
    """
```

#### analizar_especies

```python
def analizar_especies(self) -> pd.Series:
    """
    Count observations by mosquito genus.

    Returns:
        pd.Series: Genus counts, sorted descending.
            Index: Genus names (str)
            Values: Observation counts (int64)

    Stores:
        self.resultados['especies']: Result series

    Time Complexity: O(n)
    Space Complexity: O(k) where k = unique genera

    Example:
        >>> counts = analizador.analizar_especies()
        >>> print(counts)
        Aedes         542
        Culex         189
        Anopheles      67
        Unknown        23
        dtype: int64
    """
```

#### analizar_fuentes_agua

```python
def analizar_fuentes_agua(self) -> pd.DataFrame:
    """
    Analyze water source distribution.

    Returns:
        pd.DataFrame: Water source statistics.
            Columns:
                - Cantidad (int64): Observation count
                - Porcentaje (float64): Percentage of total (0-100)
            Index: Water source names (str)

    Stores:
        self.resultados['fuentes_agua']: Result DataFrame

    Time Complexity: O(n)
    Space Complexity: O(m) where m = unique water sources

    Example:
        >>> df = analizador.analizar_fuentes_agua()
        >>> print(df)
                                    Cantidad  Porcentaje
        container                        123       45.2
        lake/pond                         89       32.7
        ditch                             60       22.1
    """
```

#### analizar_reportes_mensuales

```python
def analizar_reportes_mensuales(self) -> pd.Series:
    """
    Count observations by month.

    Returns:
        pd.Series: Monthly observation counts.
            Index: Month numbers (1-12, int64)
            Values: Counts (int64)

    Stores:
        self.resultados['reportes_mensuales']: Result series

    Time Complexity: O(n)
    Space Complexity: O(12)

    Note:
        Index may not contain all 12 months if no observations
        exist for some months.

    Example:
        >>> counts = analizador.analizar_reportes_mensuales()
        >>> print(counts)
        1      23
        2      18
        3      45
        ...
        12     12
        dtype: int64
    """
```

#### analizar_presencia_larvas

```python
def analizar_presencia_larvas(self) -> dict:
    """
    Analyze larvae presence in observations.

    Returns:
        dict: Larvae statistics.
            Keys:
                - con_larvas (int): Count with larvae (count > 0)
                - sin_larvas (int): Count without larvae (count == 0 or null)
                - porcentaje_con_larvas (float): Percentage with larvae (0-100)

    Stores:
        self.resultados['larvas']: Result dict

    Time Complexity: O(n)
    Space Complexity: O(1)

    Algorithm:
        1. Count non-null, non-zero larvae observations
        2. Count zero or null larvae observations
        3. Calculate percentage: (con_larvas / total) * 100

    Example:
        >>> stats = analizador.analizar_presencia_larvas()
        >>> print(stats)
        {'con_larvas': 187, 'sin_larvas': 624, 'porcentaje_con_larvas': 23.1}
    """
```

#### generar_mapa_calor

```python
def generar_mapa_calor(
    self,
    carpeta_salida: str = 'data/output'
) -> str:
    """
    Generate heatmap of observation locations.

    Creates interactive Folium heatmap showing observation density.

    Args:
        carpeta_salida (str): Output directory for HTML file.
            Default: 'data/output'

    Returns:
        str: Path to generated HTML file.
            Format: '{carpeta_salida}/mapa_calor_mosquitos.html'

    Stores:
        self.resultados['mapa_calor']: Output file path

    Raises:
        ValueError: If DataFrame has no valid coordinates
        OSError: If output directory is not writable

    Map Configuration:
        - Base map: OpenStreetMap
        - Center: Mean of all coordinates
        - Zoom: Auto-fit to bounds
        - Heatmap: HeatMap layer with gradient
        - Gradient: {0.4: 'blue', 0.65: 'lime', 0.8: 'orange', 1.0: 'red'}
        - Radius: 15 pixels
        - Blur: 25 pixels

    Time Complexity: O(n)
    Space Complexity: O(n)

    Example:
        >>> path = analizador.generar_mapa_calor()
        >>> print(path)
        data/output/mapa_calor_mosquitos.html
    """
```

#### generar_mapa_marcadores

````python
def generar_mapa_marcadores(
    self,
    carpeta_salida: str = 'data/output'
) -> str:
    """
    Generate marker map with observation details.

    Creates interactive Folium map with individual markers and popups.

    Args:
        carpeta_salida (str): Output directory.
            Default: 'data/output'

    Returns:
        str: Path to HTML file.
            Format: '{carpeta_salida}/mapa_marcadores_mosquitos.html'

    Stores:
        self.resultados['mapa_marcadores']: Output path

    Raises:
        ValueError: If no valid coordinates
        OSError: If directory not writable

    Map Configuration:
        - Base: OpenStreetMap
        - Center: Mean coordinates
        - Zoom: 10
        - Markers: CircleMarker for each observation
            - Radius: 5 pixels
            - Color: 'blue'
            - Fill: True, opacity 0.7
        - Popups: genus, water source, larvae count

    Popup Format:
        ```
        Género: {genus}
        Fuente: {water_source}
        Larvas: {larvae_count}
        ```

    Time Complexity: O(n)
    Space Complexity: O(n)

    Example:
        >>> path = analizador.generar_mapa_marcadores()
    """
````

#### ejecutar_analisis_completo

```python
def ejecutar_analisis_completo(
    self,
    carpeta_salida: str = 'data/output'
) -> dict:
    """
    Execute all analysis methods.

    Runs all analysis methods in sequence, stores all results.

    Args:
        carpeta_salida (str): Output directory for maps.

    Returns:
        dict: Complete results dictionary with keys:
            - especies (pd.Series)
            - fuentes_agua (pd.DataFrame)
            - reportes_mensuales (pd.Series)
            - larvas (dict)
            - mapa_calor (str)
            - mapa_marcadores (str)

    Execution Order:
        1. analizar_especies()
        2. analizar_fuentes_agua()
        3. analizar_reportes_mensuales()
        4. analizar_presencia_larvas()
        5. generar_mapa_calor()
        6. generar_mapa_marcadores()

    Time Complexity: O(n)
    Space Complexity: O(n)

    Example:
        >>> resultados = analizador.ejecutar_analisis_completo()
        >>> print(resultados.keys())
        dict_keys(['especies', 'fuentes_agua', 'reportes_mensuales',
                   'larvas', 'mapa_calor', 'mapa_marcadores'])
    """
```

### Class: AnalizadorCobertura

**Module:** `src.analisis_cobertura`

**Purpose:** Analyze land cover from aerial imagery

#### Constructor

```python
def __init__(self, df_imagery: pd.DataFrame) -> None:
    """
    Initialize land cover analyzer.

    Args:
        df_imagery (pd.DataFrame): Imagery data from DataLoader.
            Required columns:
                - ceoTREES_CANOPYCOVER (float64)
                - ceoBUSH_SCRUB (float64)
                - ceoGRASS (float64)
                - ceoBuilding (float64)
                - ceoImperviousSurface (float64)
                - ceoWaterLakePondedContainer (float64)

    Raises:
        TypeError: If not a DataFrame
        ValueError: If required columns missing

    Attributes:
        df (pd.DataFrame): Input data
        resultados (dict): Results storage

    Example:
        >>> analizador = AnalizadorCobertura(df_imagery)
    """
```

#### calcular_promedios

```python
def calcular_promedios(self) -> pd.Series:
    """
    Calculate mean coverage percentages.

    Returns:
        pd.Series: Mean percentages for each land cover type.
            Index: Column names (str)
            Values: Mean percentages (float64, 0-100)

    Stores:
        self.resultados['promedios']: Result series

    Columns Analyzed:
        - ceoTREES_CANOPYCOVER
        - ceoBUSH_SCRUB
        - ceoGRASS
        - ceoBuilding
        - ceoImperviousSurface
        - ceoWaterLakePondedContainer

    Time Complexity: O(n * m) where m = number of columns
    Space Complexity: O(m)

    Example:
        >>> promedios = analizador.calcular_promedios()
        >>> print(promedios)
        ceoTREES_CANOPYCOVER           45.2
        ceoBUSH_SCRUB                  18.7
        ceoGRASS                       12.3
        ceoBuilding                     8.1
        ceoImperviousSurface           10.5
        ceoWaterLakePondedContainer     5.2
        dtype: float64
    """
```

#### identificar_areas_agua

```python
def identificar_areas_agua(self, umbral: float = 5.0) -> pd.DataFrame:
    """
    Identify plots with significant water coverage.

    Args:
        umbral (float): Minimum water percentage threshold.
            Default: 5.0 (%)

    Returns:
        pd.DataFrame: Subset of plots with water >= umbral.
            All original columns included.

    Stores:
        self.resultados['areas_con_agua']: Result DataFrame

    Filter Condition:
        ceoWaterLakePondedContainer >= umbral

    Time Complexity: O(n)
    Space Complexity: O(k) where k = filtered rows

    Example:
        >>> areas = analizador.identificar_areas_agua(umbral=10.0)
        >>> print(f"Found {len(areas)} plots with ≥10% water")
        Found 23 plots with ≥10% water
    """
```

#### calcular_correlaciones

```python
def calcular_correlaciones(self) -> pd.DataFrame:
    """
    Calculate correlation matrix between land cover types.

    Returns:
        pd.DataFrame: Pearson correlation matrix (m × m).
            Index: Column names
            Columns: Column names
            Values: Correlation coefficients (-1 to +1)

    Stores:
        self.resultados['correlaciones']: Correlation matrix

    Columns Analyzed:
        All CEO coverage columns (6 total)

    Correlation Coefficient (Pearson's r):
        r = cov(X, Y) / (σ_X × σ_Y)

        Where:
            - cov(X, Y): Covariance
            - σ_X, σ_Y: Standard deviations

        Interpretation:
            - r = +1: Perfect positive correlation
            - r = 0: No correlation
            - r = -1: Perfect negative correlation

    Time Complexity: O(n * m²)
    Space Complexity: O(m²)

    Example:
        >>> corr = analizador.calcular_correlaciones()
        >>> print(corr.loc['ceoTREES_CANOPYCOVER', 'ceoBuilding'])
        -0.67
    """
```

#### comparar_vegetacion_urbano

```python
def comparar_vegetacion_urbano(self) -> dict:
    """
    Compare total vegetation vs urban coverage.

    Returns:
        dict: Comparison statistics.
            Keys:
                - vegetacion_total (float): Mean vegetation (%)
                - urbano_total (float): Mean urban (%)
                - diferencia (float): vegetacion - urbano (%)
                - ratio (float): vegetacion / urbano

    Stores:
        self.resultados['vegetacion_urbano']: Result dict

    Definitions:
        - Vegetation = TREES + BUSH_SCRUB + GRASS
        - Urban = Building + ImperviousSurface

    Time Complexity: O(n)
    Space Complexity: O(1)

    Example:
        >>> comp = analizador.comparar_vegetacion_urbano()
        >>> print(comp)
        {
            'vegetacion_total': 76.2,
            'urbano_total': 18.6,
            'diferencia': 57.6,
            'ratio': 4.1
        }
    """
```

#### ejecutar_analisis_completo

```python
def ejecutar_analisis_completo(self) -> dict:
    """
    Execute all analysis methods.

    Returns:
        dict: Complete results with keys:
            - promedios (pd.Series)
            - areas_con_agua (pd.DataFrame)
            - correlaciones (pd.DataFrame)
            - vegetacion_urbano (dict)

    Execution Order:
        1. calcular_promedios()
        2. identificar_areas_agua()
        3. calcular_correlaciones()
        4. comparar_vegetacion_urbano()

    Time Complexity: O(n * m²)
    Space Complexity: O(n + m²)

    Example:
        >>> resultados = analizador.ejecutar_analisis_completo()
    """
```

## Prediction Modules

### Class: PredictorMosquitos

**Module:** `src.prediccion`

**Purpose:** Predict mosquito presence using Random Forest

#### Constructor

```python
def __init__(self, df_imagery: pd.DataFrame, df_mosquitos: pd.DataFrame) -> None:
    """
    Initialize mosquito predictor.

    Args:
        df_imagery (pd.DataFrame): Land cover data
        df_mosquitos (pd.DataFrame): Mosquito observations

    Raises:
        ValueError: If DataFrames incompatible or insufficient data

    Attributes:
        df_imagery (pd.DataFrame): Stored imagery data
        df_mosquitos (pd.DataFrame): Stored mosquito data
        modelo (RandomForestClassifier): Untrained model
        resultados (dict): Training/evaluation results
        X_train, X_test, y_train, y_test: Train/test splits

    Example:
        >>> predictor = PredictorMosquitos(df_imagery, df_mosquitos)
    """
```

#### preparar_datos

```python
def preparar_datos(self, test_size: float = 0.2, random_state: int = 42) -> None:
    """
    Prepare features and labels for training.

    Merges datasets spatially, creates binary target, splits data.

    Args:
        test_size (float): Proportion for test set (0-1).
            Default: 0.2 (20% test)
        random_state (int): Random seed for reproducibility.
            Default: 42

    Raises:
        ValueError: If insufficient data after merge

    Side Effects:
        Sets attributes:
            - self.X_train (np.ndarray): Training features
            - self.X_test (np.ndarray): Test features
            - self.y_train (np.ndarray): Training labels
            - self.y_test (np.ndarray): Test labels

    Feature Engineering:
        1. Spatial join (nearest neighbor matching)
        2. Feature selection: 6 CEO coverage columns
        3. Target: 1 if larvae present, 0 otherwise
        4. Train/test split with stratification

    Time Complexity: O(n * m) for spatial join
    Space Complexity: O(n + m)

    Example:
        >>> predictor.preparar_datos(test_size=0.3)
        >>> print(predictor.X_train.shape)
        (700, 6)
    """
```

#### entrenar_modelo

```python
def entrenar_modelo(
    self,
    n_estimators: int = 100,
    max_depth: Optional[int] = None,
    random_state: int = 42
) -> None:
    """
    Train Random Forest classifier.

    Args:
        n_estimators (int): Number of trees.
            Default: 100
        max_depth (Optional[int]): Maximum tree depth.
            Default: None (unlimited)
        random_state (int): Random seed.
            Default: 42

    Raises:
        RuntimeError: If preparar_datos() not called first

    Side Effects:
        - Trains self.modelo
        - Populates self.resultados with:
            - train_score (float): Training accuracy
            - test_score (float): Test accuracy

    Algorithm:
        1. Initialize RandomForestClassifier
        2. Fit on (X_train, y_train)
        3. Evaluate on train and test sets
        4. Store scores

    Time Complexity: O(n * m * k * log(n))
        n = samples, m = features, k = trees
    Space Complexity: O(k * n)

    Example:
        >>> predictor.entrenar_modelo(n_estimators=200, max_depth=10)
        >>> print(predictor.resultados['test_score'])
        0.87
    """
```

#### evaluar_modelo

```python
def evaluar_modelo(self) -> dict:
    """
    Comprehensive model evaluation.

    Returns:
        dict: Evaluation metrics.
            Keys:
                - accuracy (float): Overall accuracy
                - precision (float): Positive predictive value
                - recall (float): Sensitivity, true positive rate
                - f1_score (float): Harmonic mean of precision/recall
                - confusion_matrix (np.ndarray): 2×2 matrix
                - classification_report (str): Detailed text report

    Stores:
        Updates self.resultados with all metrics

    Raises:
        RuntimeError: If model not trained

    Metrics:
        - Accuracy: (TP + TN) / (TP + TN + FP + FN)
        - Precision: TP / (TP + FP)
        - Recall: TP / (TP + FN)
        - F1: 2 * (Precision * Recall) / (Precision + Recall)

    Confusion Matrix:
        [[TN, FP],
         [FN, TP]]

    Time Complexity: O(n)
    Space Complexity: O(1)

    Example:
        >>> metrics = predictor.evaluar_modelo()
        >>> print(f"F1: {metrics['f1_score']:.3f}")
        F1: 0.843
    """
```

#### validacion_cruzada

```python
def validacion_cruzada(self, cv: int = 5) -> dict:
    """
    Perform k-fold cross-validation.

    Args:
        cv (int): Number of folds.
            Default: 5

    Returns:
        dict: Cross-validation results.
            Keys:
                - cv_scores (np.ndarray): Score per fold
                - cv_mean (float): Mean score
                - cv_std (float): Standard deviation

    Stores:
        Updates self.resultados with CV metrics

    Raises:
        RuntimeError: If preparar_datos() not called

    Algorithm:
        1. Split data into k folds
        2. For each fold:
            a. Train on k-1 folds
            b. Test on held-out fold
            c. Record accuracy
        3. Compute mean and std dev

    Time Complexity: O(k * n * m * t * log(n))
        k = folds, t = trees
    Space Complexity: O(k * n)

    Example:
        >>> cv_results = predictor.validacion_cruzada(cv=10)
        >>> print(f"CV: {cv_results['cv_mean']:.3f} ± {cv_results['cv_std']:.3f}")
        CV: 0.856 ± 0.042
    """
```

#### obtener_importancia_caracteristicas

```python
def obtener_importancia_caracteristicas(self) -> pd.DataFrame:
    """
    Get feature importance from trained model.

    Returns:
        pd.DataFrame: Feature importances sorted descending.
            Columns:
                - caracteristica (str): Feature name
                - importancia (float): Importance score (0-1)

    Stores:
        self.resultados['feature_importances']: Result DataFrame

    Raises:
        RuntimeError: If model not trained

    Importance Metric:
        Mean decrease in Gini impurity across all trees.
        Higher = more important for classification.

    Time Complexity: O(m)
    Space Complexity: O(m)

    Example:
        >>> importances = predictor.obtener_importancia_caracteristicas()
        >>> print(importances.head())
                         caracteristica  importancia
        0  ceoWaterLakePondedContainer        0.342
        1            ceoTREES_CANOPYCOVER        0.215
        2                   ceoBUSH_SCRUB        0.187
    """
```

### Class: PredictorTemporal

**Module:** `src.prediccion_temporal`

**Purpose:** Forecast time series using polynomial regression

#### Constructor

```python
def __init__(self, df_temporal: pd.DataFrame) -> None:
    """
    Initialize temporal predictor.

    Args:
        df_temporal (pd.DataFrame): Sentinel-2 time series from DataLoader.
            Required columns:
                - fecha (datetime64[ns])
                - vegetation_pct, water_pct, etc. (float64)
                - dias_desde_inicio (float64)

    Raises:
        ValueError: If insufficient data or invalid format

    Attributes:
        df (pd.DataFrame): Input time series
        modelos (dict): Trained models per variable
        predicciones (pd.DataFrame): Forecasts

    Example:
        >>> predictor = PredictorTemporal(df_temporal)
    """
```

#### preparar_datos

```python
def preparar_datos(self, columnas_objetivo: Optional[List[str]] = None) -> None:
    """
    Prepare time series for modeling.

    Args:
        columnas_objetivo (Optional[List[str]]): Variables to forecast.
            Default: None (forecasts all percentage columns)

    Side Effects:
        Sets self.columnas_objetivo

    Default Columns:
        - vegetation_pct
        - not_vegetated_pct
        - water_pct
        - snow_ice_pct
        - unclassified_pct
        - cloud_cover

    Time Complexity: O(1)
    Space Complexity: O(1)

    Example:
        >>> predictor.preparar_datos(['vegetation_pct', 'water_pct'])
    """
```

#### entrenar_modelos

```python
def entrenar_modelos(self, grado: int = 2) -> None:
    """
    Train polynomial regression models.

    Args:
        grado (int): Polynomial degree.
            Default: 2 (quadratic)
            Range: 1-5 recommended

    Side Effects:
        Populates self.modelos dict:
            Keys: Variable names (str)
            Values: dict with:
                - modelo (LinearRegression): Trained model
                - poly (PolynomialFeatures): Feature transformer
                - r2 (float): R² score
                - rmse (float): Root mean squared error

    Algorithm:
        For each target variable:
            1. Create polynomial features
            2. Fit LinearRegression
            3. Compute R² and RMSE
            4. Store model and metrics

    Polynomial Features:
        Degree 2: [1, x, x²]
        Degree 3: [1, x, x², x³]
        etc.

    Time Complexity: O(k * n * d²)
        k = variables, d = degree
    Space Complexity: O(k * d)

    Example:
        >>> predictor.entrenar_modelos(grado=3)
        >>> print(predictor.modelos['vegetation_pct']['r2'])
        0.89
    """
```

#### predecir_futuro

```python
def predecir_futuro(
    self,
    dias_futuro: int = 30,
    intervalo_confianza: float = 0.95
) -> pd.DataFrame:
    """
    Forecast future values with confidence intervals.

    Args:
        dias_futuro (int): Number of days to forecast.
            Default: 30
        intervalo_confianza (float): Confidence level (0-1).
            Default: 0.95 (95% CI)

    Returns:
        pd.DataFrame: Predictions with columns:
            - fecha (datetime64[ns]): Future date
            - dias_desde_inicio (float64): Time index
            - {var}_pred (float64): Point prediction
            - {var}_lower (float64): Lower CI bound
            - {var}_upper (float64): Upper CI bound
            For each variable in columnas_objetivo

    Stores:
        self.predicciones: Result DataFrame

    Confidence Interval Calculation:
        CI = ŷ ± z * σ_residuals

        Where:
            - ŷ: Point prediction
            - z: z-score for confidence level (e.g., 1.96 for 95%)
            - σ_residuals: Std dev of training residuals

    Time Complexity: O(dias_futuro * k * d)
    Space Complexity: O(dias_futuro * k)

    Example:
        >>> pred = predictor.predecir_futuro(dias_futuro=60)
        >>> print(pred[['fecha', 'vegetation_pct_pred']].head())
                fecha  vegetation_pct_pred
        0  2025-11-01                 45.2
        1  2025-11-02                 45.3
    """
```

#### evaluar_modelos

```python
def evaluar_modelos(self) -> dict:
    """
    Evaluate model performance on training data.

    Returns:
        dict: Metrics for each variable.
            Keys: Variable names (str)
            Values: dict with:
                - r2 (float): R² score
                - rmse (float): Root mean squared error
                - mae (float): Mean absolute error
                - mape (float): Mean absolute percentage error

    Raises:
        RuntimeError: If models not trained

    Metrics:
        - R² = 1 - (SS_res / SS_tot)
        - RMSE = sqrt(mean((y - ŷ)²))
        - MAE = mean(|y - ŷ|)
        - MAPE = mean(|y - ŷ| / |y|) * 100

    Time Complexity: O(n * k)
    Space Complexity: O(k)

    Example:
        >>> metrics = predictor.evaluar_modelos()
        >>> print(metrics['vegetation_pct'])
        {'r2': 0.89, 'rmse': 3.42, 'mae': 2.67, 'mape': 5.8}
    """
```

## Utility Functions

### src.utils.visualizacion

#### crear_grafico_series_temporales

```python
def crear_grafico_series_temporales(
    df: pd.DataFrame,
    columna_fecha: str,
    columnas_y: List[str],
    titulo: str = "Series Temporales",
    ruta_salida: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6),
    dpi: int = 100
) -> None:
    """
    Create time series line plot.

    Args:
        df (pd.DataFrame): Data with time series
        columna_fecha (str): Date column name
        columnas_y (List[str]): Variables to plot
        titulo (str): Plot title
        ruta_salida (Optional[str]): Save path (if None, uses default)
        figsize (Tuple[int, int]): Figure size (width, height) in inches
        dpi (int): Resolution

    Raises:
        ValueError: If columns not in DataFrame
        OSError: If save path not writable

    Plot Style:
        - Multiple lines (one per variable)
        - Line width: 2
        - Markers: 'o', size 4
        - Grid: True, alpha 0.3
        - Legend: Upper right
        - X-axis: Dates, rotated 45°
        - Y-axis: Percentage label

    Example:
        >>> crear_grafico_series_temporales(
        ...     df_temporal,
        ...     'fecha',
        ...     ['vegetation_pct', 'water_pct'],
        ...     titulo="Vegetation and Water Trends"
        ... )
    """
```

#### crear_mapa_coropletas

```python
def crear_mapa_coropletas(
    df: pd.DataFrame,
    columna_lat: str,
    columna_lon: str,
    columna_valor: str,
    titulo: str = "Mapa de Coroplestas",
    colormap: str = 'YlOrRd',
    ruta_salida: Optional[str] = None
) -> str:
    """
    Create choropleth map visualization.

    Args:
        df (pd.DataFrame): Data with coordinates and values
        columna_lat (str): Latitude column
        columna_lon (str): Longitude column
        columna_valor (str): Value column for color scale
        titulo (str): Map title
        colormap (str): Matplotlib colormap name
        ruta_salida (Optional[str]): Save path

    Returns:
        str: Path to generated HTML file

    Map Features:
        - Circle markers sized by value
        - Color gradient based on colormap
        - Popup with value
        - Legend with color scale
        - Base: OpenStreetMap

    Example:
        >>> crear_mapa_coropletas(
        ...     df_mosquitos,
        ...     'latitude',
        ...     'longitude',
        ...     'larvae_count',
        ...     colormap='Reds'
        ... )
    """
```

### src.utils.metricas

#### calcular_metricas_clasificacion

```python
def calcular_metricas_clasificacion(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> dict:
    """
    Calculate classification metrics.

    Args:
        y_true (np.ndarray): True labels
        y_pred (np.ndarray): Predicted labels

    Returns:
        dict: Metrics including accuracy, precision, recall, F1

    Example:
        >>> metrics = calcular_metricas_clasificacion(y_test, y_pred)
    """
```

#### calcular_metricas_regresion

```python
def calcular_metricas_regresion(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> dict:
    """
    Calculate regression metrics.

    Args:
        y_true (np.ndarray): True values
        y_pred (np.ndarray): Predicted values

    Returns:
        dict: Metrics including R², RMSE, MAE, MAPE

    Example:
        >>> metrics = calcular_metricas_regresion(y_test, y_pred)
    """
```

## Quick Reference

### Complete Workflow

```python
# 1. Load Data
from src.data_loader import DataLoader

loader = DataLoader()
df_mosquitos = loader.cargar_datos_mosquitos()
df_imagery = loader.cargar_datos_imagery()
df_temporal = loader.cargar_datos_temporales()

# 2. Analyze Mosquitos
from src.analisis_mosquitos import AnalizadorMosquitos

analizador_mosq = AnalizadorMosquitos(df_mosquitos)
resultados_mosq = analizador_mosq.ejecutar_analisis_completo()

# 3. Analyze Land Cover
from src.analisis_cobertura import AnalizadorCobertura

analizador_cob = AnalizadorCobertura(df_imagery)
resultados_cob = analizador_cob.ejecutar_analisis_completo()

# 4. Predict Mosquito Presence
from src.prediccion import PredictorMosquitos

predictor_mosq = PredictorMosquitos(df_imagery, df_mosquitos)
predictor_mosq.preparar_datos()
predictor_mosq.entrenar_modelo()
metrics = predictor_mosq.evaluar_modelo()

# 5. Forecast Temporal Trends
from src.prediccion_temporal import PredictorTemporal

predictor_temp = PredictorTemporal(df_temporal)
predictor_temp.preparar_datos()
predictor_temp.entrenar_modelos(grado=2)
predicciones = predictor_temp.predecir_futuro(dias_futuro=30)
```

### Exception Handling

```python
from src.data_loader import DataLoader

try:
    loader = DataLoader()
    df = loader.cargar_datos_mosquitos(ruta='data/raw/file.csv')
except FileNotFoundError:
    print("Error: CSV file not found")
except pd.errors.EmptyDataError:
    print("Error: CSV file is empty")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Type Hints Summary

```python
from typing import Optional, List, Tuple, Dict
import pandas as pd
import numpy as np

# DataLoader
def cargar_datos_mosquitos(ruta: str) -> pd.DataFrame: ...

# AnalizadorMosquitos
def analizar_especies() -> pd.Series: ...
def analizar_fuentes_agua() -> pd.DataFrame: ...
def ejecutar_analisis_completo() -> Dict: ...

# PredictorMosquitos
def preparar_datos(test_size: float, random_state: int) -> None: ...
def entrenar_modelo(n_estimators: int, max_depth: Optional[int]) -> None: ...
def evaluar_modelo() -> Dict: ...

# PredictorTemporal
def predecir_futuro(dias_futuro: int, intervalo_confianza: float) -> pd.DataFrame: ...
```

For complete system architecture, see [Architecture](01_ARCHITECTURE.md).

For detailed algorithm explanations, see [Analysis Modules](02_ANALYSIS_MODULES.md) and [Prediction System](03_PREDICTION_SYSTEM.md).

For data structure details, see [Data Structures](04_DATA_STRUCTURES.md).
