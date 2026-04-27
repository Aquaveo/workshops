"""Validate offline assets for the HydroServer 1-hour workshop."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    ROOT / "README.md",
    ROOT / "requirements.txt",
    ROOT / "data" / "sample_streamflow_observations.csv",
    ROOT / "data" / "sample_forecast_timeseries.csv",
    ROOT / "imgs" / "hydroserver_logo.png",
    ROOT / "notebooks" / "01_hydroserver_30_min_workshop.ipynb",
    ROOT / "presentation" / "hydroserver_30_min_workshop_slides.md",
    ROOT / "presentation" / "hydroserver_30_min_workshop_slides.html",
]

REQUIRED_SECTIONS = [
    "hydroserver_uganda_demo",
    "AUTH_METHOD",
    "Connect to HydroServer",
    "Find or Optionally Create Demo Workspace",
    "CREATE_WORKSPACE_IF_MISSING",
    "Optional: Create a Workspace API Key",
    "CREATE_WORKSPACE_API_KEY",
    "workspace.create_api_key",
    "Anonymous mode is useful for public reads, but it is limited",
    "Track Created Resource UUIDs",
    "CREATE_DEMO_METADATA",
    "DELETE_DEMO_RESOURCES_AT_END",
    "HydroServerPy Data Management Essentials",
    "core_resources",
    "Datastreams and Observations",
    "Optional: Create Demo Metadata and Capture UUIDs",
    "Orchestration Systems, Data Connections, Tasks, and Task Runs",
    "result_qualifier_codes",
    "generate_fake_historical_observations",
    "FAKE_OBSERVATION_YEARS",
    "Optional `hydroserverpy.etl` Package Overview",
    "ETLPipeline",
    "LocalFileExtractor",
    "CSVTransformer",
    "ETLDataMapping",
    "TemporalAggregationOperation",
    "raise_on_error=False",
    "Optional HydroServerPy Quality-Control Package",
    "HydroServerQualityControl",
    "find_gaps",
    "include_quality",
    "phenomenon_time",
    "result",
    "Inspect HydroServer Metadata",
    "Prepare Sample Observations",
    "Quality Control and Forecast Readiness",
    "Visualize the Time Series",
    "Loading Demonstration",
    "Optional Cleanup: Delete Demo-Created Resources",
    "Optional Forecast Extension",
]

REQUIRED_PRESENTATION_PHRASES = [
    "Peer-to-Peer Technical Workshop",
    "HydroServer",
    "40 Minutes",
    "HydroServerPy Management Pattern",
    "Optional Reference Layer",
    "hydroserverpy.etl",
    "HydroServerQualityControl",
    "hydroserver_uganda_demo",
    "API key",
    "Anonymous mode is limited",
    "workspace API key",
    "already-created workspace",
    "Notebook Workflow",
    "Quality Control and Forecast Readiness",
    "Safe Live Demonstration",
    "Forecast Extension",
    "../imgs/hydroserver_logo.png",
]


def collect_errors() -> list[str]:
    errors: list[str] = []

    missing = [path for path in EXPECTED_FILES if not path.exists()]
    if missing:
        errors.extend(f"Missing expected file: {path.relative_to(ROOT)}" for path in missing)
        return errors

    errors.extend(_validate_csv(ROOT / "data" / "sample_streamflow_observations.csv", {"timestamp", "value"}))
    errors.extend(
        _validate_csv(
            ROOT / "data" / "sample_forecast_timeseries.csv",
            {"timestamp", "forecast_issue_time", "lead_time_hours", "value"},
        )
    )
    errors.extend(_validate_notebook(ROOT / "notebooks" / "01_hydroserver_30_min_workshop.ipynb"))
    errors.extend(_validate_presentation())
    return errors


def _validate_csv(path: Path, required_columns: set[str]) -> list[str]:
    errors: list[str] = []
    try:
        frame = pd.read_csv(path)
    except Exception as exc:  # pragma: no cover - defensive validation
        return [f"Could not read {path.relative_to(ROOT)}: {exc}"]

    missing_columns = sorted(required_columns.difference(frame.columns))
    if missing_columns:
        errors.append(f"{path.relative_to(ROOT)} missing columns: {', '.join(missing_columns)}")

    if len(frame) < 5:
        errors.append(f"{path.relative_to(ROOT)} should contain at least 5 rows")

    if "timestamp" in frame.columns:
        parsed = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
        if parsed.isna().any():
            errors.append(f"{path.relative_to(ROOT)} contains unparseable timestamps")

    return errors


def _validate_notebook(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"Notebook is not valid JSON: {exc}"]

    cells = notebook.get("cells", [])
    if not cells:
        errors.append("Notebook has no cells")
        return errors

    text = "\n".join(
        "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
        for cell in cells
    )
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"Notebook missing section heading: {section}")

    return errors


def _validate_presentation() -> list[str]:
    errors: list[str] = []
    markdown_path = ROOT / "presentation" / "hydroserver_30_min_workshop_slides.md"
    html_path = ROOT / "presentation" / "hydroserver_30_min_workshop_slides.html"
    logo_path = ROOT / "imgs" / "hydroserver_logo.png"

    markdown = markdown_path.read_text(encoding="utf-8")
    html = html_path.read_text(encoding="utf-8")
    combined = f"{markdown}\n{html}"

    for phrase in REQUIRED_PRESENTATION_PHRASES:
        if phrase not in combined:
            errors.append(f"Presentation missing required phrase or reference: {phrase}")

    if "../imgs/hydroserver_logo.png" in combined and not logo_path.exists():
        errors.append("Presentation references ../imgs/hydroserver_logo.png but the logo file is missing")

    return errors


def main() -> int:
    errors = collect_errors()
    if errors:
        print("Workshop asset validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Workshop asset validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
