# HydroServer 40-Minute Workshop

Workshop: Peer-to-Peer Technical Workshop Open Source and Interoperable Hydrological and Meteorological Data Systems for Multi-Hazard Early Warning Systems

This folder contains a short, hands-on HydroServer notebook for hydrology, meteorology, forecasting, and early-warning professionals. It is designed for a 40-minute session and assumes little to no Python experience.

## What Participants Will Do

- Configure the `hydroserver_uganda_demo` workspace for the workshop.
- Connect to a HydroServer instance in anonymous read mode or with an API key.
- Find and reuse the already-created demo workspace when authenticated.
- Optionally create the demo workspace programmatically only when the facilitator enables that fallback.
- Optionally create a workspace API key programmatically for facilitator-led authenticated workflows.
- Learn the HydroServerPy data-management pattern: `list`, `get`, `create`, and collection `.items`.
- Review optional HydroServerPy reference sections for collections, workspace resources, metadata creation templates, datastream operations, data connections, tasks, and task runs.
- Inspect HydroServer concepts using hydrologic terms: sites, datastreams, observed properties, units, timestamps, and observations.
- Load a small local streamflow time series from CSV.
- Run simple quality-control and forecast-readiness checks.
- See how `HydroServerQualityControl` can find observation gaps in an authenticated HydroServer-backed workflow.
- Prepare a HydroServer-style observation payload.
- Optionally use facilitator-provided credentials and a prepared datastream to post observations.
- Review optional `hydroserverpy.etl` examples for extractors, transformers, loaders, data mappings, data operations, results, and debugging.
- See how forecast time series can be adapted for HydroServer workflows.

## Folder Layout

```text
hydroserver_workshop/
  README.md
  requirements.txt
  data/
    sample_streamflow_observations.csv
    sample_forecast_timeseries.csv
  imgs/
    hydroserver_logo.png
  notebooks/
    01_hydroserver_30_min_workshop.ipynb
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
jupyter notebook notebooks/01_hydroserver_30_min_workshop.ipynb
```

The default notebook path works with the bundled CSV files and does not require credentials. Internet access is useful for the HydroServer connection demonstration, but the sample-data, quality-control, plotting, and payload-preparation sections are designed to remain useful offline.

The notebook has two layers. The required live path is intended for the 40-minute session. The optional reference sections expand on HydroServerPy data management, `hydroserverpy.etl`, and HydroServer-backed quality control for facilitators and advanced participants.

## Presentation

Open the companion presentation before starting the notebook:

```text
presentation/hydroserver_30_min_workshop_slides.html
```

The slides are intended for the opening, transitions, and closing discussion. Use them to frame why HydroServer matters, orient participants to the notebook workflow, and keep most of the 40-minute session hands-on. The editable slide source is available at `presentation/hydroserver_30_min_workshop_slides.md`.

## Workspace and Credentials

The workshop workspace name is `hydroserver_uganda_demo`.

HydroServer supports anonymous read access for public data and API-key authenticated access for finding private/associated workspaces, creating workspaces, creating API keys, creating metadata, or modifying data. Anonymous mode is intentionally limited: use it for public reads and local examples, not for workspace administration or uploads. The notebook keeps write operations disabled by default and supports two connection modes:

- `anonymous`: default read-only mode for participants.
- `api_key`: facilitator-provided API key.

If the facilitator wants to demonstrate the already-created workspace, API key creation, or a live write:

- Prepare a HydroServer API key before the session.
- Choose `api_key` in the notebook configuration cell.
- Find and reuse the already-created `hydroserver_uganda_demo` workspace at the beginning of the notebook.
- Keep `CREATE_WORKSPACE_IF_MISSING = False` for the normal workshop path.
- Set `CREATE_WORKSPACE_IF_MISSING = True` only if you intentionally want to demonstrate workspace creation.
- Optionally set `CREATE_WORKSPACE_API_KEY = True` after API-key authenticated workspace setup to create a workspace API key.
- Copy the API key secret immediately and do not commit it to the notebook or repository.
- Prepare or identify a datastream that workshop data can be posted to.
- Set the notebook write flag only in the optional authenticated section.
- Confirm that the target datastream is safe for workshop/demo data.

## 40-Minute Run Sheet

- 0-5 minutes: Use the slides to frame why HydroServer matters for interoperable early-warning data systems.
- 5-10 minutes: Configure `hydroserver_uganda_demo`, connect to HydroServer, and explain anonymous versus API-key access.
- 10-18 minutes: Find and reuse the already-created workspace, then introduce HydroServerPy resource properties, UUIDs, `list`, `get`, and collection `.items`.
- 18-27 minutes: Inspect metadata concepts and prepare a HydroServer-ready five-year `phenomenon_time`/`result` table.
- 27-34 minutes: Run quality-control and forecast-readiness checks, then visualize the hydrograph.
- 34-38 minutes: Demonstrate loading payloads and the optional authenticated write path.
- 38-40 minutes: Show the cleanup section and point advanced participants to optional reference sections.

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
