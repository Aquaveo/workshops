import json
from pathlib import Path

import pandas as pd

from hydroserver_workshop.scripts.validate_workshop_assets import collect_errors


ROOT = Path(__file__).resolve().parents[1]


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
    assert "workspace API key" in combined
    assert "already-created workspace" in combined
    assert "API key authentication" in combined
    assert "Notebook Workflow" in combined
    assert "Quality Control and Forecast Readiness" in combined
    assert "Safe Live Demonstration" in combined
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


def test_notebook_metadata_cell_handles_hydroserver_collections():
    notebook = json.loads((ROOT / "notebooks" / "01_hydroserver_30_min_workshop.ipynb").read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
        for cell in notebook["cells"]
    )

    assert 'collection = endpoint.list() if hasattr(endpoint, "list") else endpoint' in source
    assert 'items = getattr(collection, "items", collection)' in source
    assert "len(list(records))" not in source
    assert "print(type(records))" not in source


def test_notebook_starts_with_workspace_and_auth_options():
    notebook = json.loads((ROOT / "notebooks" / "01_hydroserver_30_min_workshop.ipynb").read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
        for cell in notebook["cells"]
    )

    assert 'WORKSPACE_NAME = "hydroserver_uganda_demo"' in source
    assert 'AUTH_METHOD = "anonymous"' in source
    assert '"api_key"' in source
    assert "HydroServer(host=HYDROSERVER_HOST, apikey=api_key)" in source
    assert "HydroServer(host=HYDROSERVER_HOST, email=email, password=password)" not in source
    assert "AUTH_METHOD must be 'anonymous' or 'api_key'." in source
    assert "CREATE_WORKSPACE_IF_MISSING = False" in source
    assert "if workspace is None and CREATE_WORKSPACE_IF_MISSING:" in source
    assert "hs_api.workspaces.create(name=WORKSPACE_NAME, is_private=WORKSPACE_IS_PRIVATE)" in source
    assert "Ask the facilitator to create it first" in source
    assert "CREATE_WORKSPACE_API_KEY = False" in source
    assert "WORKSPACE_API_KEY_NAME = \"uganda-demo-api-key\"" in source
    assert "workspace.create_api_key(" in source
    assert "hs_api.roles.list(workspace=workspace, is_apikey_role=True, fetch_all=True)" in source
    assert "CREATE_DEMO_METADATA = False" in source
    assert "DELETE_DEMO_RESOURCES_AT_END = False" in source
    assert 'DEMO_RUN_SUFFIX = ""' in source
    assert 'demo_run_suffix = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")' in source
    assert 'f"UGANDA_DEMO_GAUGE_{demo_run_suffix}"' in source
    assert 'f"WORKSHOP_DEMO_{demo_run_suffix}"' in source


def test_notebook_includes_hydroserverpy_data_management_patterns():
    notebook = json.loads((ROOT / "notebooks" / "01_hydroserver_30_min_workshop.ipynb").read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
        for cell in notebook["cells"]
    )

    assert "HydroServerPy Data Management Essentials" in source
    assert "Track Created Resource UUIDs" in source
    assert "resource_uid" in source
    assert "created_resources_dataframe" in source
    assert "core_resources = [" in source
    assert "fetch_all=True" in source
    assert "page_size=5, page=1, order_by=[\"name\"]" in source
    assert '"dataconnections"' in source
    assert '"tasks"' in source
    assert "Datastreams and Observations" in source
    assert "Optional: Create Demo Metadata and Capture UUIDs" in source
    assert "Orchestration Systems, Data Connections, Tasks, and Task Runs" in source
    assert "thing_create_template" in source
    assert "datastream_create_template" in source
    assert "csv_data_connection_template" in source
    assert "task_create_template" in source
    assert "hs_api.workspaces.list(page_size=5, page=1, order_by=[\"name\"])" in source
    assert "phenomenon_time" in source
    assert "result" in source
    assert "result_qualifier_codes" in source
    assert 'columns={"timestamp": "phenomenon_time", "value": "result"}' in source


def test_notebook_generates_five_year_historical_upload_payload():
    notebook = json.loads((ROOT / "notebooks" / "01_hydroserver_30_min_workshop.ipynb").read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
        for cell in notebook["cells"]
    )

    assert "GENERATE_FIVE_YEAR_OBSERVATIONS = True" in source
    assert "FAKE_OBSERVATION_YEARS = 5" in source
    assert "def generate_fake_historical_observations(years=5" in source
    assert "pd.date_range" in source
    assert "historical_observations" in source
    assert "upload_source_observations = historical_observations" in source
    assert "display(hydroserver_observations.head())" in source
    assert "display(hydroserver_observations.tail())" in source


def test_notebook_includes_etl_and_quality_control_reference_patterns():
    notebook = json.loads((ROOT / "notebooks" / "01_hydroserver_30_min_workshop.ipynb").read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
        for cell in notebook["cells"]
    )

    for expected in [
        "Optional `hydroserverpy.etl` Package Overview",
        "ETLPipeline",
        "HTTPExtractor",
        "FTPExtractor",
        "LocalFileExtractor",
        "CSVTransformer",
        "JSONTransformer",
        "HydroServerLoader",
        "ETLDataMapping",
        "ETLTargetPath",
        "timestamp_type",
        "timestamp_format",
        "timezone_type",
        "ArithmeticExpressionOperation",
        "RatingCurveDataOperation",
        "TemporalAggregationOperation",
        "raise_on_error=False",
        "target_results",
        "HydroServerQualityControl",
        "find_gaps",
        "include_quality=True",
        "quality_controlled_observations",
    ]:
        assert expected in source


def test_notebook_keeps_write_and_destructive_paths_disabled_by_default():
    notebook = json.loads((ROOT / "notebooks" / "01_hydroserver_30_min_workshop.ipynb").read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
        for cell in notebook["cells"]
    )

    assert "CREATE_WORKSPACE_IF_MISSING = False" in source
    assert "CREATE_WORKSPACE_API_KEY = False" in source
    assert "CREATE_DEMO_METADATA = False" in source
    assert "DELETE_DEMO_RESOURCES_AT_END = False" in source
    assert "ENABLE_LIVE_WRITE = False" in source
    assert "HYDROSERVER_API_KEY = \"\"" in source
    assert "# workspace.remove_collaborator(" not in source
    assert "# workspace.transfer_ownership(" not in source
    assert "quality_controlled_datastream.load_observations(quality_controlled_observations)" in source
    assert "Optional Cleanup: Delete Demo-Created Resources" in source
    assert "resource.delete()" in source
    assert "cleanup_order = [" in source
    assert "if not DELETE_DEMO_RESOURCES_AT_END:" in source
