# Basic Usage

This guide explains how to use Orbita-CodeCaster for different types of analyses. All examples use simple commands you can copy and paste.

## Understanding the System

Orbita-CodeCaster analyzes three types of environmental data:

1. **Mosquito Habitats** - Where mosquitoes are found and why
2. **Land Cover** - What covers the ground (trees, water, buildings, etc.)
3. **Satellite Imagery** - Changes in vegetation over time

## Running Analyses

### Complete Analysis (Recommended for Beginners)

This runs everything and produces a full report:

```bash
python main.py
```

**What it does:**

- Analyzes all mosquito observations
- Studies land cover patterns
- Creates multiple visualizations
- Builds prediction models
- Generates an HTML report

**Time:** 5-15 minutes

**Output:** Files in `data/output/` folder

### Individual Analyses

If you only need specific information, use these scripts:

#### Mosquito Analysis Only

```bash
python -c "from src.analisis_mosquitos import AnalizadorMosquitos; from src.utils.data_loader import DataLoader; loader = DataLoader(); df = loader.cargar_datos_mosquitos(); analizador = AnalizadorMosquitos(df); analizador.ejecutar_analisis_completo()"
```

**What you get:**

- Species distribution charts
- Water source analysis
- Temporal patterns (when mosquitoes appear)
- Interactive maps with mosquito locations

#### Land Cover Analysis Only

```bash
python -c "from src.analisis_cobertura import AnalizadorCobertura; from src.utils.data_loader import DataLoader; loader = DataLoader(); df = loader.cargar_datos_cobertura(); analizador = AnalizadorCobertura(df); analizador.ejecutar_analisis_completo()"
```

**What you get:**

- Percentage of different land types
- Distribution of trees, grass, and water
- Correlation between different features
- Vegetation vs. urban area comparison

#### Prediction Model

```bash
python scripts/ejecutar_prediccion_temporal.py
```

**What you get:**

- Future vegetation predictions (30-90 days ahead)
- Trend analysis
- Charts showing predicted changes
- CSV file with numerical predictions

#### Bloom Detection Map

```bash
python scripts/generar_mapa_floraciones.py
```

**What you get:**

- Interactive map showing bloom locations
- Satellite imagery overlay (NASA MODIS)
- Color-coded intensity indicators

## Understanding the Data Files

### Input Files (what you provide)

**Location:** `data/raw/`

1. **CSV Files** (spreadsheet-like data)

   - `AdoptAPixel3km2020_GO_MosquitoHabitatMapper.csv` - Mosquito observations
   - `AdoptAPixel3km2020_GO_LandCover.csv` - Land cover data
   - `AdoptAPixel3km2020_100m_aerialImageryLabels.csv` - Aerial image classifications

2. **GeoJSON Files** (satellite images with metadata)
   - Files named like `S2A_T12RWU_20250422T175740_L2A.geojson`
   - Contains Sentinel-2 satellite data
   - Multiple dates for temporal analysis

### Output Files (what you receive)

**Location:** `data/output/`

1. **Maps** (`.html` files)

   - `mapa.html` - Main interactive map
   - Open with any web browser
   - Click markers for detailed information
   - Zoom and pan to explore

2. **Charts** (`.png` files)

   - `especies_mosquitos.png` - Mosquito species distribution
   - `distribucion_cobertura.png` - Land cover percentages
   - `series_temporales.png` - Changes over time
   - `predicciones_temporales.png` - Future forecasts
   - And more...

3. **Reports** (`.html` files)

   - `reporte.html` - Complete analysis report
   - Contains all charts and maps in one document
   - Includes explanatory text
   - Printable and shareable

4. **Data** (`.csv` files)
   - `predicciones_futuras.csv` - Numerical predictions
   - Can be opened in Excel or any spreadsheet program

## Reading the Visualizations

### Maps

**What the colors mean:**

- **Green markers** - Areas with vegetation
- **Blue markers** - Water bodies
- **Red markers** - High mosquito activity
- **Gray markers** - Urban/built areas

**How to use:**

- Click any marker for details
- Use the layer controls to show/hide different data types
- Zoom in for more detail
- The background shows satellite imagery

### Charts

**Common chart types you'll see:**

1. **Bar Charts** - Compare quantities

   - Taller bars = more of something
   - Used for species counts, land cover percentages

2. **Line Graphs** - Show changes over time

   - Rising line = increasing trend
   - Falling line = decreasing trend
   - Used for temporal predictions

3. **Heatmaps** - Show concentrations

   - Red/orange = high concentration
   - Yellow/green = moderate
   - Blue = low
   - Used for mosquito density

4. **Pie Charts** - Show proportions
   - Bigger slices = larger percentage
   - Used for land cover distribution

### The HTML Report

The complete report contains:

1. **Summary Section** - Key findings in plain language
2. **Data Overview** - What data was analyzed
3. **Mosquito Analysis** - Findings about mosquito habitats
4. **Land Cover Analysis** - Environmental characteristics
5. **Predictions** - Future forecasts with explanations
6. **Maps** - Interactive visualizations
7. **Appendix** - Technical details (optional reading)

**To read the report:**

1. Open `data/output/reporte.html` in your browser
2. Use the table of contents to navigate
3. Hover over charts for more details
4. Click maps to interact with them

## Common Tasks

### Analyzing New Data

1. Place your new CSV/GeoJSON files in `data/raw/`
2. Run `python main.py`
3. Check `data/output/` for new results
4. Old results are automatically backed up

### Comparing Different Time Periods

1. Run analysis with first dataset: `python main.py`
2. Rename the output folder (e.g., `output_2024`)
3. Replace data files with new period
4. Run again: `python main.py`
5. Compare the two output folders

### Generating Only a Report from Existing Data

```bash
python scripts/generar_reporte_html.py
```

This creates a fresh HTML report from already-processed data.

### Viewing Previous Results

All results remain in `data/output/` unless you delete them. Old reports have timestamps in their names.

## Tips for Best Results

### Data Quality

- **Use complete datasets** - Missing data can skew results
- **Check dates** - Ensure temporal data covers the period you want
- **Verify coordinates** - Geographic data must be in the correct region

### Performance

- **Close other programs** - Free up memory for analysis
- **Use smaller datasets first** - Test with a subset before full analysis
- **Be patient** - Large datasets take time to process

### Interpretation

- **Look for patterns** - Trends are more important than individual points
- **Consider context** - Environmental factors affect results
- **Compare periods** - Changes over time reveal insights
- **Check confidence** - Predictions include uncertainty measures

## What Each Analysis Tells You

### Mosquito Habitat Analysis

**Questions it answers:**

- Which mosquito species are most common?
- Where are mosquitoes concentrated?
- When are mosquitoes most active?
- What water sources do they prefer?

**Why it matters:**

- Understand disease vector distribution
- Plan mosquito control efforts
- Predict seasonal patterns
- Identify high-risk areas

### Land Cover Analysis

**Questions it answers:**

- What percentage is water, trees, grass, buildings?
- Where is vegetation most dense?
- How urban vs. natural is the area?
- What correlations exist between features?

**Why it matters:**

- Assess environmental health
- Understand ecosystem composition
- Identify habitat types
- Monitor land use changes

### Temporal Predictions

**Questions it answers:**

- How will vegetation change in coming weeks?
- What are the trends?
- When will changes peak?
- How confident are the predictions?

**Why it matters:**

- Plan ahead for seasonal changes
- Anticipate bloom events
- Prepare for environmental shifts
- Validate with actual observations

## Frequently Used Commands

### Activate Environment (do this first)

**Windows:**

```bash
mi_entorno\Scripts\activate
```

**Mac/Linux:**

```bash
source mi_entorno/bin/activate
```

### Run Full Analysis

```bash
python main.py
```

### Generate Report Only

```bash
python scripts/generar_reporte_html.py
```

### Create Bloom Map

```bash
python scripts/generar_mapa_floraciones.py
```

### Make Predictions

```bash
python scripts/ejecutar_prediccion_temporal.py
```

### View Prediction Results

```bash
python scripts/ver_resultados_prediccion.py
```

## Troubleshooting Common Issues

### "Module not found"

- Activate the virtual environment first
- Check that `pip install -r requirements.txt` completed successfully

### "No such file or directory"

- Verify you're in the Orbita-CodeCaster folder
- Check that data files exist in `data/raw/`

### "Permission denied"

- You may need administrator/sudo privileges
- Check file permissions on the data folders

### Blank or empty outputs

- Ensure input data files contain data
- Check terminal for error messages
- Verify file formats match expectations

### Analysis takes too long

- Normal for large datasets (15+ minutes)
- Check CPU and memory usage
- Consider processing smaller data subsets

For more help, see the [FAQ](04_FAQ.md) or check the [GitHub Issues](https://github.com/Sadrach34/Orbita-CodeCaster/issues) page.

## Next Steps

- Read [Understanding Results](03_UNDERSTANDING_RESULTS.md) for detailed interpretation
- Check the [FAQ](04_FAQ.md) for answers to common questions
- Explore [Technical Documentation](../TECHNICAL/README.md) if you want to understand how it works
