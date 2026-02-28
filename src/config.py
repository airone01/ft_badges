import json
import os
from typing import cast
from src.types import ConfigData

OUTPUT_DIR: str = "badges"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_config(filepath: str = "config.json") -> ConfigData:
    """Loads and types the configuration JSON."""
    with open(filepath, "r") as f:
        return cast(ConfigData, json.load(f))


# singleton
APP_CONFIG: ConfigData = load_config()
