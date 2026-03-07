"""Shared utility functions for the Depository auto-posting system."""

import json
import logging
import os
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any


def get_repo_root() -> Path:
    """Return the repository root directory."""
    return Path(__file__).resolve().parent.parent


def load_json(path: Path) -> Any:
    """Load and return parsed JSON from a file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_settings() -> dict:
    """Load general settings from config/settings.json."""
    return load_json(get_repo_root() / "config" / "settings.json")


def load_platforms() -> dict:
    """Load platform configuration from config/platforms.json."""
    return load_json(get_repo_root() / "config" / "platforms.json")


def load_post_for_date(target_date: date | None = None) -> dict | None:
    """
    Load the post JSON file for a given date (defaults to today).
    Returns None if no post file exists for that date.
    """
    settings = load_settings()
    if target_date is None:
        target_date = date.today()

    content_dir = get_repo_root() / settings.get("content_dir", "content/posts")
    post_file = content_dir / f"{target_date.isoformat()}.json"

    if not post_file.exists():
        return None

    return load_json(post_file)


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure and return the root logger."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        level=numeric_level,
    )
    return logging.getLogger("depository")


def get_env(var_name: str) -> str:
    """
    Retrieve a required environment variable.
    Raises EnvironmentError if the variable is not set.
    """
    value = os.environ.get(var_name)
    if not value:
        raise EnvironmentError(f"Required environment variable '{var_name}' is not set.")
    return value


def retry(func, attempts: int = 3, delay: int = 5):
    """
    Call *func* up to *attempts* times, waiting *delay* seconds between retries.
    Re-raises the last exception if all attempts fail.
    """
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001
            logging.getLogger("depository").warning(
                "Attempt %d/%d failed: %s", attempt, attempts, exc
            )
            if attempt < attempts:
                time.sleep(delay)
            else:
                raise
