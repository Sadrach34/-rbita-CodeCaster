# Understanding Results

This guide helps you interpret the outputs from Orbita-CodeCaster. You don't need technical knowledge – just follow along with the explanations.

## Types of Results

When analysis completes, you'll find several types of files in `data/output/`:

1. **Interactive Maps** (HTML) - Explore data geographically
2. **Charts and Graphs** (PNG) - See patterns visually
3. **Data Tables** (CSV) - Numbers you can analyze further
4. **Complete Report** (HTML) - Everything in one document

## Reading the Maps

### Main Map (`mapa.html`)

**Open it by:** Double-clicking the file (opens in your browser)

**What you see:**

- A zoomable, pannable map
- Colored markers showing data points
- Background satellite imagery
- Controls for layers and display options

**How to use:**

- **Click markers** - See detailed information about that location
- **Zoom in/out** - Use mouse wheel or +/- buttons
- **Pan** - Click and drag to move around
- **Layer control** - Toggle different data types on/off (usually top-right corner)

**Marker colors mean:**

- **Green** - High vegetation, healthy areas
- **Blue** - Water bodies, wet areas
- **Red** - High mosquito density, alert areas
- **Orange** - Moderate levels
- **Gray** - Urban or bare ground

### Bloom Map (`mapa.html` or specific bloom maps)

**Shows:** Areas where algae blooms or vegetation changes are detected

**Features:**

- **Heatmap overlay** - Color intensity shows bloom strength

  - Dark red = Very strong bloom
  - Orange = Moderate bloom
  - Yellow = Weak bloom
  - No color = No bloom detected

- **NDVI overlay** - Vegetation health from satellites
  - Bright green = Very healthy vegetation
  - Light green = Moderate vegetation
  - Brown/tan = Little vegetation

**When to look:**

- After rain or wet seasons (more blooms)
- To identify problem water bodies
- To track changes over time

## Reading the Charts

### Bar Charts

**Example:** Species Distribution (`especies_mosquitos.png`)

**How to read:**

- Bars represent different categories (e.g., mosquito species)
- Taller bars = more observations of that type
- Look at the y-axis for exact numbers

**What it tells you:**

- Which categories are most common
- Relative proportions at a glance
- Outliers (unusually high or low values)

**Example interpretation:**

> "Aedes mosquitoes have the tallest bar (50 observations), while Culex has 30 observations. Aedes is the dominant species in this area."

### Line Graphs

**Example:** Temporal Trends (`series_temporales.png`)

**How to read:**

- X-axis = Time (dates)
- Y-axis = Measured value
- Line shows how values change over time

**Patterns to notice:**

- **Rising line** - Values are increasing
- **Falling line** - Values are decreasing
- **Flat line** - Stable, no change
- **Zigzag** - Fluctuating, seasonal patterns

**Example interpretation:**

> "Vegetation index starts at 0.5 in April, rises to 0.7 in June (growing season), then falls to 0.4 in September (dry season)."

### Heatmaps

**Example:** Mosquito Density (`mapa_calor.html`)

**How to read:**

- Colors represent intensity or concentration
- Hot colors (red/orange) = High concentration
- Cool colors (blue/green) = Low concentration
- Larger colored areas = Broader regions affected

**What it tells you:**

- Where problems are concentrated
- Geographic hotspots
- Patterns of distribution

**Example interpretation:**

> "The red zone in the northeast corner shows high mosquito density. This area needs monitoring or intervention."

### Pie Charts

**Example:** Land Cover Distribution (`distribucion_cobertura.png`)

**How to read:**

- Each slice represents a category
- Bigger slice = larger percentage
- Labels show exact percentages

**What it tells you:**

- Proportions of the whole
- Dominant categories
- Overall composition

**Example interpretation:**

> "Trees cover 40% of the area (largest slice), followed by grass (30%), water (20%), and urban areas (10%)."

### Scatter Plots with Trend Lines

**Example:** Predictions (`predicciones_temporales.png`)

**How to read:**

- Each dot is an actual observation
- The line shows the predicted trend
- Dots near the line = Good prediction
- Dots far from line = Prediction uncertainty

**Colors often mean:**

- Blue dots = Historical data
- Red line = Predicted future trend
- Gray shading = Confidence range

**Example interpretation:**

> "Blue dots show past vegetation levels. The red line predicts it will rise in the next month. Most dots are close to the line, so the prediction is reliable."

## Understanding the HTML Report

The complete report (`reporte.html`) combines everything. It has sections:

### 1. Executive Summary

**What it is:** A brief overview in plain language

**Look for:**

- Key findings (e.g., "Mosquito activity increased 30%")
- Major trends (e.g., "Vegetation is declining")
- Important alerts (e.g., "Bloom detected in Lake X")

**Why it matters:** Get the big picture in 1-2 minutes

### 2. Data Overview

**What it is:** Description of what data was analyzed

**Information includes:**

- Date range (e.g., "April-September 2025")
- Number of observations (e.g., "1,250 mosquito reports")
- Geographic area (e.g., "Tile 12RWU, North America")

**Why it matters:** Understand the scope and limitations

### 3. Mosquito Analysis Section

**Contains:**

- Species breakdown
- Temporal patterns (when mosquitoes appear)
- Geographic distribution
- Water source preferences

**How to use:**

- Identify peak mosquito seasons
- Find high-risk areas
- Plan control measures
- Understand habitat preferences

**Example insights:**

- "Aedes peaks in June-July"
- "Most mosquitoes near standing water"
- "Urban areas have 40% more observations"

### 4. Land Cover Analysis Section

**Contains:**

- Percentage breakdown of cover types
- Vegetation density maps
- Urban vs. natural area comparison
- Correlations between features

**How to use:**

- Assess environmental health
- Identify habitat types
- Understand ecosystem balance
- Monitor land use

**Example insights:**

- "30% of area is water"
- "High correlation between trees and mosquitoes"
- "Urban expansion increased 5% since last year"

### 5. Temporal Prediction Section

**Contains:**

- Future forecasts (30-90 days ahead)
- Confidence intervals
- Trend analysis
- Historical comparison

**How to use:**

- Plan for upcoming changes
- Anticipate bloom events
- Schedule field work
- Compare predictions to actual outcomes later

**How to read confidence:**

- **High confidence (>80%):** Very likely to occur
- **Medium confidence (50-80%):** Possible, monitor closely
- **Low confidence (<50%):** Uncertain, use caution

**Example insights:**

- "Vegetation will increase 15% in next 30 days (high confidence)"
- "Bloom likely in mid-October (medium confidence)"

### 6. Recommendations Section

**Contains:** Actionable suggestions based on the analysis

**Types of recommendations:**

- Monitoring priorities
- Areas needing attention
- Timing for interventions
- Data collection suggestions

## Reading Prediction Data (CSV Files)

**File:** `predicciones_futuras.csv`

**Open with:** Excel, Google Sheets, or any spreadsheet program

**Columns you'll see:**

| Column               | What it means                                      |
| -------------------- | -------------------------------------------------- |
| `fecha`              | Future date of prediction                          |
| `valor_predicho`     | Predicted value (e.g., vegetation index)           |
| `confianza_inferior` | Lower bound (worst case)                           |
| `confianza_superior` | Upper bound (best case)                            |
| `tendencia`          | Direction: "aumentando", "disminuyendo", "estable" |

**How to interpret:**

```
fecha: 2025-11-01
valor_predicho: 0.65
confianza_inferior: 0.60
confianza_superior: 0.70
```

**Means:** On November 1st, the vegetation index will likely be 0.65, but could range from 0.60 to 0.70.

**The wider the confidence range, the less certain the prediction.**

## Common Metrics Explained

### NDVI (Vegetation Index)

**Range:** -1.0 to +1.0

**What it means:**

- **0.6 to 1.0** - Dense, healthy vegetation (forests, crops)
- **0.3 to 0.6** - Moderate vegetation (grassland, shrubs)
- **0.1 to 0.3** - Sparse vegetation
- **Below 0.1** - No vegetation (water, urban, bare ground)

**Use it to:** Monitor plant health, detect drought, track growing seasons

### Mosquito Density

**Usually expressed as:** Number per unit area or risk level

**Interpretations:**

- **High** - More than 50 observations per km²
- **Medium** - 20-50 observations per km²
- **Low** - Less than 20 observations per km²

**Use it to:** Identify areas needing mosquito control

### Land Cover Percentage

**Expressed as:** Percentage of total area

**Typical healthy ecosystem:**

- Trees: 30-50%
- Grass/shrubs: 20-40%
- Water: 5-15%
- Urban: 5-20%

**Red flags:**

- Very low vegetation (<20% total)
- Very high urban (>60%)
- No water sources (<2%)
- Extreme values suggest data issues or unique environments

### Correlation Values

**Range:** -1.0 to +1.0

**What it means:**

- **+0.7 to +1.0** - Strong positive relationship (when one increases, other increases)
- **+0.3 to +0.7** - Moderate positive relationship
- **-0.3 to +0.3** - Weak or no relationship
- **-0.7 to -0.3** - Moderate negative relationship
- **-1.0 to -0.7** - Strong negative relationship (when one increases, other decreases)

**Example:**

> "Tree cover and mosquitoes have a correlation of +0.65, meaning areas with more trees tend to have more mosquitoes."

## Spotting Unusual Results

### When to Double-Check

**Red flags that might indicate problems:**

1. **All zeros or all the same values** - Data loading issue
2. **Values outside expected ranges** - Data error or unusual event
3. **Sudden huge spikes** - Outliers or data entry errors
4. **Predictions that don't make sense** - Model needs more data
5. **Missing maps or charts** - Processing error

**What to do:**

- Check that input data files are correct
- Look for error messages in the terminal
- Try re-running the analysis
- See the [FAQ](04_FAQ.md) for troubleshooting

### Normal Variations vs. Problems

**Normal:**

- Seasonal patterns (higher values in summer)
- Gradual trends (slow increase over months)
- Some scatter in scatter plots
- A few missing data points

**Problematic:**

- Completely flat lines (no variation)
- Values that violate physical limits (e.g., NDVI > 1.0)
- Predictions that contradict historical patterns
- All observations in one tiny area

## Comparing Results Over Time

To track changes, save each analysis:

1. After analysis, rename output folder: `output_2025-10-05`
2. Run analysis again with new data
3. Open both sets of results side-by-side
4. Look for differences in:
   - Map marker locations and colors
   - Chart value levels
   - Trends (increasing vs. decreasing)
   - Prediction accuracy (compare old predictions to actual new data)

**Questions to ask:**

- Are mosquito numbers rising or falling?
- Is vegetation improving or degrading?
- Were past predictions accurate?
- Are new areas showing up on the map?

## Using Results for Decision-Making

### For Public Health Officials

**Focus on:**

- Mosquito density maps (where to spray)
- Species distribution (which diseases are risks)
- Temporal predictions (when to intensify monitoring)

**Actions:**

- Allocate resources to red zones on heatmaps
- Plan interventions before predicted peaks
- Monitor areas with increasing trends

### For Environmental Managers

**Focus on:**

- Land cover percentages (ecosystem health)
- Vegetation trends (restoration success)
- Water body analysis (habitat quality)

**Actions:**

- Protect high-vegetation areas
- Restore degraded zones (low NDVI)
- Monitor water quality in bloom areas

### For Researchers

**Focus on:**

- Correlation analyses (relationships)
- Prediction accuracy (model validation)
- Temporal patterns (seasonal cycles)

**Actions:**

- Test hypotheses with the data
- Validate predictions with field observations
- Identify areas for further study

## Getting More Details

For deeper technical understanding:

- [Technical Architecture](../TECHNICAL/01_ARCHITECTURE.md)
- [How Predictions Work](../TECHNICAL/03_PREDICTION_SYSTEM.md)
- [Data Structure Details](../TECHNICAL/04_DATA_STRUCTURES.md)

For help with problems:

- [FAQ](04_FAQ.md)
- [GitHub Issues](https://github.com/Sadrach34/Orbita-CodeCaster/issues)

## Summary Checklist

When reviewing results, check:

- [ ] Maps load and are interactive
- [ ] Charts show clear patterns
- [ ] Numbers are within expected ranges
- [ ] Predictions have confidence intervals
- [ ] Report sections are complete
- [ ] Key findings make sense in context
- [ ] No obvious errors or missing data

If everything checks out, you can confidently use the results for your work!
