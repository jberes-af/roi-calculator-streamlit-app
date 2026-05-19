# src/gui/streamlit/streamlit_settings_loader.py

from datetime import datetime
from pathlib import Path
from typing import Any

import os
import subprocess

"""
STREAMLIT SECRETS
"""


def _get_streamlit_secrets() -> Any | None:
    try:
        import streamlit as st
        return st.secrets
    except Exception:
        return None


def streamlit_secrets_available() -> bool:
    secrets = _get_streamlit_secrets()

    if secrets is None:
        return False

    try:
        # this triggers parsing, so it must be inside try
        return len(secrets) > 0
    except Exception:
        return False


def get_secret(name: str, default: str | None = None) -> str | None:
    secrets = _get_streamlit_secrets()

    if secrets is not None:
        try:
            if name in secrets:
                value = secrets[name]
                return str(value).strip()
        except Exception:
            pass

    value = os.getenv(name, default)
    return value.strip() if value else None


def get_required_secret(name: str) -> str:
    value = get_secret(name)
    if not value:
        raise RuntimeError(f"Missing required setting: {name}")
    return value


"""
LATEST TIMESTAMP
"""

PROJECT_DIR = Path(__file__).resolve().parents[3]

timestamp_files_map: dict[str, list[Path]] = {
    "care": [
        PROJECT_DIR / "src/gui/streamlit/screens/care/care_flow.py",
        PROJECT_DIR / "src/infrastructure/renderer/flow_diagram/diagram_nodes/care_flow_nodes.py",
        PROJECT_DIR / "src/infrastructure/renderer/flow_diagram/design_definitions/care_diagram_node_definitions.py",
    ],
}


def _get_latest_git_modified_at(
        path_key: str,
) -> str | None:
    paths: list[Path] = timestamp_files_map[path_key]

    latest_timestamp: int | None = None

    for path in paths:
        result = subprocess.run(
            [
                "git",
                "log",
                "-1",
                "--format=%ct",
                "--",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0 or not result.stdout.strip():
            continue

        timestamp = int(result.stdout.strip())
        latest_timestamp = max(latest_timestamp or timestamp, timestamp)

    if latest_timestamp is None:
        return None

    from datetime import datetime

    return datetime.fromtimestamp(latest_timestamp).strftime(
        "%b %d, %Y at %-I:%M %p"
    )


def _get_latest_modified_timestamp_local_file_system(
        path_key: str,
) -> str | None:
    paths: list[Path] = timestamp_files_map[path_key]

    latest_timestamp = max(
        path.stat().st_mtime
        for path in paths
        if path.exists()
    )

    return datetime.fromtimestamp(latest_timestamp).strftime(
        "%b %d, %Y at %I:%M %p"
    )


def get_last_updated_at_timestamp(path_key: str) -> str:
    if path_key not in timestamp_files_map:
        return "Unavailable"

    last_updated_at = _get_latest_modified_timestamp_local_file_system(path_key)
    return last_updated_at if last_updated_at else "Unavailable"
