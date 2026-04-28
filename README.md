# Workshops

This repository contains workshop materials for hands-on technical training.

## Available Workshops

### HydroServer 40-Minute Workshop

Path: `hydroserver_workshop/`

This workshop introduces HydroServer and HydroServerPy for managing hydrologic and meteorological time series data. It includes:

- four Jupyter notebooks for metadata, bulk loading, ETL, and quality control
- bundled sample streamflow and forecast CSV files
- real Uganda Hydroweb station metadata and per-station water-level CSV files
- a 5-station `data/subset/` package for lightweight live demos
- support for matching future two-column GEOGLOWS station CSV files
- a bulk station loader that creates one thing with Hydroweb and GEOGLOWS datastreams per eligible station
- an HTTP-only GEOGLOWS forecast ETL example for the Aroca River point
- a companion slide deck
- validation scripts and tests
- optional authenticated HydroServer write examples

Start with the workshop-specific README:

```bash
cd hydroserver_workshop
```

Then read:

```text
README.md
```

## Quick Start

From the repository root:

```bash
cd hydroserver_workshop
python -m pip install -r requirements.txt
jupyter notebook notebooks/
```

## Google Colab

The notebooks resolve data paths for both local Jupyter and Google Colab. In Colab, use one of these layouts:

- upload the full `hydroserver_workshop/` folder under `/content`
- upload the `data/` folder beside the notebook under `/content/data`
- mount Google Drive and set `DATA_DIR_OVERRIDE` in the notebook to the mounted data folder

The expected station data folders are:

```text
hydroserver_workshop/data/hydroweb/
hydroserver_workshop/data/geoglows/
hydroserver_workshop/data/subset/hydroweb/
hydroserver_workshop/data/subset/geoglows/
```

The notebooks default to `hydroserver_workshop/data/subset/`, which contains 5 paired Hydroweb/GEOGLOWS stations. Hydroweb files are named by station ID, such as `H-102549.csv`, with `Datetime` and `Water Level (m)` columns. GEOGLOWS files are one two-column CSV per station: timestamp/date and streamflow value.

## Validate Workshop Assets

```bash
cd hydroserver_workshop
python scripts/validate_workshop_assets.py
pytest tests/test_workshop_assets.py
```

## Notes

The HydroServer notebooks are safe by default: anonymous read mode is enabled, API keys are not stored in notebooks, and cleanup/delete operations require explicit facilitator configuration.
