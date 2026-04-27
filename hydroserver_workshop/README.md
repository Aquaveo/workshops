# HydroServer 40-Minute Workshop

Workshop: Peer-to-Peer Technical Workshop Open Source and Interoperable Hydrological and Meteorological Data Systems for Multi-Hazard Early Warning Systems

This folder contains four focused, hands-on HydroServer notebooks for hydrology, meteorology, forecasting, and early-warning professionals. It is designed for a 40-minute session and assumes little to no Python experience.

## What Participants Will Do

- Configure the `hydroserver_uganda_demo` workspace for the workshop.
- Connect to a HydroServer instance in anonymous read mode or with an API key.
- Find and reuse the already-created demo workspace when authenticated.
- Optionally create the demo workspace programmatically only when the facilitator enables that fallback.
- Build a bulk station load plan from `Uganda_Hydroweb.csv`.
- Read Hydroweb water-level observations from per-station CSV files in `data/hydroweb/`.
- Read GEOGLOWS streamflow observations from two-column per-station CSV files in `data/geoglows/` when those files are present.
- Create one HydroServer thing per eligible station, with Hydroweb water-level and GEOGLOWS streamflow datastreams.
- Learn the HydroServerPy data-management pattern: `list`, `get`, `create`, and collection `.items`.
- Work through a focused metadata notebook, bulk-loading notebook, ETL notebook, and quality-control notebook.
- Inspect HydroServer concepts using hydrologic terms: sites, datastreams, observed properties, units, timestamps, and observations.
- Load a small local streamflow time series from CSV.
- Run simple quality-control and forecast-readiness checks.
- See how `HydroServerQualityControl` can find observation gaps in an authenticated HydroServer-backed workflow.
- Prepare a HydroServer-style observation payload.
- Optionally use facilitator-provided credentials and a prepared datastream to post observations.
- Review the optional `hydroserverpy.etl` HTTPExtractor example for the Aroca River GEOGLOWS forecast point.
- See how forecast time series can be adapted for HydroServer workflows.

## Folder Layout

```text
hydroserver_workshop/
  README.md
  requirements.txt
  data/
    Uganda_Hydroweb.csv
    uganda_selected_station.csv
    uganda_hydroweb_water_level_sample.csv
    uganda_geoglows_streamflow_sample.csv
    hydroweb/
      H-104255.csv
      ...
    geoglows/
      .gitkeep
    sample_streamflow_observations.csv
    sample_forecast_timeseries.csv
  imgs/
    hydroserver_logo.png
  notebooks/
    01_things_and_metadata.ipynb
    02_bulk_loading_demo.ipynb
    03_etl_demo.ipynb
    04_quality_control_demo.ipynb
  presentation/
    hydroserver_30_min_workshop_slides.html
    hydroserver_30_min_workshop_slides.md
  scripts/
    validate_workshop_assets.py
  tests/
    test_workshop_assets.py
```

## Setup

From this directory, install the workshop dependencies:

```bash
python -m pip install -r requirements.txt
```

Then open the notebooks:

```bash
jupyter notebook notebooks/
```

The default notebook paths work with the bundled CSV files and do not require credentials. Internet access is useful for the HydroServer connection demonstration, but the station-data, quality-control, plotting, and payload-preparation sections are designed to remain useful offline.

The notebooks are split by purpose:

1. `01_things_and_metadata.ipynb`: create things and the metadata needed by datastreams; this is the HydroServerPy data management starting point.
2. `02_bulk_loading_demo.ipynb`: create things, datastreams, and upload Hydroweb/GEOGLOWS observations for all eligible stations.
3. `03_etl_demo.ipynb`: short `HTTPExtractor` GEOGLOWS forecast ETL example for Aroca River.
4. `04_quality_control_demo.ipynb`: short local and optional HydroServer-backed quality-control workflow.

Each notebook starts with setup and any needed creation path, and ends with a cleanup section for disposable demo resources.
The shorter ETL and quality-control notebooks serve as optional reference sections when the live session needs to stay focused on metadata and bulk loading.

## Real Uganda Station Data

The real-data path starts with `data/Uganda_Hydroweb.csv`. The selected station is stored in `data/uganda_selected_station.csv`.

Hydroweb files are stored in:

```text
data/hydroweb/
```

They are named by station ID. For example, `H-104255.csv` corresponds to station `H-104255` in the catalog and contains:

```text
Datetime,Water Level (m)
```

GEOGLOWS files should be stored in:

```text
data/geoglows/
```

GEOGLOWS station files should contain exactly two columns: one timestamp/date column and one streamflow value column. The notebook will match these files to the station catalog using station ID or `COMID_v2` when the files are added. Stations become bulk-load eligible only when both the Hydroweb CSV and GEOGLOWS CSV are present and both COMIDs are nonzero.

For each eligible station, the authenticated bulk path creates one thing and two datastreams:

- Hydroweb/Theia water level, keyed by `COMID_v1`.
- GEOGLOWS streamflow, keyed by `COMID_v2`.

## Google Colab

The notebook is compatible with Google Colab as long as the `data/` folder is available. Use one of these layouts:

- Upload the full `hydroserver_workshop/` folder under `/content`.
- Upload only `data/` beside the notebook under `/content/data`.
- Mount Google Drive and set `DATA_DIR_OVERRIDE` in the notebook to the mounted data folder.

Each notebook checks common local and Colab paths, including `/content/hydroserver_workshop/data` and `/content/data`, and prints the resolved `DATA_DIR` near the top.

## Presentation

Open the companion presentation before starting the notebook:

```text
presentation/hydroserver_30_min_workshop_slides.html
```

The slides are intended for the opening, transitions, and closing discussion. Use them to frame why HydroServer matters, orient participants to the four-notebook workflow, and keep most of the 40-minute session hands-on. The editable slide source is available at `presentation/hydroserver_30_min_workshop_slides.md`.

## Workspace and Credentials

The workshop workspace name is `hydroserver_uganda_demo`.

HydroServer supports anonymous read access for public data and API-key authenticated access for finding private/associated workspaces, creating workspaces, creating metadata, or modifying data. Anonymous mode is intentionally limited: use it for public reads and local examples, not for workspace administration or uploads. The notebooks keep write operations disabled by default and support two connection modes:

- `anonymous`: default read-only mode for participants.
- `api_key`: facilitator-provided API key.

If the facilitator wants to demonstrate the already-created workspace or a live write:

- Prepare a HydroServer API key before the session.
- Choose `api_key` in the relevant notebook configuration cell.
- Find and reuse the already-created `hydroserver_uganda_demo` workspace at the beginning of each notebook.
- Keep `CREATE_WORKSPACE_IF_MISSING = False` for the normal workshop path.
- Set `CREATE_WORKSPACE_IF_MISSING = True` only if you intentionally want to demonstrate workspace creation.
- Keep the API key local to the notebook session and do not commit it to the notebook or repository.
- Add GEOGLOWS station CSVs before demonstrating the full bulk load.
- Confirm that all created resources are disposable workshop/demo data.

## 40-Minute Run Sheet

- 0-5 minutes: Use the slides to frame why HydroServer matters for interoperable early-warning data systems.
- 5-10 minutes: Configure `hydroserver_uganda_demo`, connect to HydroServer, and explain anonymous versus API-key access.
- 10-16 minutes: Open notebook 1 and show things plus required metadata.
- 16-30 minutes: Open notebook 2 and demonstrate the bulk station plan, datastream creation path, and observation upload path.
- 30-35 minutes: Open notebook 3 and show the short Aroca River GEOGLOWS `HTTPExtractor` ETL path.
- 35-40 minutes: Open notebook 4 and run the quality-control checks, then point out each cleanup section.

## Validate Before Teaching

Run the offline asset validation:

```bash
python scripts/validate_workshop_assets.py
```

Or run the test file:

```bash
pytest tests/test_workshop_assets.py
```

These checks validate the expected files, sample CSV columns, timestamp parsing, notebook JSON, required notebook section headings, presentation files, and presentation logo references. They do not validate live HydroServer credentials or posting observations.

## References

- HydroServer: https://hydroserver2.github.io/hydroserver/
- HydroServerPy: https://hydroserver2.github.io/hydroserverpy/hydroserverpy.html
- HydroServer loading tutorial: https://hydroserver2.github.io/hydroserver/tutorials/loading-data.html
- Global Forecast Validation package context: https://pypi.org/project/global-forecast-validation/
