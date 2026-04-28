import json
from pathlib import Path

import pandas as pd

from hydroserver_workshop.scripts.validate_workshop_assets import collect_errors


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    ROOT / "notebooks" / "quick_demo_data.ipynb",
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


def test_station_catalog_and_files_are_usable():
    data_dir = ROOT / "data"
    catalog = pd.read_csv(data_dir / "Uganda_Hydroweb_subset.csv")
    hydroweb_files = {path.name for path in (data_dir / "hydroweb").glob("*.csv")}
    geoglows_files = {path.name for path in (data_dir / "geoglows").glob("*.csv")}

    assert len(catalog) == 5
    assert {"ID", "COMID_v1", "COMID_v2", "hydroweb_file", "geoglows_file"}.issubset(catalog.columns)
    assert set(catalog["hydroweb_file"]).issubset(hydroweb_files)
    assert set(catalog["geoglows_file"]).issubset(geoglows_files)
    assert ((catalog["COMID_v1"] != 0) & (catalog["COMID_v2"] != 0)).all()


def test_hydroweb_station_csv_and_normalized_payload_shape():
    data_dir = ROOT / "data"
    station = pd.read_csv(data_dir / "Uganda_Hydroweb_subset.csv").iloc[0]
    raw = pd.read_csv(data_dir / "hydroweb" / station["hydroweb_file"])
    geoglows_raw = pd.read_csv(data_dir / "geoglows" / station["geoglows_file"])

    assert list(raw.columns) == ["Datetime", "Water Level (m)"]
    assert pd.to_datetime(raw["Datetime"], utc=True, errors="coerce").notna().all()
    assert pd.to_numeric(raw["Water Level (m)"], errors="coerce").notna().all()
    assert len(geoglows_raw.columns) == 2
    timestamp_column, value_column = geoglows_raw.columns
    assert pd.to_datetime(geoglows_raw[timestamp_column], utc=True, errors="coerce").notna().all()
    assert pd.to_numeric(geoglows_raw[value_column], errors="coerce").notna().all()


def test_geoglows_directory_accepts_two_column_station_csvs():
    geoglows_files = sorted((ROOT / "data" / "geoglows").glob("*.csv"))

    assert len(geoglows_files) == 5
    for path in geoglows_files:
        frame = pd.read_csv(path)
        assert len(frame.columns) == 2
        timestamp_column, value_column = frame.columns
        assert pd.to_datetime(frame[timestamp_column], utc=True, errors="coerce").notna().all()
        assert pd.to_numeric(frame[value_column], errors="coerce").notna().all()


def test_catalog_contains_five_paired_stations():
    data_dir = ROOT / "data"
    stations = pd.read_csv(data_dir / "Uganda_Hydroweb_subset.csv")

    assert len(stations) == 5
    assert {"ID", "COMID_v1", "COMID_v2", "hydroweb_file", "geoglows_file"}.issubset(stations.columns)
    for _, station in stations.iterrows():
        assert (data_dir / "hydroweb" / station["hydroweb_file"]).exists()
        assert (data_dir / "geoglows" / station["geoglows_file"]).exists()
        assert int(station["COMID_v1"]) != 0
        assert int(station["COMID_v2"]) != 0


def test_presentation_references_logo_and_quick_demo_flow():
    markdown = (ROOT / "presentation" / "hydroserver_30_min_workshop_slides.md").read_text(encoding="utf-8")
    html = (ROOT / "presentation" / "hydroserver_30_min_workshop_slides.html").read_text(encoding="utf-8")
    combined = f"{markdown}\n{html}"

    assert "../imgs/hydroserver_logo.png" in combined
    assert (ROOT / "imgs" / "hydroserver_logo.png").exists()
    assert "HydroServer in 40 Minutes" in combined
    assert "quick_demo_data.ipynb" in combined
    assert "The Only Notebook Today" in combined
    assert "demo1" in combined
    assert "AUTH_METHOD" in combined
    assert "password" in combined
    assert "API key" in combined
    assert "Anonymous mode is limited" in combined
    assert "Input Data" in combined
    assert "Live Workflow" in combined
    assert "Safe Live Demonstration" in combined
    assert "Uganda_Hydroweb_subset.csv" in combined
    assert "/content/sample_data/ts/hydroweb" in combined
    assert "/content/sample_data/ts/geoglows" in combined
    assert "Hydroweb" in combined
    assert "GEOGLOWS" in combined
    assert "COMID_v1" in combined
    assert "COMID_v2" in combined
    assert "HydroServerPy Management Pattern" not in combined
    assert "Optional Reference Layer" not in combined
    assert "Notebook 1" not in combined
    assert "01_things_and_metadata.ipynb" not in combined
    assert "ENABLE_LIVE_WRITE" not in combined


def test_readme_mentions_single_quick_demo_notebook():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "HydroServer 40-Minute Workshop" in readme
    assert "40-Minute Run Sheet" in readme
    assert "quick_demo_data.ipynb" in readme
    assert "single live notebook" in readme
    assert "presentation/hydroserver_30_min_workshop_slides.html" in readme
    assert "presentation/hydroserver_30_min_workshop_slides.md" in readme
    assert "Google Colab" in readme
    assert "/content/sample_data" in readme
    assert "data/Uganda_Hydroweb_subset.csv" in readme


def test_workshop_has_single_quick_demo_notebook_with_setup_and_cleanup():
    assert [path.name for path in NOTEBOOKS] == ["quick_demo_data.ipynb"]
    for path in NOTEBOOKS:
        assert path.exists()
        source = notebook_source(path)
        assert "Setup and Creation Controls" in source
        assert "Connect to HydroServer" in source
        assert "Find or Optionally Create Demo Workspace" in source
        assert "Cleanup: Delete Created Resources" in source
        assert 'AUTH_METHOD = "password"' in source
        assert "HYDROSERVER_API_KEY = \"\"" in source
        assert "HydroServer(host=HYDROSERVER_HOST, email=username, password=password)" in source
        assert "HydroServer(host=HYDROSERVER_HOST, apikey=api_key)" in source
        assert "CREATE_WORKSPACE_IF_MISSING = True" in source
        assert "DELETE_CREATED_RESOURCES_AT_END = True" in source


def test_quick_demo_notebook_covers_live_station_upload_workflow():
    source = all_notebook_source()

    for expected in [
        "01 - HydroServer Things and Metadata",
        "Create Needed Metadata and an Example Thing",
        "Prepare some Time Series",
        "Upload observations to HydroServer datastreams",
        "Uganda_Hydroweb_subset.csv",
        "/content/sample_data/ts/hydroweb",
        "/content/sample_data/ts/geoglows",
        "bulk_station_load_plan",
        "loadable_station_plan",
        "workspace_inventory_dataframe",
        "upload_summary_df",
        "normalize_hydroweb_water_level",
        "normalize_two_column_geoglows",
        "prepare_observations_for_hydroserver",
        "upload_observations_to_datastream",
        "mode=\"replace\"",
        "phenomenon_time",
        "result",
        "COMID_v1",
        "COMID_v2",
    ]:
        assert expected in source


def test_notebook_keeps_secret_paths_safe():
    source = all_notebook_source()

    assert "HYDROSERVER_API_KEY = \"\"" in source
    assert "CREATE_WORKSPACE_API_KEY" not in source
    assert "WORKSPACE_API_KEY_NAME" not in source
    assert "workspace.create_api_key(" not in source
    assert "ENABLE_LIVE_WRITE" not in source
