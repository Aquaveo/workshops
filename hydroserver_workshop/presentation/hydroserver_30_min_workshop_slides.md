# HydroServer in 40 Minutes

![HydroServer logo](../imgs/hydroserver_logo.png)

Peer-to-Peer Technical Workshop Open Source and Interoperable Hydrological and Meteorological Data Systems for Multi-Hazard Early Warning Systems

---

## Why This Matters

- Early warning systems depend on trusted hydrologic and meteorological time series.
- Forecast workflows need observations, metadata, units, and timestamps to line up.
- Open and interoperable systems reduce manual reconciliation during high-pressure events.

---

## What HydroServer Provides

- A place to publish and discover hydrometeorological time-series data.
- Shared metadata for sites, variables, units, sensors, processing levels, and datastreams.
- Programmatic access through APIs and Python workflows.
- A practical path from field or model data to reusable early-warning information.

---

## HydroServer Data Model in Hydrology Terms

- **Thing:** station, gauge, river reach, forecast point, or monitored location.
- **Observed property:** water level, streamflow, rainfall, temperature, or forecast value.
- **Sensor:** instrument, model, satellite product, or data source.
- **Unit:** m, m3/s, mm, degC, or another standard measurement unit.
- **Datastream:** the time series connecting location, variable, method, unit, and observations.

---

## The Only Notebook Today

- We will use `quick_demo_data.ipynb`.
- The notebook runs as a single live workflow from connection through cleanup.
- It uses five paired Uganda stations with both Hydroweb water level and GEOGLOWS streamflow files.
- It is designed for Google Colab using files under `/content/sample_data/`.
- The main station file is `Uganda_Hydroweb_subset.csv`.

---

## Workspace and Connection

- Demo workspace in the notebook: `demo1`.
- `AUTH_METHOD = "password"` is the live-demo path in the current notebook.
- `AUTH_METHOD = "api_key"` is still available if the facilitator switches to an API key.
- Anonymous mode is limited to public reads and cannot create workspaces, metadata, datastreams, or observations.
- `CREATE_WORKSPACE_IF_MISSING = True` lets the notebook create the workspace when needed.

---

## Input Data

- Station metadata comes from `Uganda_Hydroweb_subset.csv`.
- Hydroweb files are expected under `/content/sample_data/ts/hydroweb/`.
- GEOGLOWS files are expected under `/content/sample_data/ts/geoglows/`.
- Hydroweb files are matched by station ID or `COMID_v1`.
- GEOGLOWS files are matched by station ID or `COMID_v2`.

---

## Live Workflow

1. Connect to HydroServer.
2. Find or create the demo workspace.
3. Read the five-station subset catalog.
4. Create things, observed properties, units, sensors, processing level, and result qualifier.
5. Build two datastreams per station: Hydroweb water level and GEOGLOWS streamflow.
6. Upload observations with `mode="replace"`.
7. Verify one uploaded datastream.
8. Clean up created resources when the demo is finished.

---

## What Participants Will See

- DataFrames showing metadata templates, loadable stations, workspace inventory, and upload summary.
- UUIDs for created HydroServer resources.
- One thing per station.
- Two datastreams per station.
- Normalized observation payloads with `phenomenon_time` and `result`.
- Hydroweb rows and GEOGLOWS rows loaded into HydroServer.

---

## Safe Live Demonstration

- Live writes target disposable demo resources.
- `DEMO_RUN_SUFFIX` keeps resource names unique for each run.
- `UPLOAD_MODE = "replace"` keeps reruns from duplicating observations.
- The cleanup section can preview deletion with `dry_run=True`.
- The final cleanup can delete observations, datastreams, things, and metadata from the workspace.

---

## Teaching Rhythm

- 0-5 minutes: frame HydroServer and the data model.
- 5-10 minutes: open `quick_demo_data.ipynb`, install/import dependencies, and configure credentials.
- 10-18 minutes: connect and create or find the workspace.
- 18-28 minutes: inspect the station subset and create HydroServer metadata.
- 28-36 minutes: create datastreams and upload observations.
- 36-40 minutes: verify results and show cleanup.

---

## What Participants Should Leave With

- A mental model of how HydroServer stores hydrometeorological time series.
- A runnable notebook for creating metadata, datastreams, and observations.
- A clear mapping between station metadata, source files, and HydroServer resources.
- A safe pattern for live demos: unique resource names, upload summary tables, verification, and cleanup.

---

## Next Steps

- Run `quick_demo_data.ipynb` from top to bottom.
- Change only the marked configuration values.
- Keep credentials local to the notebook session.
- Use the upload summary and workspace inventory tables to explain what was created.
- Run the cleanup section before ending the live demo.
