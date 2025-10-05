# Orbita-CodeCaster Documentation

Welcome to the Orbita-CodeCaster documentation. This guide is divided into two main sections tailored to different audiences.

## Documentation Structure

### For End Users

If you want to use the system without diving into technical details, start here:

**[USER_GUIDE/](USER_GUIDE/README.md)** - Non-technical documentation

- [Getting Started](USER_GUIDE/01_GETTING_STARTED.md) - Installation and first steps
- [Basic Usage](USER_GUIDE/02_BASIC_USAGE.md) - How to run analyses
- [Understanding Results](USER_GUIDE/03_UNDERSTANDING_RESULTS.md) - Interpreting outputs
- [FAQ](USER_GUIDE/04_FAQ.md) - Common questions and troubleshooting

### For Developers and Engineers

If you need deep technical understanding or want to extend the system:

**[TECHNICAL/](TECHNICAL/README.md)** - Technical documentation

- [Architecture](TECHNICAL/01_ARCHITECTURE.md) - System design and components
- [Analysis Modules](TECHNICAL/02_ANALYSIS_MODULES.md) - Core analysis implementations
- [Prediction System](TECHNICAL/03_PREDICTION_SYSTEM.md) - ML models and algorithms
- [Data Structures](TECHNICAL/04_DATA_STRUCTURES.md) - Data schemas and formats
- [API Reference](TECHNICAL/05_API_REFERENCE.md) - Complete API documentation
- [Development Guide](TECHNICAL/06_DEVELOPMENT_GUIDE.md) - Contributing and extending

## Quick Navigation

| I want to...                    | Go to                                                           |
| ------------------------------- | --------------------------------------------------------------- |
| Install and run the system      | [Getting Started](USER_GUIDE/01_GETTING_STARTED.md)             |
| Understand what the system does | [Basic Usage](USER_GUIDE/02_BASIC_USAGE.md)                     |
| Read my analysis results        | [Understanding Results](USER_GUIDE/03_UNDERSTANDING_RESULTS.md) |
| Understand the architecture     | [Architecture](TECHNICAL/01_ARCHITECTURE.md)                    |
| Modify or extend functionality  | [Development Guide](TECHNICAL/06_DEVELOPMENT_GUIDE.md)          |
| Use the API                     | [API Reference](TECHNICAL/05_API_REFERENCE.md)                  |

## About This Project

Orbita-CodeCaster is a geospatial analysis platform designed for the NASA Bloomwatch challenge. It monitors and predicts global blooms using NASA Earth observation data, integrating land cover analysis and mosquito habitat data with citizen science data from GLOBE Observer.

**Key Features:**

- Bloom visualization with NASA GIBS satellite imagery (MODIS NDVI)
- Mosquito habitat analysis using GLOBE Observer data
- Land cover classification (trees, vegetation, water, buildings)
- Interactive dashboards with dynamic maps
- Predictive analysis of phenological patterns
- Temporal prediction with Sentinel-2 (45+ satellite images)
- Data visualization with charts and statistics
- Interactive HTML reports with embedded graphics and folium maps

## Version Information

**Current Version:** 1.0.0  
**Last Updated:** October 5, 2025  
**Language:** English  
**Python Version:** 3.8+

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For questions, issues, or contributions:

- GitHub: [github.com/Sadrach34/Orbita-CodeCaster](https://github.com/Sadrach34/Orbita-CodeCaster)
- Issues: [GitHub Issues](https://github.com/Sadrach34/Orbita-CodeCaster/issues)
