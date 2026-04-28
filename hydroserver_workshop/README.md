# HydroServer 40-Minute Workshop

Workshop: Peer-to-Peer Technical Workshop Open Source and Interoperable Hydrological and Meteorological Data Systems for Multi-Hazard Early Warning Systems

This folder contains a single live notebook for a 40-minute HydroServer demonstration. The notebook creates HydroServer metadata for five Uganda stations, creates Hydroweb and GEOGLOWS datastreams, uploads observations, verifies one upload, and shows how to clean up the demo resources.

## What Participants Will Do

- Open `quick_demo_data.ipynb` as the only workshop notebook.
- Connect to `https://playground.hydroserver.org`.
- Use the notebook's `demo1` workspace, creating it when needed.
- Read the five-station data package in `data/`.
- Match Hydroweb files by station ID or `COMID_v1`.
- Match GEOGLOWS files by station ID or `COMID_v2`.
- Create one HydroServer thing per station.
- Create two datastreams per station: Hydroweb water level and GEOGLOWS streamflow.
- Upload observations with `mode="replace"` so reruns do not duplicate data.
- Inspect DataFrames for metadata templates, loadable stations, workspace inventory, and upload summary.
- Preview and run cleanup for disposable demo resources.

## Folder Layout

```text
hydroserver_workshop/
  README.md
  requirements.txt
  data/
    Uganda_Hydroweb_subset.csv
    hydroweb/
      H-102549.csv
      ...
    geoglows/
      160214697.csv
      ...
  imgs/
    hydroserver_logo.png
  notebooks/
    quick_demo_data.ipynb
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

Then open the notebook:

```bash
jupyter notebook notebooks/quick_demo_data.ipynb
```

The live demo notebook is configured for Google Colab-style paths under `/content/sample_data`. For local Jupyter testing, either adjust the path variables in the setup cell or stage the subset files in the same layout.

## Real Uganda Station Data

The lightweight live-demo package is:

```text
data/
```

The station catalog is:

```text
data/Uganda_Hydroweb_subset.csv
```

The Colab upload file used by the notebook is:

```text
data/Uganda_Hydroweb_subset.csv
```

Each station row includes `ID`, `COMID_v1`, `COMID_v2`, `hydroweb_file`, and `geoglows_file`. Those file columns are the source of truth for which observation files belong to each station.

Hydroweb files are stored in:

```text
data/hydroweb/
```

They contain:

```text
Datetime,Water Level (m)
```

GEOGLOWS files are stored in:

```text
data/geoglows/
```

Each GEOGLOWS station file contains exactly two columns: one timestamp/date column and one streamflow value column.

## Google Colab

The notebook expects this Colab layout:

```text
/content/sample_data/Uganda_Hydroweb_subset.csv
/content/sample_data/ts/hydroweb/
/content/sample_data/ts/geoglows/
```

For the current subset, copy:

- `data/Uganda_Hydroweb_subset.csv` to `/content/sample_data/Uganda_Hydroweb_subset.csv`
- `data/hydroweb/*.csv` to `/content/sample_data/ts/hydroweb/`
- `data/geoglows/*.csv` to `/content/sample_data/ts/geoglows/`

## Presentation

Open the companion presentation before starting the notebook:

```text
presentation/hydroserver_30_min_workshop_slides.html
```

The slides are intended for the opening, transitions, and closing discussion. Use them to frame why HydroServer matters, orient participants to the single live notebook, and keep most of the 40-minute session hands-on. The editable slide source is available at `presentation/hydroserver_30_min_workshop_slides.md`.

## Workspace and Credentials

The notebook currently uses:

```python
WORKSPACE_NAME = "demo1"
AUTH_METHOD = "password"
CREATE_WORKSPACE_IF_MISSING = True
DELETE_CREATED_RESOURCES_AT_END = True
```

`AUTH_METHOD = "api_key"` is also available in the connection cell if the facilitator wants to use an API key instead of username/password. Anonymous mode is limited to public reads and cannot create workspaces, metadata, datastreams, or observations.

Keep credentials local to the notebook session and do not commit them to the repository.

## 40-Minute Run Sheet

- 0-5 minutes: Use the slides to frame HydroServer and the data model.
- 5-10 minutes: Open `quick_demo_data.ipynb`, install/import dependencies, and configure credentials.
- 10-18 minutes: Connect to HydroServer and create or find the `demo1` workspace.
- 18-28 minutes: Inspect the five-station subset and create things plus required metadata.
- 28-36 minutes: Create Hydroweb and GEOGLOWS datastreams, then upload observations.
- 36-40 minutes: Verify one uploaded datastream and show the cleanup section.

## Validate Before Teaching

Run the offline asset validation:

```bash
python scripts/validate_workshop_assets.py
```

Or run the test file:

```bash
pytest tests/test_workshop_assets.py
```

These checks validate the expected files, subset CSV columns, timestamp parsing, notebook JSON, required notebook section headings, presentation files, and presentation logo references. They do not validate live HydroServer credentials or posting observations.

## References

- HydroServer: https://hydroserver2.github.io/hydroserver/
- HydroServerPy: https://hydroserver2.github.io/hydroserverpy/hydroserverpy.html
- HydroServer loading tutorial: https://hydroserver2.github.io/hydroserver/tutorials/loading-data.html
