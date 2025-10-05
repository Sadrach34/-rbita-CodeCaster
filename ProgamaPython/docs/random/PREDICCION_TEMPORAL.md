# 🔮 Predicción Temporal - Análisis Sentinel-2

## 📋 Descripción

Este módulo realiza predicciones temporales sobre el estado futuro de la vegetación en una zona de Sonora, México, utilizando series temporales de imágenes satelitales Sentinel-2.

## 🎯 ¿Qué hace?

1. **Carga datos satelitales**: Procesa archivos GeoJSON de Sentinel-2 (33 imágenes)
2. **Extrae índices espectrales**:
   - NDVI (Índice de Vegetación Normalizado)
   - Greenness Index (Índice de Verdor)
   - Water Index (Índice de Agua)
   - Aridity Index (Índice de Aridez)
3. **Analiza tendencias**: Identifica patrones temporales y estacionalidad
4. **Entrena modelos**: Utiliza Random Forest para modelar cada índice
5. **Genera predicciones**: Predice valores para 2 meses adelante
6. **Visualiza resultados**: Crea gráficos y reportes detallados

## 🚀 Uso

### Opción 1: Script independiente

```bash
python scripts/ejecutar_prediccion_temporal.py
```

### Opción 2: Integrado en análisis completo

```bash
python main.py
```

El módulo de predicción temporal se ejecutará automáticamente como parte del análisis completo.

### Opción 3: Uso programático

```python
from src.prediccion_temporal import PredictorTemporal

# Crear predictor
predictor = PredictorTemporal(directorio_geojson="data/raw")

# Ejecutar análisis completo
resultados = predictor.ejecutar_analisis_completo(meses_adelante=2)

# Ver predicciones
for indice, pred in resultados.items():
    print(f"{indice}: {pred['prediccion']:.4f} ({pred['cambio_porcentual']:+.2f}%)")
```

## 📊 Archivos generados

Todos los archivos se guardan en `data/output/`:

1. **prediccion_series_temporales.png**

   - Gráficos de series temporales históricas
   - Visualización de predicciones futuras
   - Tendencias para cada índice

2. **prediccion_comparacion.png**

   - Comparación lado a lado: valores actuales vs predicciones
   - Porcentajes de cambio esperado
   - Análisis visual de diferencias

3. **reporte*prediccion_temporal*\*.txt**
   - Reporte completo en texto plano
   - Estadísticas detalladas
   - Métricas de confianza para cada predicción

## 📈 Índices analizados

### 🌿 NDVI Estimado

- **Qué mide**: Salud y densidad de la vegetación
- **Rango**: 0.0 (sin vegetación) a 1.0 (vegetación densa)
- **Uso**: Identificar áreas verdes y cultivos

### 🟢 Greenness Index

- **Qué mide**: Proporción de cobertura vegetal
- **Rango**: 0.0 a 1.0
- **Uso**: Evaluar verdor general de la zona

### 💧 Water Index

- **Qué mide**: Presencia de cuerpos de agua
- **Rango**: 0.0 a 1.0
- **Uso**: Detectar lagos, ríos, agua acumulada

### 🏜️ Aridity Index

- **Qué mide**: Áreas sin vegetación (suelo desnudo)
- **Rango**: 0.0 a 1.0
- **Uso**: Identificar zonas áridas o degradadas

## 🔬 Metodología

### 1. Extracción de datos

```
GeoJSON → Properties → Índices espectrales
         ↓
    vegetation_percentage
    not_vegetated_percentage
    water_percentage
    cloud_cover
```

### 2. Preparación de series temporales

- Ordenamiento cronológico
- Eliminación de outliers
- Agregación de características temporales (mes, día del año)

### 3. Entrenamiento de modelos

- Algoritmo: **Random Forest Regressor**
- Features: `dias_desde_inicio`, `mes`, `dia_año`, `cloud_cover`
- Cross-validation para validación

### 4. Predicción

- Extrapolación a 2 meses (60 días)
- Cálculo de intervalos de confianza
- Estimación de cambios porcentuales

## 📊 Métricas de evaluación

Cada modelo incluye:

- **R² Score**: Bondad de ajuste (0-1, mayor es mejor)
- **Cambio porcentual**: % de cambio esperado
- **Confianza**: Basada en el score del modelo
- **Importancia de características**: Qué variables influyen más

## ⚙️ Configuración

### Cambiar período de predicción

```python
predictor.ejecutar_analisis_completo(meses_adelante=3)  # 3 meses en vez de 2
```

### Cambiar directorio de datos

```python
predictor = PredictorTemporal(directorio_geojson="ruta/a/tus/geojson")
```

### Personalizar modelos

Edita `src/prediccion_temporal.py` en la función `entrenar_modelos_predictivos()`:

```python
modelo = RandomForestRegressor(
    n_estimators=200,      # Más árboles
    max_depth=15,          # Mayor profundidad
    min_samples_split=5,   # Ajustar según datos
    random_state=42
)
```

## 🎓 Interpretación de resultados

### 📈 Tendencia Ascendente (↗️)

- **NDVI/Greenness aumenta**: Mayor vegetación esperada
- **Water aumenta**: Más agua acumulada
- **Aridity disminuye**: Menos zonas áridas

### 📉 Tendencia Descendente (↘️)

- **NDVI/Greenness disminuye**: Pérdida de vegetación
- **Water disminuye**: Sequía o evaporación
- **Aridity aumenta**: Aridificación

### ➡️ Tendencia Estable (→)

- Cambio < 5%: Condiciones similares a las actuales

## 🔍 Ejemplo de salida

```
🔮 PREDICCIÓN PARA 2 MESES ADELANTE
================================================================================

📅 Última observación: 2025-10-02
🎯 Predicción para: 2025-12-02

🎯 PREDICCIONES:
--------------------------------------------------------------------------------
📈 NDVI Estimado:
   Valor actual: 0.4523
   Predicción: 0.4289
   Cambio esperado: -5.17%
   Confianza (R²): 0.8234

📈 Greenness Index:
   Valor actual: 0.3244
   Predicción: 0.3012
   Cambio esperado: -7.15%
   Confianza (R²): 0.8567

💧 Water Index:
   Valor actual: 0.0012
   Predicción: 0.0018
   Cambio esperado: +50.00%
   Confianza (R²): 0.7123
```

## ⚠️ Limitaciones

1. **Datos históricos**: La calidad de la predicción depende de tener suficientes observaciones (mínimo 10-15)
2. **Nubosidad**: Días muy nublados pueden afectar la calidad de los índices
3. **Eventos extremos**: No predice eventos atípicos (sequías severas, inundaciones)
4. **Rango temporal**: Predicciones a más de 3 meses tienen menor confianza

## 🛠️ Dependencias

```python
pandas
numpy
matplotlib
seaborn
scikit-learn
```

## 📞 Soporte

Si tienes preguntas o encuentras problemas:

1. Revisa los archivos de log en `data/output/`
2. Verifica que tienes archivos GeoJSON válidos
3. Asegúrate de tener todas las dependencias instaladas

## 🎉 Próximas mejoras

- [ ] Soporte para ARIMA/SARIMA
- [ ] Predicciones con LSTM
- [ ] Mapas interactivos de predicciones
- [ ] Comparación con años anteriores
- [ ] Alertas automáticas por cambios significativos
