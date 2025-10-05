# Prediction System - Technical Reference

Comprehensive technical documentation for machine learning and temporal prediction systems.

## Table of Contents

1. [System Overview](#system-overview)
2. [PredictorMosquitos - Random Forest Classifier](#predictormosquitos)
3. [PredictorTemporal - Time Series Forecasting](#predictortemporal)
4. [Mathematical Foundations](#mathematical-foundations)
5. [Model Validation](#model-validation)
6. [Performance Optimization](#performance-optimization)

## System Overview

The prediction system implements two complementary approaches:

**Spatial Prediction (PredictorMosquitos):**

- Algorithm: Random Forest Classification
- Purpose: Predict mosquito habitat suitability
- Input: Land cover features (trees, grass, impervious surfaces)
- Output: Binary classification (habitat suitable: yes/no)
- Validation: Cross-validation, confusion matrix, ROC-AUC

**Temporal Prediction (PredictorTemporal):**

- Algorithm: Polynomial Regression
- Purpose: Forecast vegetation changes
- Input: Sentinel-2 time series data
- Output: Continuous predictions (30-90 days ahead)
- Validation: R², RMSE, residual analysis

## PredictorMosquitos

### Class Overview

**Location:** `src/prediccion.py`

**Purpose:** Binary classification model for mosquito habitat suitability prediction using Random Forest algorithm.

**Algorithm:** Random Forest Classifier (ensemble of decision trees)

### Class Definition

```python
class PredictorMosquitos:
    """
    Random Forest classifier for mosquito habitat prediction.

    Uses land cover characteristics to predict water presence
    as a proxy for mosquito breeding habitat suitability.

    Attributes:
        df (pd.DataFrame): Input imagery data
        modelo (RandomForestClassifier): Trained model
        X_train, X_test (pd.DataFrame): Feature matrices
        y_train, y_test (pd.Series): Target vectors
        feature_names (list): Feature column names
        resultados (dict): Metrics and results storage

    Model Configuration:
        n_estimators=100: Number of decision trees
        max_depth=10: Maximum tree depth
        min_samples_split=5: Minimum samples to split node
        min_samples_leaf=2: Minimum samples in leaf
        random_state=42: Reproducibility seed
        n_jobs=-1: Use all CPU cores
    """
```

### Constructor

```python
def __init__(self, df_imagery: pd.DataFrame) -> None:
    """
    Initialize mosquito habitat predictor.

    Args:
        df_imagery: DataFrame with land cover observations.
            Required columns:
                - ceoTREES_CANOPYCOVER (float): Tree canopy % [0-100]
                - ceoBUSH_SCRUB (float): Bush/scrub % [0-100]
                - ceoGRASS (float): Grass coverage % [0-100]
                - ceoImperviousSurface (float): Impervious surfaces % [0-100]
                - ceoWaterLakePondedContainer (float): Water presence % [0-100]

    Side Effects:
        - Initializes empty model attributes
        - Creates results dictionary

    Note:
        Model training occurs in separate preparar_datos() and
        entrenar_modelo() methods, not in constructor.
    """
```

### Methods

#### preparar_datos()

**Purpose:** Feature engineering and train/test split.

```python
def preparar_datos(self) -> bool:
    """
    Prepare features and target variable for modeling.

    Returns:
        bool: True if successful, False if required columns missing

    Algorithm:
        1. Select feature columns (trees, shrubs, grass, impervious)
        2. Create binary target: water > 0 → class 1, else → class 0
        3. Remove rows with missing values
        4. Stratified train/test split (70/30)
        5. Print dataset statistics

    Feature Selection Rationale:
        - Trees: Shade and moisture retention
        - Shrubs: Ground cover and water retention
        - Grass: Vegetation indicator
        - Impervious surfaces: Water runoff patterns

        Excluded:
        - Buildings: Redundant with impervious surfaces
        - Existing water: This is the target variable

    Target Variable:
        Proxy indicator: Water presence (ceoWaterLakePondedContainer > 0)
        Assumption: Water presence correlates with mosquito habitat

        Binary encoding:
            y = 1 if water > 0  (suitable habitat)
            y = 0 if water == 0 (unsuitable habitat)

    Train/Test Split:
        Method: train_test_split from scikit-learn
        Ratio: 70% training, 30% testing
        Stratification: Maintains class balance in both sets
        Random seed: 42 (reproducibility)

    Class Balance:
        Prints class distribution:
            - Class 1 count and percentage
            - Class 0 count and percentage

        Important: Imbalanced classes may require:
            - Class weighting
            - SMOTE oversampling
            - Adjusted decision threshold

    Performance:
        Time: O(n × m) for n rows, m features
        Space: O(n × m) for train/test sets

    Side Effects:
        - Sets self.X_train, self.X_test
        - Sets self.y_train, self.y_test
        - Sets self.feature_names
        - Prints statistics to stdout
    """
```

**Example Output:**

```
📊 Características seleccionadas:
   • ceoTREES_CANOPYCOVER
   • ceoBUSH_SCRUB
   • ceoGRASS
   • ceoImperviousSurface

🎯 Variable objetivo: ceoWaterLakePondedContainer
   (Presencia de agua como proxy para hábitat de mosquitos)

📈 Tamaño del dataset:
   Total de muestras: 1000
   Muestras con agua (clase 1): 450 (45.0%)
   Muestras sin agua (clase 0): 550 (55.0%)

✂️ División de datos:
   Entrenamiento: 700 muestras
   Prueba: 300 muestras
```

#### entrenar_modelo()

**Purpose:** Train Random Forest classifier.

```python
def entrenar_modelo(self) -> bool:
    """
    Train Random Forest classification model.

    Returns:
        bool: True if successful, False if data not prepared

    Algorithm:
        1. Instantiate RandomForestClassifier with hyperparameters
        2. Fit model on training data
        3. Evaluate on training set (check overfitting)
        4. Evaluate on test set (generalization)
        5. Store scores in results dict

    Random Forest Hyperparameters:
        n_estimators=100:
            - Number of decision trees in forest
            - More trees = better performance but slower
            - Diminishing returns beyond 100-200 trees

        max_depth=10:
            - Maximum depth of each tree
            - Prevents overfitting
            - Typical range: 5-20

        min_samples_split=5:
            - Minimum samples required to split internal node
            - Higher = more conservative (less overfitting)

        min_samples_leaf=2:
            - Minimum samples required in leaf node
            - Prevents tiny leaves that overfit noise

        random_state=42:
            - Seed for reproducibility
            - Same data → same model

        n_jobs=-1:
            - Use all available CPU cores
            - Parallelizes tree building

    Training Process:
        1. For each tree (parallelized):
            a. Bootstrap sample from training data
            b. Grow tree with random feature subsets
            c. Store trained tree
        2. Aggregate trees into ensemble
        3. Use majority voting for predictions

    Scoring:
        Training score: Model performance on training data
            - Should be high (>80%)
            - Much higher than test = overfitting

        Test score: Model performance on held-out data
            - True generalization metric
            - Should be close to training score
            - Gap > 10% suggests overfitting

    Performance:
        Time: O(n × m × log(n) × trees)
            - n: training samples
            - m: features
            - trees: n_estimators
            - Typical: 5-30 seconds for 1000 samples

        Space: O(trees × nodes)
            - Model size: ~1-10 MB typical

    Side Effects:
        - Sets self.modelo (trained classifier)
        - Updates self.resultados['train_score']
        - Updates self.resultados['test_score']
        - Prints training progress and scores
    """
```

#### validar_modelo()

**Purpose:** Compute comprehensive validation metrics.

```python
def validar_modelo(self) -> dict:
    """
    Calculate detailed performance metrics.

    Returns:
        dict: {
            'accuracy': float [0-1],
            'precision': float [0-1],
            'recall': float [0-1],
            'f1_score': float [0-1],
            'confusion_matrix': np.ndarray (2×2),
            'classification_report': str
        }

    Metrics Explained:

    Accuracy:
        Formula: (TP + TN) / (TP + TN + FP + FN)
        Meaning: Fraction of correct predictions
        Good when: Classes are balanced
        Problem: Misleading with imbalanced classes
        Example: 0.85 = 85% of predictions correct

    Precision:
        Formula: TP / (TP + FP)
        Meaning: Of positive predictions, how many are truly positive
        Good for: Minimizing false alarms
        Example: 0.80 = 80% of "habitat suitable" predictions are correct

    Recall (Sensitivity):
        Formula: TP / (TP + FN)
        Meaning: Of actual positives, how many are detected
        Good for: Minimizing missed cases
        Example: 0.75 = 75% of actual habitats are detected

    F1-Score:
        Formula: 2 × (Precision × Recall) / (Precision + Recall)
        Meaning: Harmonic mean of precision and recall
        Good for: Balanced metric when both matter
        Range: [0, 1], higher is better

    Confusion Matrix:
        Layout:
                    Predicted
                    0     1
        Actual  0  [TN   FP]
                1  [FN   TP]

        TN (True Negative): Correctly predicted no habitat
        FP (False Positive): Incorrectly predicted habitat
        FN (False Negative): Missed actual habitat
        TP (True Positive): Correctly predicted habitat

    Classification Report:
        Detailed per-class metrics:
            - Precision, recall, F1 for each class
            - Support (number of samples per class)
            - Weighted and macro averages

    Performance:
        Time: O(n_test) for predictions + O(1) for metrics
        Space: O(1) for metric storage

    Side Effects:
        - Updates self.resultados with all metrics
        - Prints metrics to stdout
    """
```

#### validacion_cruzada()

**Purpose:** K-fold cross-validation for robust performance estimation.

```python
def validacion_cruzada(self, cv: int = 5) -> dict:
    """
    Perform k-fold cross-validation.

    Args:
        cv: Number of folds (default: 5)

    Returns:
        dict: {
            'scores': np.ndarray (cv scores),
            'mean': float (average score),
            'std': float (standard deviation)
        }

    Algorithm:
        1. Split data into k folds
        2. For each fold:
            - Train on k-1 folds
            - Test on remaining fold
            - Record score
        3. Compute mean and standard deviation

    Cross-Validation Benefits:
        - More robust than single train/test split
        - Uses all data for both training and testing
        - Provides confidence interval (mean ± std)
        - Detects overfitting (high variance in scores)

    Fold Selection:
        k=5: Standard choice, good bias-variance trade-off
        k=10: More thorough, slower
        k=n (LOO): Maximum rigor, very slow

    Stratification:
        Automatically applied by cross_val_score
        Maintains class proportions in each fold

    Interpretation:
        Mean score: Expected performance on unseen data
        Std dev: Consistency across different splits
            - Low std (<0.05): Stable model
            - High std (>0.10): Unstable, dataset-dependent

    Performance:
        Time: O(cv × training_time)
        Typical: 30-90 seconds for cv=5

    Example Output:
        Fold 1: 0.83
        Fold 2: 0.85
        Fold 3: 0.82
        Fold 4: 0.84
        Fold 5: 0.83
        Mean: 0.834 ± 0.011
    """
```

#### obtener_importancia_features()

**Purpose:** Extract and rank feature importance scores.

```python
def obtener_importancia_features(self) -> pd.DataFrame:
    """
    Get feature importance from trained model.

    Returns:
        pd.DataFrame: Features ranked by importance
            Columns: ['feature', 'importance']
            Sorted: Descending by importance

    Feature Importance Calculation:
        Random Forest computes importance as:
            - Mean decrease in impurity (Gini importance)
            - Averaged across all trees
            - Normalized to sum to 1.0

    Interpretation:
        High importance (>0.3): Strong predictor
        Medium importance (0.1-0.3): Moderate predictor
        Low importance (<0.1): Weak predictor, consider removing

    Use Cases:
        - Understand model decision-making
        - Feature selection (remove low-importance features)
        - Domain insight (which factors matter most)
        - Model validation (check if logical)

    Caveats:
        - Biased toward high-cardinality features
        - Doesn't account for feature interactions
        - Alternative: Permutation importance (more robust)

    Visualization:
        Generates horizontal bar chart showing importance scores

    Example Output:
        Feature                    Importance
        ceoTREES_CANOPYCOVER       0.42
        ceoGRASS                   0.28
        ceoImperviousSurface       0.18
        ceoBUSH_SCRUB              0.12
    """
```

#### generar_visualizaciones()

**Purpose:** Create confusion matrix and feature importance plots.

```python
def generar_visualizaciones(self) -> None:
    """
    Generate model interpretation visualizations.

    Outputs:
        - data/output/matriz_confusion.png
        - data/output/importancia_features.png

    Confusion Matrix Heatmap:
        - 2×2 grid (actual vs. predicted)
        - Color: YlOrRd (yellow to red)
        - Annotations: Cell counts
        - Format: Integer counts

    Feature Importance Bar Chart:
        - Horizontal bars
        - Color: skyblue
        - Sorted: Descending importance
        - X-axis: Importance score [0-1]

    Chart Specifications:
        Size: (10, 8) inches
        DPI: 300
        Format: PNG
        Layout: tight_layout()

    Performance:
        Time: ~2 seconds
        I/O: 2 PNG files (~1MB each)
    """
```

#### predecir()

**Purpose:** Make predictions on new data.

```python
def predecir(self, X_new: pd.DataFrame) -> np.ndarray:
    """
    Predict habitat suitability for new observations.

    Args:
        X_new: DataFrame with same features as training data
            Must contain: ceoTREES_CANOPYCOVER, ceoBUSH_SCRUB,
                         ceoGRASS, ceoImperviousSurface

    Returns:
        np.ndarray: Binary predictions [0, 1]
            0 = Unsuitable habitat
            1 = Suitable habitat

    Algorithm:
        1. Validate input features match training features
        2. For each tree in forest:
            - Traverse tree with input features
            - Reach leaf node with prediction
        3. Majority vote across all trees
        4. Return binary class

    Prediction Confidence:
        Use predict_proba() for probability scores:
            probs = modelo.predict_proba(X_new)
            probs[:, 1]  # Probability of class 1

    Performance:
        Time: O(n × trees × depth)
        Typical: <1ms per prediction

    Example:
        new_obs = pd.DataFrame({
            'ceoTREES_CANOPYCOVER': [45.0],
            'ceoBUSH_SCRUB': [20.0],
            'ceoGRASS': [15.0],
            'ceoImperviousSurface': [5.0]
        })
        prediction = predictor.predecir(new_obs)
        print(f"Habitat suitable: {prediction[0] == 1}")
    """
```

### Usage Example

```python
from src.prediccion import PredictorMosquitos
from src.utils.data_loader import DataLoader

# Load data
loader = DataLoader("data/raw")
loader.cargar_todos()
df_imagery = loader.get_imagery()

# Initialize predictor
predictor = PredictorMosquitos(df_imagery)

# Prepare and train
if predictor.preparar_datos():
    predictor.entrenar_modelo()

    # Validate
    metricas = predictor.validar_modelo()
    print(f"Accuracy: {metricas['accuracy']:.2%}")
    print(f"F1-Score: {metricas['f1_score']:.2%}")

    # Cross-validation
    cv_results = predictor.validacion_cruzada(cv=5)
    print(f"CV Score: {cv_results['mean']:.2%} ± {cv_results['std']:.2%}")

    # Feature importance
    importancia = predictor.obtener_importancia_features()
    print("\nTop features:")
    print(importancia.head())

    # Generate plots
    predictor.generar_visualizaciones()

    # Make predictions on new data
    new_data = pd.DataFrame({
        'ceoTREES_CANOPYCOVER': [50, 10, 30],
        'ceoBUSH_SCRUB': [20, 5, 15],
        'ceoGRASS': [10, 80, 40],
        'ceoImperviousSurface': [5, 2, 10]
    })
    predictions = predictor.predecir(new_data)
    print(f"\nPredictions: {predictions}")
```

## PredictorTemporal

### Class Overview

**Location:** `src/prediccion_temporal.py`

**Purpose:** Time series forecasting of vegetation and land cover changes using Sentinel-2 satellite imagery.

**Algorithm:** Polynomial Regression (degree 3)

### Class Definition

```python
class PredictorTemporal:
    """
    Temporal forecasting using Sentinel-2 time series.

    Fits polynomial regression models to historical satellite
    observations and projects future trends.

    Attributes:
        directorio (Path): Directory containing GeoJSON files
        datos_temporales (list): Parsed satellite observations
        df_temporal (pd.DataFrame): Time-indexed dataset
        modelos (dict): Trained models per variable
        predicciones (dict): Forecast results
        figuras (list): Generated matplotlib figures

    Polynomial Degree: 3 (cubic)
        Rationale: Captures non-linear trends without overfitting
    """
```

### Methods

#### cargar_datos_geojson()

**Purpose:** Load and parse Sentinel-2 GeoJSON files.

```python
def cargar_datos_geojson(self) -> bool:
    """
    Load satellite imagery metadata from GeoJSON files.

    Returns:
        bool: True if files loaded successfully

    Algorithm:
        1. Glob pattern: "S2*_L2A.geojson"
        2. For each file:
            a. Parse JSON
            b. Extract properties dict
            c. Parse datetime from 'datetime' field
            d. Extract cover percentages:
                - vegetation_pct
                - not_vegetated_pct
                - water_pct
                - snow_ice_pct
                - cloud_cover
            e. Append to list
        3. Convert to DataFrame
        4. Sort by date
        5. Calculate days since first observation

    GeoJSON Structure:
        {
            "type": "Feature",
            "properties": {
                "datetime": "2025-04-22T17:57:40Z",
                "eo:cloud_cover": 12.5,
                "s2:vegetation_percentage": 45.2,
                "s2:not_vegetated_percentage": 38.1,
                "s2:water_percentage": 8.3,
                "s2:snow_ice_percentage": 0.0,
                ...
            },
            "geometry": {...}
        }

    Temporal Index:
        dias_desde_inicio: Numeric time index
            - First observation = day 0
            - Second observation = days elapsed
            - Enables regression fitting

    Error Handling:
        - Skips files with parse errors
        - Continues with partial dataset
        - Prints warnings for failed files

    Performance:
        Time: O(n) for n files (~1-2s for 50 files)
        Space: O(n) for DataFrame storage
    """
```

#### preparar_datos()

**Purpose:** Transform raw data for modeling.

```python
def preparar_datos(self) -> tuple:
    """
    Prepare time series data for regression.

    Returns:
        tuple: (X, y_dict) where:
            X: np.ndarray (days since start)
            y_dict: dict of np.ndarray (one per variable)

    Variables Prepared:
        - vegetation_pct: Total vegetation coverage
        - not_vegetated_pct: Bare ground, urban, etc.
        - water_pct: Water bodies
        - snow_ice_pct: Snow and ice
        - cloud_cover: Cloud obstruction

    Data Cleaning:
        - Remove null values
        - Filter outliers (3-sigma rule)
        - Handle missing dates (interpolation optional)

    Transformation:
        X = dias_desde_inicio (1D array)
        y = variable_values (1D array)

        For polynomial regression:
            X_poly = PolynomialFeatures(degree=3).fit_transform(X)
    """
```

#### entrenar_modelo()

**Purpose:** Fit polynomial regression for a specific variable.

```python
def entrenar_modelo(self, variable: str) -> None:
    """
    Train polynomial regression model.

    Args:
        variable: Column name to predict (e.g., 'vegetation_pct')

    Algorithm:
        1. Extract X (days) and y (variable values)
        2. Create polynomial features (degree=3):
            X_poly = [1, x, x², x³]
        3. Fit linear regression on polynomial features:
            y = β₀ + β₁x + β₂x² + β₃x³
        4. Store model and coefficients

    Polynomial Regression Math:
        Cubic model: y = β₀ + β₁x + β₂x² + β₃x³

        Where:
            β₀: Intercept (baseline value)
            β₁: Linear trend coefficient
            β₂: Quadratic curvature
            β₃: Cubic flex point

        Least squares solution:
            β = (X^T X)^(-1) X^T y

    Model Storage:
        self.modelos[variable] = {
            'poly_features': PolynomialFeatures object,
            'regressor': LinearRegression object,
            'coef': np.ndarray (coefficients),
            'intercept': float
        }

    Performance:
        Time: O(n³) for matrix inversion (small n, fast)
        Space: O(degree × n) for polynomial features
    """
```

#### predecir_futuro()

**Purpose:** Generate forecasts for future dates.

```python
def predecir_futuro(self, dias_adelante: int = 30) -> pd.DataFrame:
    """
    Forecast variable values for future dates.

    Args:
        dias_adelante: Number of days to forecast (default: 30)

    Returns:
        pd.DataFrame: Predictions with columns:
            - fecha: Future date
            - dias_desde_inicio: Numeric time index
            - {variable}_pred: Predicted value
            - {variable}_lower: Lower confidence bound
            - {variable}_upper: Upper confidence bound

    Algorithm:
        1. Determine last observation date
        2. Generate future date range (last_date + 1 to last_date + dias_adelante)
        3. Convert to numeric (days since start)
        4. For each variable:
            a. Transform to polynomial features
            b. Predict using trained model
            c. Calculate confidence interval (± 1 std dev)
        5. Compile to DataFrame

    Confidence Intervals:
        Standard error of prediction:
            SE = σ × √(1 + x^T (X^T X)^(-1) x)

        Where:
            σ: Residual standard deviation
            x: New observation (polynomial features)
            X: Training data matrix

        95% CI: prediction ± 1.96 × SE
        (Using 1 std dev for simplicity)

    Extrapolation Warning:
        Predictions beyond training data range are less reliable.
        Polynomial models can diverge rapidly.
        Recommended: dias_adelante ≤ 30-60 days

    Performance:
        Time: O(dias_adelante × variables)
        Typical: <1 second
    """
```

#### analizar_tendencias()

**Purpose:** Compute trend statistics.

```python
def analizar_tendencias(self) -> dict:
    """
    Analyze historical trends in variables.

    Returns:
        dict: {
            'variable': {
                'trend': str ('increasing', 'decreasing', 'stable'),
                'slope': float (% change per day),
                'r2': float (model fit quality),
                'direction': str ('up', 'down', 'flat')
            }
        }

    Trend Classification:
        Linear fit: y = mx + b

        Slope interpretation:
            m > +0.1: Increasing
            m < -0.1: Decreasing
            -0.1 ≤ m ≤ +0.1: Stable

    R² Interpretation:
        R² = 1 - (SS_res / SS_tot)

        Values:
            0.9-1.0: Excellent fit
            0.7-0.9: Good fit
            0.5-0.7: Moderate fit
            <0.5: Poor fit, high uncertainty

    Use Cases:
        - Identify improving/degrading areas
        - Validate predictions (check for realistic trends)
        - Prioritize monitoring (focus on changing areas)
    """
```

#### calcular_metricas()

**Purpose:** Compute model performance metrics.

```python
def calcular_metricas(self) -> dict:
    """
    Calculate regression performance metrics.

    Returns:
        dict: {
            'variable': {
                'r2': float [0-1],
                'rmse': float,
                'mae': float,
                'mape': float (%)
            }
        }

    Metrics Explained:

    R² (Coefficient of Determination):
        Formula: 1 - Σ(y - ŷ)² / Σ(y - ȳ)²
        Range: 0 to 1 (higher is better)
        Meaning: Proportion of variance explained
        Interpretation:
            0.9: Model explains 90% of variance
            0.5: Model explains 50% of variance

    RMSE (Root Mean Square Error):
        Formula: √(Σ(y - ŷ)² / n)
        Units: Same as target variable
        Meaning: Average prediction error magnitude
        Sensitive to outliers
        Example: RMSE=5 means average error is 5 percentage points

    MAE (Mean Absolute Error):
        Formula: Σ|y - ŷ| / n
        Units: Same as target variable
        Meaning: Average absolute error
        More robust to outliers than RMSE

    MAPE (Mean Absolute Percentage Error):
        Formula: (100/n) × Σ|y - ŷ| / |y|
        Units: Percentage
        Meaning: Average percent error
        Good for comparing across scales
        Example: MAPE=10% means average 10% error

    Performance Targets:
        Good model: R² > 0.8, MAPE < 15%
        Acceptable: R² > 0.6, MAPE < 25%
        Poor: R² < 0.5, MAPE > 30%
    """
```

#### generar_visualizaciones()

**Purpose:** Create time series plots with forecasts.

```python
def generar_visualizaciones(self) -> None:
    """
    Generate comprehensive time series visualizations.

    Outputs:
        - data/output/series_temporales.png
        - data/output/predicciones_temporales.png

    Chart 1: Historical Time Series (3×2 subplots)
        - Observed values (scatter + line)
        - Linear trend line
        - One subplot per variable
        - Legend: Observed, Trend

    Chart 2: Forecasts (3×2 subplots)
        - Historical data (blue)
        - Predictions (red)
        - Confidence interval (shaded)
        - Vertical line: present/future boundary

    Chart Specifications:
        Size: (16, 12) inches
        DPI: 150 (balance quality/size)
        Colors:
            Historical: blue (#1f77b4)
            Prediction: red (#d62728)
            Trend: red dashed
            Confidence: gray shaded (alpha=0.3)

    Performance:
        Time: ~5 seconds total
        I/O: 2 PNG files (~2-3MB each)
    """
```

### Usage Example

```python
from src.prediccion_temporal import PredictorTemporal

# Initialize predictor
predictor = PredictorTemporal("data/raw")

# Load Sentinel-2 data
if predictor.cargar_datos_geojson():
    # Train models
    for variable in ['vegetation_pct', 'water_pct', 'cloud_cover']:
        predictor.entrenar_modelo(variable)

    # Generate forecasts
    pred_30 = predictor.predecir_futuro(30)   # 30 days
    pred_60 = predictor.predecir_futuro(60)   # 60 days
    pred_90 = predictor.predecir_futuro(90)   # 90 days

    # Analyze trends
    tendencias = predictor.analizar_tendencias()
    for var, trend in tendencias.items():
        print(f"{var}: {trend['trend']} (slope={trend['slope']:.3f})")

    # Compute metrics
    metricas = predictor.calcular_metricas()
    for var, metrics in metricas.items():
        print(f"{var}: R²={metrics['r2']:.2f}, RMSE={metrics['rmse']:.2f}")

    # Generate plots
    predictor.generar_visualizaciones()

    # Save predictions to CSV
    pred_30.to_csv('data/output/predicciones_30dias.csv', index=False)
```

## Mathematical Foundations

### Random Forest Mathematics

**Decision Tree Split Criterion (Gini Impurity):**

$$
Gini(D) = 1 - \sum_{i=1}^{C} p_i^2
$$

Where:

- $D$: Dataset at node
- $C$: Number of classes
- $p_i$: Proportion of class $i$ in $D$

**Information Gain:**

$$
IG(D, A) = Gini(D) - \sum_{v \in Values(A)} \frac{|D_v|}{|D|} Gini(D_v)
$$

Where:

- $A$: Attribute to split on
- $D_v$: Subset where $A = v$

**Ensemble Prediction:**

$$
\hat{y} = mode\{h_1(x), h_2(x), ..., h_T(x)\}
$$

Where:

- $h_t$: Prediction from tree $t$
- $T$: Number of trees
- $mode$: Majority vote

### Polynomial Regression Mathematics

**Cubic Polynomial Model:**

$$
y = \beta_0 + \beta_1 x + \beta_2 x^2 + \beta_3 x^3 + \epsilon
$$

**Matrix Form:**

$$
\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}
$$

Where:

$$
\mathbf{X} = \begin{bmatrix}
1 & x_1 & x_1^2 & x_1^3 \\
1 & x_2 & x_2^2 & x_2^3 \\
\vdots & \vdots & \vdots & \vdots \\
1 & x_n & x_n^2 & x_n^3
\end{bmatrix}
$$

**Least Squares Solution:**

$$
\boldsymbol{\beta} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}
$$

**Prediction:**

$$
\hat{y}_{new} = \mathbf{x}_{new}^T \boldsymbol{\beta}
$$

**Standard Error of Prediction:**

$$
SE(\hat{y}) = \hat{\sigma} \sqrt{1 + \mathbf{x}^T (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{x}}
$$

Where $\hat{\sigma}$ is residual standard deviation.

## Model Validation

### Validation Strategies

**1. Train/Test Split:**

- Simple, fast
- Single performance estimate
- May be optimistic/pessimistic

**2. K-Fold Cross-Validation:**

- More robust
- Multiple performance estimates
- Confidence intervals

**3. Time Series Split:**

- Respects temporal ordering
- No data leakage
- Appropriate for temporal data

**4. Out-of-Time Validation:**

- Hold out recent data
- Test forecasting ability
- Most realistic for production

### Validation Metrics Summary

| Metric    | Type           | Range   | Best Value | Use Case                  |
| --------- | -------------- | ------- | ---------- | ------------------------- |
| Accuracy  | Classification | [0, 1]  | 1.0        | Balanced classes          |
| Precision | Classification | [0, 1]  | 1.0        | Minimize false positives  |
| Recall    | Classification | [0, 1]  | 1.0        | Minimize false negatives  |
| F1-Score  | Classification | [0, 1]  | 1.0        | Balanced precision/recall |
| AUC-ROC   | Classification | [0, 1]  | 1.0        | Threshold-independent     |
| R²        | Regression     | [−∞, 1] | 1.0        | Explained variance        |
| RMSE      | Regression     | [0, ∞)  | 0.0        | Absolute error            |
| MAE       | Regression     | [0, ∞)  | 0.0        | Robust error              |
| MAPE      | Regression     | [0, ∞)  | 0.0        | Percentage error          |

## Performance Optimization

### Random Forest Optimization

**1. Feature Selection:**

```python
# Remove low-importance features
importances = modelo.feature_importances_
keep_features = importances > 0.05
X_reduced = X[:, keep_features]
```

**2. Hyperparameter Tuning:**

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='f1'
)
grid_search.fit(X_train, y_train)
best_modelo = grid_search.best_estimator_
```

**3. Parallelization:**

```python
# Already enabled with n_jobs=-1
# Uses all CPU cores
```

### Polynomial Regression Optimization

**1. Degree Selection:**

```python
# Test multiple degrees
for degree in [2, 3, 4]:
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)
    model = LinearRegression().fit(X_poly, y)
    score = r2_score(y, model.predict(X_poly))
    print(f"Degree {degree}: R²={score:.3f}")
```

**2. Regularization (Ridge):**

```python
from sklearn.linear_model import Ridge

# Prevent overfitting with L2 regularization
ridge = Ridge(alpha=1.0)
ridge.fit(X_poly, y)
```

**3. Feature Scaling:**

```python
from sklearn.preprocessing import StandardScaler

# Scale before polynomial expansion
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_poly = poly.fit_transform(X_scaled)
```

For data structure details, see [Data Structures](04_DATA_STRUCTURES.md).
