# Getting Started with Orbita-CodeCaster

Welcome! This guide will help you set up and run Orbita-CodeCaster on your computer. No technical expertise required.

## What You'll Need

Before starting, make sure you have:

- A computer with Windows, Mac, or Linux
- Internet connection (for downloading files and satellite data)
- At least 4GB of available storage space
- About 20 minutes for installation

## Step 1: Install Python

Python is the programming language that runs Orbita-CodeCaster.

### Check if Python is Already Installed

Open a terminal or command prompt and type:

```bash
python --version
```

If you see something like `Python 3.8` or higher, you're good! Skip to Step 2.

### Installing Python (if needed)

1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.8 or newer
3. Run the installer
4. **Important:** Check "Add Python to PATH" during installation

## Step 2: Download Orbita-CodeCaster

### Option A: Using Git (Recommended)

If you have Git installed:

```bash
git clone https://github.com/Sadrach34/Orbita-CodeCaster.git
cd Orbita-CodeCaster
```

### Option B: Direct Download

1. Go to [github.com/Sadrach34/Orbita-CodeCaster](https://github.com/Sadrach34/Orbita-CodeCaster)
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file to a folder on your computer
5. Open a terminal in that folder

## Step 3: Set Up the Environment

This creates an isolated space for Orbita-CodeCaster to run.

### On Windows:

```bash
python -m venv mi_entorno
mi_entorno\Scripts\activate
```

### On Mac/Linux:

```bash
python3 -m venv mi_entorno
source mi_entorno/bin/activate
```

You'll see `(mi_entorno)` appear in your terminal when it's active.

## Step 4: Install Dependencies

This installs all the tools Orbita-CodeCaster needs:

```bash
pip install -r requirements.txt
```

This may take 5-10 minutes. You'll see progress messages as each component installs.

## Step 5: Verify Installation

Check that everything installed correctly:

```bash
python -c "import pandas, folium, sklearn; print('Success! All components installed.')"
```

If you see "Success!" you're ready to go!

## Step 6: Prepare Your Data

Orbita-CodeCaster expects data files in the `data/raw/` folder:

1. **CSV Files**: Place your GLOBE Observer CSV files here

   - Mosquito habitat data
   - Land cover observations
   - Aerial imagery labels

2. **GeoJSON Files**: Place Sentinel-2 satellite images here
   - Files from ESA Sentinel-2 missions
   - Named like `S2A_T12RWU_20250422T175740_L2A.geojson`

The system comes with sample data, so you can try it immediately!

## Step 7: Run Your First Analysis

Let's run a complete analysis:

```bash
python main.py
```

What happens now:

1. The system loads your data
2. Analyzes mosquito habitats and land cover
3. Creates maps and charts
4. Generates predictions
5. Produces a report

This takes about 5-15 minutes depending on your computer.

## Understanding What Happens

While the analysis runs, you'll see status messages like:

- "Loading data..." - Reading your files
- "Analyzing mosquito habitats..." - Finding patterns in mosquito reports
- "Analyzing land cover..." - Understanding the environment
- "Training prediction model..." - Teaching the computer to make forecasts
- "Generating visualizations..." - Creating maps and charts
- "Creating report..." - Assembling your final document

## Where to Find Results

When finished, check the `data/output/` folder for:

- **Maps** (HTML files): Interactive maps you can open in a browser
- **Charts** (PNG files): Pictures showing trends and patterns
- **Report** (HTML file): Complete analysis report
- **Predictions** (CSV file): Forecast data for future conditions

## Quick Test

To verify everything works, try opening one of the generated maps:

1. Navigate to `data/output/`
2. Find `mapa.html`
3. Double-click to open in your web browser
4. You should see an interactive map with data points

## What If Something Goes Wrong?

### Python Not Found

- Make sure Python is installed and added to PATH
- Try `python3` instead of `python`

### Module Not Found Error

- Your environment may not be activated
- Run the activation command again (Step 3)
- Reinstall dependencies: `pip install -r requirements.txt`

### Out of Memory

- Close other programs
- Try processing smaller datasets first

### No Output Files

- Check that data files are in `data/raw/`
- Look for error messages in the terminal
- See the [FAQ](04_FAQ.md) for common issues

## Next Steps

Now that you're set up:

- Read [Basic Usage](02_BASIC_USAGE.md) to learn about different analyses
- Check [Understanding Results](03_UNDERSTANDING_RESULTS.md) to interpret your outputs
- Browse the [FAQ](04_FAQ.md) for tips and troubleshooting

## Getting Help

If you're stuck:

1. Check the [FAQ](04_FAQ.md) for common problems
2. Review error messages carefully
3. Visit the [GitHub Issues](https://github.com/Sadrach34/Orbita-CodeCaster/issues) page
4. Search for your error message online

Congratulations! You're ready to analyze geospatial data with Orbita-CodeCaster.
