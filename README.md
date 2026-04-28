# Workshops

This repository contains workshop materials for hands-on technical training.

## Available Workshops

### HydroServer 40-Minute Workshop

Path: `hydroserver_workshop/`

This workshop introduces HydroServer and HydroServerPy for managing hydrologic and meteorological time series data. It includes:

- one Jupyter notebook, `quick_demo_data.ipynb`, for the live demo
- bundled sample streamflow and forecast CSV files
- a 5-station data package with paired Hydroweb and GEOGLOWS files
- a live workflow that creates one thing with Hydroweb and GEOGLOWS datastreams per station
- observation upload with `mode="replace"` and a verification cell
- cleanup cells for disposable demo resources
- a companion slide deck
- validation scripts and tests
- authenticated HydroServer write examples

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
jupyter notebook notebooks/quick_demo_data.ipynb
```

## Google Colab

The live notebook is configured for Google Colab-style paths. In Colab, stage the subset files like this:

- `/content/sample_data/Uganda_Hydroweb_subset.csv`
- `/content/sample_data/ts/hydroweb/`
- `/content/sample_data/ts/geoglows/`

The repository data is in `hydroserver_workshop/data/`, which contains 5 paired Hydroweb/GEOGLOWS stations. Hydroweb files are named by station ID, such as `H-102549.csv`, with `Datetime` and `Water Level (m)` columns. GEOGLOWS files are one two-column CSV per station: timestamp/date and streamflow value.

## Validate Workshop Assets

```bash
cd hydroserver_workshop
python scripts/validate_workshop_assets.py
pytest tests/test_workshop_assets.py
```

## Notes

The HydroServer notebook keeps credentials out of the repository. Live writes should target disposable demo resources, and the notebook includes cleanup cells for deleting created resources after the demo.
