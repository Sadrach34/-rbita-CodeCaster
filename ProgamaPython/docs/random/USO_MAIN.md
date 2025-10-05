# 📖 Guía de Uso - main.py

## 🚀 Análisis Completo de Datos GLOBE Observer

El script `main.py` ejecuta un análisis completo de los datos del proyecto, generando reportes en formato TXT y mapas interactivos en HTML.

---

## 📋 ¿Qué hace main.py?

El script realiza los siguientes análisis automáticamente:

### 1️⃣ **Carga de Datos**

- Lee los 3 archivos CSV de GLOBE Observer
- Procesa y valida los datos
- Genera estadísticas básicas

### 2️⃣ **Análisis de Mosquitos** 🦟

- Especies de mosquitos reportadas (Aedes, Culex, Anopheles)
- Fuentes de agua más comunes
- Distribución temporal de reportes
- Mapa de calor interactivo

### 3️⃣ **Análisis de Cobertura del Suelo** 🌍

- Promedios de cada tipo de cobertura:
  - Árboles
  - Arbustos
  - Pasto
  - Edificios
  - Superficies impermeables
  - Agua
- Gráficos de distribución
- Mapa interactivo de observaciones

### 4️⃣ **Modelo Predictivo** 🤖

- Entrena un modelo de Machine Learning (Random Forest)
- Predice áreas propensas a mosquitos basándose en cobertura del suelo
- Reporta precisión del modelo

### 5️⃣ **Generación de Reportes** 📄

- Reporte completo en formato TXT
- 2 mapas interactivos en HTML
- Gráficos en PNG

---

## 🎯 Cómo Ejecutar

### Opción 1: Desde la terminal

```bash
# Asegúrate de estar en el directorio del proyecto
cd /home/sadrach/Documentos/Orbita-CodeCaster

# Activa el entorno virtual (si usas uno)
source mi_entorno/bin/activate

# Ejecuta el script
python main.py
```

### Opción 2: Desde VS Code

1. Abre `main.py`
2. Presiona `F5` o click en "Run Python File"
3. O usa el botón ▶️ en la esquina superior derecha

---

## 📁 Archivos Generados

Todos los archivos se guardan en `data/output/` con timestamp:

```
data/output/
├── reporte_completo_YYYYMMDD_HHMMSS.txt    # Reporte en texto
├── mapa_mosquitos_YYYYMMDD_HHMMSS.html     # Mapa interactivo de mosquitos
├── mapa_cobertura_YYYYMMDD_HHMMSS.html     # Mapa interactivo de cobertura
└── promedio_cobertura_suelo.png            # Gráfico de barras
```

### 📄 Reporte TXT

Contiene:

- Estadísticas de mosquitos (especies, fuentes de agua, temporalidad)
- Promedios de cobertura del suelo
- Precisión del modelo predictivo
- Resumen de mapas generados

**Ejemplo:**

```
================================================================================
  2. ANÁLISIS DE MOSQUITOS
================================================================================

🦟 Especies reportadas:
   - Aedes: 9 reportes
   - Culex: 7 reportes
   - Anopheles: 3 reportes

💧 Fuentes de agua más comunes:
   - ovitrap: 125 reportes
   - adult mosquito trap: 104 reportes
   - cement, metal or plastic tank: 71 reportes
```

### 🗺️ Mapas HTML

**Mapa de Mosquitos:**

- Mapa de calor (HeatMap) de reportes
- Cluster de marcadores por ubicación
- Popup con información detallada de cada reporte
- Capas interactivas (mapa base + calor)

**Mapa de Cobertura:**

- Marcadores de observaciones
- Colores según tipo de cobertura dominante
- Círculos de tamaño proporcional a cobertura de árboles
- Información detallada en popup

---

## 🎨 Personalización

### Cambiar directorio de salida

Edita en `main.py`:

```python
def __init__(self, output_dir="data/output"):  # Cambiar aquí
```

### Modificar el centro del mapa

En la función `generar_mapa_mosquitos()`:

```python
mapa = folium.Map(
    location=[39.8, -98.5],  # Cambiar coordenadas
    zoom_start=4              # Cambiar zoom inicial
)
```

### Agregar más análisis

Agrega nuevas secciones en la función `main()`:

```python
# Nuevo análisis
generador.separador("7. MI ANÁLISIS PERSONALIZADO")
# Tu código aquí
generador.log("Análisis personalizado completado")
```

---

## 🐛 Solución de Problemas

### Error: "Archivo no encontrado"

**Solución:** Verifica que los archivos CSV estén en `data/raw/`:

```bash
ls data/raw/
# Deberías ver:
# - AdoptAPixel3km2020_GO_LandCover.csv
# - AdoptAPixel3km2020_GO_MosquitoHabitatMapper.csv
# - AdoptAPixel3km2020_100m_aerialImageryLabels.csv
```

### Error: "ModuleNotFoundError"

**Solución:** Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Error: "Permission denied"

**Solución:** Verifica permisos de la carpeta `data/output/`:

```bash
chmod -R 755 data/output/
```

### Los mapas no se abren

**Solución:** Abre manualmente el archivo HTML:

```bash
# En Linux
xdg-open data/output/mapa_mosquitos_*.html

# En Mac
open data/output/mapa_mosquitos_*.html

# En Windows
start data/output/mapa_mosquitos_*.html
```

---

## 📊 Ejemplo de Salida Completa

```
================================================================================
  🌍 ORBITA-CODECASTER - ANÁLISIS COMPLETO
================================================================================

[17:15:41] INFO: ✅ Datos de mosquitos: 534 registros
[17:15:41] INFO: ✅ Datos de imagery: 1800 registros

================================================================================
  2. ANÁLISIS DE MOSQUITOS
================================================================================
[17:15:41] INFO: Analizando datos temporales...

================================================================================
  3. ANÁLISIS DE COBERTURA DEL SUELO
================================================================================
Promedio de cobertura del suelo (%):
   Árboles: 33.02%
   Arbustos: 1.93%
   Pasto: 16.13%
   Edificios: 12.45%
   Superficies Impermeables: 19.57%
   Agua: 0.99%

✅ Gráfico guardado: data/output/promedio_cobertura_suelo.png

================================================================================
  4. MODELO PREDICTIVO
================================================================================
📊 Precisión en prueba: 96.85%

================================================================================
  5. GENERANDO MAPAS INTERACTIVOS
================================================================================
[17:15:45] INFO: ✅ Mapa de mosquitos guardado
[17:15:45] INFO: ✅ Mapa de cobertura guardado

================================================================================
  ✅ ANÁLISIS COMPLETADO EXITOSAMENTE
================================================================================

📁 Todos los archivos se guardaron en: data/output/
🌐 Abre los archivos HTML en tu navegador para ver los mapas interactivos
```

---

## 🔗 Enlaces Útiles

- [Documentación del Proyecto](../README.md)
- [API de los módulos](API.md) _(próximamente)_
- [GLOBE Observer](https://observer.globe.gov/)
- [NASA GIBS](https://earthdata.nasa.gov/eosdis/science-system-description/eosdis-components/gibs)

---

## 🤝 Contribuir

Si encuentras errores o quieres agregar funcionalidades:

1. Reporta issues en GitHub
2. Crea un Pull Request con mejoras
3. Documenta tus cambios

---

**Última actualización:** 4 de octubre de 2025  
**Versión:** 1.0.0
