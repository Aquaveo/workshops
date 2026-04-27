# Workshops

This repository contains workshop materials for hands-on technical training.

## Available Workshops

### HydroServer 40-Minute Workshop

Path: `hydroserver_workshop/`

This workshop introduces HydroServer and HydroServerPy for managing hydrologic and meteorological time series data. It includes:

- a Jupyter notebook for the live session
- bundled sample streamflow and forecast CSV files
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
jupyter notebook notebooks/01_hydroserver_30_min_workshop.ipynb
```

## Validate Workshop Assets

```bash
cd hydroserver_workshop
python scripts/validate_workshop_assets.py
pytest tests/test_workshop_assets.py
```

## Notes

The HydroServer notebook is safe by default: anonymous read mode is enabled, API keys are not stored in the notebook, and write/delete operations require explicit facilitator configuration.
