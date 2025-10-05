# Frequently Asked Questions (FAQ)

Common questions and solutions for Orbita-CodeCaster users.

## Installation and Setup

### Q: Python is not found when I try to install

**A:** Make sure Python is added to your system PATH.

**Windows:** Reinstall Python and check "Add Python to PATH" during installation.

**Mac/Linux:** Python 3 is usually pre-installed. Try `python3` instead of `python`.

### Q: pip install fails with "permission denied"

**A:** You may need administrator privileges.

**Windows:** Run command prompt as administrator.

**Mac/Linux:** Use `sudo pip install -r requirements.txt` (not recommended) or ensure your virtual environment is activated.

**Better solution:** Always use a virtual environment:

```bash
python -m venv mi_entorno
source mi_entorno/bin/activate  # or mi_entorno\Scripts\activate on Windows
pip install -r requirements.txt
```

### Q: "Module not found" error even after installing

**A:** Your virtual environment may not be activated.

**Check:** Look for `(mi_entorno)` at the start of your command line.

**Solution:** Run the activation command again:

- Windows: `mi_entorno\Scripts\activate`
- Mac/Linux: `source mi_entorno/bin/activate`

### Q: Installation takes forever or hangs

**A:** Some packages are large and take time.

**Solutions:**

- Ensure stable internet connection
- Try installing packages one at a time
- Use `pip install --no-cache-dir -r requirements.txt`
- Check disk space (need at least 2GB free)

### Q: What Python version should I use?

**A:** Python 3.8 or newer. Python 3.10 or 3.11 is recommended for best performance.

Check your version: `python --version`

### Q: Can I use Anaconda instead of standard Python?

**A:** Yes! Anaconda works fine.

```bash
conda create -n orbita python=3.10
conda activate orbita
pip install -r requirements.txt
```

## Running Analyses

### Q: How long should analysis take?

**A:** Depends on data size and your computer.

**Typical times:**

- Small dataset (< 1000 records): 2-5 minutes
- Medium dataset (1000-10000 records): 5-15 minutes
- Large dataset (> 10000 records): 15-30 minutes
- With predictions: Add 5-10 minutes

If it takes much longer, check CPU usage and available memory.

### Q: Analysis stops halfway through with no error

**A:** Usually a memory issue.

**Solutions:**

- Close other programs
- Restart your computer
- Process smaller datasets
- Check terminal for error messages (scroll up)

### Q: "No module named 'src'" error

**A:** You're not in the correct directory.

**Solution:** Navigate to the Orbita-CodeCaster folder:

```bash
cd /path/to/Orbita-CodeCaster
```

### Q: Can I run analysis in the background?

**A:** Yes, on Mac/Linux:

```bash
nohup python main.py > output.log 2>&1 &
```

Check progress with `tail -f output.log`

On Windows, consider using a terminal multiplexer or just keep the window open.

### Q: How do I stop a running analysis?

**A:** Press `Ctrl+C` in the terminal.

Note: This may leave incomplete output files. Delete the `data/output/` folder and run again if needed.

### Q: Can I analyze multiple datasets at once?

**A:** Not simultaneously with the same files. Instead:

1. Run first dataset: `python main.py`
2. Rename output folder: `mv data/output data/output_dataset1`
3. Replace data in `data/raw/` with second dataset
4. Run again: `python main.py`

## Data and Files

### Q: What data files do I need?

**A:** At minimum, place these in `data/raw/`:

**Required:**

- `AdoptAPixel3km2020_GO_MosquitoHabitatMapper.csv` (mosquito data)
- `AdoptAPixel3km2020_GO_LandCover.csv` (land cover data)

**Optional but recommended:**

- `AdoptAPixel3km2020_100m_aerialImageryLabels.csv` (for predictions)
- Sentinel-2 GeoJSON files (for temporal predictions)

### Q: Where do I get Sentinel-2 data?

**A:** Download from:

- [Copernicus Open Access Hub](https://scihub.copernicus.eu/)
- [Sentinel Hub](https://www.sentinel-hub.com/)
- [AWS Sentinel-2](https://registry.opendata.aws/sentinel-2/)

Export as GeoJSON with metadata.

### Q: My data has different column names

**A:** The system expects specific column names.

**Solution:** Rename columns in your CSV to match expected names (see [Data Structures](../TECHNICAL/04_DATA_STRUCTURES.md)).

Or modify the data loader in `src/utils/data_loader.py`.

### Q: Can I use data from a different region?

**A:** Yes! As long as the CSV format matches.

The system is region-agnostic. It will analyze any geospatial data in the expected format.

### Q: Output folder is empty after analysis

**A:** Check for error messages in the terminal.

**Common causes:**

- Missing input data files
- Incorrect file format
- Insufficient disk space
- Permission issues

**Solution:** Scroll up in your terminal to find error messages. They usually explain what went wrong.

### Q: Can I delete old output files?

**A:** Yes, it's safe to delete `data/output/` contents.

Results are regenerated each time you run an analysis. Consider backing up important results first.

## Results and Interpretation

### Q: What does NDVI mean?

**A:** Normalized Difference Vegetation Index - measures plant health.

**Scale:** -1 to +1

- Higher values = healthier, denser vegetation
- Lower values = sparse or no vegetation

See [Understanding Results](03_UNDERSTANDING_RESULTS.md) for details.

### Q: Why are some map markers missing?

**A:** Could be:

- Data points outside the map bounds (zoom out)
- Coordinates are invalid (0,0 or null)
- Markers are clustered (click cluster to expand)

### Q: Predictions seem inaccurate

**A:** Predictions have uncertainty. Check:

1. **Confidence intervals** - Wide intervals mean low confidence
2. **Historical accuracy** - Compare old predictions to actual data
3. **Data quality** - More data = better predictions
4. **Timeframe** - Predictions are less accurate further into the future

**Typical accuracy:**

- 30 days ahead: Good
- 60 days ahead: Moderate
- 90+ days ahead: Use with caution

### Q: What's a "good" correlation value?

**A:** Depends on context, but generally:

- **0.7-1.0:** Strong (actionable insights)
- **0.4-0.7:** Moderate (worth investigating)
- **0.0-0.4:** Weak (might be noise)

Environmental data rarely has perfect correlations (1.0).

### Q: Charts show "No data"

**A:** The dataset might be missing required columns or all values are null.

**Check:**

- Input CSV files have data
- Column names are correct
- Values are not all zeros or nulls

### Q: Map won't open or shows errors

**A:** HTML maps need a web browser.

**Solutions:**

- Try a different browser (Chrome, Firefox, Edge)
- Check the HTML file isn't corrupted (file size > 0)
- Disable browser extensions that block scripts
- Open from local filesystem, not from a server

### Q: How do I share results with others?

**A:** The HTML report is self-contained.

**To share:**

1. Find `data/output/reporte.html`
2. Send via email or cloud storage
3. Recipient opens in any web browser
4. No software installation needed for viewing

Note: Very large reports (>50MB) may be slow to load.

## Performance and Optimization

### Q: Can I make analysis faster?

**A:** Yes, several options:

1. **Use fewer Sentinel-2 images** - 20-30 is usually enough
2. **Reduce chart resolution** - Edit DPI settings in code
3. **Skip prediction models** - Comment out prediction sections in `main.py`
4. **Use faster computer** - More RAM and CPU cores help

### Q: Computer freezes during analysis

**A:** Not enough RAM.

**Solutions:**

- Close all other programs
- Process smaller datasets
- Increase system virtual memory
- Upgrade RAM if possible

### Q: Disk space fills up quickly

**A:** Output files can be large.

**Space usage:**

- Maps: 1-5 MB each
- Charts: 0.5-2 MB each
- Reports: 5-20 MB each
- CSV: <1 MB each

**Solutions:**

- Delete old outputs regularly
- Compress reports (ZIP)
- Reduce chart DPI in code
- Use external storage

## Errors and Troubleshooting

### Q: "FileNotFoundError: data/raw/..."

**A:** Input data file is missing.

**Solution:** Ensure all required CSV files are in `data/raw/` folder with correct names.

### Q: "KeyError: 'columnName'"

**A:** CSV is missing expected columns.

**Solution:** Check CSV headers match expected names. See [Data Structures](../TECHNICAL/04_DATA_STRUCTURES.md).

### Q: "MemoryError" or "Out of memory"

**A:** Dataset is too large for available RAM.

**Solutions:**

- Close other programs
- Process data in chunks (requires code modification)
- Use computer with more RAM
- Sample dataset (use fewer rows)

### Q: "ModuleNotFoundError: matplotlib"

**A:** Dependencies not fully installed.

**Solution:**

```bash
pip install matplotlib seaborn folium pandas numpy scikit-learn
```

Or reinstall all:

```bash
pip install -r requirements.txt --force-reinstall
```

### Q: Charts look distorted or wrong colors

**A:** Matplotlib backend issue.

**Solution:** Add this to top of `main.py`:

```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
```

### Q: "Permission denied" when saving files

**A:** Output folder or files are read-only.

**Windows:** Right-click folder > Properties > uncheck "Read-only"

**Mac/Linux:**

```bash
chmod -R 755 data/output
```

### Q: Script crashes with no error message

**A:** Python may be killed by OS (out of memory).

**Check:**

- System logs (Event Viewer on Windows, Console on Mac, dmesg on Linux)
- Available memory before running
- Try with smaller dataset to confirm

## Advanced Questions

### Q: Can I customize the analysis?

**A:** Yes! The code is open source.

**Common customizations:**

- Add new chart types (edit `src/analisis_*.py`)
- Change color schemes (edit visualization code)
- Modify prediction parameters (edit `src/prediccion*.py`)
- Add new metrics (extend analysis classes)

See [Development Guide](../TECHNICAL/06_DEVELOPMENT_GUIDE.md) for details.

### Q: How do I add new data sources?

**A:** Extend the `DataLoader` class.

**Steps:**

1. Add loading method to `src/utils/data_loader.py`
2. Call from `main.py`
3. Update analysis modules to use new data

### Q: Can I export results in different formats?

**A:** Currently supports HTML, PNG, and CSV.

**To add:**

- PDF: Use libraries like `pdfkit` or `reportlab`
- Excel: Use `pandas.to_excel()`
- JSON: Use `json.dump()` with Python dicts

### Q: How accurate are the prediction models?

**A:** Varies by data quality and quantity.

**Typical metrics:**

- **R² (coefficient of determination):** 0.70-0.90 for temporal predictions
- **Accuracy:** 75-85% for classification (mosquito habitat prediction)

More data = better accuracy. Models are statistical, not perfect.

### Q: Can I run this on a server or in the cloud?

**A:** Yes, works on any system with Python.

**Cloud options:**

- AWS EC2
- Google Cloud Compute
- Azure VM
- Heroku (for small datasets)

Install same dependencies as local setup.

### Q: Is there a GUI version?

**A:** Not currently. This is a command-line tool.

**Alternatives:**

- Use Jupyter notebooks for interactive analysis
- Build custom GUI with Tkinter or PyQt (requires development)
- Use HTML reports as visual interface

## Getting Help

### Q: Where can I get more help?

**A:** Multiple resources:

1. **This Documentation** - Start with [Getting Started](01_GETTING_STARTED.md)
2. **GitHub Issues** - [github.com/Sadrach34/Orbita-CodeCaster/issues](https://github.com/Sadrach34/Orbita-CodeCaster/issues)
3. **Code Comments** - Read the Python source files
4. **Technical Docs** - [Technical Documentation](../TECHNICAL/README.md)

### Q: How do I report a bug?

**A:** File a GitHub Issue with:

- Description of the problem
- Steps to reproduce
- Error messages (copy full text)
- Your Python version (`python --version`)
- Operating system

### Q: Can I contribute improvements?

**A:** Yes! Contributions welcome.

**Process:**

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

See [Development Guide](../TECHNICAL/06_DEVELOPMENT_GUIDE.md) for coding standards.

## Still Have Questions?

If your question isn't answered here:

1. Check the [Technical Documentation](../TECHNICAL/README.md) for detailed explanations
2. Search existing [GitHub Issues](https://github.com/Sadrach34/Orbita-CodeCaster/issues)
3. Open a new issue if the problem persists

We're here to help!
