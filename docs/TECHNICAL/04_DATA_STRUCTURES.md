# Data Structures - Technical Reference

Complete specification of data formats, schemas, validation rules, and transformations.

## Table of Contents

1. [CSV Data Structures](#csv-data-structures)
2. [GeoJSON Data Structures](#geojson-data-structures)
3. [Internal Data Structures](#internal-data-structures)
4. [Validation Rules](#validation-rules)
5. [Data Transformations](#data-transformations)

## CSV Data Structures

### Mosquito Habitat Mapper CSV

**File:** `AdoptAPixel3km2020_GO_MosquitoHabitatMapper.csv`

**Source:** GLOBE Observer Mosquito Habitat Mapper Protocol

**Purpose:** Citizen science mosquito habitat observations

**Schema:**

| Column                                          | Type    | Range/Format                      | Nullable | Description                             |
| ----------------------------------------------- | ------- | --------------------------------- | -------- | --------------------------------------- |
| `OBJECTID`                                      | int     | 1+                                | No       | Unique database identifier              |
| `mosquitohabitatmapperMosquitoHabitatMapperId`  | int     | 1+                                | No       | Observation ID                          |
| `protocol`                                      | string  | Fixed: "mosquito_habitat_mapper"  | No       | Protocol type                           |
| `mosquitohabitatmapperDataSource`               | string  | "GLOBE Observer App"              | No       | Data collection tool                    |
| `mosquitohabitatmapperMeasuredAt`               | string  | "M/D/YY H:MM"                     | No       | Observation timestamp                   |
| `siteName`                                      | string  | MGRS format (e.g., "14RPU075612") | Yes      | Military Grid Reference System location |
| `elevation`                                     | float   | meters                            | Yes      | Elevation above sea level               |
| `mosquitohabitatmapperMeasurementLatitude`      | float   | -90 to +90                        | No       | Latitude (WGS84)                        |
| `mosquitohabitatmapperMeasurementLongitude`     | float   | -180 to +180                      | No       | Longitude (WGS84)                       |
| `mosquitohabitatmapperGenus`                    | string  | Taxonomy (e.g., "Aedes", "Culex") | Yes      | Mosquito genus                          |
| `mosquitohabitatmapperSpecies`                  | string  | Scientific name                   | Yes      | Species name                            |
| `mosquitohabitatmapperWaterSource`              | string  | Categorical                       | Yes      | Water source type                       |
| `mosquitohabitatmapperWaterSourceType`          | string  | Categorical                       | Yes      | Source classification                   |
| `mosquitohabitatmapperLarvaeCount`              | int     | 0+                                | Yes      | Number of larvae observed               |
| `mosquitohabitatmapperLast IdentifyStage`       | string  | Protocol stage                    | Yes      | Identification stage reached            |
| `mosquitohabitatmapperMosquitoAdults`           | boolean | TRUE/FALSE                        | Yes      | Adult mosquitoes present                |
| `mosquitohabitatmapperMosquitoEggs`             | boolean | TRUE/FALSE                        | Yes      | Eggs present                            |
| `mosquitohabitatmapperMosquitoPupae`            | boolean | TRUE/FALSE                        | Yes      | Pupae present                           |
| `mosquitohabitatmapperBreedingGroundEliminated` | boolean | TRUE/FALSE                        | Yes      | Site was eliminated                     |
| `mosquitohabitatmapperComments`                 | string  | Free text                         | Yes      | Observer notes                          |
| `mosquitohabitatmapperWaterSourcePhotoUrls`     | string  | Semicolon-separated URLs          | Yes      | Photo URLs                              |
| `mosquitohabitatmapperLarvaFullBodyPhotoUrls`   | string  | Semicolon-separated URLs          | Yes      | Larvae photos                           |
| `mosquitohabitatmapperAbdomenCloseupPhotoUrls`  | string  | Semicolon-separated URLs          | Yes      | Abdomen closeup photos                  |
| `mosquitohabitatmapperExtraData`                | string  | JSON                              | Yes      | Additional metadata                     |

**Water Source Categories:**

```python
WATER_SOURCE_TYPES = [
    "container: artificial",  # Human-made containers
    "still: lake/pond/swamp", # Natural standing water
    "flowing: river/stream",  # Moving water
    "pond",
    "ditch",
    "ovitrap",               # Mosquito trap
    "adult mosquito trap",
    "can or bottle",
    "puddle, vehicle or animal tracks",
    "other"
]
```

**Genus Values:**

```python
MOSQUITO_GENUS = [
    "Aedes",        # Disease vectors (dengue, Zika, yellow fever)
    "Culex",        # Common house mosquito, West Nile virus
    "Anopheles",    # Malaria vector
    "Psorophora",   # Floodwater mosquito
    "Toxorhynchites", # Non-biting, predatory
    "Unknown"       # Not identified
]
```

**Example Record:**

```csv
12,23971,mosquito_habitat_mapper,GLOBE Observer App,6/29/20 19:04,19QFV960942,28.7,18.0278,-67.14770,null,FALSE,"There's larvae of all sizes.",null,null,null,null,identify-saddle-comb,TRUE,null,FALSE,FALSE,null,"cement, metal or plastic tank",https://data.globe.gov/system/photos/2020/06/29/1724939/original.jpg,container: artificial
```

### Land Cover CSV

**File:** `AdoptAPixel3km2020_GO_LandCover.csv`

**Source:** GLOBE Observer Land Cover Protocol

**Purpose:** Ground truth land cover observations

**Schema:**

| Column                 | Type   | Range        | Description                         |
| ---------------------- | ------ | ------------ | ----------------------------------- |
| `OBJECTID`             | int    | 1+           | Unique identifier                   |
| `landCoverId`          | int    | 1+           | Observation ID                      |
| `protocol`             | string | "land_cover" | Protocol type                       |
| `dataSource`           | string | App name     | Data source                         |
| `measuredAt`           | string | ISO date     | Observation timestamp               |
| `measurementLatitude`  | float  | -90 to +90   | Latitude                            |
| `measurementLongitude` | float  | -180 to +180 | Longitude                           |
| `MUC_*` columns        | int    | 0-100        | Land Use Classification percentages |
| `photoUrls`            | string | URLs         | Observation photos                  |

**MUC Columns (Most Dominant Land Cover):**

- MUC_code: Numeric code
- MUC_name: Text description

### Aerial Imagery Labels CSV

**File:** `AdoptAPixel3km2020_100m_aerialImageryLabels.csv`

**Source:** CEO (Collect Earth Online) aerial imagery classification

**Purpose:** Machine learning training/validation data

**Schema:**

| Column                        | Type   | Range        | Description              |
| ----------------------------- | ------ | ------------ | ------------------------ |
| `ceoPLOTID`                   | int    | 1+           | Plot identifier          |
| `ceoLON`                      | float  | -180 to +180 | Plot center longitude    |
| `ceoLAT`                      | float  | -90 to +90   | Plot center latitude     |
| `ceoTREES_CANOPYCOVER`        | float  | 0-100        | Tree canopy coverage (%) |
| `ceoBUSH_SCRUB`               | float  | 0-100        | Bush/scrub coverage (%)  |
| `ceoGRASS`                    | float  | 0-100        | Grass coverage (%)       |
| `ceoBuilding`                 | float  | 0-100        | Building coverage (%)    |
| `ceoImperviousSurface`        | float  | 0-100        | Impervious surface (%)   |
| `ceoWaterLakePondedContainer` | float  | 0-100        | Water bodies (%)         |
| `ceoSampleGeometry`           | string | WKT          | Plot geometry (POINT)    |

**Validation Rules:**

```python
# Coverage constraints
assert 0 <= coverage <= 100 for all ceo* columns

# Coordinate validation
assert -90 <= ceoLAT <= 90
assert -180 <= ceoLON <= 180

# Completeness (optional, allows partial coverage)
total_coverage = sum([trees, bush, grass, building, impervious, water])
# Note: May not sum to 100% (bare ground, clouds, etc.)
```

**Example Record:**

```python
{
    'ceoPLOTID': 1,
    'ceoLON': -97.8805,
    'ceoLAT': 30.3787,
    'ceoTREES_CANOPYCOVER': 45.0,
    'ceoBUSH_SCRUB': 20.0,
    'ceoGRASS': 15.0,
    'ceoBuilding': 5.0,
    'ceoImperviousSurface': 10.0,
    'ceoWaterLakePondedContainer': 5.0,
    'ceoSampleGeometry': 'POINT(-97.8805 30.3787)'
}
```

## GeoJSON Data Structures

### Sentinel-2 GeoJSON

**Files:** `S2A_T12RWU_YYYYMMDDTHHMMSS_L2A.geojson` and `S2B_T12RWU_YYYYMMDDTHHMMSS_L2A.geojson`

**Source:** ESA Sentinel-2 satellites (S2A and S2B)

**Purpose:** Multispectral satellite imagery metadata and surface classification

**Filename Convention:**

```
S2{A|B}_T{MGRS}_YYYYMMDDTHHMMSS_L2A.geojson

Where:
  S2A/S2B: Sentinel-2A or 2B satellite
  T: Tile indicator
  MGRS: Military Grid Reference System tile (e.g., 12RWU)
  YYYYMMDD: Acquisition date
  THHMMSS: Acquisition time (UTC)
  L2A: Processing level (atmospherically corrected)
```

**Schema:**

```json
{
    "type": "Feature",
    "id": "S2A_T12RWU_20250422T175740_L2A",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [lon1, lat1],
            [lon2, lat2],
            [lon3, lat3],
            [lon4, lat4],
            [lon1, lat1]
        ]]
    },
    "properties": {
        "datetime": "2025-04-22T17:57:40Z",
        "platform": "Sentinel-2A",
        "instruments": ["MSI"],
        "constellation": "Sentinel-2",
        "eo:cloud_cover": 12.5,
        "s2:vegetation_percentage": 45.2,
        "s2:not_vegetated_percentage": 38.1,
        "s2:water_percentage": 8.3,
        "s2:snow_ice_percentage": 0.0,
        "s2:unclassified_percentage": 8.4,
        "s2:high_proba_clouds_percentage": 5.2,
        "s2:medium_proba_clouds_percentage": 4.1,
        "s2:thin_cirrus_percentage": 3.2,
        "s2:cloud_shadow_percentage": 2.8,
        "s2:dark_features_percentage": 1.5,
        "processing:level": "L2A",
        "processing:software": {
            "sen2cor": "2.10"
        }
    }
}
```

**Properties Specification:**

| Property                            | Type   | Range                          | Description                         |
| ----------------------------------- | ------ | ------------------------------ | ----------------------------------- |
| `datetime`                          | string | ISO 8601                       | Acquisition timestamp (UTC)         |
| `platform`                          | string | "Sentinel-2A" or "Sentinel-2B" | Satellite platform                  |
| `instruments`                       | array  | ["MSI"]                        | Multispectral Instrument            |
| `constellation`                     | string | "Sentinel-2"                   | Satellite constellation             |
| `eo:cloud_cover`                    | float  | 0-100                          | Cloud coverage percentage           |
| `s2:vegetation_percentage`          | float  | 0-100                          | Vegetation coverage                 |
| `s2:not_vegetated_percentage`       | float  | 0-100                          | Non-vegetated land                  |
| `s2:water_percentage`               | float  | 0-100                          | Water bodies                        |
| `s2:snow_ice_percentage`            | float  | 0-100                          | Snow and ice                        |
| `s2:unclassified_percentage`        | float  | 0-100                          | Unclassified pixels                 |
| `s2:high_proba_clouds_percentage`   | float  | 0-100                          | High probability clouds             |
| `s2:medium_proba_clouds_percentage` | float  | 0-100                          | Medium probability clouds           |
| `s2:thin_cirrus_percentage`         | float  | 0-100                          | Thin cirrus clouds                  |
| `s2:cloud_shadow_percentage`        | float  | 0-100                          | Cloud shadows                       |
| `s2:dark_features_percentage`       | float  | 0-100                          | Dark features (water, shadows)      |
| `processing:level`                  | string | "L2A"                          | Processing level (L1C=TOA, L2A=BOA) |

**Surface Classification Details:**

```python
# Sentinel-2 Scene Classification Layer (SCL)
SCL_CLASSES = {
    0: "NO_DATA",
    1: "SATURATED_OR_DEFECTIVE",
    2: "DARK_AREA_PIXELS",          # Water, shadows
    3: "CLOUD_SHADOWS",
    4: "VEGETATION",
    5: "NOT_VEGETATED",             # Bare soil, rocks, buildings
    6: "WATER",
    7: "UNCLASSIFIED",
    8: "CLOUD_MEDIUM_PROBABILITY",
    9: "CLOUD_HIGH_PROBABILITY",
    10: "THIN_CIRRUS",
    11: "SNOW_ICE"
}

# Aggregation for analysis
VEGETATION_CLASSES = [4]
NOT_VEGETATED_CLASSES = [5]
WATER_CLASSES = [6]
CLOUD_CLASSES = [8, 9, 10]
SNOW_ICE_CLASSES = [11]
```

## Internal Data Structures

### DataFrames

**Post-Processing DataFrames (after DataLoader):**

#### df_mosquitos

```python
pd.DataFrame({
    # Original columns (all from CSV)
    'OBJECTID': int64,
    'mosquitohabitatmapperMosquitoHabitatMapperId': int64,
    'protocol': object,
    'mosquitohabitatmapperDataSource': object,
    'mosquitohabitatmapperMeasuredAt': object,
    'siteName': object,
    'elevation': float64,
    'mosquitohabitatmapperMeasurementLatitude': float64,
    'mosquitohabitatmapperMeasurementLongitude': float64,
    'mosquitohabitatmapperGenus': object,
    'mosquitohabitatmapperWaterSource': object,
    'mosquitohabitatmapperLarvaeCount': float64,
    # ... (all other columns)

    # Added by DataLoader.cargar_datos_mosquitos()
    'fecha': datetime64[ns],        # Parsed from mosquitohabitatmapperMeasuredAt
    'mes': int64,                   # Month (1-12)
    'año': int64                    # Year (e.g., 2020)
})
```

#### df_imagery

```python
pd.DataFrame({
    'ceoPLOTID': int64,
    'ceoLON': float64,
    'ceoLAT': float64,
    'ceoTREES_CANOPYCOVER': float64,
    'ceoBUSH_SCRUB': float64,
    'ceoGRASS': float64,
    'ceoBuilding': float64,
    'ceoImperviousSurface': float64,
    'ceoWaterLakePondedContainer': float64,
    'ceoSampleGeometry': object
})
```

#### df_temporal (Sentinel-2 time series)

```python
pd.DataFrame({
    'fecha': datetime64[ns],                # Acquisition date
    'cloud_cover': float64,                 # Cloud percentage
    'vegetation_pct': float64,              # Vegetation percentage
    'not_vegetated_pct': float64,           # Non-vegetated percentage
    'water_pct': float64,                   # Water percentage
    'snow_ice_pct': float64,                # Snow/ice percentage
    'unclassified_pct': float64,            # Unclassified percentage
    'archivo': object,                      # Source filename
    'dias_desde_inicio': float64           # Days since first observation
})
```

### Analysis Results Dictionaries

#### AnalizadorMosquitos.resultados

```python
{
    'especies': pd.Series,                 # Genus counts
    'fuentes_agua': pd.DataFrame,          # Water source distribution
    'reportes_mensuales': pd.Series,       # Monthly observation counts
    'larvas': {
        'con_larvas': int,
        'sin_larvas': int,
        'porcentaje_con_larvas': float
    },
    'mapa_calor': str,                     # Path to heatmap HTML
    'mapa_marcadores': str                 # Path to marker map HTML
}
```

#### AnalizadorCobertura.resultados

```python
{
    'promedios': pd.Series,                # Mean coverage percentages
    'areas_con_agua': pd.DataFrame,        # Water-containing observations
    'correlaciones': pd.DataFrame,         # Correlation matrix (m × m)
    'vegetacion_urbano': {
        'vegetacion_total': float,
        'urbano_total': float,
        'diferencia': float,
        'ratio': float
    }
}
```

#### PredictorMosquitos.resultados

```python
{
    'train_score': float,                  # Training accuracy
    'test_score': float,                   # Test accuracy
    'accuracy': float,                     # Overall accuracy
    'precision': float,                    # Precision
    'recall': float,                       # Recall (sensitivity)
    'f1_score': float,                     # F1-score
    'confusion_matrix': np.ndarray,        # 2×2 matrix
    'classification_report': str,          # Detailed report
    'cv_scores': np.ndarray,               # Cross-validation scores
    'cv_mean': float,                      # Mean CV score
    'cv_std': float,                       # Std dev CV score
    'feature_importances': pd.DataFrame    # Feature importance ranking
}
```

#### PredictorTemporal Predictions

```python
pd.DataFrame({
    'fecha': datetime64[ns],               # Future date
    'dias_desde_inicio': float64,          # Numeric time index
    'vegetation_pct_pred': float64,        # Predicted vegetation
    'vegetation_pct_lower': float64,       # Lower confidence bound
    'vegetation_pct_upper': float64,       # Upper confidence bound
    'water_pct_pred': float64,             # Predicted water
    'water_pct_lower': float64,
    'water_pct_upper': float64,
    # ... (other variables)
})
```

## Validation Rules

### Data Quality Checks

**Coordinate Validation:**

```python
def validate_coordinates(lat: float, lon: float) -> bool:
    """
    Validate geographic coordinates.

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        bool: True if valid

    Rules:
        - Latitude: -90 to +90 (inclusive)
        - Longitude: -180 to +180 (inclusive)
        - Not null
        - Not (0, 0) unless in Gulf of Guinea
    """
    if pd.isna(lat) or pd.isna(lon):
        return False
    if not (-90 <= lat <= 90):
        return False
    if not (-180 <= lon <= 180):
        return False
    if lat == 0 and lon == 0:
        return False  # Likely missing data
    return True
```

**Coverage Percentage Validation:**

```python
def validate_coverage(value: float, column_name: str) -> bool:
    """
    Validate coverage percentage values.

    Args:
        value: Coverage percentage
        column_name: Column name for context

    Returns:
        bool: True if valid

    Rules:
        - Range: 0 to 100 (inclusive)
        - Null allowed (missing observations)
    """
    if pd.isna(value):
        return True  # Allow missing
    return 0 <= value <= 100
```

**Temporal Consistency:**

```python
def validate_temporal_ordering(df: pd.DataFrame) -> bool:
    """
    Validate temporal ordering of time series data.

    Args:
        df: DataFrame with 'fecha' column

    Returns:
        bool: True if dates are monotonically increasing

    Rules:
        - Dates must be in chronological order
        - No duplicate dates (aggregate if needed)
        - No future dates beyond present
    """
    dates = pd.to_datetime(df['fecha'])
    is_sorted = dates.is_monotonic_increasing
    has_duplicates = dates.duplicated().any()
    has_future_dates = (dates > pd.Timestamp.now()).any()

    return is_sorted and not has_duplicates and not has_future_dates
```

**Data Completeness:**

```python
def check_completeness(df: pd.DataFrame, required_columns: list) -> dict:
    """
    Check data completeness.

    Args:
        df: DataFrame to check
        required_columns: List of required column names

    Returns:
        dict: {
            'missing_columns': list,
            'null_counts': dict,
            'completeness_pct': float
        }
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    null_counts = df[required_columns].isnull().sum().to_dict()
    total_values = len(df) * len(required_columns)
    null_values = sum(null_counts.values())
    completeness = ((total_values - null_values) / total_values) * 100

    return {
        'missing_columns': missing_cols,
        'null_counts': null_counts,
        'completeness_pct': completeness
    }
```

### Data Cleaning

**Outlier Detection:**

```python
def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5) -> pd.Series:
    """
    Detect outliers using Interquartile Range method.

    Args:
        series: Numeric series
        multiplier: IQR multiplier (default: 1.5)

    Returns:
        pd.Series: Boolean mask (True = outlier)

    Algorithm:
        1. Compute Q1 (25th percentile)
        2. Compute Q3 (75th percentile)
        3. IQR = Q3 - Q1
        4. Lower bound = Q1 - multiplier × IQR
        5. Upper bound = Q3 + multiplier × IQR
        6. Outliers: values < lower or > upper
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR
    return (series < lower) | (series > upper)
```

**Missing Data Handling:**

```python
def handle_missing_data(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
    """
    Handle missing data.

    Args:
        df: Input DataFrame
        strategy: Handling strategy
            - 'drop': Remove rows with any nulls
            - 'fill_mean': Fill numeric with mean
            - 'fill_median': Fill numeric with median
            - 'fill_mode': Fill categorical with mode
            - 'interpolate': Linear interpolation (time series)

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    if strategy == 'drop':
        return df.dropna()

    elif strategy == 'fill_mean':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        return df

    elif strategy == 'fill_median':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        return df

    elif strategy == 'fill_mode':
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = df[col].fillna(df[col].mode()[0])
        return df

    elif strategy == 'interpolate':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].interpolate(method='linear')
        return df

    else:
        raise ValueError(f"Unknown strategy: {strategy}")
```

## Data Transformations

### Date Parsing

```python
def parse_globe_observer_date(date_str: str) -> pd.Timestamp:
    """
    Parse GLOBE Observer date format.

    Args:
        date_str: Date string (e.g., "6/29/20 19:04")

    Returns:
        pd.Timestamp: Parsed datetime

    Format: "M/D/YY H:MM" or "M/D/YY HH:MM"
        - Month: 1-12 (no leading zero)
        - Day: 1-31 (no leading zero)
        - Year: 2-digit (assumes 2000s)
        - Hour: 0-23
        - Minute: 00-59

    Example:
        "6/29/20 19:04" → 2020-06-29 19:04:00
    """
    return pd.to_datetime(date_str, format='%m/%d/%y %H:%M')
```

### Feature Engineering

```python
def extract_temporal_features(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """
    Extract temporal features from datetime column.

    Args:
        df: Input DataFrame
        date_col: Name of datetime column

    Returns:
        pd.DataFrame: DataFrame with added features

    Features Added:
        - año: Year (int)
        - mes: Month (1-12)
        - dia: Day of month (1-31)
        - dia_semana: Day of week (0=Monday, 6=Sunday)
        - dia_año: Day of year (1-366)
        - semana_año: Week of year (1-53)
        - trimestre: Quarter (1-4)
        - es_fin_semana: Weekend flag (bool)
        - estacion: Season (str, Northern Hemisphere)
    """
    df['año'] = df[date_col].dt.year
    df['mes'] = df[date_col].dt.month
    df['dia'] = df[date_col].dt.day
    df['dia_semana'] = df[date_col].dt.dayofweek
    df['dia_año'] = df[date_col].dt.dayofyear
    df['semana_año'] = df[date_col].dt.isocalendar().week
    df['trimestre'] = df[date_col].dt.quarter
    df['es_fin_semana'] = df['dia_semana'].isin([5, 6])

    # Season (Northern Hemisphere)
    mes = df['mes']
    df['estacion'] = pd.cut(
        mes,
        bins=[0, 3, 6, 9, 12],
        labels=['Invierno', 'Primavera', 'Verano', 'Otoño']
    )

    return df
```

### Coordinate Transformations

```python
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great circle distance between two points.

    Args:
        lat1, lon1: First point (degrees)
        lat2, lon2: Second point (degrees)

    Returns:
        float: Distance in kilometers

    Formula:
        a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
        c = 2 × atan2(√a, √(1-a))
        d = R × c

        Where R = 6371 km (Earth's radius)
    """
    from math import radians, sin, cos, sqrt, atan2

    R = 6371  # Earth radius in km

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance
```

### Data Aggregation

```python
def aggregate_sentinel2_by_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate multiple Sentinel-2 observations per date.

    Args:
        df: Temporal DataFrame with multiple obs per date

    Returns:
        pd.DataFrame: One row per unique date

    Aggregation Strategy:
        - fecha: First occurrence (date only)
        - Percentages: Mean across observations
        - cloud_cover: Minimum (select clearest image)
        - archivo: Concatenate filenames
    """
    df['fecha_only'] = df['fecha'].dt.date

    agg_dict = {
        'vegetation_pct': 'mean',
        'not_vegetated_pct': 'mean',
        'water_pct': 'mean',
        'snow_ice_pct': 'mean',
        'unclassified_pct': 'mean',
        'cloud_cover': 'min',  # Select clearest
        'archivo': lambda x: '; '.join(x)
    }

    df_agg = df.groupby('fecha_only').agg(agg_dict).reset_index()
    df_agg.rename(columns={'fecha_only': 'fecha'}, inplace=True)
    df_agg['fecha'] = pd.to_datetime(df_agg['fecha'])

    return df_agg
```

## Data Export Formats

### CSV Export

```python
# Predictions export
df_predictions.to_csv(
    'data/output/predicciones_futuras.csv',
    index=False,
    float_format='%.2f',
    encoding='utf-8'
)

# Columns: fecha, valor_predicho, confianza_inferior, confianza_superior
```

### HTML Export

```python
# DataFrames embedded in HTML reports
html_table = df.to_html(
    classes='data-table',
    border=0,
    index=False,
    float_format='%.2f',
    na_rep='N/A'
)
```

### GeoJSON Export (future feature)

```python
def dataframe_to_geojson(df: pd.DataFrame, lat_col: str, lon_col: str) -> dict:
    """Convert DataFrame to GeoJSON FeatureCollection."""
    features = []
    for _, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row[lon_col], row[lat_col]]
            },
            'properties': row.drop([lat_col, lon_col]).to_dict()
        }
        features.append(feature)

    return {
        'type': 'FeatureCollection',
        'features': features
    }
```

For complete API reference with method signatures, see [API Reference](05_API_REFERENCE.md).
