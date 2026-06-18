"""Data loading utilities for the website."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class DataLoader:
    """Handles loading of YAML data files."""

    def __init__(self, data_dir: str = "data"):
        """Initialize with data directory path."""
        self.data_dir = Path(data_dir)

    def load_yaml_file(self, filename: str) -> list[dict[str, Any]]:
        """Load YAML data from a specific file."""
        try:
            file_path = self.data_dir / filename
            with open(file_path, encoding="utf-8") as f:
                return yaml.safe_load(f) or []
        except FileNotFoundError:
            return []
        except yaml.YAMLError as e:
            print(f"Error loading {filename}: {e}")
            return []

    def get_all_data(self) -> dict[str, list[dict[str, Any]]]:
        """Load all site data."""
        return {
            "publist": self.load_yaml_file("publist.yml"),
            "datalist": self.load_yaml_file("datalist.yml"),
            "news": self.load_yaml_file("news.yml"),
            "years": self.load_yaml_file("years.yml"),
            "pi": self.load_yaml_file("pi.yml"),
        }
