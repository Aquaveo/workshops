"""Validate offline assets for the HydroServer 1-hour workshop."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_NOTEBOOKS = [
    ROOT / "notebooks" / "01_things_and_metadata.ipynb",
    ROOT / "notebooks" / "02_bulk_loading_demo.ipynb",
    ROOT / "notebooks" / "03_etl_demo.ipynb",
    ROOT / "notebooks" / "04_quality_control_demo.ipynb",
]

EXPECTED_FILES = [
    ROOT / "README.md",
    ROOT / "requirements.txt",
    ROOT / "data" / "sample_streamflow_observations.csv",
    ROOT / "data" / "sample_forecast_timeseries.csv",
    ROOT / "data" / "subset" / "stations.csv",
    ROOT / "data" / "subset" / "Uganda_Hydroweb_subset.csv",
    ROOT / "data" / "subset" / "uganda_selected_station.csv",
    ROOT / "imgs" / "hydroserver_logo.png",
    ROOT / "presentation" / "hydroserver_30_min_workshop_slides.md",
    ROOT / "presentation" / "hydroserver_30_min_workshop_slides.html",
] + EXPECTED_NOTEBOOKS

EXPECTED_DIRECTORIES = [
    ROOT / "data" / "subset" / "hydroweb",
    ROOT / "data" / "subset" / "geoglows",
]

REQUIRED_NOTEBOOK_PHRASES = [
    "hydroserver_uganda_demo",
    "AUTH_METHOD",
    "Google Colab",
    "DATA_DIR",
    "USE_DATA_SUBSET",
    "SUBSET_DATA_DIR",
    "Uganda_Hydroweb.csv",
    "COMID_v1",
    "COMID_v2",
    "hydroweb",
    "geoglows",
    "Water Level",
    "GEOGLOWS",
    "Connect to HydroServer",
    "Find or Optionally Create Demo Workspace",
    "CREATE_WORKSPACE_IF_MISSING",
    "Track Created Resources",
    "DELETE_CREATED_RESOURCES_AT_END",
    "Bulk Loading Demo",
    "bulk_station_load_plan",
    "eligible_stations",
    "Create Needed Metadata, Things, and Datastreams",
    "result_qualifier_codes",
    "HydroServer ETL Demo",
    "ETLPipeline",
    "HTTPExtractor",
    "Aroca River",
    "160180844",
    "1.533355",
    "32.21666",
    "geoglows.ecmwf.int/api",
    "CSVTransformer",
    "ETLDataMapping",
    "raise_on_error=False",
    "HydroServer Quality Control Demo",
    "HydroServerQualityControl",
    "find_gaps",
    "include_quality",
    "phenomenon_time",
    "result",
    "Cleanup: Delete Created Resources",
]

REQUIRED_NOTEBOOK_TITLES = [
    "01 - HydroServer Things and Metadata",
    "02 - HydroServer Bulk Loading Demo",
    "03 - HydroServer ETL Demo",
    "04 - HydroServer Quality Control Demo",
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
    "already-created workspace",
    "Bulk station load",
    "Aroca River",
    "160180844",
    "HTTPExtractor",
    "Notebook Workflow",
    "Quality Control and Forecast Readiness",
    "Safe Live Demonstration",
    "Forecast Extension",
    "../imgs/hydroserver_logo.png",
    "Google Colab",
    "Hydroweb",
    "GEOGLOWS",
    "COMID_v1",
    "COMID_v2",
]


def collect_errors() -> list[str]:
    errors: list[str] = []

    missing = [path for path in EXPECTED_FILES if not path.exists()]
    if missing:
        errors.extend(f"Missing expected file: {path.relative_to(ROOT)}" for path in missing)
        return errors

    missing_directories = [path for path in EXPECTED_DIRECTORIES if not path.exists()]
    if missing_directories:
        errors.extend(f"Missing expected directory: {path.relative_to(ROOT)}" for path in missing_directories)
        return errors

    errors.extend(_validate_subset_files())
    errors.extend(_validate_csv(ROOT / "data" / "sample_streamflow_observations.csv", {"timestamp", "value"}))
    errors.extend(
        _validate_csv(
            ROOT / "data" / "sample_forecast_timeseries.csv",
            {"timestamp", "forecast_issue_time", "lead_time_hours", "value"},
        )
    )
    errors.extend(_validate_notebooks())
    errors.extend(_validate_presentation())
    return errors


def _validate_subset_files() -> list[str]:
    errors: list[str] = []
    subset_dir = ROOT / "data" / "subset"
    subset_catalog_path = subset_dir / "stations.csv"
    hydroweb_dir = subset_dir / "hydroweb"
    geoglows_dir = subset_dir / "geoglows"

    try:
        subset = pd.read_csv(subset_catalog_path)
    except Exception as exc:  # pragma: no cover - defensive validation
        return [f"Could not read {subset_catalog_path.relative_to(ROOT)}: {exc}"]

    if len(subset) != 5:
        errors.append("data/subset/stations.csv should contain exactly 5 stations")

    required_columns = {
        "ID",
        "Name",
        "River",
        "Latitude",
        "Longitude",
        "Elevation",
        "Missions",
        "COMID_v1",
        "COMID_v2",
        "Status",
        "hydroweb_file",
        "geoglows_file",
    }
    missing_columns = sorted(required_columns.difference(subset.columns))
    if missing_columns:
        errors.append(f"data/subset/stations.csv missing columns: {', '.join(missing_columns)}")
        return errors

    for _, station in subset.iterrows():
        hydroweb_file = hydroweb_dir / str(station["hydroweb_file"])
        geoglows_file = geoglows_dir / str(station["geoglows_file"])
        if not hydroweb_file.exists():
            errors.append(f"Missing subset Hydroweb file: {hydroweb_file.relative_to(ROOT)}")
        if not geoglows_file.exists():
            errors.append(f"Missing subset GEOGLOWS file: {geoglows_file.relative_to(ROOT)}")
        if pd.isna(station["COMID_v1"]) or int(station["COMID_v1"]) == 0:
            errors.append(f"Subset station {station['ID']} must have a nonzero COMID_v1")
        if pd.isna(station["COMID_v2"]) or int(station["COMID_v2"]) == 0:
            errors.append(f"Subset station {station['ID']} must have a nonzero COMID_v2")

    for path in sorted(hydroweb_dir.glob("*.csv")):
        try:
            frame = pd.read_csv(path, nrows=5)
        except Exception as exc:  # pragma: no cover - defensive validation
            errors.append(f"Could not read {path.relative_to(ROOT)}: {exc}")
            continue
        if list(frame.columns) != ["Datetime", "Water Level (m)"]:
            errors.append(f"{path.relative_to(ROOT)} should have columns: Datetime, Water Level (m)")
        if "Datetime" in frame.columns and pd.to_datetime(frame["Datetime"], utc=True, errors="coerce").isna().any():
            errors.append(f"{path.relative_to(ROOT)} contains unparseable Hydroweb dates")
        if "Water Level (m)" in frame.columns and pd.to_numeric(frame["Water Level (m)"], errors="coerce").isna().any():
            errors.append(f"{path.relative_to(ROOT)} contains non-numeric water levels")

    for path in sorted(geoglows_dir.glob("*.csv")):
        try:
            frame = pd.read_csv(path, nrows=5)
        except Exception as exc:  # pragma: no cover - defensive validation
            errors.append(f"Could not read {path.relative_to(ROOT)}: {exc}")
            continue
        if len(frame.columns) != 2:
            errors.append(f"{path.relative_to(ROOT)} should have exactly two columns")
        if len(frame.columns) == 2:
            timestamp_column, value_column = frame.columns
            if pd.to_datetime(frame[timestamp_column], utc=True, errors="coerce").isna().any():
                errors.append(f"{path.relative_to(ROOT)} contains unparseable GEOGLOWS timestamps")
            if pd.to_numeric(frame[value_column], errors="coerce").isna().any():
                errors.append(f"{path.relative_to(ROOT)} contains non-numeric GEOGLOWS streamflow values")

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

    timestamp_column = "timestamp" if "timestamp" in frame.columns else "phenomenon_time" if "phenomenon_time" in frame.columns else None
    if timestamp_column:
        parsed = pd.to_datetime(frame[timestamp_column], utc=True, errors="coerce")
        if parsed.isna().any():
            errors.append(f"{path.relative_to(ROOT)} contains unparseable timestamps")

    return errors


def _notebook_text(path: Path) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return None, [f"{path.relative_to(ROOT)} is not valid JSON: {exc}"]

    cells = notebook.get("cells", [])
    if not cells:
        return None, [f"{path.relative_to(ROOT)} has no cells"]

    text = "\n".join(
        "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
        for cell in cells
    )
    return text, errors


def _validate_notebooks() -> list[str]:
    errors: list[str] = []
    texts: dict[Path, str] = {}

    for path in EXPECTED_NOTEBOOKS:
        text, notebook_errors = _notebook_text(path)
        errors.extend(notebook_errors)
        if text is None:
            continue
        texts[path] = text
        for required in ["Setup and Creation Controls", "Connect to HydroServer", "Cleanup: Delete Created Resources"]:
            if required not in text:
                errors.append(f"{path.relative_to(ROOT)} missing required section: {required}")

    combined = "\n".join(texts.values())
    for title in REQUIRED_NOTEBOOK_TITLES:
        if title not in combined:
            errors.append(f"Notebook set missing title: {title}")
    for phrase in REQUIRED_NOTEBOOK_PHRASES:
        if phrase not in combined:
            errors.append(f"Notebook set missing required phrase: {phrase}")

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
