import json
from pathlib import Path

import pandas as pd

from hydroserver_workshop.scripts.validate_workshop_assets import collect_errors


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    ROOT / "notebooks" / "01_things_and_metadata.ipynb",
    ROOT / "notebooks" / "02_bulk_loading_demo.ipynb",
    ROOT / "notebooks" / "03_etl_demo.ipynb",
    ROOT / "notebooks" / "04_quality_control_demo.ipynb",
]


def notebook_source(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
        for cell in notebook["cells"]
    )


def all_notebook_source() -> str:
    return "\n".join(notebook_source(path) for path in NOTEBOOKS)


def test_workshop_assets_validate():
    assert collect_errors() == []


def test_streamflow_sample_has_intentional_qc_issue():
    frame = pd.read_csv(ROOT / "data" / "sample_streamflow_observations.csv")

    assert frame["value"].isna().sum() == 1
    assert frame["value"].max() > 100
    assert "suspicious spike" in " ".join(frame["quality_note"].dropna())


def test_forecast_sample_has_required_forecast_fields():
    frame = pd.read_csv(ROOT / "data" / "sample_forecast_timeseries.csv")

    assert {"timestamp", "forecast_issue_time", "lead_time_hours", "value"}.issubset(frame.columns)
    assert frame["lead_time_hours"].is_monotonic_increasing
    assert pd.to_datetime(frame["timestamp"], utc=True, errors="coerce").notna().all()


def test_uganda_hydroweb_station_catalog_and_files_are_usable():
    catalog = pd.read_csv(ROOT / "data" / "Uganda_Hydroweb.csv")
    selected = pd.read_csv(ROOT / "data" / "uganda_selected_station.csv")
    hydroweb_files = {path.stem for path in (ROOT / "data" / "hydroweb").glob("*.csv")}

    assert len(selected) == 1
    station = selected.iloc[0]
    assert station["ID"] in set(catalog["ID"])
    assert station["ID"] in hydroweb_files
    assert int(station["COMID_v1"]) != 0
    assert int(station["COMID_v2"]) != 0
    assert ((catalog["COMID_v1"] != 0) & (catalog["COMID_v2"] != 0)).any()


def test_hydroweb_station_csv_and_normalized_payload_shape():
    selected = pd.read_csv(ROOT / "data" / "uganda_selected_station.csv").iloc[0]
    raw = pd.read_csv(ROOT / "data" / "hydroweb" / f"{selected['ID']}.csv")
    normalized = pd.read_csv(ROOT / "data" / "uganda_hydroweb_water_level_sample.csv")
    geoglows_sample = pd.read_csv(ROOT / "data" / "uganda_geoglows_streamflow_sample.csv")

    assert list(raw.columns) == ["Datetime", "Water Level (m)"]
    assert pd.to_datetime(raw["Datetime"], utc=True, errors="coerce").notna().all()
    assert pd.to_numeric(raw["Water Level (m)"], errors="coerce").notna().all()
    assert {
        "phenomenon_time",
        "result",
        "source",
        "source_identifier",
        "station_id",
        "observed_property",
        "unit",
    }.issubset(normalized.columns)
    assert set(normalized["station_id"]) == {selected["ID"]}
    assert set(normalized["observed_property"]) == {"Water Level"}
    assert set(normalized["unit"]) == {"m"}
    assert set(geoglows_sample["station_id"]) == {selected["ID"]}
    assert set(geoglows_sample["observed_property"]) == {"Streamflow"}
    assert set(geoglows_sample["unit"]) == {"m3/s"}
    assert pd.to_datetime(geoglows_sample["phenomenon_time"], utc=True, errors="coerce").notna().all()
    assert pd.to_numeric(geoglows_sample["result"], errors="coerce").notna().all()


def test_geoglows_directory_accepts_two_column_station_csvs_when_present():
    geoglows_files = sorted((ROOT / "data" / "geoglows").glob("*.csv"))

    for path in geoglows_files[:5]:
        frame = pd.read_csv(path)
        assert len(frame.columns) == 2
        timestamp_column, value_column = frame.columns
        assert pd.to_datetime(frame[timestamp_column], utc=True, errors="coerce").notna().all()
        assert pd.to_numeric(frame[value_column], errors="coerce").notna().all()


def test_presentation_references_logo_and_notebook_flow():
    markdown = (ROOT / "presentation" / "hydroserver_30_min_workshop_slides.md").read_text(encoding="utf-8")
    html = (ROOT / "presentation" / "hydroserver_30_min_workshop_slides.html").read_text(encoding="utf-8")
    combined = f"{markdown}\n{html}"

    assert "../imgs/hydroserver_logo.png" in combined
    assert (ROOT / "imgs" / "hydroserver_logo.png").exists()
    assert "HydroServer in 40 Minutes" in combined
    assert "HydroServerPy Management Pattern" in combined
    assert "Optional Reference Layer" in combined
    assert "hydroserverpy.etl" in combined
    assert "HydroServerQualityControl" in combined
    assert "hydroserver_uganda_demo" in combined
    assert "API key" in combined
    assert "Anonymous mode is limited" in combined
    assert "workspace API key" not in combined
    assert "already-created workspace" in combined
    assert "API key authentication" in combined
    assert "Bulk station load" in combined
    assert "Aroca River" in combined
    assert "160180844" in combined
    assert "HTTPExtractor" in combined
    assert "Notebook Workflow" in combined
    assert "Quality Control and Forecast Readiness" in combined
    assert "Safe Live Demonstration" in combined
    assert "Uganda station data" in combined
    assert "Hydroweb" in combined
    assert "GEOGLOWS" in combined
    assert "COMID_v1" in combined
    assert "COMID_v2" in combined
    assert "ENABLE_LIVE_WRITE" not in combined


def test_readme_mentions_companion_presentation():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "HydroServer 40-Minute Workshop" in readme
    assert "40-Minute Run Sheet" in readme
    assert "optional reference sections" in readme
    assert "HydroServerPy data management" in readme
    assert "hydroserverpy.etl" in readme
    assert "HydroServerQualityControl" in readme
    assert "presentation/hydroserver_30_min_workshop_slides.html" in readme
    assert "presentation/hydroserver_30_min_workshop_slides.md" in readme
    assert "Google Colab" in readme
    assert "DATA_DIR" in readme
    assert "data/hydroweb" in readme
    assert "data/geoglows" in readme


def test_workshop_has_four_focused_notebooks_with_setup_and_cleanup():
    assert [path.name for path in NOTEBOOKS] == [
        "01_things_and_metadata.ipynb",
        "02_bulk_loading_demo.ipynb",
        "03_etl_demo.ipynb",
        "04_quality_control_demo.ipynb",
    ]
    for path in NOTEBOOKS:
        assert path.exists()
        source = notebook_source(path)
        assert "Setup and Creation Controls" in source
        assert "Connect to HydroServer" in source
        assert "Find or Optionally Create Demo Workspace" in source
        assert "Cleanup: Delete Created Resources" in source
        assert "DELETE_CREATED_RESOURCES_AT_END = False" in source
        assert 'AUTH_METHOD = "anonymous"' in source
        assert "HydroServer(host=HYDROSERVER_HOST, apikey=api_key)" in source


def test_split_notebooks_cover_requested_workflows():
    source = all_notebook_source()

    for expected in [
        "01 - HydroServer Things and Metadata",
        "02 - HydroServer Bulk Loading Demo",
        "03 - HydroServer ETL Demo",
        "04 - HydroServer Quality Control Demo",
        "Create Needed Metadata and an Example Thing",
        "Create Needed Metadata, Things, and Datastreams",
        "Upload Hydroweb and GEOGLOWS Observations",
        "HydroServerQualityControl",
        "find_gaps",
        "include_quality=True",
        "result_qualifier_codes",
        "ETLPipeline",
        "HTTPExtractor",
        "CSVTransformer",
        "HydroServerLoader",
        "ETLDataMapping",
        "ETLTargetPath",
        "Aroca River",
        "160180844",
        "1.533355",
        "32.21666",
        "geoglows.ecmwf.int/api",
        "bulk_station_load_plan",
        "eligible_stations",
        "MAX_STATIONS_TO_LOAD = None",
        "normalize_hydroweb_water_level",
        "normalize_two_column_geoglows",
    ]:
        assert expected in source


def test_notebooks_keep_write_and_secret_paths_safe_by_default():
    source = all_notebook_source()

    assert "CREATE_WORKSPACE_IF_MISSING = False" in source
    assert "HYDROSERVER_API_KEY = \"\"" in source
    assert "RUN_ETL = False" in source
    assert "UPLOAD_QUALITY_CONTROLLED_RESULTS = False" in source
    assert "CREATE_WORKSPACE_API_KEY" not in source
    assert "WORKSPACE_API_KEY_NAME" not in source
    assert "workspace.create_api_key(" not in source
    assert "HydroServer(host=HYDROSERVER_HOST, email=email, password=password)" not in source
    assert "ENABLE_LIVE_WRITE" not in source
    assert "# workspace.remove_collaborator(" not in source
    assert "# workspace.transfer_ownership(" not in source


def test_etl_notebook_is_http_only():
    source = notebook_source(ROOT / "notebooks" / "03_etl_demo.ipynb")

    assert "HTTPExtractor" in source
    for removed in [
        "FTPExtractor",
        "LocalFileExtractor",
        "JSONTransformer",
        "RatingCurveDataOperation",
        "TemporalAggregationOperation",
    ]:
        assert removed not in source
