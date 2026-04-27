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

## HydroServerPy Management Pattern

- Connect once with `HydroServer(...)`.
- Use resource properties such as `workspaces`, `things`, `datastreams`, `sensors`, `units`, `observedproperties`, `dataconnections`, and `tasks`.
- Read collections with `list(...)` and access records with `.items`.
- Use pagination, ordering, filtering, and `fetch_all=True` for larger collections.
- Retrieve one object with `get(uid=...)`.
- Create resources with `create(...)` when authenticated and authorized.

---

## HydroServer Data Model in Hydrology Terms

- **Thing:** gauge, station, watershed outlet, forecast point, or monitored location.
- **Observed property:** streamflow, rainfall, water level, temperature, or forecast value.
- **Sensor:** instrument, model, data source, or processing workflow.
- **Unit:** m3/s, mm, m, degC, or another standard measurement unit.
- **Datastream:** the time series connecting location, variable, method, unit, and observations.

---

## Workspace and Connection

- Workshop workspace: `hydroserver_uganda_demo`.
- Anonymous mode is limited to public reads and local examples.
- Use an API key when the facilitator has prepared one for the demo.
- Use an API key when the facilitator wants authenticated access.
- Find and reuse the already-created workspace before loading or publishing data.
- Create the workspace programmatically only when the facilitator enables that optional fallback.
- Optionally create a workspace API key programmatically after authenticated setup.

---

## Notebook Workflow

1. Configure the workspace and connection method.
2. Connect to a HydroServer instance.
3. Reuse the already-created demo workspace when authenticated.
4. Explore HydroServerPy `list`, `get`, `create`, pagination, ordering, and filtering patterns.
5. Inspect sites, datastreams, observed properties, units, data connections, tasks, and task runs.
6. Prepare a small streamflow observation table.
7. Convert local `timestamp`/`value` columns into HydroServerPy `phenomenon_time`/`result` columns.
8. Check timestamps, missing values, units, and suspicious values.
9. Visualize the hydrograph.
10. Demonstrate a safe loading payload.

---

## Optional Reference Layer

- Resource-by-resource HydroServerPy examples stay in the notebook for follow-up learning.
- `hydroserverpy.etl` examples show extractors, transformers, loaders, mappings, operations, and debugging.
- `HydroServerQualityControl` examples show authenticated observation QC and gap detection.
- These sections are optional during the live 40-minute workshop.

---

## Quality Control and Forecast Readiness

- Are timestamps parseable and in the expected order?
- Are values missing at critical times?
- Are units consistent across the table?
- Do spikes or impossible values need review before warning workflows use the data?
- HydroServer-backed QC can use `HydroServerQualityControl.find_gaps(...)` when a prepared datastream is available.

---

## Safe Live Demonstration

- Anonymous read access is the default path for participants.
- Finding the demo workspace uses API key authentication.
- Workspace creation is optional and facilitator controlled.
- API key creation is facilitator-only and requires an authenticated workspace.
- The notebook uses local CSV data when credentials or network access are not available.
- Posting observations is optional and facilitator controlled.
- Live writes should only target a prepared demo datastream.

---

## Forecast Extension

- Forecast output can be reshaped into the same timestamp and value pattern.
- Validation workflows compare forecast time series with observed data.
- HydroServer can help make those inputs and outputs discoverable and reusable.
- The optional notebook section gives advanced participants a starting point.

---

## What Participants Should Leave With

- A mental model of how HydroServer stores hydrometeorological time series.
- A runnable notebook for connecting, checking, plotting, and preparing data.
- A safer way to discuss operational data sharing for multi-hazard early warning.
- Pointers for extending the workflow into forecast validation.

---

## Next Steps

- Run the notebook cells in order.
- Change only the marked configuration values.
- Keep live writes disabled unless the facilitator provides credentials and a demo datastream.
- Continue with HydroServer documentation and the optional forecast extension after the session.
