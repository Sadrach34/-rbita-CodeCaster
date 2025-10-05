# 📊 Generación de Reportes HTML - Predicción Temporal

## 🎯 Descripción

Este módulo genera reportes HTML interactivos y profesionales con todas las visualizaciones de predicción temporal embebidas. ¡Todo en una sola página web!

## ✨ Características

✅ **Diseño Moderno y Responsive** - Se adapta a cualquier pantalla  
✅ **Gráficos Embebidos** - Todas las visualizaciones en base64  
✅ **Métricas Interactivas** - Tarjetas con información clave  
✅ **CSS Profesional** - Gradientes, sombras y animaciones  
✅ **Tablas de Datos** - Predicciones en formato tabla  
✅ **Sin Dependencias Externas** - Todo en un solo archivo HTML

## 🚀 Uso Rápido

### Generar Reporte HTML Completo

```bash
# Método 1: Ejecutar script directo
python scripts/generar_reporte_html.py

# Método 2: Importar en tu código
from src.prediccion_temporal import PredictorTemporal
from src.reporte_html import GeneradorReporteHTML

predictor = PredictorTemporal()
resumen = predictor.ejecutar_analisis_completo(meses_adelante=2)

reporte = GeneradorReporteHTML("Mi Reporte")
# ... agregar contenido ...
reporte.generar_html("mi_reporte.html")
```

### Abrir el Reporte

```bash
# Linux
xdg-open data/output/reporte_prediccion_temporal.html

# macOS
open data/output/reporte_prediccion_temporal.html

# Windows
start data/output/reporte_prediccion_temporal.html
```

## 📁 Estructura del Reporte

El reporte HTML incluye:

1. **📊 Métricas Principales**

   - Archivos procesados
   - Periodo analizado
   - Fecha de predicción
   - Precisión del modelo

2. **📋 Resumen Ejecutivo**

   - Descripción del análisis
   - Contexto y objetivos

3. **🤖 Información de Modelos**

   - R² Score de cada modelo
   - RMSE (Error Cuadrático Medio)
   - Calidad del modelo

4. **📈 Visualizaciones**

   - Series temporales históricas
   - Predicciones con intervalos de confianza
   - Análisis de cambios esperados

5. **📊 Tablas de Datos**

   - Predicciones futuras detalladas
   - Valores numéricos formateados

6. **🎯 Conclusiones**
   - Insights principales
   - Recomendaciones

## 🎨 Personalización

### Cambiar Título

```python
reporte = GeneradorReporteHTML("Tu Título Personalizado")
```

### Agregar Métricas Personalizadas

```python
reporte.agregar_metrica(
    nombre="Tu Métrica",
    valor="100%",
    descripcion="Descripción de la métrica",
    icono="🎯"
)
```

### Agregar Gráficos

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])

reporte.agregar_grafico(
    fig,
    titulo="Mi Gráfico",
    descripcion="Descripción del gráfico"
)
```

### Agregar Secciones

```python
# Texto
reporte.agregar_seccion(
    "Mi Sección",
    "Contenido de la sección...",
    "texto"
)

# Lista
reporte.agregar_seccion(
    "Lista de Items",
    ["Item 1", "Item 2", "Item 3"],
    "lista"
)

# Tabla
datos_tabla = [
    {"Columna1": "Valor1", "Columna2": "Valor2"},
    {"Columna1": "Valor3", "Columna2": "Valor4"}
]
reporte.agregar_seccion(
    "Mi Tabla",
    datos_tabla,
    "tabla"
)
```

## 🎨 Estilos Incluidos

El reporte incluye:

- Gradientes modernos (violeta/morado)
- Animaciones suaves
- Tarjetas con sombras
- Diseño responsive (móvil/tablet/desktop)
- Hover effects
- Tablas interactivas

## 📊 Ejemplo de Salida

El reporte generado incluye:

```
┌─────────────────────────────────────┐
│  🛰️ Reporte de Predicción Temporal │
│  Generado el: 2025-10-04 23:46:36  │
└─────────────────────────────────────┘

📊 MÉTRICAS
┌──────────┬──────────┬──────────┬──────────┐
│ 📁       │ 📅       │ 🔮       │ 🎯       │
│ 34       │ 6 meses  │ Nov 2025 │ 68.3%    │
│ Archivos │ Periodo  │ Hasta    │ Precisión│
└──────────┴──────────┴──────────┴──────────┘

📈 VISUALIZACIONES
[Gráficos embebidos como imágenes base64]

📋 TABLAS
[Datos tabulares con formato]

🎯 CONCLUSIONES
[Insights y recomendaciones]
```

## 🔧 Requisitos

- Python 3.7+
- matplotlib
- pandas
- numpy
- sklearn
- seaborn

## 💡 Tips

1. **Compartir el reporte**: El HTML es autocontenido, puedes enviarlo por email o subirlo a un servidor web
2. **Imprimir**: El reporte se ve bien en modo impresión del navegador
3. **Guardar como PDF**: Usa la función "Imprimir → Guardar como PDF" del navegador
4. **Personalizar colores**: Edita el método `generar_css()` en `src/reporte_html.py`

## 📞 Soporte

Si tienes problemas:

1. Verifica que todos los gráficos se hayan generado
2. Revisa que el directorio `data/output/` exista
3. Asegúrate de tener permisos de escritura

## 🎉 ¡Listo!

Tu reporte HTML está ahora disponible en:
`data/output/reporte_prediccion_temporal.html`

¡Ábrelo en tu navegador favorito y disfruta de la visualización interactiva! 🚀
